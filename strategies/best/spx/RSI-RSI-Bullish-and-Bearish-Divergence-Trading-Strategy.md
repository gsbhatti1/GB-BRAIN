``` pinescript
/*backtest
start: 2024-01-07 00:00:00
end: 2024-01-14 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title="Divergence Indicator")
len = input.int(title="RSI Period", minval=1, defval=20)
src = input(title="RSI Source", defval="close")
lbR = input(title="Pivot Lookback Right", defval=5)
lbL = input(title="Pivot Lookback Left", defval=5)
rangeUpper = input(title="Max of Lookback Range", defval=60)
rangeLower = input(title="Min of Lookback Range", defval=5)
plotBull = input(title="Plot Bullish", defval=true)
plotHiddenBull = input(title="Plot Hidden Bullish", defval=true)
plotBear = input(title="Plot Bearish", defval=true)
plotHiddenBear = input(title="Plot Hidden Bearish", defval=true)

// Calculate RSI
rsiValue = rsi(src, len)

// Functions to check divergence
isBullishDivergence = (highs[rangeUpper] > highs[rangeLower + lbR] and lows[len] < lows[len - 1])
isBearishDivergence = (lowers[rangeUpper] < lowers[rangeLower + lbR] and highs[len] > highs[len - 1])

// Plot signals
plot(series=rsiValue, title="RSI Value", color=color.blue)
if (plotBull)
    plotshape(series=isBullishDivergence ? rsiValue : na, location=location.belowbar, style=shape.labeldown, color=color.green, text="Bullish")
if (plotHiddenBull)
    plotshape(series=isBullishDivergence ? rsiValue : na, location=location.belowbar, style=shape.labeldown, color=color.orange, text="Hidden Bullish")
if (plotBear)
    plotshape(series=isBearishDivergence ? rsiValue : na, location=location.abovebar, style=shape.labelup, color=color.red, text="Bearish")
if (plotHiddenBear)
    plotshape(series=isBearishDivergence ? rsiValue : na, location=location.abovebar, style=shape.labelup, color=color.orange, text="Hidden Bearish")

// Example entry logic based on signals
// Note: This is a placeholder and should be replaced with actual trading logic.
if (isBullishDivergence)
    strategy.entry("Buy", strategy.long)
if (isBearishDivergence)
    strategy.close("Buy")
```

This script defines the RSI divergence strategy, including the calculation of RSI, detection of bullish and bearish divergences, and plotting of signals. The placeholder entry logic should be replaced with actual trading logic based on your specific requirements.