"""BloFin public websocket candle feed for GB-BRAIN Phase 2."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import asyncio
import json
import logging
import os
from collections import OrderedDict
from typing import Any

import pandas as pd
import websockets

logger = logging.getLogger("gb_brain.blofin_ws")


class BloFinPublicCandleFeed:
    TIMEFRAME_TO_CHANNEL = {
        "1m": "candle1m",
        "3m": "candle3m",
        "5m": "candle5m",
        "15m": "candle15m",
        "30m": "candle30m",
        "1h": "candle1H",
        "2h": "candle2H",
        "4h": "candle4H",
        "1d": "candle1D",
    }

    def __init__(
        self,
        inst_id: str,
        timeframe: str,
        *,
        demo: bool = True,
        max_candles: int = 500,
        ws_url: str | None = None,
        ping_interval_seconds: int = 20,
    ) -> None:
        self.inst_id = inst_id
        self.timeframe = timeframe
        self.channel = self.TIMEFRAME_TO_CHANNEL[timeframe]
        self.max_candles = max_candles
        self.ping_interval_seconds = ping_interval_seconds
        self.ws_url = ws_url or os.getenv(
            "BLOFIN_DEMO_PUBLIC_WS_URL" if demo else "BLOFIN_PUBLIC_WS_URL",
            "wss://demo-trading-openapi.blofin.com/ws/public" if demo else "wss://openapi.blofin.com/ws/public",
        )
        self._candles: OrderedDict[str, dict[str, Any]] = OrderedDict()

    @staticmethod
    def _to_candle(row: list[str]) -> dict[str, Any]:
        ts = pd.to_datetime(int(row[0]), unit="ms", utc=True)
        return {
            "timestamp": ts,
            "open": float(row[1]),
            "high": float(row[2]),
            "low": float(row[3]),
            "close": float(row[4]),
            "volume": float(row[5]),
            "volume_currency": float(row[6]),
            "volume_quote": float(row[7]),
            "confirm": int(row[8]),
        }

    def ingest_rows(self, rows: list[list[str]]) -> list[dict[str, Any]]:
        updates: list[dict[str, Any]] = []
        for row in rows:
            candle = self._to_candle(row)
            key = candle["timestamp"].isoformat()
            self._candles[key] = candle
            self._candles.move_to_end(key)
            while len(self._candles) > self.max_candles:
                self._candles.popitem(last=False)
            updates.append(candle)
        return updates

    def apply_message(self, message: dict[str, Any]) -> list[dict[str, Any]]:
        data = message.get("data", [])
        if not isinstance(data, list) or not data:
            return []
        if isinstance(data[0], list):
            return self.ingest_rows(data)
        return []

    def frame(self, confirmed_only: bool = False) -> pd.DataFrame:
        rows = list(self._candles.values())
        if confirmed_only:
            rows = [row for row in rows if int(row.get("confirm", 0)) == 1]
        if not rows:
            return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
        df = pd.DataFrame(rows).set_index("timestamp")
        df.index = pd.to_datetime(df.index, utc=True)
        return df[["open", "high", "low", "close", "volume"]].sort_index()

    async def stream(self):
        subscribe = {
            "op": "subscribe",
            "args": [{"channel": self.channel, "instId": self.inst_id}],
        }
        logger.info("Connecting BloFin public WS: %s | %s %s", self.ws_url, self.inst_id, self.channel)
        async with websockets.connect(self.ws_url, ping_interval=None, open_timeout=20, close_timeout=10) as ws:
            await ws.send(json.dumps(subscribe))
            logger.info("Subscribed: %s", subscribe)

            while True:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=self.ping_interval_seconds)
                except asyncio.TimeoutError:
                    await ws.send("ping")
                    continue

                if raw == "pong":
                    continue

                payload = json.loads(raw)

                if payload.get("event") in {"subscribe", "unsubscribe"}:
                    logger.info("WS event: %s", payload)
                    continue

                if payload.get("event") == "error":
                    raise RuntimeError(f"BloFin WS error: {payload}")

                for candle in self.apply_message(payload):
                    yield candle


def build_blofin_candle_row(timestamp_ms: int, open_: str, high: str, low: str, close: str,
                            volume: str, volume_currency: str, volume_quote: str,
                            confirm: str) -> list[str]:
    return [str(timestamp_ms), open_, high, low, close, volume, volume_currency, volume_quote, confirm]


if __name__ == "__main__":
    sample = {
        "arg": {"channel": "candle15m", "instId": "SOL-USDT"},
        "data": [
            build_blofin_candle_row(1696636800000, "19.1", "19.4", "18.9", "19.2", "95359", "95.359", "2621407.651", "0")
        ],
    }
    feed = BloFinPublicCandleFeed("SOL-USDT", "15m")
    out = feed.apply_message(sample)
    print(out[0]["timestamp"].isoformat(), out[0]["confirm"])