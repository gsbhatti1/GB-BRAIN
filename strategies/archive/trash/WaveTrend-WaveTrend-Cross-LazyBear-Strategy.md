``` pinescript
/*backtest
start: 2024-03-01 00:00:00
end: 2024-03-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © burakaydingr

//@version=5
strategy("WaveTrend with Crosses [LazyBear]", shorttitle="WT_CROSS_LB", overlay=true)

// User inputs
n1 = input(10, title="Channel Length")
n2 = input(21, title="Average Length")
obLevel1 = input(60, title="Over Bought Level 1")
obLevel2 = input(53, title="Over Bought Level 2")
osLevel1 = input(-60, title="Over Sold Level 1")
osLevel2 = input(-53, title="Over Sold Level 2")

// Basic calculations
ap = hlc3
esa = ta.ema(ap, n1)
d = ta.ema(math.abs(ap - esa), n1)
ci = (ap - esa) / (0.015 * d)
tci = ta.ema(ci, n2)

// WaveTrend indicators
wt1 = tci
wt2 = ta.sma(wt1, 4)

// Buy and Sell Signals
buySignal = ta.crossover(wt1, wt2)
sellSignal = ta.crossunder(wt1, wt2)

// Plotting the signals
plotshape(series=buySignal, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=sellSignal, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Overbought and Oversold Levels
hline(obLevel1, "Over Bought Level 1", color=color.orange)
hline(obLevel2, "Over Bought Level 2", color=color.orange)
hline(osLevel1, "Over Sold Level 1", color=color.orange)
hline(osLevel2, "Over Sold Level 2", color=color.orange)

// Strategy logic
if (buySignal)
    strategy.entry("Buy", strategy.long)
elif (sellSignal)
    strategy.exit("Sell", "Buy")
```

This updated Pine Script includes the completion of the buy and sell signal definitions using `ta.crossover` and `ta.crossunder`, respectively, as well as plotting these signals on the chart. The overbought and oversold levels are also plotted for visual reference.