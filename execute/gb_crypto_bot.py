"""Wrapper for GB-CRYPTO-BOT runtime."""

from pathlib import Path
import sys
import subprocess

ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "execute" / "custom_runtime_runner.py"

def main():
    args = [
        sys.executable,
        str(RUNNER),
        "--profile", "gb-crypto-bot",
        "--broker", "auto",
        "--mode", "paper",
    ]
    args.extend(sys.argv[1:])
    raise SystemExit(subprocess.call(args, cwd=str(ROOT)))

if __name__ == "__main__":
    main()
