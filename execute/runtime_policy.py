"""Phase 2 runtime policy + routing."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dataclasses import dataclass
from execute.gem_loader import canonical_symbol, get_runtime_profile


@dataclass
class RuntimePolicy:
    profile_name: str
    bot_name: str
    category: str
    symbol: str
    timeframe: str
    family: str
    market_data_broker: str
    observer_broker: str
    execution_venue: str
    runtime_mode: str
    notes: str


def _normalize_broker_choice(choice: str | None) -> str:
    raw = (choice or "auto").strip().lower()
    aliases = {
        "auto": "auto",
        "yf": "yfinance",
        "yahoo": "yfinance",
        "yfinance": "yfinance",
        "blofin": "blofin-ws",
        "blofin-ws": "blofin-ws",
        "oanda": "oanda-practice",
        "oanda-practice": "oanda-practice",
        "manual": "manual",
    }
    if raw not in aliases:
        raise ValueError(f"Unsupported broker choice: {choice}")
    return aliases[raw]


def _normalize_mode_choice(choice: str | None, profile: dict) -> str:
    raw = (choice or "").strip().lower()
    if raw in {"shadow", "paper"}:
        return raw
    if profile.get("paper_default", False):
        return "paper"
    return "shadow"


def resolve_runtime_policy(
    *,
    profile_name: str,
    family: str,
    symbol: str,
    timeframe: str | None,
    broker_choice: str | None = None,
    mode_choice: str | None = None,
) -> RuntimePolicy:
    profile = get_runtime_profile(profile_name)
    canonical = canonical_symbol(symbol)
    family = family.strip().lower()

    allowed_symbols = {str(s).upper() for s in profile.get("symbols", [])}
    if canonical.upper() not in allowed_symbols:
        raise ValueError(f"{canonical} is not allowed for profile {profile_name}")

    allowed_families = {str(f).lower() for f in profile.get("engine_families", [])}
    if family not in allowed_families:
        raise ValueError(f"{family} is not allowed for profile {profile_name}")

    timeframe = timeframe or profile.get("default_timeframe", "15m")
    requested_broker = _normalize_broker_choice(broker_choice)
    runtime_mode = _normalize_mode_choice(mode_choice, profile)

    declared_broker = str(profile.get("broker", "")).strip().lower()
    notes: list[str] = []

    if requested_broker == "auto":
        if declared_broker == "blofin":
            market_data_broker = "blofin-ws"
            observer_broker = "blofin-ws"
            execution_venue = "blofin-demo"
        elif declared_broker == "oanda":
            market_data_broker = "oanda-practice"
            observer_broker = "oanda-practice"
            execution_venue = "oanda-practice"
        else:
            market_data_broker = "yfinance"
            observer_broker = "yfinance[manual]"
            execution_venue = "manual"
    elif requested_broker == "blofin-ws":
        market_data_broker = "blofin-ws"
        observer_broker = "blofin-ws"
        execution_venue = "blofin-demo"
        if declared_broker != "blofin":
            notes.append("Explicit BloFin transport overrides profile broker.")
    elif requested_broker == "oanda-practice":
        market_data_broker = "oanda-practice"
        observer_broker = "oanda-practice"
        execution_venue = "oanda-practice"
    elif requested_broker == "manual":
        market_data_broker = "yfinance"
        observer_broker = "yfinance[manual]"
        execution_venue = "manual"
    else:
        market_data_broker = "yfinance"
        observer_broker = "yfinance"
        execution_venue = "paper"

    return RuntimePolicy(
        profile_name=profile_name,
        bot_name=profile["bot_name"],
        category=profile.get("category", "unknown"),
        symbol=canonical,
        timeframe=timeframe,
        family=family,
        market_data_broker=market_data_broker,
        observer_broker=observer_broker,
        execution_venue=execution_venue,
        runtime_mode=runtime_mode,
        notes=" ".join(notes).strip(),
    )