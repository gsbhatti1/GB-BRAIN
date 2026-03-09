# GB-BRAIN: Complete Trading Knowledge Base
## Everything Hedge Funds & Bankers Know That You Need

---

## PART 1: INSTITUTIONAL BEHAVIORS
### What Smart Money Does That Retail Doesn't See

---

### A. LIQUIDITY ENGINEERING (The #1 Thing You're Missing)

**1. Liquidity Sweeps / Stop Hunts**
- Institutions NEED liquidity to fill their massive orders
- They push price THROUGH obvious support/resistance to trigger retail stop-losses
- Those triggered stops BECOME the liquidity institutions use to enter
- This is EXACTLY what Parallax detects as a "trap"
- Your Parallax trap detection IS a liquidity sweep detector — you just didn't name it that

**2. Buy-Side Liquidity (BSL)**
- Resting buy stops above swing highs, equal highs, trendline highs
- Institutions drive price UP to grab these stops
- After the sweep: sharp reversal down
- On US30: those 250-increment levels are BSL magnets

**3. Sell-Side Liquidity (SSL)**
- Resting sell stops below swing lows, equal lows, trendline lows
- Institutions drive price DOWN to grab these stops
- After the sweep: sharp reversal up

**4. Equal Highs / Equal Lows**
- When price makes 2+ highs at the same level = retail sees "resistance"
- What institutions see: a POOL of stop-losses sitting above
- Equal lows = same thing on the downside
- Cipher should detect and mark these — it currently doesn't

**5. Inducement**
- A small fake move that lures retail into a trade before the real move
- Example: price breaks above a small resistance, retail goes long, then price dumps
- This is a mini-version of Parallax's trap concept

---

### B. ORDER FLOW & ACCUMULATION

**6. Wyckoff Accumulation / Distribution**
- 4 phases: Accumulation → Markup → Distribution → Markdown
- Accumulation: institutions quietly buying in a range (looks boring/sideways)
- Spring: the fake breakdown at the end of accumulation (= liquidity sweep)
- Distribution: institutions quietly selling in a range at highs
- UTAD (Upthrust After Distribution): fake breakout before markdown

**7. ICT Kill Zones (Time-Based)**
- London Open: 02:00-05:00 ET — first major liquidity of the day
- New York Open: 09:30-11:00 ET — highest volume, biggest moves
- London Close: 10:00-12:00 ET — reversal zone
- Asian Session: 20:00-00:00 ET — accumulation/ranging (low conviction)
- Parallax is already using session times — but could optimize for kill zones specifically

**8. Market Maker Buy/Sell Models (ICT)**
- MM Buy Model: SSL sweep → accumulation → markup (long)
- MM Sell Model: BSL sweep → distribution → markdown (short)
- This is the full cycle your combined system should detect

**9. Displacement**
- A large, aggressive candle that breaks structure with force
- Signals institutional commitment — not just a wick, a BODY close through a level
- Your Parallax already checks candle body direction — this is displacement detection

**10. Propulsion Blocks**
- A candle during an aggressive move that marks where institutions added to positions
- When price returns to this level, it acts as continuation support
- Different from regular Order Blocks — these are mid-move, not pre-move

---

### C. TIME & PRICE THEORY

**11. Time of Day Bias**
- Institutions have execution algorithms that run at specific times
- 09:30-09:45 ET: initial volatility/fakeouts (your ORB window)
- 09:45-10:30 ET: true direction often established
- 10:30-11:30 ET: first pullback zone
- 14:00-15:00 ET: afternoon reversal zone
- 15:30-16:00 ET: end-of-day profit-taking

**12. Day of Week Bias**
- Monday: range-finding, low conviction — AVOID for best win rate
- Tuesday: direction often established
- Wednesday: often the strongest trending day (mid-week reversal point)
- Thursday: continuation or reversal setup
- Friday: profit-taking, reduced conviction after 12:00 ET

