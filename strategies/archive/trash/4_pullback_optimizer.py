# ================================================================
# GB PULLBACK OPTIMIZER - 2000 LOOP BRUTE FORCE
# Based on: GB Master Ultimate Strategy - Pullback to EMA method
# Variables: EMA_FAST, RSI_ZONE, ATR_MULT, RR_RATIO
# Asset: NAS100 (NQ=F) - 5 minute bars
# Output: Top 5 variable combos ranked by Score
# Score = Win Rate * Profit Factor
# ================================================================

import yfinance as yf
import pandas as pd
import numpy as np
import itertools
import os
import json
from datetime import datetime

# ---- CONFIG ----
SYMBOL   = "NQ=F"
PERIOD   = "2y"
INTERVAL = "5m"
OUT_DIR  = os.path.join(os.path.expanduser("~"), "qwen-dev", "Future-Trading", "4_backtest_results")
os.makedirs(OUT_DIR, exist_ok=True)

print("[INFO] Downloading NAS100 5m data...")
try:
    df = yf.download(SYMBOL, period=PERIOD, interval=INTERVAL, auto_adjust=True, progress=False)
except Exception as e:
    print(f"[RETRY] {e}")
    df = yf.download("^NDX", period="60d", interval="5m", auto_adjust=True, progress=False)

if df.empty:
    print("[ERROR] No data downloaded.")
    exit()

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df.index = pd.to_datetime(df.index)
if df.index.tz is None:
    df.index = df.index.tz_localize("UTC").tz_convert("America/New_York")
else:
    df.index = df.index.tz_convert("America/New_York")

df["hour"]   = df.index.hour
df["minute"] = df.index.minute
df["date"]   = df.index.date

print(f"[INFO] Downloaded {len(df)} bars. Running Pullback optimizer...")

# ---- 4 VARIABLES (GB Master Pullback) ----
# 1. EMA_FAST  - Fast EMA period (price must be near this)
# 2. RSI_ZONE  - RSI threshold for pullback confirmation
# 3. ATR_MULT  - ATR multiplier for stop loss
# 4. RR_RATIO  - Reward to Risk ratio

ema_fast_periods = [8, 10, 13, 20, 21, 34]         # Variable 1: EMA FAST
rsi_zones        = [40, 45, 50, 55, 60]             # Variable 2: RSI ZONE
atr_mults        = [0.5, 0.75, 1.0, 1.5, 2.0]      # Variable 3: ATR MULT
rr_ratios        = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]  # Variable 4: RR RATIO

all_combos = list(itertools.product(ema_fast_periods, rsi_zones, atr_mults, rr_ratios))
total = len(all_combos)
print(f"[INFO] Total combinations: {total}")

# ---- HELPER: EMA ----
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

# ---- HELPER: RSI ----
def rsi(series, period=14):
    delta = series.diff()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta.clip(upper=0)).rolling(period).mean()
    rs    = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

