``` pinescript
/*backtest
start: 2022-11-30 00:00:00
end: 2023-12-06 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("CCI Zero Cross Trading Strategy (by ChaoZhang) v1.0", shorttitle="CCI_ZeroCross_Strat_v1.0", overlay=true)

///////////// CCI
cciLength = input(20, minval=1, title="CCI Period Length")

// Calculate CCI
cci = ta.cci(close, cciLength)

// Define stops based on overbought and oversold levels
longStop = -100
shortStop = 100

// Generate signals
buySignal = crossover(cci, 0)
sellSignal = crossunder(cci, 0)

// Enter trades based on signals
if (buySignal)
    strategy.entry("Long", strategy.long, stop=longStop)

if (sellSignal)
    strategy.entry("Short", strategy.short, stop=shortStop)

// Plot CCI and stops
plotcci = plot(cci, color=color.blue)
plotshape(series=buySignal, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=sellSignal, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Plot stops
hline(-100, "Overbought Level", color=color.red)
hline(100, "Oversold Level", color=color.green)

```

This Pine Script code implements the CCI Zero Cross Trading Strategy as described in the Chinese document. The key elements such as the CCI calculation, signal generation based on crossovers with zero level, and plotting of signals and stops are included in the script.