"""Shared live/shadow adapter for custom GB-BRAIN engines."""

from dataclasses import dataclass, asdict
from typing import Any
from datetime import date, datetime

import pandas as pd

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

from execute.gem_loader import canonical_symbol, get_strategy_profile
from strategies.custom.cipher_engine import CipherEngine
from strategies.custom.parallax_engine import ParallaxEngine
from strategies.custom.combined_engine import CombinedEngine
from strategies.custom.ticker_presets import get_preset


OHLCV_COLUMNS = ["open", "high", "low", "close", "volume"]


def _sanitize_json_value(value: Any):
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if np is not None:
        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, np.ndarray):
            return value.tolist()
    if isinstance(value, dict):
        return {str(k): _sanitize_json_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_sanitize_json_value(v) for v in value]
    return value


@dataclass
class StandardizedSignal:
    strategy_family: str
    symbol: str
    timeframe: str
    timestamp: str
    direction: int
    entry_price: float
    stop_loss: float
    tp1: float | None
    tp2: float | None
    tp3: float | None
    score: float | None
    source: str
    reason: str
    raw: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return _sanitize_json_value(asdict(self))


def _flatten_columns(columns) -> list[str]:
    flat: list[str] = []
    for col in columns:
        if isinstance(col, tuple):
            flat.append(str(col[0]).strip().lower())
        else:
            flat.append(str(col).strip().lower())
    return flat


def normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=OHLCV_COLUMNS)

    out = df.copy()
    out.columns = _flatten_columns(out.columns)
    out.index = pd.to_datetime(pd.Index(out.index.astype(str)), utc=True, errors="coerce", format="mixed")
    out.index.name = "datetime"
    out = out[out.index.notna()]

    if not out.empty:
        out = out[~out.index.duplicated(keep="last")].sort_index()

    for col in OHLCV_COLUMNS:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    missing = [c for c in ["open", "high", "low", "close"] if c not in out.columns]
    if missing:
        raise ValueError(f"Missing OHLC columns: {', '.join(missing)}")

    if "volume" not in out.columns:
        out["volume"] = 0.0

    out = out.dropna(subset=["open", "high", "low", "close"])
    return out[OHLCV_COLUMNS]


def _deep_merge(base: dict, overlay: dict) -> dict:
    result = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


class CustomLiveEngine:
    def __init__(self, strategy_family: str, symbol: str, timeframe: str):
        self.strategy_family = strategy_family.lower().strip()
        self.symbol = canonical_symbol(symbol)
        self.timeframe = timeframe

        preset = get_preset(self.symbol, timeframe=timeframe)
        strategy_profile = get_strategy_profile(self.strategy_family, self.symbol, timeframe)

        self.preset = preset
        self.strategy_profile = strategy_profile
        self.params = _deep_merge(preset.get(self.strategy_family, {}), strategy_profile.get("params", {}))

        if self.strategy_family == "cipher":
            self.engine = CipherEngine(self.params)
        elif self.strategy_family == "parallax":
            self.engine = ParallaxEngine(self.params)
        elif self.strategy_family == "combined":
            combo = _deep_merge(preset, {"combined": self.params})
            self.engine = CombinedEngine(combo)
        else:
            raise ValueError(f"Unsupported strategy family: {strategy_family}")

    def run(self, df: pd.DataFrame):
        clean = normalize_ohlcv(df)
        return self.engine.run(clean)

    def latest_signal(self, df: pd.DataFrame) -> StandardizedSignal | None:
        clean = normalize_ohlcv(df)
        signals = self.engine.run(clean)
        if not signals:
            return None

        sig = signals[-1]
        raw = dict(getattr(sig, "__dict__", {}))
        timestamp = getattr(sig, "timestamp", clean.index[-1])
        score = getattr(sig, "score", getattr(sig, "confluence_score", None))
        source = getattr(sig, "source", self.strategy_family.upper())

        return StandardizedSignal(
            strategy_family=self.strategy_family,
            symbol=self.symbol,
            timeframe=self.timeframe,
            timestamp=str(timestamp),
            direction=int(getattr(sig, "direction")),
            entry_price=float(getattr(sig, "entry_price")),
            stop_loss=float(getattr(sig, "stop_loss")),
            tp1=float(getattr(sig, "tp1", 0) or 0) if hasattr(sig, "tp1") else None,
            tp2=float(getattr(sig, "tp2", 0) or 0) if hasattr(sig, "tp2") else None,
            tp3=float(getattr(sig, "tp3", 0) or 0) if hasattr(sig, "tp3") else None,
            score=float(score) if score is not None else None,
            source=str(source),
            reason=str(getattr(sig, "reason", "")),
            raw=raw,
        )

    def latest_signal_for_bar(self, df: pd.DataFrame, target_timestamp: str | None = None) -> StandardizedSignal | None:
        sig = self.latest_signal(df)
        if sig is None:
            return None
        if target_timestamp is None:
            return sig
        return sig if str(sig.timestamp) == str(target_timestamp) else None

    def latest_confirmed_signal(self, df: pd.DataFrame) -> StandardizedSignal | None:
        return self.latest_signal(df)