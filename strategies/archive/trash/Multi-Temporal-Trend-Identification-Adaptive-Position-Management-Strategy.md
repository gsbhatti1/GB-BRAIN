``` pinescript
/*backtest
start: 2025-02-16 00:00:00
end: 2025-02-23 00:00:00
period: 5m
basePeriod: 5m
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=6
strategy("Supertrend with DEMA Strategy (Reversal Enabled)", overlay=true)

// ===== Parameters for Supertrend =====
atrPeriod = input.int(10, "ATR Length", minval=1)
factor    = input.float(3.0, "Factor", minval=0.01, step=0.01)

// ===== Parameters for Allowing Trade Directions =====
allowLong  = input.bool(true,  "Allow LONG")
allowShort = input.bool(true,  "Allow SHORT")

// Supertrend Calculation
[supertrend, direction] = ta.supertrend(factor, atrPeriod)
// Set the value to na for the first bar to avoid false signals
supertrend := barstate.isfirst ? na : supertrend

// Plot Supertrend Lines
plot(direction < 0 ? supertrend : na, "Up Trend",   color=color.green, style=plot.style_linebr)
plot(direction < 0 ? na : supertrend, "Down Trend", color=color.red,   style=plot.style_linebr)

// ===== Parameters and Calculation for DEMA =====
demaLength = input.int(100, "DEMA Length", minval=1)
e1 = ta.ema(close, demaLength)
e2 = ta.ema(e1, demaLength)
dema = 2 * e1 - e2

// Plot DEMA
plot(dema, "DEMA", color=#43A047)

// ===== Signal Definitions =====
// Basic Supertrend Trend Change Signals
trendUp   = ta.crossover(close, supertrend)
trendDown = ta.crossunder(close, supertrend)

// Long Signal
longSignal = trendUp and direction < 0 and close > dema

// Short Signal
shortSignal = trendDown and direction > 0 and close < dema

// Plot Signals
plotshape(series=longSignal, title="Long Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="LONG")
plotshape(series=shortSignal, title="Short Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SHORT")

// Position Management
if (longSignal and allowLong)
    strategy.entry("Long", strategy.long)
if (shortSignal and allowShort)
    strategy.entry("Short", strategy.short)

// Close Positions
if (barstate.islast)
    strategy.close("Long")
    strategy.close("Short")
```

This Pine Script translates the provided strategy description into a Pine Script code for backtesting and implementation on TradingView.