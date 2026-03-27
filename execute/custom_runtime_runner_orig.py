"""Phase 2 unified custom runtime runner."""

from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import argparse
import asyncio
import json
import logging
import time

import pandas as pd
import yfinance as yf


from execute.blofin_ws_candles import BloFinPublicCandleFeed
from execute.custom_live_engine import CustomLiveEngine
from execute.live_observer import LiveObserver
from execute.oanda_practice_feed import OandaPracticeFeed
from execute.paper_executor import SinglePositionPaperExecutor
from execute.runtime_policy import resolve_runtime_policy

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("gb_brain.runtime")


def seed_history(symbol: str, timeframe: str, limit: int = 400) -> pd.DataFrame:
    backtest_map = {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "SOL": "SOL-USD",
        "US30": "^DJI",
        "NAS100": "^NDX",
        "SPX500": "^GSPC",
    }
    ticker = backtest_map[symbol]
    period = "60d" if timeframe in {"5m", "15m", "30m"} else "730d"
    interval = {"5m": "5m", "15m": "15m", "30m": "30m", "1h": "1h"}.get(timeframe, "15m")

    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
    if df is None or df.empty:
        raise RuntimeError(f"Failed to seed history from yfinance for {symbol} {timeframe}")

    df = df.tail(limit)
    df.columns = [str(c[0]).lower() if isinstance(c, tuple) else str(c).lower() for c in df.columns]
    return df[["open", "high", "low", "close", "volume"]].copy()


def candle_dict_from_row(ts: pd.Timestamp, row: pd.Series, confirm: int = 1) -> dict:
    timestamp = pd.Timestamp(ts)
    if timestamp.tzinfo is None:
        timestamp = timestamp.tz_localize("UTC")
    else:
        timestamp = timestamp.tz_convert("UTC")

    return {
        "timestamp": timestamp,
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": float(row.get("volume", 0.0)),
        "confirm": int(confirm),
    }


def make_paper(observer, policy):
    if policy.runtime_mode != "paper":
        return None
    return SinglePositionPaperExecutor(
        observer,
        policy.bot_name,
        policy.observer_broker,
        policy.symbol,
        policy.timeframe,
    )


async def run_blofin_ws(args: argparse.Namespace, policy) -> None:
    inst_map = {"BTC": "BTC-USDT", "ETH": "ETH-USDT", "SOL": "SOL-USDT"}
    inst_id = inst_map[policy.symbol]

    history = seed_history(policy.symbol, policy.timeframe, limit=args.seed_limit)
    feed = BloFinPublicCandleFeed(inst_id, policy.timeframe, demo=args.demo, max_candles=args.seed_limit + 100)

    for ts, row in history.iterrows():
        feed.ingest_rows([[
            str(int(pd.Timestamp(ts).timestamp() * 1000)),
            str(row["open"]),
            str(row["high"]),
            str(row["low"]),
            str(row["close"]),
            str(row.get("volume", 0.0)),
            str(row.get("volume", 0.0)),
            str(float(row.get("close", 0.0)) * float(row.get("volume", 0.0))),
            "1",
        ]])

    observer = LiveObserver()
    engine = CustomLiveEngine(policy.family, policy.symbol, policy.timeframe)
    paper = make_paper(observer, policy)

    active_candidates: dict[str, int] = {}
    logged_candidate_keys: set[str] = set()
    event_count = 0

    async for candle in feed.stream():
        event_count += 1
        frame = feed.frame(confirmed_only=False)
        if frame.empty:
            continue

        bar_ts = candle["timestamp"].isoformat()
        signal = engine.latest_signal_for_bar(frame, target_timestamp=bar_ts)

        if int(candle["confirm"]) == 0:
            if signal is None:
                continue

            payload = signal.to_dict()
            dedupe_key = f"{payload['strategy_family']}|{payload['symbol']}|{payload['timeframe']}|{payload['timestamp']}|{payload['direction']}"
            if dedupe_key in logged_candidate_keys:
                continue

            candidate_id = observer.log_candidate(
                bot_name=policy.bot_name,
                strategy_family=policy.family,
                symbol=payload["symbol"],
                timeframe=payload["timeframe"],
                broker=policy.observer_broker,
                signal=payload,
                status="candidate-live",
            )
            active_candidates[bar_ts] = candidate_id
            logged_candidate_keys.add(dedupe_key)
            logger.info("Candidate flash: %s", json.dumps(payload, default=str))

        else:
            if paper is not None:
                paper.on_candle(candle)

            if signal is None:
                candidate_id = active_candidates.pop(bar_ts, None)
                if candidate_id is not None:
                    observer.log_confirmation(
                        candidate_id=candidate_id,
                        confirmed=False,
                        confirmation_bar_ts=bar_ts,
                        invalidation_reason="signal_disappeared_by_close",
                        payload={"bar_timestamp": bar_ts, "symbol": policy.symbol, "timeframe": policy.timeframe},
                    )
                    logger.info("Candidate invalidated by close: %s %s %s", policy.family, policy.symbol, bar_ts)
            else:
                payload = signal.to_dict()
                candidate_id = active_candidates.pop(bar_ts, None)

                if candidate_id is None:
                    candidate_id = observer.log_candidate(
                        bot_name=policy.bot_name,
                        strategy_family=policy.family,
                        symbol=payload["symbol"],
                        timeframe=payload["timeframe"],
                        broker=policy.observer_broker,
                        signal=payload,
                        status="confirmed-close",
                    )

                confirmation_id = observer.log_confirmation(
                    candidate_id=candidate_id,
                    confirmed=True,
                    confirmation_bar_ts=bar_ts,
                    payload=payload,
                )
                logger.info("Confirmed close-bar signal: %s", json.dumps(payload, default=str))

                if paper is not None:
                    execution_id = paper.on_confirmed_signal(payload, candidate_id, confirmation_id)
                    logger.info("Paper execution id=%s venue=%s", execution_id, policy.execution_venue)

        if args.max_events and event_count >= args.max_events:
            logger.info("Max events reached (%s). Exiting.", args.max_events)
            break


