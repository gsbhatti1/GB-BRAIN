import os, time
import pandas as pd
import yfinance as yf
from binance.client import Client
from datetime import datetime, timedelta
import importlib.util

def load_config():
    spec = importlib.util.spec_from_file_location("config",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "0_config.py"))
    cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg

cfg = load_config()
os.makedirs(cfg.RESULTS_DIR, exist_ok=True)
CACHE = os.path.join(cfg.RESULTS_DIR, "data_cache")
os.makedirs(CACHE, exist_ok=True)
LOOKBACK = {"1m": 7, "5m": 59, "15m": 59, "30m": 59, "1h": 365}
YF_MAP = {"SPY": "^GSPC", "QQQ": "^NDX", "DIA": "^DJI"}
client = Client(cfg.BINANCE_KEY, cfg.BINANCE_SECRET)

def fetch_binance(ticker, tf, days):
    start = (datetime.now() - timedelta(days=days)).strftime("%d %b %Y")
    klines = client.get_historical_klines(ticker, tf, start)
    df = pd.DataFrame(klines, columns=["timestamp","open","high","low","close","volume","ct","qv","t","tbb","tbq","ignore"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    for c in ["open","high","low","close","volume"]:
        df[c] = df[c].astype(float)
    return df[["open","high","low","close","volume"]]

def fetch_yfinance(yticker, tf, days):
    end = datetime.now()
    start = end - timedelta(days=days)
    df = yf.download(yticker, start=start, end=end, interval=tf, progress=False, auto_adjust=True)
    df.columns = [c.lower() for c in df.columns]
    return df[["open","high","low","close","volume"]].dropna()

print("\nFetching market data...\n")
for tf in cfg.TIMEFRAMES:
    lb = LOOKBACK[tf]
    for ticker in cfg.CRYPTO_TICKERS:
        f = os.path.join(CACHE, f"{ticker}_{tf}.csv")
        if os.path.exists(f): print(f"  cached: {ticker} {tf}"); continue
        try:
            df = fetch_binance(ticker, tf, lb); df.to_csv(f)
            print(f"  {ticker} {tf} -> {len(df)} rows"); time.sleep(0.3)
        except Exception as e: print(f"  FAIL {ticker} {tf}: {e}")
    for ticker, yticker in YF_MAP.items():
        f = os.path.join(CACHE, f"{ticker}_{tf}.csv")
        if os.path.exists(f): print(f"  cached: {ticker} {tf}"); continue
        try:
            df = fetch_yfinance(yticker, tf, lb); df.to_csv(f)
            print(f"  {ticker} {tf} -> {len(df)} rows"); time.sleep(0.3)
        except Exception as e: print(f"  FAIL {ticker} {tf}: {e}")
print("\nData fetch complete!\n")
