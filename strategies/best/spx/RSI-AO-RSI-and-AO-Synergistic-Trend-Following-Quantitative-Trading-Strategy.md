``` pinescript
/*backtest
start: 2024-10-01 00:00:00
end: 2024-10-31 23:59:59
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title="RSI and AO Synergistic Trend-Following Strategy", shorttitle="RSI+AO Strategy", overlay=true)

// -----------------------------
// --- User Inputs ---
// -----------------------------

// RSI Settings
rsiPeriod = input.int(title="RSI Period", defval=14, minval=1)

// AO Settings
aoShortPeriod = input.int(title="AO Short Period", defval=5, minval=1)
aoLongPeriod = input.int(title="AO Long Period", defval=34, minval=1)

// Strategy Settings
takeProfitPerc = input.float(title="Take Profit (%)", defval=2.0, minval=0.0, step=0.1)
stopLossPerc = input.float(title="Stop Loss (%)", defval=1.0, minval=0.0, step=0.1)

// -----------------------------
// --- Awesome Oscillator (AO) Calculation ---
// -----------------------------

// Calculate the Awesome Oscillator
ao = ta.sma(hl2, aoShortPeriod) - ta.sma(hl2, aoLongPeriod)

// Detect AO Crossing Zero
aoCrossOverZero = ta.crossover(ao, 0)
aoCrossUnderZero = ta.crossunder(ao, 0)

// -----------------------------
// --- Relative Strength Index (RSI) Calculation ---
// -----------------------------

// Calculate RSI
rsiValue = ta.rsi(close, rsiPeriod)

// Detect RSI Crossing 50
rsiCrossOver50 = ta.crossover(rsiValue, 50)
rsiCrossUnder50 = ta.crossunder(rsiValue, 50)

// -----------------------------
// --- Plotting Arrows and Labels ---
// -----------------------------

// Plot AO Cross Over Arrow (AO+)
plotshape(series=aoCrossOverZero,
          location=location.belowbar,
          color=color.green,
          style=shape.triangleup,
          title="AO Crossed Above Zero")

// Plot RSI Cross Under 50
plotshape(series=rsiCrossUnder50,
          location=location.abovebar,
          color=color.red,
          style=shape.triangledown,
          title="RSI Below 50")

// -----------------------------
// --- Trading Logic ---
// -----------------------------

longCondition = rsiCrossOver50 and aoCrossUnderZero

if (longCondition)
    strategy.entry("Long", strategy.long)

// -----------------------------
// --- Stop Loss and Take Profit ---
// -----------------------------

stopLossLevel = close * (1 - stopLossPerc / 100)
takeProfitLevel = close * (1 + takeProfitPerc / 100)

strategy.exit("Take Profit", from_entry="Long", limit=takeProfitLevel, stop=stopLossLevel)
```

This Pine Script defines a strategy that combines the RSI and AO indicators to identify potential long trading opportunities. It includes logic for plotting signals on the chart, setting entry conditions based on crossover events, and managing risk with take profit and stop loss levels.