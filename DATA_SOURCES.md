# GB-BRAIN: Data Source Guide
## Where to Get Every Piece of Institutional Data

---

## FREE — No API Key Needed

| Data | Source | Python Package | What You Get |
|------|--------|---------------|--------------|
| **OHLCV (stocks/indices)** | Yahoo Finance | `yfinance` | 5m/15m for 60 days, 1h for 2 years |
| **OHLCV (crypto)** | Binance | `python-binance` | All timeframes, years of history |
| **Volume Profile / VPOC** | **Calculated from OHLCV** | Built into combined_engine.py | VPOC, Value Area, HVN/LVN |
| **Delta (buy/sell pressure)** | **Calculated from candles** | Built into combined_engine.py | Estimated from close position in range |
| **COT Reports** | CFTC.gov | `cot-reports` or `pycot-reports` | Weekly institutional positioning |
| **Market Breadth (Dow 30)** | Yahoo Finance | `yfinance` | Download all 30 stocks, count green/red |
| **Bollinger Squeeze** | **Calculated from OHLCV** | Built into combined_engine.py | BB inside Keltner = squeeze |
| **RSI Divergence** | **Calculated from OHLCV** | Built into combined_engine.py | Price vs RSI disagreement |
| **Economic Calendar** | ForexFactory or Investing.com | `investpy` or web scraping | NFP, CPI, FOMC dates and times |

## FREE — API Key Required (Free Tier)

| Data | Source | API Key | Limits |
|------|--------|---------|--------|
| **Intraday data** | Alpha Vantage | Free key at alphavantage.co | 25 calls/day on free |
| **Real-time crypto** | Binance API | Free signup | No limit on market data |
| **US stocks real-time** | Alpaca | Free paper trading account | Unlimited on paper account |
| **Forex data** | OANDA | Free demo account | Full access on demo |
| **News sentiment** | Finnhub | Free tier | 60 calls/minute |

## PAID — Worth It If Serious

| Data | Source | Cost | What You Get |
|------|--------|------|-------------|
| **True Order Flow / DOM** | Bookmap, Jigsaw | $50-100/mo | Real bid/ask, iceberg orders |
| **Dark Pool data** | Unusual Whales, FlowAlgo | $40-70/mo | Off-exchange institutional trades |
| **Options Flow** | Unusual Whales, Cheddar Flow | $40-100/mo | Unusual options activity = institutional bets |
| **Level 2 / Tape** | Your broker | Usually included | Real-time order book |

---

## WHAT'S ALREADY BUILT (in combined_engine.py)

These institutional features are calculated FROM your OHLCV data — no extra data needed:

1. **Volume Profile / VPOC** — Rolling 50-bar VPOC computed from volume distribution
2. **Cumulative Volume Delta** — Estimated buy vs sell pressure from candle structure
3. **Bollinger Band Squeeze** — BB inside Keltner = compression before breakout
4. **RSI Divergence** — Price/RSI disagreement detection
5. **Displacement Detection** — Large body candles > 1.5x ATR = institutional commitment
6. **Round Number Levels** — Auto-calculated from ticker preset increment
7. **Kill Zone Timing** — Session-based trade quality weighting
8. **News Window Blocking** — Time-based blackout during high-impact releases
9. **Day-of-Week Filter** — Monday penalty, Wednesday bonus

## WHAT TO ADD NEXT (needs external data)

### Market Breadth (Dow 30 Advance/Decline)
```python
# This replaces your CNBC manual check
import yfinance as yf
dow30 = ['AAPL','AMGN','AXP','BA','CAT','CRM','CSCO','CVX','DIS','DOW',
         'GS','HD','HON','IBM','INTC','JNJ','JPM','KO','MCD','MMM',
         'MRK','MSFT','NKE','PG','SHW','TRV','UNH','V','VZ','WMT']
data = yf.download(dow30, period='2d', interval='1d')['Close']
today = data.iloc[-1]
yesterday = data.iloc[-2]
green = (today > yesterday).sum()
red = (today < yesterday).sum()
breadth_score = green / 30  # 0.0 to 1.0
# breadth_score > 0.66 = bullish, < 0.33 = bearish
```

### COT Report (Institutional Positioning)
```python
from cot_reports import cot_report
# Get Dow Jones futures COT data
df = cot_report(report_type='legacy_fut', cot_report_type='futures_only')
djia = df[df['Market and Exchange Names'].str.contains('DJIA')]
# Commercials net position = institutional bias
commercial_net = djia['Commercial Long'] - djia['Commercial Short']
```

---

## HOW TO RUN BACKTESTS

```bash
# Install dependencies first
pip install yfinance pandas numpy ta backtesting pycot-reports --break-system-packages

# Test one ticker
python backtest/run_custom_backtest.py --ticker US30 --tf 5m --strategy combined

# Test all tickers on their best timeframes
python backtest/run_custom_backtest.py --save

# List available tickers
python backtest/run_custom_backtest.py --list

# Test your theory: 5m Parallax vs 15m Cipher
python backtest/run_custom_backtest.py --ticker US30 --tf 5m --strategy parallax
python backtest/run_custom_backtest.py --ticker US30 --tf 15m --strategy cipher
```
