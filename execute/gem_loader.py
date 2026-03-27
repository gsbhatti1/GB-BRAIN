"""GB-BRAIN gem + symbol config loader."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import json
from copy import deepcopy
from pathlib import Path

from config.settings import GEMS_CONFIG_PATH, SYMBOL_REGISTRY_PATH


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_gems() -> dict:
    return _load_json(GEMS_CONFIG_PATH)


def load_symbol_registry() -> dict:
    return _load_json(SYMBOL_REGISTRY_PATH)


def canonical_symbol(symbol: str) -> str:
    if not symbol:
        raise ValueError("symbol is required")
    raw = symbol.strip()
    raw_upper = raw.upper()
    registry = load_symbol_registry()["symbols"]
    for canonical, payload in registry.items():
        aliases = {canonical.upper(), *[str(a).upper() for a in payload.get("aliases", [])]}
        if raw_upper in aliases:
            return canonical
    raise ValueError(f"Unknown symbol: {symbol}")


def get_symbol_profile(symbol: str) -> dict:
    key = canonical_symbol(symbol)
    return deepcopy(load_symbol_registry()["symbols"][key])


def get_runtime_profile(profile_name: str) -> dict:
    key = profile_name.strip().lower()
    profiles = load_gems().get("runtime_profiles", {})
    for name, payload in profiles.items():
        if name.lower() == key or payload.get("bot_name", "").lower() == key:
            return deepcopy(payload)
    raise ValueError(f"Unknown runtime profile: {profile_name}")


def get_strategy_profile(strategy_family: str, symbol: str, timeframe: str) -> dict:
    gems = load_gems().get("strategy_families", {})
    fam = gems.get(strategy_family.lower())
    if fam is None:
        raise ValueError(f"Unknown strategy family: {strategy_family}")
    key = canonical_symbol(symbol)
    payload = deepcopy(fam.get(key, {}).get(timeframe, {}))
    payload.setdefault("status", "inactive")
    payload.setdefault("params", {})
    payload.setdefault("notes", "")
    return payload


def get_best_timeframes(symbol: str) -> list[str]:
    return list(get_symbol_profile(symbol).get("best_timeframes", []))


def build_runtime_context(profile_name: str, strategy_family: str, symbol: str, timeframe: str) -> dict:
    runtime = get_runtime_profile(profile_name)
    sym = get_symbol_profile(symbol)
    strat = get_strategy_profile(strategy_family, symbol, timeframe)
    return {
        "profile": runtime,
        "symbol": sym,
        "strategy": strat,
        "canonical_symbol": canonical_symbol(symbol),
        "timeframe": timeframe,
        "strategy_family": strategy_family.lower(),
    }


if __name__ == "__main__":
    import json as _json
    print(_json.dumps(build_runtime_context("gb-crypto-bot", "combined", "SOL", "15m"), indent=2))
