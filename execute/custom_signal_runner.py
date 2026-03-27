"""Shadow/alert runner for Cipher, Parallax, and Combined custom engines."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import argparse
import json
import logging
import time

import pandas as pd
import requests
import yfinance as yf

from execute.custom_live_engine import CustomLiveEngine
from execute.gem_loader import get_runtime_profile, get_symbol_profile
from execute.live_observer import LiveObserver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("gb_brain.shadow")


def fetch_candles(broker: str, symbol: str, timeframe: str, limit: int = 400) -> pd.DataFrame | None:
    broker = broker.lower()
    profile = get_symbol_profile(symbol)
    tf_map = {"5m": "5m", "15m": "15m", "30m": "30m", "1h": "1h"}

    if broker in {"yfinance", "yahoo", "oanda"}:
        ticker = profile["backtest"]["symbol"]
        period = "60d" if timeframe in {"5m", "15m", "30m"} else "730d"
        df = yf.download(
            ticker,
            period=period,
            interval=tf_map.get(timeframe, "1h"),
            progress=False,
            auto_adjust=True,
        )
        if df is None or df.empty:
            return None
        return df.tail(limit)

    if broker == "blofin":
        inst = profile["brokers"]["blofin"]
        bar_map = {"5m": "5m", "15m": "15m", "30m": "30m", "1h": "1H"}
        url = "https://demo-trading-openapi.blofin.com/api/v1/market/candles"
        params = {
            "instId": inst,
            "bar": bar_map.get(timeframe, "15m"),
            "limit": str(limit),
        }
        headers = {"User-Agent": "GB-BRAIN/2.0", "Accept": "application/json"}

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=15)
            resp.raise_for_status()
            try:
                result = resp.json()
            except ValueError:
                logger.error(
                    "BloFin candles returned non-JSON body: status=%s body=%r",
                    resp.status_code,
                    resp.text[:300],
                )
                return None
        except requests.RequestException as exc:
            body = getattr(getattr(exc, "response", None), "text", "")
            logger.error("BloFin candles request failed: %s | body=%r", exc, body[:300])
            return None

        data = result.get("data", []) if isinstance(result, dict) else []
        if not data:
            logger.warning("BloFin candles returned no data for %s %s", inst, timeframe)
            return None

        df = pd.DataFrame(
            data,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "volCcy",
                "volQuote",
                "confirm",
            ],
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit="ms", utc=True)
        df.set_index("timestamp", inplace=True)

        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        if "confirm" in df.columns:
            df = df[df["confirm"].astype(str) == "1"]

        return df[["open", "high", "low", "close", "volume"]].sort_index()

    raise ValueError(f"Unsupported broker/data source: {broker}")


def main() -> None:
    parser = argparse.ArgumentParser(description="GB-BRAIN custom shadow runner")
    parser.add_argument("--family", required=True, choices=["cipher", "parallax", "combined"])
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--timeframe", required=True)
    parser.add_argument("--broker", default="yfinance", help="blofin | yfinance | oanda")
    parser.add_argument("--profile", default="manual-signals", help="Runtime profile name")
    parser.add_argument("--shadow", action="store_true", help="Log to observer tables only")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--interval", type=int, default=60)
    args = parser.parse_args()

    runtime = get_runtime_profile(args.profile)
    bot_name = runtime["bot_name"]
    observer = LiveObserver()
    engine = CustomLiveEngine(args.family, args.symbol, args.timeframe)
    seen_bar_ts: set[str] = set()

    def run_once() -> None:
        df = fetch_candles(args.broker, args.symbol, args.timeframe)
        if df is None or df.empty:
            logger.warning("No candles returned.")
            return

        sig = engine.latest_confirmed_signal(df)
        if sig is None:
            logger.info("No confirmed signal.")
            return

        payload = sig.to_dict()
        print(json.dumps(payload, indent=2, default=str))

        if payload["timestamp"] in seen_bar_ts:
            return

        seen_bar_ts.add(payload["timestamp"])

        candidate_id = observer.log_candidate(
            bot_name=bot_name,
            strategy_family=args.family,
            symbol=payload["symbol"],
            timeframe=payload["timeframe"],
            broker=args.broker,
            signal=payload,
            status="confirmed-close",
        )

        observer.log_confirmation(
            candidate_id=candidate_id,
            confirmed=True,
            confirmation_bar_ts=payload["timestamp"],
            payload=payload,
        )

        logger.info(
            "Logged confirmed signal: %s %s %s %s",
            args.family,
            payload["symbol"],
            payload["timeframe"],
            payload["timestamp"],
        )

    if args.once:
        run_once()
        return

    while True:
        run_once()
        time.sleep(args.interval)


if __name__ == "__main__":
    main()