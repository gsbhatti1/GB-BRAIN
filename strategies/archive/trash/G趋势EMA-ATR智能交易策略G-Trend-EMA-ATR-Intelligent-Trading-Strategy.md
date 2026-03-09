``` pinescript
/*backtest
start: 2024-05-01 00:00:00
end: 2024-05-31 23:59:59
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
// Full credit to AlexGrover: https://www.tradingview.com/script/fIvlS64B-G-Channels-Efficient-Calculation-Of-Upper-Lower-Extremities/
strategy("G-Channel Trend Detection with EMA Strategy and ATR", shorttitle="G-Trend EMA ATR Strategy", overlay=true)

// Inputs for G-Channel
length = input(100, title="G-Channel Length")
src = input(close, title="Source")

// G-Channel Calculation
var float a = na
var float b = na
a := max(src, nz(a[1])) - (nz(a[1] - b[1]) / length)
b := min(src, nz(b[1])) + (nz(a[1] - b[1]) / length)
avg = (a + b) / 2

// G-Channel Signals
crossup = b[1] < close[1] and b > close
crossdn = a[1] < close[1] and a > close
bullish = barssince(crossdn) <= barssince(crossup)
c = bullish ? color.lime : color.red

// Plot G-Channel Average
p1 = plot(avg, "Average", color=c, linewidth=1, transp=90)
p2 = plot(close, "Close price", color=c, linewidth=1, transp=100)
fill(p1, p2, color=c, transp=90)

// Show Buy/Sell Labels
showcross = input(true, title="Show Buy/Sell Labels")
plotshape(showcross and not bullish and bullish[1] ? avg : na, location=location.belowbar, color=color.lime, style=shape.labeldown, text="Buy", size=size.small)
plotshape(showcross and bullish and not bullish[1] ? avg : na, location=location.abovebar, color=color.red, style=shape.labelup, text="Sell", size=size.small)

// EMA Calculation
emaLength = input(20, title="EMA Length")
ema = ta.ema(src, emaLength)

// ATR Calculation
atrLength = input(14, title="ATR Length")
atr = ta.atr(atrLength)

// Buy Condition
longCondition = close > b and close < ema
strategy.entry("Long", strategy.long, when=longCondition)
stopLoss = entry_price - 2 * atr
takeProfit = entry_price + 4 * atr

// Sell Condition
shortCondition = close < a and close > ema
strategy.entry("Short", strategy.short, when=shortCondition)
stopLossShort = entry_price + 2 * atr
takeProfitShort = entry_price - 4 * atr

// Set Stop Loss and Take Profit
strategy.exit("Long Exit", "Long", stop=stopLoss, limit=takeProfit)
strategy.exit("Short Exit", "Short", stop=stopLossShort, limit=takeProfitShort)
```

This script integrates the G-Channel trend detection with EMA strategy and ATR for setting stop-loss and take-profit levels. It plots the G-Channel average, shows buy/sell labels, calculates the EMA and ATR, and sets conditions for entering long or short positions based on these indicators.