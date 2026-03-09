``` pinescript
/*backtest
start: 2024-01-04 00:00:00
end: 2024-01-11 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//2019
//Noro

//@version=4
strategy(title = "Trend-Tracking-Strategy-Based-on-Moving-Average-and-Average-True-Range", shorttitle = "MA+ATR str", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0)

//Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
capital = input(100, defval = 100, minval = 1, maxval = 10000, title = "Capital, %")
len = input(30, minval = 2, title = "MA Length")
src = input(ohlc4, title = "MA Source")
limitmode = input(false)
fromyear = input(1900, defval = 1900, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
fromday = input(01, defval = 01, minval = 01, maxval = 31, title = "From day")
today = input(31, defval = 31, minval = 01, maxval = 31, title = "To day")

//MA + ATR
atr = sma(tr(true), len) * 2
ma = sma(src, len)
plot(ma, color = color.blue, linewidth = 4)
trend = 0
trend := low > ma + atr ? 1 : high < ma - atr ? -1 : trend[1]
col = trend == 1 ? color.lime : color.red
bgcolor(col, transp = 70)

//Trading
lot = 0.0
lot := strategy.position_size != strategy.position_size[1] ? abs(strategy.percent_change_from_open) * capital / 100 : lot
longCondition = trend == 1 and needlong
shortCondition = trend == -1 and needshort

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

// Exit on end date
exit_date = time >= timestamp(fromyear, frommonth, today, 0, 0) or time >= timestamp(toyear, tomonth, 31, 23, 59)
if (exit_date)
    for i = 0 to strategy.opentrades.count - 1
        strategy.close(strategy.opentrades[i].tid)
```

This Pine Script code implements the translated trading strategy based on moving average and average true range. It includes all necessary settings and logic as per the provided translation, ensuring that the original formatting is maintained while translating the text into English.