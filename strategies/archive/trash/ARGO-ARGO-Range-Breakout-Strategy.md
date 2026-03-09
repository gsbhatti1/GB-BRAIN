``` pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-10-06 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2

// strategy("ARGO_RANGE-BREAKOUT-STRATEGY", overlay=true, default_qty_value=10000, scale=true, initial_capital=100, currency=currency.USD)

// A 4-hour breakout strategy in progress...it's a starting point, thanks to all TradingView community.
// How to use: Test it only on GBPJPY 240 min, wait for the end of the candle to place next order. Red and blue dots are short and long stop orders, Targets are Upper and Lower Bands. Test it and enjoy but use at your own risk...
// © 2016 F.Peluso

risk = input(title="Risk", defval=1)
length = input(title="Length", minval=1, maxval=1000, defval=47)
stopBound = input(title="Previous", defval=10)
upBound = highest(high, length)
downBound = lowest(low, length)
point = 1
tol = 1000
stopT = input(title="Stop", defval=5, minval=1, maxval=5)
dev = input(title="Tolerance", defval=2, minval=1, maxval=5)
limitBoundUp = (highest(high, length)) * (point - (dev / tol))
limitBoundDown = downBound / (point - (dev / tol))

plot(limitBoundUp[1], linewidth=3, style=circles, color=navy, trackprice=true), transp=0
plot(limitBoundDown[1], linewidth=3, style=circles, color=red, trackprice=true, transp=0)
mezzalinea = ((upBound + downBound) / 2)

// Color Bands

colo = (close > limitBoundUp[1] ? blue : close < upBound[1] ? white : na)
UpB = plot(upBound[1], title="Upper Bound", style=linebr, linewidth=1, color=colo)
DownB = plot(limitBoundUp[1], title="Lower Bound", style=linebr, linewidth=2, color=colo)
fill(UpB, DownB, color=colo, transp=90)

plot(limitBoundUp[2] / (point + (stopT / tol)), color=colo)

coloS = (close < limitBoundDown[1] ? red : close > downBound[1] ? white : na)
DB = plot(downBound[1], title="Upper Bound", style=linebr, linewidth=1, color=coloS)
DoB = plot(limitBoundDown[1], title="Lower Bound", style=linebr, linewidth=2, color=coloS)

// Buy and Sell Conditions
longCondition = close > limitBoundUp[1] and close[1] < limitBoundUp[1]
if (longCondition)
    strategy.entry("Long Entry", strategy.long)

shortCondition = close < limitBoundDown[1] and close[1] > limitBoundDown[1]
if (shortCondition)
    strategy.entry("Short Entry", strategy.short)

// Stop Loss and Take Profit
stopLossPrice = na
takeProfitPrice = na

if (strategy.opentrades > 0)
    stopLossPrice := valuewhen(strategy.opentrades == 1, limitBoundDown[1], 0)
    takeProfitPrice := valuewhen(strategy.opentrades == 1, limitBoundUp[1], 0)

if (strategy.opentrades > 0 and close <= stopLossPrice)
    strategy.close("Long Entry", comment="Stop Loss Hit")
if (strategy.opentrades > 0 and close >= takeProfitPrice)
    strategy.close("Short Entry", comment="Take Profit Hit")

```

This script translates the provided Pine Script code into English while maintaining its original structure, numbers, and formatting.