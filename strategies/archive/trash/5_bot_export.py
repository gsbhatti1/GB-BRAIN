import os, shutil, importlib.util
import pandas as pd

def load_config():
    spec = importlib.util.spec_from_file_location("config",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "0_config.py"))
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg

cfg = load_config()
for folder in ["scalp","swing","intraday"]:
    os.makedirs(os.path.join(cfg.BOT_READY_DIR, folder), exist_ok=True)
df = pd.read_csv(os.path.join(cfg.RESULTS_DIR, "master_results.csv"))
winners = df[df["bot_ready"] == "YES"]
copied = 0
for _, row in winners.iterrows():
    src = os.path.join(cfg.TRANSLATED_DIR, f"{row['strategy']}.md")
    if not os.path.exists(src): continue
    tt = row["trade_type"].lower() if row["trade_type"] in ["SCALP","SWING","INTRADAY"] else "intraday"
    shutil.copy2(src, os.path.join(cfg.BOT_READY_DIR, tt, f"{row['strategy']}.md"))
    copied += 1
print(f"\nExported {copied} bot-ready strategies to {cfg.BOT_READY_DIR}\n")
