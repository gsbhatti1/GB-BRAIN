"""Phase 2 BloFin websocket runner.

Seeds history from yfinance for warmup, then streams BloFin public websocket candles.
Logs both candidate intrabar flashes and confirmed close-bar signals. Optional paper mode
opens a single simulated position and closes on TP/SL or reverse signal.
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import argparse
import asyncio
import json
import logging

import pandas as pd
import yfinance as yf

from execute.blofin_ws_candles import BloFinPublicCandleFeed
from execute.custom_live_engine import CustomLiveEngine
from execute.gem_loader import get_runtime_profile, get_symbol_profile
from execute.live_observer import LiveObserver
from execute.paper_executor import SinglePositionPaperExecutor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("gb_brain.ws_shadow")


def seed_history(symbol: str, timeframe: str, limit: int = 400) -> pd.DataFrame:
    profile = get_symbol_profile(symbol)
    ticker = profile["backtest"]["symbol"]
    period = "60d" if timeframe in {"5m", "15m", "30m"} else "730d"
    interval = {"5m": "5m", "15m": "15m", "30m": "30m", "1h": "1h"}.get(timeframe, "15m")
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
    if df is None or df.empty:
        raise RuntimeError(f"Failed to seed history from yfinance for {symbol} {timeframe}")
    df = df.tail(limit)
    df.columns = [str(c[0]).lower() if isinstance(c, tuple) else str(c).lower() for c in df.columns]
    return df[["open", "high", "low", "close", "volume"]].copy()


async def run(args: argparse.Namespace) -> None:
    runtime = get_runtime_profile(args.profile)
    symbol_profile = get_symbol_profile(args.symbol)
    bot_name = runtime["bot_name"]
    inst_id = symbol_profile["brokers"]["blofin"]

    history = seed_history(args.symbol, args.timeframe, limit=args.seed_limit)

    feed = BloFinPublicCandleFeed(inst_id, args.timeframe, demo=args.demo, max_candles=args.seed_limit + 100)
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
    engine = CustomLiveEngine(args.family, args.symbol, args.timeframe)
    paper = SinglePositionPaperExecutor(observer, bot_name, "blofin-ws", args.symbol, args.timeframe) if args.paper else None

    active_candidates: dict[str, int] = {}
    candidate_keys_logged: set[str] = set()
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
            if dedupe_key in candidate_keys_logged:
                continue

            candidate_id = observer.log_candidate(
                bot_name=bot_name,
                strategy_family=args.family,
                symbol=payload["symbol"],
                timeframe=payload["timeframe"],
                broker="blofin-ws",
                signal=payload,
                status="candidate-live",
            )
            active_candidates[bar_ts] = candidate_id
            candidate_keys_logged.add(dedupe_key)
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
                        payload={"bar_timestamp": bar_ts, "symbol": args.symbol, "timeframe": args.timeframe},
                    )
                    logger.info("Candidate invalidated by close: %s %s %s", args.family, args.symbol, bar_ts)

            else:
                payload = signal.to_dict()
                candidate_id = active_candidates.pop(bar_ts, None)
                if candidate_id is None:
                    candidate_id = observer.log_candidate(
                        bot_name=bot_name,
                        strategy_family=args.family,
                        symbol=payload["symbol"],
                        timeframe=payload["timeframe"],
                        broker="blofin-ws",
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
                    logger.info("Paper execution id=%s", execution_id)

        if args.max_events and event_count >= args.max_events:
            logger.info("Max events reached (%s). Exiting.", args.max_events)
            break


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GB-BRAIN Phase 2 BloFin websocket shadow runner")
    parser.add_argument("--family", required=True, choices=["cipher", "parallax", "combined"])
    parser.add_argument("--symbol", required=True, choices=["BTC", "ETH", "SOL"])
    parser.add_argument("--timeframe", required=True, choices=["5m", "15m", "30m", "1h"])
    parser.add_argument("--profile", default="gb-crypto-bot")
    parser.add_argument("--demo", action="store_true", default=True)
    parser.add_argument("--paper", action="store_true")
    parser.add_argument("--seed-limit", type=int, default=400)
    parser.add_argument("--max-events", type=int, default=0)
    return parser.parse_args()


if __name__ == "__main__":
    asyncio.run(run(parse_args()))