**13. Quarterly Theory / Market Cycles**
- Institutions rebalance quarterly (March, June, September, December)
- Last 2 weeks of quarter: unusual volume and reversals
- First week of quarter: new institutional positioning begins
- FOMC meetings + NFP + CPI = institutional re-pricing events

**14. AMD (Accumulation, Manipulation, Distribution)**
- Every trading day follows this cycle
- Asian session = Accumulation (range)
- London open = Manipulation (fake move to grab liquidity)
- NY session = Distribution (real move)
- Your Parallax sessions literally map to this

---

### D. PRICE DELIVERY CONCEPTS

**15. Premium / Discount Arrays**
- Premium zone (above 50% of range): sell zone for institutions
- Discount zone (below 50% of range): buy zone for institutions
- Cipher already has this — but it's not weighted into entry scoring

**16. Optimal Trade Entry (OTE)**
- Fib 61.8-78.6% retracement of the impulse leg
- Sweet spot: 70.5% — your Cipher OTE is already set here
- This is WHERE institutions re-enter after an impulse

**17. Dealing Range**
- The range between the most recent swing high and swing low
- All institutional activity happens WITHIN this range until it breaks
- Cipher tracks this but doesn't score entries by WHERE in the range they occur

**18. Consequent Encroachment (CE)**
- The 50% midpoint of any zone (FVG, OB, breaker)
- When price reaches CE of a zone, consider it "mitigated"
- Your FVG mitigation currently uses the midpoint — this is the same concept

**19. Mitigation Blocks**
- When an Order Block fails and price returns to close out those trapped orders
- The OB gets "mitigated" — absorbed by the market
- Your OB/Breaker detection does this already

**20. Imbalance / Inefficiency**
- Any price range where one side (buyers or sellers) overwhelmingly dominated
- FVGs are the visual representation of imbalance
- Price tends to return to fill these imbalances
- Cipher detects these but doesn't score their quality

---

### E. WHAT YOU DON'T HAVE YET (and should)

**21. Volume Profile / VPOC**
- Shows WHERE most trading happened (not just how much)
- VPOC (Volume Point of Control) = price level with most volume
- Acts as a magnet — price returns to VPOC repeatedly
- Not available in basic PineScript — but Python can calculate it

**22. Delta (Cumulative Volume Delta)**
- Difference between buying and selling volume at each price
- Rising price + negative delta = weak rally (institutions distributing)
- Falling price + positive delta = weak selloff (institutions accumulating)
- This is ORDER FLOW — the most advanced institutional tool

**23. Market Breadth**
- How many stocks in the index are going up vs down
- You're doing this manually on CNBC — checking green vs red in Dow 30
- Python can pull this automatically via Yahoo Finance or Alpha Vantage

**24. Commitment of Traders (COT)**
- Weekly report showing what large speculators and commercials are doing
- If commercials are heavily long while price drops = accumulation
- Available for futures markets (NAS100, US30, etc.)

**25. Dark Pool Activity**
- Off-exchange institutional trades
- When dark pool volume spikes at a level = institutional interest
- Available through some data providers (not free)

---

## PART 2: COMPLETE INDICATOR & STRATEGY TAXONOMY
### Every Tool in the Trading Arsenal

---

### A. TREND INDICATORS (Direction)

