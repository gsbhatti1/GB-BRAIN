"""Phase 2C OANDA practice candle feed."""
from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import os
import requests
import pandas as pd

class OandaPracticeFeed:
    SYMBOL_TO_ENV = {
        "US30": "OANDA_US30_INSTRUMENT",
        "NAS100": "OANDA_NAS100_INSTRUMENT",
        "SPX500": "OANDA_SPX500_INSTRUMENT",
    }

    SYMBOL_DEFAULTS = {
        "US30": "US30_USD",
        "NAS100": "NAS100_USD",
        "SPX500": "SPX500_USD",
    }

    TF_TO_GRANULARITY = {
        "5m": "M5",
        "15m": "M15",
        "30m": "M30",
        "1h": "H1",
    }

    def __init__(self) -> None:
        self.api_host = os.getenv("OANDA_API_HOST", "https://api-fxpractice.oanda.com").rstrip("/")
        self.api_token = os.getenv("OANDA_API_TOKEN", "")
        self.account_id = os.getenv("OANDA_ACCOUNT_ID", "")

        if not self.api_token:
            raise RuntimeError("Missing OANDA_API_TOKEN")

    def instrument_for_symbol(self, symbol: str) -> str:
        env_name = self.SYMBOL_TO_ENV[symbol]
        return os.getenv(env_name, self.SYMBOL_DEFAULTS[symbol])

    def fetch_candles(self, symbol: str, timeframe: str, count: int = 500) -> pd.DataFrame:
        instrument = self.instrument_for_symbol(symbol)
        granularity = self.TF_TO_GRANULARITY[timeframe]

        url = f"{self.api_host}/v3/instruments/{instrument}/candles"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        params = {
            "price": "M",
            "granularity": granularity,
            "count": str(count),
        }

        resp = requests.get(url, headers=headers, params=params, timeout=20)
        resp.raise_for_status()
        payload = resp.json()

        candles = payload.get("candles", [])
        rows = []
        for candle in candles:
            if not candle.get("complete", False):
                continue
            mid = candle.get("mid", {})
            rows.append({
                "timestamp": pd.to_datetime(candle["time"], utc=True),
                "open": float(mid["o"]),
                "high": float(mid["h"]),
                "low": float(mid["l"]),
                "close": float(mid["c"]),
                "volume": float(candle.get("volume", 0.0)),
            })

        if not rows:
            return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])

        df = pd.DataFrame(rows).set_index("timestamp")
        return df[["open", "high", "low", "close", "volume"]].sort_index()


if __name__ == "__main__":
    feed = OandaPracticeFeed()
    df = feed.fetch_candles("US30", "5m", count=10)
    print(df.tail(3))