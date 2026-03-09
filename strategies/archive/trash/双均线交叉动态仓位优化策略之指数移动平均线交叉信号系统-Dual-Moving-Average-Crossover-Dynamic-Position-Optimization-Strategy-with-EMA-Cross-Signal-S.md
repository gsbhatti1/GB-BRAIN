```pinescript
/*backtest
start: 2024-07-01 00:00:00
end: 2025-01-01 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

// This Pine Script™ code is licensed under the Mozilla Public License 2.0. https://mozilla.org/MPL/2.0/
// © pyoungil0842
//@version=6
strategy("EMA Gold/Death Cross with Dynamic Position Optimization", overlay=true, calc_on_every_tick=true)

// EMA settings
ema12 = ta.ema(close, 12)
ema25 = ta.ema(close, 25)

// Golden and Death Cross conditions
goldenCross = ta.crossover(ema12, ema25)  // When EMA12 crosses above EMA25
deathCross = ta.crossunder(ema12, ema25)  // When EMA12 crosses below EMA25

// Check current position status
isLong = strategy.position_size > 0  // Whether there is a long position
isShort = strategy.position_size < 0  // Whether there is a short position

// Handle Golden Cross
if (goldenCross)
    if (isShort)  // If there is a short position, close short and open long
        strategy.close("Short")  // Close the short position
        strategy.entry("Long", strategy.long)  // Enter a long position
    else if (not isLong)  // If there is no long position, open new long
        strategy.entry("Long", strategy.long)

// Handle Death Cross
if (deathCross)
    if (isLong)  // If there is a long position, close long and open short
        strategy.close("Long")  // Close the long position
        strategy.entry("Short", strategy.short)  // Enter a short position
    else if (not isShort)  // If there is no short position, open new short
        strategy.entry("Short", strategy.short)

// Plot EMA lines on the chart
plot(ema12, title="EMA 12", color=color.blue)
plot(ema25, title="EMA 25", color=color.orange)

// Plot signals on the chart
plotshape(series=goldenCross, title="Golden Cross", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=deathCross, title="Death Cross", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)
```

Note: The Pine Script code was adjusted to ensure proper plotting of the signals on the chart, with the addition of `plotshape` to indicate the `Golden Cross` and `Death Cross` on the chart.