# ---- HELPER: ATR ----
def atr(df, period=14):
    tr = pd.concat([
        df["High"] - df["Low"],
        (df["High"] - df["Close"].shift()).abs(),
        (df["Low"]  - df["Close"].shift()).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()

# Pre-compute indicators on full dataset
print("[INFO] Pre-computing indicators...")
df["atr14"] = atr(df, 14)
df["rsi14"] = rsi(df["Close"], 14)
for p in ema_fast_periods:
    df[f"ema{p}"] = ema(df["Close"], p)
df["ema200"] = ema(df["Close"], 200)
df["ema50"]  = ema(df["Close"], 50)

# ---- BACKTEST FUNCTION ----
def backtest_pullback(df, ema_fast_p, rsi_zone, atr_mult, rr_ratio):
    results = []
    ema_col = f"ema{ema_fast_p}"

    # NY session filter 9:30-15:30
    session = df[
        ((df["hour"] == 9)  & (df["minute"] >= 30)) |
        ((df["hour"] >= 10) & (df["hour"] < 15)) |
        ((df["hour"] == 15) & (df["minute"] <= 30))
    ].copy()

    in_trade = False
    sl = None
    tp = None
    direction = None

    for idx, row in session.iterrows():
        if pd.isna(row[ema_col]) or pd.isna(row["ema200"]) or pd.isna(row["rsi14"]) or pd.isna(row["atr14"]):
            continue

        # Exit check first
        if in_trade:
            if direction == "long":
                if row["Low"] <= sl:
                    results.append(-abs(row[ema_col] - sl))
                    in_trade = False
                elif row["High"] >= tp:
                    results.append(abs(tp - row[ema_col]))
                    in_trade = False
            elif direction == "short":
                if row["High"] >= sl:
                    results.append(-abs(sl - row[ema_col]))
                    in_trade = False
                elif row["Low"] <= tp:
                    results.append(abs(row[ema_col] - tp))
                    in_trade = False
            continue

        # LONG: HTF trend up (ema50 > ema200) + price above ema200
        # + RSI pulled back below zone + price near ema_fast
        htf_bull = row["ema50"] > row["ema200"]
        near_ema = abs(row["Close"] - row[ema_col]) / row[ema_col] < 0.003

        if htf_bull and row["Close"] > row["ema200"] and row["rsi14"] < rsi_zone and near_ema:
            entry = row["Close"]
            sl    = row["Low"] - (row["atr14"] * atr_mult)
            risk  = entry - sl
            if risk <= 0:
                continue
            tp = entry + (risk * rr_ratio)
            in_trade  = True
            direction = "long"

        # SHORT: HTF trend down + price below ema200
        # + RSI pushed above (100 - zone) + price near ema_fast
        htf_bear = row["ema50"] < row["ema200"]
        if htf_bear and row["Close"] < row["ema200"] and row["rsi14"] > (100 - rsi_zone) and near_ema:
            entry = row["Close"]
            sl    = row["High"] + (row["atr14"] * atr_mult)
            risk  = sl - entry
            if risk <= 0:
                continue
            tp = entry - (risk * rr_ratio)
            in_trade  = True
            direction = "short"

    if len(results) < 10:
        return None

    wins  = [r for r in results if r > 0]
    losses= [r for r in results if r <= 0]
    win_rate = len(wins) / len(results) * 100
    gross_profit = sum(wins)
    gross_loss   = abs(sum(losses)) if losses else 0.0001
    profit_factor = gross_profit / gross_loss
    net_pnl = sum(results)
    score   = (win_rate / 100) * profit_factor

    return {
        "ema_fast"     : ema_fast_p,
        "rsi_zone"     : rsi_zone,
        "atr_mult"     : atr_mult,
        "rr_ratio"     : rr_ratio,
        "trades"       : len(results),
        "win_rate"     : round(win_rate, 2),
        "profit_factor": round(profit_factor, 3),
        "net_pnl"      : round(net_pnl, 2),
        "score"        : round(score, 4)
    }

# ---- RUN 2000+ LOOPS ----
all_results = []
for i, (ema_p, rsi_z, atr_m, rr) in enumerate(all_combos):
    if i % 100 == 0:
        print(f"[PROGRESS] [{i}/{total}] EMA={ema_p} RSI={rsi_z} ATR={atr_m} RR={rr}")
    result = backtest_pullback(df, ema_p, rsi_z, atr_m, rr)
    if result:
        all_results.append(result)

# ---- RANK AND SAVE TOP 5 ----
if not all_results:
    print("[ERROR] No valid results.")
    exit()

ranked = sorted(all_results, key=lambda x: x["score"], reverse=True)
top5   = ranked[:5]

print("\n" + "="*60)
print("  GB PULLBACK OPTIMIZER - TOP 5 RESULTS")
print("="*60)
for rank, r in enumerate(top5, 1):
    print(f"\nRank #{rank}")
    print(f"  EMA Fast     : {r['ema_fast']}")
    print(f"  RSI Zone     : <{r['rsi_zone']} (Long) / >{100 - r['rsi_zone']} (Short)")
    print(f"  ATR Mult     : {r['atr_mult']}")
    print(f"  RR Ratio     : {r['rr_ratio']}")
    print(f"  Trades       : {r['trades']}")
    print(f"  Win Rate     : {r['win_rate']}%")
    print(f"  Profit Factor: {r['profit_factor']}")
    print(f"  Net PnL      : {r['net_pnl']}")
    print(f"  Score        : {r['score']}")
print("="*60)

out_file = os.path.join(OUT_DIR, "pullback_optimizer_top5.json")
with open(out_file, "w") as f:
    json.dump({"timestamp": str(datetime.now()), "top5": top5, "total_combos_tested": len(all_combos), "valid_results": len(all_results)}, f, indent=2)
print(f"\n[SAVED] {out_file}")

out_csv = os.path.join(OUT_DIR, "pullback_optimizer_full.csv")
pd.DataFrame(ranked).to_csv(out_csv, index=False)
print(f"[SAVED] {out_csv}")
print("\n[DONE] Copy Rank #1 variables into GB-Master-Ultimate-Strategy.pine settings!")
