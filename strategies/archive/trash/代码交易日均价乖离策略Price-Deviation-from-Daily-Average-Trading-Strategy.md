``` pinescript
/*backtest
start: 2022-12-08 00:00:00
end: 2023-12-14 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Ichimoku Cloud", shorttitle="Ichimoku", overlay=true)

previous_close = close[1]

conversionPeriods = input.int(20, minval=1, title="Conversion Line Periods"),
basePeriods = input.int(60, minval=1, title="Base Line Periods")
laggingSpan2Periods = input.int(120, minval=1, title="Lagging Span 2 Periods"),
displacement = input.int(30, minval=1, title="Displacement")

long_entry = input.bool(true, title="Long Entry")
short_entry = input.bool(true, title="Short Entry")
e2e_entry = input.bool(true, title="E2E Entry")

donchian(len) => math.avg(ta.lowest(len), ta.highest(len))

tenkan = donchian(conversionPeriods)
kijun = donchian(basePeriods)
spanA = math.avg(tenkan, kijun)
spanB = donchian(laggingSpan2Periods)

plot(tenkan, color=#0496ff, title="Conversion Line")
plot(kijun, color=#991515, title="Base Line")
plot(close, offset = -displacement, color=#459915, title="Lagging Span")

p1 = plot(spanA, offset
```