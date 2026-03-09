```pinescript
plot(KijunSen, color=green, title="21 EMA", linewidth = 2)
plot(SenkouSpanA, color=black, title="Senkou Span A", linewidth = 1)
plot(SenkouSpanB, color=red, title="Senkou Span B", linewidth = 1)
plot(SenkouSpanH, color=blue, title="Senkou Span High", linewidth = 1)
plot(SenkouSpanL, color=blue, title="Senkou Span Low", linewidth = 1)
plot(ChikouSpan, color=red, title="Chikou Span", linewidth = 1)

longCondition = crossover(TenkanSen, KijunSen) and ChikouSpan > SenkouSpanL
shortCondition = crossunder(TenkanSen, KijunSen) and ChikouSpan < SenkouSpanH

plotshape(series=longCondition, title="Long Signal", location=location.belowbar, color=limegreen, style=shape.labelup, text="BUY", size=size.small)
plotshape(series=shortCondition, title="Short Signal", location=location.abovebar, color=red, style=shape.labeldown, text="SELL", size=size.small)

buySignal = longCondition ? 1 : na
sellSignal = shortCondition ? -1 : na

strategy.entry("Long", strategy.long, when=buySignal)
strategy.exit("Take Profit", "Long", loss=50, profit=100)
strategy.exit("Stop Loss", "Long", stop=50)
```

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Tenkan Sen Periods|
|v_input_2|26|Kijun Sen Periods|
|v_input_3|52|Senkou Span B Periods|
|v_input_4|26|Displacement|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-01-11 00:00:00
end: 2024-01-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3

strategy("EMA + Ichimoku Kinko Hyo Strategy", shorttitle="EMI", overlay=true, default_qty_type=strategy.percent_of_equity, max_bars_back=1000, default_qty_value=100, calc_on_order_fills= true, calc_on_every_tick=true, pyramiding=0)

TenkanSenPeriods = input(9, minval=1, title="Tenkan Sen Periods")
KijunSenPeriods = input(26, minval=1, title="Kijun Sen Periods")
SenkouSpanBPeriods = input(52, minval=1, title="Senkou Span B Periods")
displacement = input(26, minval=1, title="Displacement")

donchian(len) => avg(lowest(len), highest(len))
TenkanSen = donchian(TenkanSenPeriods)
KijunSen = donchian(KijunSenPeriods)
SenkouSpanA = avg(TenkanSen, KijunSen)
SenkouSpanB = donchian(SenkouSpanBPeriods)
SenkouSpanH = max(SenkouSpanA[displacement - 1], SenkouSpanB[displacement - 1])
SenkouSpanL = min(SenkouSpanA[displacement - 1], SenkouSpanB[displacement - 1])
ChikouSpan = close[displacement - 1]

Sema = ema(close, 13)
Mema = ema(close, 21)
Lema = ema(close, 89)
XLema = ema(close, 233)

plot(Sema, color=blue, title="13 EMA", linewidth = 2)
plot(Mema, color=fuchsia, title="21 EMA", linewidth = 1)
plot(Lema, color=orange, title="89 EMA", linewidth = 2)
plot(XLema, color=teal, title="233 EMA", linewidth = 2)
plot(KijunSen, color=green, title="21 EMA", linewidth = 2)
plot(SenkouSpanA, color=black, title="Senkou Span A", linewidth = 1)
plot(SenkouSpanB, color=red, title="Senkou Span B", linewidth = 1)
plot(SenkouSpanH, color=blue, title="Senkou Span High", linewidth = 1)
plot(SenkouSpanL, color=blue, title="Senkou Span Low", linewidth = 1)
plot(ChikouSpan, color=red, title="Chikou Span", linewidth = 1)

longCondition = crossover(TenkanSen, KijunSen) and ChikouSpan > SenkouSpanL
shortCondition = crossunder(TenkanSen, KijunSen) and ChikouSpan < SenkouSpanH

plotshape(series=longCondition, title="Long Signal", location=location.belowbar, color=limegreen, style=shape.labelup, text="BUY", size=size.small)
plotshape(series=shortCondition, title="Short Signal", location=location.abovebar, color=red, style=shape.labeldown, text="SELL", size=size.small)

buySignal = longCondition ? 1 : na
sellSignal = shortCondition ? -1 : na

strategy.entry("Long", strategy.long, when=buySignal)
strategy.exit("Take Profit", "Long", loss=50, profit=100)
strategy.exit("Stop Loss", "Long", stop=50)
```