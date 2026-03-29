# patch_demo_runner.py -- patch demo_runner.py to use new gb_strategy_gems.json v2.0 format
# Run from /home/gb-brain/GB-BRAIN
import re
from pathlib import Path

target = Path("runtime/demo_runner.py")
src = target.read_text(encoding="utf-8")

OLD = '''        # Signal engine — CombinedEngine takes a preset dict
        CE = _import_engine()
        if CE:
            gems_path = ROOT / "config" / "gb_strategy_gems.json"
            try:
                gems   = json.loads(gems_path.read_text(encoding="utf-8"))
                preset = gems.get("combined", {}).get(self.symbol, {}).get("params", {})
            except Exception:
                preset = {}
            self._engine = CE(preset=preset) if preset else None
            if self._engine is None:
                logger.warning(
                    "No preset found for combined/%s — signal engine disabled", self.symbol
                )'''

NEW = '''        # Signal engine — CombinedEngine takes a preset dict
        # gb_strategy_gems.json v2.0: keyed by symbol -> list of GEM dicts
        CE = _import_engine()
        if CE:
            gems_path = ROOT / "config" / "gb_strategy_gems.json"
            preset = {}
            self._active_gem = None
            try:
                gems = json.loads(gems_path.read_text(encoding="utf-8"))
                sym_gems = gems.get(self.symbol, [])
                # Pick best deploy_ready GEM (first = highest composite_score)
                for g in sym_gems:
                    if g.get("deploy_ready", False):
                        preset = g.get("parameters", {})
                        self._active_gem = g.get("name", "unknown")
                        break
            except Exception as exc:
                logger.warning("Failed to load gems config: %s", exc)
            self._engine = CE(preset=preset) if preset else None
            if self._engine is None:
                logger.warning(
                    "No deploy-ready GEM found for %s — signal engine disabled", self.symbol
                )
            else:
                logger.info(
                    "Loaded GEM preset for %s: %s (params=%s)",
                    self.symbol, self._active_gem, list(preset.keys())
                )'''

if OLD in src:
    patched = src.replace(OLD, NEW)
    target.write_text(patched, encoding="utf-8")
    print("OK — demo_runner.py patched successfully")
    print(f"  Symbol: loaded from gb_strategy_gems.json v2.0")
    print(f"  Logic: picks first deploy_ready=true GEM per symbol")
else:
    print("ERROR — old pattern not found. Was demo_runner.py already patched?")
    # Show context around the relevant section
    idx = src.find("Signal engine")
    if idx >= 0:
        print("Found 'Signal engine' at char", idx)
        print(src[idx:idx+600])
    else:
        print("'Signal engine' not found in file at all.")