| Indicator | What It Does | Best Use | Your GEM Data |
|-----------|-------------|----------|---------------|
| **EMA** (Exponential MA) | Weighted moving average, recent data heavier | Trend direction, dynamic S/R | 58 SPX GEMs |
| **SMA** (Simple MA) | Equal-weight moving average | Longer-term trend | 26 SPX GEMs |
| **DEMA** (Double EMA) | Less lag than EMA | Faster trend signals | 2 SPX GEMs |
| **TEMA** (Triple EMA) | Even less lag | Very responsive trend | 4 SPX GEMs |
| **HMA** (Hull MA) | Smoothed, minimal lag | Clean crossovers | 5 SPX GEMs |
| **WMA** (Weighted MA) | Linear weight | Alternative trend | 4 SPX GEMs |
| **VWAP** | Volume-weighted average price | Institutional fair value | 15 SPX GEMs |
| **SuperTrend** | ATR-based trend band | Trend + SL level | 4 SPX GEMs |
| **Ichimoku** | Cloud system (5 components) | Multi-signal trend | 16 SPX GEMs |
| **Parabolic SAR** | Trailing dots | Trend + exit timing | Present in GEMs |
| **ADX** | Trend strength (not direction) | Filter weak trends | 13 SPX GEMs |
| **Aroon** | Time since last high/low | Trend maturity | Rare |
| **DMI** | Directional movement +DI/-DI | Trend direction | 6 SPX GEMs |

