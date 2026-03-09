```pinescript
/*backtest
start: 2024-01-04 00:00:00
end: 2024-02-03 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Stochastic Weekly Options Strategy", overlay=true, shorttitle="WOS")

// Stochastic settings
K = ta.stoch(close, high, low, 14)
D = ta.sma(K, 3)

// Entry and exit conditions
longEntry = ta.crossover(K, 20)
longExit = ta.crossunder(K, 80)

shortEntry = ta.crossunder(K, 80)
shortExit = ta.crossover(K, 20)

// Strategy execution
strategy.entry("Long", strategy.long, when=longEntry)
strategy.close("Long", when=longExit)

strategy.entry("Short", strategy.short, when=shortEntry)
strategy.close("Short", when=shortExit)

// Alert conditions
alertcondition(longEntry, title="Long Entry Alert", message="Stochastic bullish crossover! Consider buying a call option.")
alertcondition(longExit, title="Long Exit Alert", message="Stochastic bearish crossover! Consider selling the call option.")
alertcondition(shortEntry, title="Short Entry Alert", message="Stochastic bearish crossover! Consider buying a put option.")
alertcondition(shortExit, title="Short Exit Alert", message="Stochastic bullish crossover! Consider selling the put option.")

// Plotting shapes for buy and sell signals
plotshape(longEntry, title="Calls Entry Label", color=color.new(color.green, 25),
     textcolor=color.white, style=shape.triangleup, text="Calls", location=location.belowbar, size=size.small)
     
plotshape(longExit, title="Calls Exit Label", color=color.new(color.green, 25),
     textcolor=color.white, style=shape.circle, text="Exit", location=location.belowbar, size=size.small)

plotshape(shortEntry, title="Puts Entry Label", color=color.new(color.red, 25),
     textcolor=color.white, style=shape.triangledown, text="Puts", location=location.abovebar, size=size.small)

plotshape(shortExit, title="Puts Exit Label", color=color.new(color.red, 25),
     textcolor=color.white, style=shape.circle, text="Exit", location=location.abovebar, size=size.small)

// Plotting
plot(K, color=color.blue, title="Stochastic %K")
plot(D, color=color.red, title="Stochastic %D")
hline(80, "Overbought", color=color.red)
hline(20, "Oversold", color=color.green)

```

> Detail

https://www.fmz.com/strategy/440985

> Last Modified

2024-02-04 15:14:43
```