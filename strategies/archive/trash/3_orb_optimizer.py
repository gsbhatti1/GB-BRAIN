# ================================================================
# GB ORB OPTIMIZER - 2000 LOOP BRUTE FORCE
# Based on: TradeXLabs method - 4 key variables
# Variables: TIME, ATR, VOLUME, VOLATILITY (RR ratio)
# Asset: NAS100 (^NDX) - 5 minute bars
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
SYMBOL     = "NQ=F"        # NAS100 Futures
PERIOD     = "2y"          # 2 years of data
INTERVAL   = "5m"          # 5 minute bars
OUT_DIR    = os.path.join(os.path.expanduser("~"), "qwen-dev", "Future-Trading", "4_backtest_results")
os.makedirs(OUT_DIR, exist_ok=True)

print("[INFO] Downloading NAS100 5m data...")
try:
    df = yf.download(SYMBOL, period=PERIOD, interval=INTERVAL, auto_adjust=True, progress=False)
except Exception as e:
    print(f"[ERROR] Download failed: {e}")
    print("[RETRY] Trying ^NDX...")
    df = yf.download("^NDX", period="60d", interval="5m", auto_adjust=True, progress=False)

if df.empty:
    print("[ERROR] No data. Check internet connection.")
    exit()

# Flatten columns if multi-index
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

print(f"[INFO] Downloaded {len(df)} bars. Running optimizer...")

# ---- 4 VARIABLES (matching TradeXLabs) ----
# 1. TIME     - ORB window end minute (9:35, 9:40, 9:45, 9:50, 9:55, 10:00)
# 2. ATR      - Minimum ATR multiplier for range size filter
# 3. VOLUME   - Volume multiplier vs 20-period average
# 4. RR RATIO - Reward to Risk ratio

orb_end_minutes = [35, 40, 45, 50, 55, 60]           # Variable 1: TIME
atr_multiples   = [0.3, 0.5, 0.7, 1.0, 1.2, 1.5]    # Variable 2: ATR
vol_multiples   = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]  # Variable 3: VOLUME
rr_ratios       = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]    # Variable 4: VOLATILITY/RR

all_combos = list(itertools.product(orb_end_minutes, atr_multiples, vol_multiples, rr_ratios))
total = len(all_combos)
print(f"[INFO] Total combinations: {total} (running all {total} loops)")

# ---- BACKTEST FUNCTION ----
def backtest_orb(df, orb_end_min, atr_mult, vol_mult, rr_ratio, sl_atr=0.5):
    results = []
    dates = df["date"].unique()

    for d in dates:
        day = df[df["date"] == d].copy()

        # Build ORB: 9:30 to orb_end_min
        orb_bars = day[(day["hour"] == 9) & (day["minute"] >= 30) & (day["minute"] < orb_end_min)]
        if len(orb_bars) < 2:
            continue

        orb_high = orb_bars["High"].max()
        orb_low  = orb_bars["Low"].min()
        orb_range = orb_high - orb_low

        # ATR filter: ORB range must be meaningful
        atr = day["High"].sub(day["Low"]).rolling(14).mean().iloc[-1]
        if pd.isna(atr) or orb_range < atr * atr_mult:
            continue

        # Volume filter: first ORB bar volume vs rolling average
        vol_avg = day["Volume"].rolling(20).mean().iloc[len(orb_bars)]
        if pd.isna(vol_avg) or orb_bars["Volume"].iloc[0] < vol_avg * vol_mult:
            continue

        # Trade bars: after ORB closes to 3:30 PM
        trade_bars = day[
            ((day["hour"] == 9) & (day["minute"] >= orb_end_min)) |
            ((day["hour"] >= 10) & (day["hour"] < 15)) |
            ((day["hour"] == 15) & (day["minute"] <= 30))
        ]

        in_trade = False
        for idx, row in trade_bars.iterrows():
            if in_trade:
                continue

            # Long breakout
            if row["Close"] > orb_high:
                entry = row["Close"]
                sl    = orb_low - (atr * sl_atr)
                risk  = entry - sl
                if risk <= 0:
                    continue
                tp = entry + (risk * rr_ratio)

                # Scan forward for SL or TP hit
                future = trade_bars.loc[idx:]
                outcome = None
                for _, fr in future.iterrows():
                    if fr["Low"] <= sl:
                        outcome = -risk
                        break
                    if fr["High"] >= tp:
                        outcome = risk * rr_ratio
                        break
                if outcome is not None:
                    results.append(outcome)
                    in_trade = True

            # Short breakout
            elif row["Close"] < orb_low:
                entry = row["Close"]
                sl    = orb_high + (atr * sl_atr)
                risk  = sl - entry
                if risk <= 0:
                    continue
                tp = entry - (risk * rr_ratio)

                future = trade_bars.loc[idx:]
                outcome = None
                for _, fr in future.iterrows():
                    if fr["High"] >= sl:
                        outcome = -risk
                        break
                    if fr["Low"] <= tp:
                        outcome = risk * rr_ratio
                        break
                if outcome is not None:
                    results.append(outcome)
                    in_trade = True

    if len(results) < 10:
        return None

    wins   = [r for r in results if r > 0]
    losses = [r for r in results if r <= 0]
    win_rate = len(wins) / len(results) * 100
    gross_profit = sum(wins)
    gross_loss   = abs(sum(losses)) if losses else 0.0001
    profit_factor = gross_profit / gross_loss
    net_pnl  = sum(results)
    score    = (win_rate / 100) * profit_factor  # Combined score

    return {
        "orb_end_min" : orb_end_min,
        "atr_mult"    : atr_mult,
        "vol_mult"    : vol_mult,
        "rr_ratio"    : rr_ratio,
        "trades"      : len(results),
        "win_rate"    : round(win_rate, 2),
        "profit_factor": round(profit_factor, 3),
        "net_pnl"     : round(net_pnl, 2),
        "score"       : round(score, 4)
    }

