import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def load_gems(path: str = "config/gb_strategy_gems.json") -> dict:
    with (ROOT / path).open("r", encoding="utf-8") as f:
        return json.load(f)

def strategy_name_key(name: str) -> str:
    return name.lower().replace(" ", "-")

def get_gem(gems: dict, strategy_name: str, symbol: str, interval_sec: int) -> dict | None:
    tf_map = {60: "1m", 300: "5m", 900: "15m"}
    tf = tf_map.get(interval_sec)
    if tf is None:
        return None
    strat_key = strategy_name_key(strategy_name)
    return gems.get(strat_key, gems.get("parallax", {})).get(symbol, {}).get(tf)

def main() -> None:
    gems = load_gems()
    gem = get_gem(gems, "parallax", "SPX", 300)
    print("GEM for parallax SPX 5m:")
    print(json.dumps(gem, indent=2))

if __name__ == "__main__":
    main()
