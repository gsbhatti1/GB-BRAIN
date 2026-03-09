``` pinescript
/*backtest
start: 2024-10-01 00:00:00
end: 2024-10-31 23:59:59
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title="RSI and AO Synergistic Trend Following - Buy Only", shorttitle="RSI>50 & AO<0 Strategy", overlay=true)

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
// --- Trading Conditions ---
// -----------------------------

longCondition = rsiCrossOver50 and ao < 0

// Plot AO Cross Over Arrow (AO+)
plotshape(series=aoCrossOverZero,
          location=location.belowbar,
          color=color.green,
          style=shape.labelup,
          text="AO>0",
          title="AO Crossed Above Zero")

// Plot AO Cross Under Arrow (AO-)
plotshape(series=aoCrossUnderZero,
          location=location.abovebar,
          color=color.red,
          style=shape.labeldown,
          text="AO<0",
          title="AO Crossed Below Zero")

// Plot RSI Cross Over 50
plotshape(series=rsiCrossOver50,
          location=location.belowbar,
          color=color.blue,
          style=shape.labelup,
          text="RSI>50",
          title="RSI Crossed Above 50")

// Plot RSI Cross Under 50
plotshape(series=rsiCrossUnder50,
          location=location.abovebar,
          color=color.orange,
          style=shape.labeldown,
          text="RSI<50",
          title="RSI Crossed Below 50")

// -----------------------------
// --- Entry and Exit Conditions ---
// -----------------------------

if longCondition
    strategy.entry("Long", strategy.long)

    // Plot Long Entry Arrow
    plotshape(series=true, location=location.belowbar,
              color=color.green, style=shape.triangledown, text="Buy", title="Long Entry")

// Stop Loss and Take Profit
strategy.exit("Exit Long", from_entry="Long", limit=((1 + takeProfitPerc / 100) * strategy.position_avg_price),
              stop=((1 - stopLossPerc / 100) * strategy.position_avg_price))

// Plot Stop Loss and Take Profit Levels
plot(strategy.position_avg_price, color=color.gray, title="Avg Price")
hline((1 + takeProfitPerc / 100) * strategy.position_avg_price, "Take Profit Level", color=color.green)
hline((1 - stopLossPerc / 100) * strategy.position_avg_price, "Stop Loss Level", color=color.red)

// -----------------------------
// --- Plotting Arrows and Labels ---
// -----------------------------

```

```