# ---- RUN 2000+ LOOPS ----
all_results = []
for i, (orb_end, atr_m, vol_m, rr) in enumerate(all_combos):
    if i % 100 == 0:
        print(f"[PROGRESS] [{i}/{total}] Running combo: ORB_END=9:{orb_end} ATR={atr_m} VOL={vol_m} RR={rr}")
    result = backtest_orb(df, orb_end, atr_m, vol_m, rr)
    if result:
        all_results.append(result)

# ---- RANK AND SAVE TOP 5 ----
if not all_results:
    print("[ERROR] No valid results. Try wider date range.")
    exit()

ranked = sorted(all_results, key=lambda x: x["score"], reverse=True)
top5   = ranked[:5]

print("\n" + "="*60)
print("  GB ORB OPTIMIZER - TOP 5 RESULTS")
print("="*60)
for rank, r in enumerate(top5, 1):
    orb_time = f"9:{r['orb_end_min']:02d} AM" if r['orb_end_min'] < 60 else "10:00 AM"
    print(f"\nRank #{rank}")
    print(f"  ORB Window : 9:30 - {orb_time}")
    print(f"  ATR Mult   : {r['atr_mult']}")
    print(f"  Vol Mult   : {r['vol_mult']}")
    print(f"  RR Ratio   : {r['rr_ratio']}")
    print(f"  Trades     : {r['trades']}")
    print(f"  Win Rate   : {r['win_rate']}%")
    print(f"  Profit Factor: {r['profit_factor']}")
    print(f"  Net PnL    : {r['net_pnl']}")
    print(f"  Score      : {r['score']}")
print("="*60)

# Save to JSON
out_file = os.path.join(OUT_DIR, "orb_optimizer_top5.json")
with open(out_file, "w") as f:
    json.dump({"timestamp": str(datetime.now()), "top5": top5, "total_combos_tested": len(all_combos), "valid_results": len(all_results)}, f, indent=2)
print(f"\n[SAVED] Results saved to: {out_file}")

# Save full ranked CSV
out_csv = os.path.join(OUT_DIR, "orb_optimizer_full.csv")
pd.DataFrame(ranked).to_csv(out_csv, index=False)
print(f"[SAVED] Full results saved to: {out_csv}")
print("\n[DONE] Copy the Rank #1 variables into GB-ORB-Strategy.pine settings!")
