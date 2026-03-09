``` pinescript
/*backtest
start: 2023-09-30 00:00:00
end: 2023-10-30 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Noro
//2020

//@version=4
strategy("Puling Trend Following Strategy", shorttitle = "TFFS", overlay = true, default_qty_type = strategy.percent_of_equity, initial_capital = 100, default_qty_value = 100, commission_value = 0.1)

//Settings
needlong  = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
risk      = input(2, minval = 0.1, maxval = 99, title = "Risk size, %")
fast      = input(20, minval = 1, title = "Fast channel (for stop-loss)")
slow      = input(50, minval = 1, title = "Slow channel (for entries)")
showof    = input(true, defval = true, title = "Show offset")
showll    = input(true, defval = true, title = "Show lines")
showdd    = input(true, defval = true, title = "Show label (drawdown)")
showbg    = input(true, defval = true, title = "Show background")
fromyear  = input(1900, defval = 1900, minval = 1900)
toyear    = input(2100, defval = 2100, maxval = 2100)
frommonth = input(true, defval = true, title = "From Month")
tomonth   = input(12, defval = 12, minval = 1, maxval = 12)
fromday   = input(true, defval = true, title = "From day")
today     = input(31, defval = 31, minval = 1, maxval = 31)

//Donchian Channels
fastHigh = ta.highest(high, fast)
slowHigh = ta.highest(high, slow)
fastLow  = ta.lowest(low, fast)
slowLow  = ta.lowest(low, slow)

//Stop Loss and Entry Conditions
longCondition = needlong and close > slowHigh[1]
shortCondition = needshort and close < slowLow[1]

strategy.entry("Long", strategy.long, when = longCondition)
strategy.close("Long", when = not longCondition or (close < fastLow) and time >= timestamp(fromyear, frommonth, fromday, 0, 0))

strategy.entry("Short", strategy.short, when = shortCondition)
strategy.close("Short", when = not shortCondition or (close > fastHigh) and time >= timestamp(toyear, tomonth, today, 0, 0))

//Stop Loss
stopLossLong = close < fastLow[1]
stopLossShort = close > fastHigh[1]

if stopLossLong
    strategy.exit("SL Long", from_entry="Long", limit=fastLow)
if stopLossShort
    strategy.exit("SL Short", from_entry="Short", limit=fastHigh)

//Plotting
plot(slowHigh, title="Fast Channel High", color=color.blue)
plot(slowLow, title="Fast Channel Low", color=color.red)
plot(fastHigh, title="Slow Channel High", color=color.green)
plot(fastLow, title="Slow Channel Low", color=color.orange)

if showof
    plotchar(showof == true ? 1 : na, "Offset", "", location.top, size = size.small)
if showll
    line.new(x1=bar_index[1], y1=fastHigh, x2=bar_index, y2=fastHigh, color=color.blue, width=2)
    line.new(x1=bar_index[1], y1=slowLow, x2=bar_index, y2=slowLow, color=color.red, width=2)
if showdd
    label.new(bar_index, high + (high - low) * 0.3, "Drawdown", color=color.black, textcolor=color.white, style=label.style_label_down, size=size.small)
if showbg
    bgcolor(slowHigh ? color.blue : na)
```