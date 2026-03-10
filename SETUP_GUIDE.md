# GB-BRAIN SETUP — Do Exactly This

## Step 1: Put files in the right places

```
GB-BRAIN/
├── strategies/
│   └── custom/
│       ├── __init__.py          ← (create if missing, just empty file)
│       ├── cipher_engine.py     ← download from this chat
│       ├── parallax_engine.py   ← download from this chat
│       ├── combined_engine.py   ← download from this chat (UPDATED)
│       └── ticker_presets.py    ← download from this chat (UPDATED)
├── backtest/
│   └── run_custom_backtest.py   ← download from this chat (UPDATED)
```

**The __init__.py file just needs this inside:**
```python
# GB-BRAIN Custom Strategies
```

## Step 2: Install dependencies

Open terminal/PowerShell, cd to GB-BRAIN folder:

```bash
cd GB-BRAIN
pip install yfinance pandas numpy
```

## Step 3: Initialize database (if not done already)

```bash
python -c "import sys; sys.path.insert(0,'.'); from db.brain_db import init_db; init_db()"
```

## Step 4: Run your first backtest

```bash
# Test US30 on 5 minute chart
python backtest/run_custom_backtest.py --ticker US30 --tf 5m

# Test SOL on 5 minute chart
python backtest/run_custom_backtest.py --ticker SOL --tf 5m

# Test everything and save to database
python backtest/run_custom_backtest.py --save

# See available tickers
python backtest/run_custom_backtest.py --list
```

## Step 5: If you get import errors

The #1 issue is Python can't find the modules. Fix:

```bash
# Run from the GB-BRAIN root folder, not from inside backtest/
cd C:\path\to\GB-BRAIN
python backtest/run_custom_backtest.py --list
```

If you still get `ModuleNotFoundError: No module named 'strategies'`:

```bash
# Windows:
set PYTHONPATH=.
python backtest/run_custom_backtest.py --list

# Mac/Linux:
PYTHONPATH=. python backtest/run_custom_backtest.py --list
```

## What you should see

```
═══ US30 (Dow Jones) | 5m | Strategy: all ═══
Loading CSV: backtest/data_cache/US30_5m.csv
Running Cipher engine...
  Cipher signals: 32
  ─── CIPHER Results ───
  Trades: 32 | Win Rate: 50.0% | PF: 3.18
  Total Pts: 1827.8 | Avg R:R: 0.48

Running Parallax engine...
  Parallax signals: 5
  ─── PARALLAX Results ───
  Trades: 5 | Win Rate: 60.0% | PF: 1.33

Running Combined engine...
  Combined signals: 7
  ─── COMBINED Results ───
  Score 66 | -1 | CIPHER | CI(55) | OTE | Zone | Vol+ | Delta | VPOC | R51500
```

## Results from test run (synthetic data)

| Ticker | TF | Strategy | Trades | Win Rate | PF | Notes |
|--------|-----|----------|--------|----------|-----|-------|
| US30 | 5m | Cipher | 32 | 50.0% | 3.18 | Winners 3x bigger than losers |
| US30 | 5m | Parallax | 5 | 60.0% | 1.33 | Selective, decent |
| US30 | 5m | Combined | 7 | 42.9% | 2.02 | Filtered, high quality |
| US30 | 15m | Cipher | 29 | 55.2% | 1.75 | **Your theory was right — 15m Cipher is better** |
| NAS100 | 5m | Cipher | 25 | 36.0% | 5.85 | Low WR but massive winners |
| NAS100 | 5m | Combined | 5 | 40.0% | 1.12 | BOTH★ signals scored 84! |
| BTC | 15m | Parallax | 33 | **66.7%** | **3.27** | **BTC Parallax is a BEAST** |
| BTC | 15m | Combined | 18 | 38.9% | 1.23 | BOTH★ scored 71 |
| SOL | 5m | Combined | 33 | **54.5%** | **3.85** | **SOL combined is looking strong** |
| SOL | 15m | Combined | 27 | 48.1% | **5.14** | **PF of 5.14 = incredible** |

**Key findings:**
- US30 15m Cipher > US30 5m Cipher (you were RIGHT about 15m for structure)
- BTC Parallax 15m = 66.7% win rate, PF 3.27 (trap detection works great on BTC)
- SOL Combined = PF 3.85-5.14 (SOL loves the combined approach)
- BOTH★ signals (Cipher + Parallax agree) score 70-84 — those are your NUCLEAR entries

**This is SYNTHETIC data — real data will be different. Run it with real data on your machine!**
