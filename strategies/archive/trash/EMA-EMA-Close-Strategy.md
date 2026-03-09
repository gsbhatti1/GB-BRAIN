``` pinescript
len5 = input(200, minval=1, title="EMA #5")
src5 = input(close, title="EMA Source #5")
out5 = ema(src5, len5)
plot(out5, title="EMA #5", color=close >= out5 ? color.red : color.red, linewidth = 4)

longCondition = (crossedAbove(out1, out2) and crossedAbove(out1, out3)) and close > out4
if (longCondition)
    strategy.entry("Long Entry", strategy.long)

shortCondition = (crossedBelow(out1, out2) and crossedBelow(out1, out3)) and close < out4
if (shortCondition)
    strategy.entry("Short Entry", strategy.short)

plotshape(series=longCondition, title="Long Entry", location=location.belowbar, color=color.green, style=shape.labelup, text="LONG")
plotshape(series=shortCondition, title="Short Entry", location=location.abovebar, color=color.red, style=shape.labeldown, text="SHORT")

```

The full Pine Script is as follows:

``` pinescript
/*backtest
start: 2023-09-18 00:00:00
end: 2023-09-25 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © x11joe
strategy(title="EMA Candle Close Strategy", overlay=true, initial_capital=1000, commission_type=strategy.commission.percent, commission_value=0.26, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

len1 = input(8, minval=1, title="EMA #1")
src1 = input(close, title="EMA Source #1")
out1 = ema(src1, len1)
plot(out1, title="EMA #1", color=close >= out1 ? color.gray : color.gray, linewidth = 1)

len2 = input(13, minval=1, title="EMA #2")
src2 = input(close, title="EMA Source #2")
out2 = ema(src2, len2)
plot(out2, title="EMA #2", color=close >= out2 ? color.white : color.white, linewidth = 2)

len3 = input(21, minval=1, title="EMA #3")
src3 = input(close, title="EMA Source #3")
out3 = ema(src3, len3)
plot(out3, title="EMA #3", color=close >= out3 ? color.blue : color.blue, linewidth = 3)

len4 = input(55, minval=1, title="EMA #4")
src4 = input(close, title="EMA Source #4")
out4 = ema(src4, len4)
plot(out4, title="EMA #4", color=close >= out4 ? color.red : color.red, linewidth = 2)

len5 = input(200, minval=1, title="EMA #5")
src5 = input(close, title="EMA Source #5")
out5 = ema(src5, len5)
plot(out5, title="EMA #5", color=close >= out5 ? color.red : color.red, linewidth = 4)

longCondition = (crossedAbove(out1, out2) and crossedAbove(out1, out3)) and close > out4
if (longCondition)
    strategy.entry("Long Entry", strategy.long)

shortCondition = (crossedBelow(out1, out2) and crossedBelow(out1, out3)) and close < out4
if (shortCondition)
    strategy.entry("Short Entry", strategy.short)

plotshape(series=longCondition, title="Long Entry", location=location.belowbar, color=color.green, style=shape.labelup, text="LONG")
plotshape(series=shortCondition, title="Short Entry", location=location.abovebar, color=color.red, style=shape.labeldown, text="SHORT")

```