**Key combo from your data: EMA 21/50/200 + VWAP** (your Master v27 uses this and it's your best performer)

---

### B. MOMENTUM INDICATORS (Speed & Overbought/Oversold)

| Indicator | What It Does | Best Use | Your GEM Data |
|-----------|-------------|----------|---------------|
| **RSI** | Momentum oscillator 0-100 | OB/OS + divergence | **276 SPX GEMs** (47%!) |
| **Stochastic** | Close position within range | Fast OB/OS signals | 8 SPX GEMs |
| **StochRSI** | RSI of RSI | More sensitive OB/OS | Common in SOL |
| **MACD** | Trend momentum (2 EMAs + signal) | Crossovers + divergence | 53 SPX GEMs |
| **CCI** (Commodity Channel) | Deviation from mean | Mean reversion | 9 SPX GEMs |
| **CMO** (Chande Momentum) | Modified momentum | Mean reversion | **2 SOL GEMs (89.9% WR!)** |
| **MFI** (Money Flow Index) | Volume-weighted RSI | Institutional flow | 1 SPX GEM |
| **Williams %R** | Stochastic variant | OB/OS zones | 5 SPX GEMs |
| **ROC** (Rate of Change) | Price momentum | Momentum shifts | Rare |
| **Momentum** | Raw momentum | Trend confirmation | 50 SPX GEMs |

**YOUR #1 FINDING: RSI appears in 47% of all winning strategies. It should be in EVERYTHING.**

---

### C. VOLATILITY INDICATORS (Range & Squeeze)

| Indicator | What It Does | Best Use | Your GEM Data |
|-----------|-------------|----------|---------------|
| **Bollinger Bands** | Standard deviation bands | Mean reversion + breakout | **148 SPX GEMs** (25%!) |
| **Keltner Channels** | ATR-based bands | Trend channels | 5 SPX GEMs |
| **BB + Keltner Squeeze** | BB inside KC = compression | Breakout anticipation | **3 GEMs (killer combo)** |
| **ATR** | Average True Range | SL sizing, volatility | 12 SPX GEMs |
| **Donchian Channels** | Highest high / lowest low | Breakout system | Rare |
| **Standard Deviation** | Raw volatility measure | Volatility filter | Embedded in BB |

**YOUR #2 FINDING: Bollinger + RSI = the #1 winning combo (53 GEMs). Add this to Cipher.**

---

### D. VOLUME INDICATORS (Institutional Flow)

| Indicator | What It Does | Best Use | Your GEM Data |
|-----------|-------------|----------|---------------|
| **OBV** (On-Balance Volume) | Cumulative volume direction | Divergence from price | 9 SPX GEMs |
| **Volume Profile** | Volume at each price level | S/R levels from volume | Not in current GEMs |
| **VWAP** | Institutional fair value | Mean reversion + bias | 15 SPX GEMs |
| **CMF** (Chaikin Money Flow) | Accumulation/Distribution | Institutional flow | Rare |
| **A/D Line** | Accumulation/Distribution | Confirm trends | Rare |
| **Volume SMA** | Average volume | Volume breakouts | Common |

---

### E. STRUCTURE / PATTERN STRATEGIES

| Strategy | What It Does | In Your System? |
|----------|-------------|-----------------|
| **BOS** (Break of Structure) | Trend continuation signal | ✅ Cipher |
| **ChoCh** (Change of Character) | Trend reversal signal | ✅ Cipher |
| **FVG** (Fair Value Gap) | Price imbalance zone | ✅ Cipher |
| **Order Blocks** | Institutional entry zones | ✅ Cipher |
| **Breaker Blocks** | Failed OBs that flip | ✅ Cipher |
| **ORB** (Opening Range Breakout) | Session range break | ✅ Parallax |
| **Trap Detection** | Fake breakout reversal | ✅ Parallax |
| **Liquidity Sweep** | Stop hunt detection | ⚠️ Parallax does this implicitly |
| **Engulfing Pattern** | Reversal candle pattern | ❌ Not in your system |
| **Pin Bar / Hammer** | Rejection candle | ❌ Not in your system |
| **Double Top/Bottom** | Reversal pattern | ❌ Not in your system |
| **Head & Shoulders** | Complex reversal | ❌ Not in your system |
| **ABCD Pattern** | Harmonic pattern | Present in SPX GEMs |
| **Fibonacci Retracement** | OTE / pullback levels | ✅ Cipher OTE |
| **Supply / Demand Zones** | Institutional zones | ⚠️ Similar to OB |
| **Wyckoff Phases** | Accumulation/Distribution | ❌ Not in your system |

---

### F. TOP WINNING COMBOS FROM YOUR 591 SPX GEMS

| Rank | Combination | Count | Notes |
|------|------------|-------|-------|
| 1 | **Bollinger + RSI** | 53 | THE KING — add to both strategies |
| 2 | **EMA + MACD** | 8 | Classic trend momentum |
| 3 | **RSI + Divergence** | 7 | High-conviction reversals |
| 4 | **Momentum + Squeeze** | 7 | Breakout anticipation |
| 5 | **RSI + Stochastic** | 6 | Double momentum filter |
| 6 | **Momentum + RSI** | 6 | Trend strength |
| 7 | **MACD + RSI** | 5 | Signal + filter |
| 8 | **BB + Keltner + Squeeze** | 3 | Compression detection |
| 9 | **ATR + Bollinger + RSI** | 3 | Volatility-adjusted |
| 10 | **ADX + Momentum + RSI** | 2 | Triple filter |

---

## PART 3: WHAT TO ADD TO YOUR STRATEGIES

### For CIPHER (Structure Decoder)
1. **Bollinger Band squeeze detection** — when BB narrows inside KC = breakout coming
2. **RSI divergence** — price makes new HH but RSI makes LH = weakening trend
3. **Volume confirmation** — high volume on ChoCh = real shift, low volume = fake
4. **Equal highs/lows detection** — liquidity pool markers
5. **Displacement candle filter** — only trust structure breaks with strong body candles
6. **Engulfing pattern** at OTE zone = highest conviction entry

### For PARALLAX (Trap Hunter)
1. **RSI filter already there** — but add RSI divergence at ORB level
2. **Bollinger position** — if price is at BB extreme when trap fires = better entry
3. **Volume spike on trap candle** = institutional sweep confirmation
4. **Day-of-week filter** — avoid Monday, prioritize Wednesday
5. **Market breadth** (Python only) — only enter if >20 of 30 Dow components agree
6. **Previous day's range vs ORB** — if PDR was huge, ORB trap has more fuel

### For COMBINED (Third Strategy)
1. Cipher ChoCh + Parallax Trap on same bar = NUCLEAR signal
2. Score = sum of all confluence factors
3. Score > 70 = enter, Score < 40 = skip
4. Per-ticker optimized thresholds and timeframes

---

## PART 4: PER-TICKER RECOMMENDATIONS

### US30 (Dow Jones)
- **Best timeframe**: 5m (Parallax ORB), 15m (Cipher structure)
- **ORB window**: 09:25-09:30 ET (tight, 5 min)
- **Round levels**: 250-increment (your observation is correct)
- **Target**: 100-200 pts realistic on good setups
- **SL**: Swing of last 6 candles (your current setting)
- **Kill zone**: 09:30-11:00 ET primary, avoid after 14:00

### NAS100 (Nasdaq)
- **Best timeframe**: 5m (Parallax), 15m (Cipher)
- **More volatile than US30** — wider SL needed
- **Round levels**: 500-increment
- **Target**: 150-300 pts on momentum days
- **Best combo**: RSI + Bollinger (momentum-responsive)
- **Kill zone**: 09:30-10:30 ET, 14:00-14:30 (FOMC days)

### SPX500 (S&P 500)
- **Best timeframe**: 15m (Cipher primary)
- **Less volatile, more grindy** — needs patience
- **Round levels**: 50-increment
- **Target**: 30-60 pts
- **Best combo**: EMA + VWAP (your v27 Master approach)

### BTC (Bitcoin)
- **Best timeframe**: 15m-1h (slower structure)
- **24/7 market** — no session bias, but NY and London sessions still have more volume
- **Round levels**: $1000 increments
- **Best combo**: RSI + Bollinger (high volatility suits)
- **Key**: Massive FVGs form on BTC — these are reliable

### ETH (Ethereum)
- **Best timeframe**: 15m-1h
- **Follows BTC but with its own structure**
- **Round levels**: $100 increments
- **Only 2 GEMs found** — harder instrument, needs more testing
- **Best combo**: CMO + Mean Reversion (Chande worked for SOL)

### SOL (Solana)
- **Best timeframe**: 5m-15m (more volatile, faster moves)
- **18 GEMs found — most in crypto**
- **CMO (Chande Momentum) = 89.9% win rate** — THIS IS YOUR GOLDEN CHARM
- **RSI + Breakout** — 10 out of 18 SOL GEMs use RSI
- **Best combo**: CMO + RSI + Price Action Breakout
- **Round levels**: $5-10 increments

---

## PART 5: THE PYTHON ARCHITECTURE

### What We're Building in GB-BRAIN

```
GB-BRAIN/
├── strategies/
│   └── custom/
│       ├── cipher_engine.py      ← Cipher v1.2 logic in Python
│       ├── parallax_engine.py    ← Parallax v1.6 logic in Python
│       ├── combined_engine.py    ← Third strategy (confluence scorer)
│       └── ticker_presets.py     ← Per-ticker optimized settings
├── backtest/
│   ├── run_backtest.py           ← Enhanced with custom strategy support
│   └── run_custom_backtest.py    ← NEW: Cipher/Parallax/Combined backtest
├── db/
│   └── schema.sql                ← Add: signal_log, confluence_scores tables
└── execute/
    └── signal_engine.py          ← NEW: Real-time signal generation
```

### Backtesting Plan
1. Each ticker gets tested on 5m, 15m, 30m, 1h
2. Each strategy (Cipher, Parallax, Combined) tested independently
3. Parameter sweep per ticker to find optimal settings
4. Results go to SQLite → score_and_sort ranks them
5. Best settings become the "preset" for that ticker

### The Combined Scoring System
```
Score = (
    cipher_choch_weight     * choch_active +
    cipher_fvg_golden       * fvg_in_golden_zone +
    cipher_ob_proximity     * near_order_block +
    cipher_ote_zone         * in_ote +
    cipher_premium_discount * correct_zone +
    parallax_trap           * trap_detected +
    parallax_confirm        * confirm_count / required +
    rsi_safe                * rsi_in_range +
    bollinger_position      * bb_score +
    volume_confirm          * vol_above_avg +
    news_clear              * no_news_window +
    day_of_week             * not_monday +
    market_breadth          * breadth_score
)

if score >= THRESHOLD[ticker]:
    SIGNAL = ENTER
```