def run_closed_bar_source(args: argparse.Namespace, policy, frame: pd.DataFrame) -> None:
    observer = LiveObserver()
    engine = CustomLiveEngine(policy.family, policy.symbol, policy.timeframe)
    paper = make_paper(observer, policy)

    if frame.empty:
        logger.warning("No candles returned.")
        return

    last_ts = str(frame.index[-1])
    last_candle = candle_dict_from_row(frame.index[-1], frame.iloc[-1], confirm=1)
    if paper is not None:
        paper.on_candle(last_candle)

    signal = engine.latest_signal_for_bar(frame, target_timestamp=last_ts)
    if signal is None:
        logger.info("No confirmed signal.")
        return

    payload = signal.to_dict()
    candidate_id = observer.log_candidate(
        bot_name=policy.bot_name,
        strategy_family=policy.family,
        symbol=payload["symbol"],
        timeframe=payload["timeframe"],
        broker=policy.observer_broker,
        signal=payload,
        status="confirmed-close",
    )
    confirmation_id = observer.log_confirmation(
        candidate_id=candidate_id,
        confirmed=True,
        confirmation_bar_ts=payload["timestamp"],
        payload=payload,
    )

    logger.info("Confirmed close-bar signal: %s", json.dumps(payload, default=str))

    if paper is not None:
        execution_id = paper.on_confirmed_signal(payload, candidate_id, confirmation_id)
        logger.info("Paper execution id=%s venue=%s", execution_id, policy.execution_venue)


def run_yfinance(args: argparse.Namespace, policy) -> None:
    frame = seed_history(policy.symbol, policy.timeframe, limit=args.seed_limit)
    run_closed_bar_source(args, policy, frame)


def run_oanda_practice(args: argparse.Namespace, policy) -> None:
    feed = OandaPracticeFeed()
    frame = feed.fetch_candles(policy.symbol, policy.timeframe, count=args.seed_limit)
    run_closed_bar_source(args, policy, frame)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GB-BRAIN unified custom runtime runner")
    parser.add_argument("--family", required=True, choices=["cipher", "parallax", "combined"])
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--timeframe", required=False)
    parser.add_argument("--profile", default="manual-signals")
    parser.add_argument("--broker", default="auto", choices=["auto", "yfinance", "blofin-ws", "oanda-practice", "manual"])
    parser.add_argument("--mode", default="", choices=["", "shadow", "paper"])
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--interval", type=int, default=30)
    parser.add_argument("--seed-limit", type=int, default=400)
    parser.add_argument("--max-events", type=int, default=0)
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    policy = resolve_runtime_policy(
        profile_name=args.profile,
        family=args.family,
        symbol=args.symbol,
        timeframe=args.timeframe,
        broker_choice=args.broker,
        mode_choice=args.mode,
    )

    logger.info(
        "Runtime policy | bot=%s family=%s symbol=%s tf=%s market=%s venue=%s mode=%s",
        policy.bot_name,
        policy.family,
        policy.symbol,
        policy.timeframe,
        policy.market_data_broker,
        policy.execution_venue,
        policy.runtime_mode,
    )
    if policy.notes:
        logger.info("Policy note: %s", policy.notes)

    if policy.market_data_broker == "blofin-ws":
        asyncio.run(run_blofin_ws(args, policy))
    elif policy.market_data_broker == "oanda-practice":
        run_oanda_practice(args, policy)
    else:
        run_yfinance(args, policy)


if __name__ == "__main__":
    main()