from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional, Tuple

import pandas as pd


_TIME_COLS = ("datetime", "timestamp", "time", "date", "Datetime", "Timestamp", "Date")
_COL_MAP = {
    "open": "open",
    "high": "high",
    "low": "low",
    "close": "close",
    "volume": "volume",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume",
}


@dataclass
class ReplayFeed:
    symbol: str
    timeframe: str
    csv_path: Optional[str] = None
    root_dir: Optional[str] = None

    def _default_csv_path(self) -> Path:
        root = Path(self.root_dir) if self.root_dir else Path(__file__).resolve().parents[1]
        return root / "backtest" / "data_cache" / f"{self.symbol}_{self.timeframe}.csv"

    def resolve_csv_path(self) -> Path:
        if self.csv_path:
            return Path(self.csv_path)
        return self._default_csv_path()

    def load(self) -> pd.DataFrame:
        path = self.resolve_csv_path()
        if not path.exists():
            raise FileNotFoundError(f"Replay CSV not found: {path}")

        df = pd.read_csv(path)
        if df.empty:
            raise ValueError(f"Replay CSV is empty: {path}")

        rename_map = {c: _COL_MAP[c] for c in df.columns if c in _COL_MAP}
        if rename_map:
            df = df.rename(columns=rename_map)

        time_col = next((c for c in _TIME_COLS if c in df.columns), None)
        if time_col is None:
            raise ValueError(
                f"Replay CSV missing datetime column. Expected one of: {_TIME_COLS}. "
                f"Got columns: {list(df.columns)}"
            )

        df[time_col] = pd.to_datetime(df[time_col], errors="coerce", utc=True)
        df = df.dropna(subset=[time_col]).copy()
        df = df.sort_values(time_col).reset_index(drop=True)

        required = ["open", "high", "low", "close"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Replay CSV missing OHLC columns: {missing}")

        if "volume" not in df.columns:
            df["volume"] = 0.0

        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=["open", "high", "low", "close"]).copy()
        df = df.rename(columns={time_col: "timestamp"})
        return df[["timestamp", "open", "high", "low", "close", "volume"]].copy()

    def last_price(self) -> float:
        df = self.load()
        return float(df.iloc[-1]["close"])

    def iter_windows(
        self,
        seed_limit: int = 300,
        max_events: int = 20,
    ) -> Iterator[Tuple[pd.DataFrame, dict]]:
        df = self.load()
        if len(df) < max(seed_limit + 1, 20):
            raise ValueError(
                f"Replay CSV too short for seed_limit={seed_limit}. rows={len(df)} "
                f"path={self.resolve_csv_path()}"
            )

        start_idx = max(seed_limit, len(df) - max_events)
        for idx in range(start_idx, len(df)):
            window = df.iloc[: idx + 1].copy()
            bar = df.iloc[idx].to_dict()
            yield window, bar