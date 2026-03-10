import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def load_gems(path: str = "config/gb_strategy_gems.json") -> dict:
    with (ROOT / path).open("r", encoding="utf-8") as f:
        return json.load(f)

def get_parallax_spx_5m_params() -> dict:
    gems = load_gems()
    return (
        gems
        .get("parallax", {})
        .get("SPX", {})
        .get("5m", {})
        .get("params", {})
    )

def main() -> None:
    params = get_parallax_spx_5m_params()
    print("Parallax SPX 5m params to feed into bot:")
    print(json.dumps(params, indent=2))

if __name__ == "__main__":
    main()
