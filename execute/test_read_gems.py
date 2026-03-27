from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json

from execute.gem_loader import load_gems, get_runtime_profile

def main() -> None:
    gems = load_gems()
    print("Available runtime profiles:")
    print(json.dumps(list(gems.get("runtime_profiles", {}).keys()), indent=2))
    print()
    print("GB-CRYPTO-BOT profile:")
    print(json.dumps(get_runtime_profile("gb-crypto-bot"), indent=2))

if __name__ == "__main__":
    main()
