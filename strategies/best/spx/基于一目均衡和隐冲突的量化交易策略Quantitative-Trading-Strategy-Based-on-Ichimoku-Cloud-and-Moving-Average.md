``` pinescript
/*backtest
start: 2024-01-20 00:00:00
end: 2024-02-19 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Ichimoku Cloud + ema 50 Strategy", overlay=true)

len = input.int(50, minval=1, title="Length")
src = input(close, title="Source")
out = ta.ema(src, len)

conversionPeriods = input.int(9, minval=1, title="Conversion Line Length")
basePeriods = input.int(26, minval=1, title="Base Line Length")
laggingSpan2Periods = input.int(52, minval=1, title="Leading Span B Length")
displacement = input.int(1, minval=1, title="Lagging Span")

donchian(len) => math.avg(ta.lowest(len), ta.highest(len))
conversionLine = donchian(conversionPeriods)
baseLine = donchian(basePeriods)
leadLine1 = math.avg(conversionLine, baseLine)
leadLine2 = donchian(laggingSpan2Periods)

p1 = plot(leadLine1, offset = displacement - 1, color=#A5D6A7,
     title="Leading Span A")

p2 = plot(leadLine2, offset = displacement, color=#E5B044,
     title="Leading Span B")

p3 = hline(conversionLine, title="Conversion Line", color=color.new(#A5D6A7, 90))
p4 = hline(baseLine, title="Base Line", color=color.new(#E5B044, 90))

plotshape(series=cross(out, leadLine1) and close > leadLine1, location=location.belowbar, color=color.green, style=shape.labelup, title="Buy Signal")
plotshape(series=cross(leadLine1, out) and close < leadLine1, location=location.abovebar, color=color.red, style=shape.labeldown, title="Sell Signal")

// Strategy logic
if (close > leadLine1 and leadLine1 > baseLine)
    strategy.entry("Buy", strategy.long)
if (close < leadLine1 and leadLine1 < baseLine)
    strategy.exit("Sell", from_entry="Buy", stop=baseLine)
```

This code includes the necessary Pine Script for implementing the strategy, including the calculations for the Ichimoku Cloud and the moving average. It also includes the visualization and trading logic based on the provided conditions.