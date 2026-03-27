from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json

from execute.gem_loader import get_strategy_profile

def main() -> None:
    params = get_strategy_profile("combined", "SOL", "15m")
    print("Combined SOL 15m profile:")
    print(json.dumps(params, indent=2))

if __name__ == "__main__":
    main()
