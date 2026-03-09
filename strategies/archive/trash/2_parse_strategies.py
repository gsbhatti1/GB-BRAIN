import os, re, json
from pathlib import Path
from collections import Counter
import importlib.util

def load_config():
    spec = importlib.util.spec_from_file_location("config",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "0_config.py"))
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg

cfg = load_config()
os.makedirs(cfg.RESULTS_DIR, exist_ok=True)
PATTERNS = {"RSI": r"\bRSI\b", "EMA": r"\bEMA\b", "MA": r"\bSMA\b|\bmoving average\b",
            "MACD": r"\bMACD\b", "BB": r"\bBollinger\b|\bBB\b", "STOCH": r"\bStochastic\b"}

def parse_file(fp):
    txt = open(fp, "r", encoding="utf-8", errors="ignore").read()
    name = os.path.splitext(os.path.basename(fp))[0]
    hits = [k for k, v in PATTERNS.items() if re.search(v, txt, re.IGNORECASE)]
    rsi_p = re.findall(r"RSI[^\d]*(\d+)", txt, re.IGNORECASE)
    ma_p  = re.findall(r"(?:MA|EMA|SMA)[^\d]*(\d+)", txt, re.IGNORECASE)
    stype = "RSI" if "RSI" in hits else "MACD" if "MACD" in hits else "BB" if "BB" in hits else "EMA" if "EMA" in hits else "MA" if "MA" in hits else "GENERIC"
    return {"name": name, "file": str(fp), "indicators": hits, "type": stype,
            "rsi_period": int(rsi_p[0]) if rsi_p else 14, "ma_period": int(ma_p[0]) if ma_p else 20}

files = list(Path(cfg.TRANSLATED_DIR).rglob("*.md"))
print(f"\nFound {len(files)} strategy files\n")
results = []
for i, f in enumerate(files):
    try: results.append(parse_file(f))
    except: pass
    if i % 500 == 0: print(f"  Parsed {i}/{len(files)}...")
out = os.path.join(cfg.RESULTS_DIR, "strategy_registry.json")
json.dump(results, open(out, "w"), indent=2)
print(f"\nRegistry saved: {len(results)} strategies")
types = Counter(s["type"] for s in results)
for t, c in types.most_common(): print(f"  {t}: {c}")
print()
