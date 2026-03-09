``` pinescript
/*backtest
start: 2023-12-26 00:00:00
end: 2024-01-02 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//AlexInc
//2018

// closing - calculate and stick to it for a certain number of bars
// if not, then take the first opposite one
// use stop-loss in any case - calculate the stop

//@version=2
strategy(title = "AlexInc's Bar v1.2", shorttitle = "AlexInc Bar 1.2", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0)

//Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
usemar = input(false, defval = false, title = "Use Martingale")
tryprofitbars = input(6, defval = 6, minval = 1, maxval = 100, title = "Number of candles to take profit anyway")
capital = input(100, defval = 100, minval = 1, maxval = 10000, title = "Capital, %")

useSMAfilter = input(false, defval = true, title = "Use SMA filter")
SMAlimit = input(10, defval = 10, minval = 1, maxval = 30, title = "SMA filter limit")
bodysizeMlt = input(3, defval = 3, minval = 1, maxval = 10, title = "Body Size Multiplier")
meanfulbardiv = input(3, title = "Meanful Bar size Divider")

showarr = input(false, defval = false, title = "Show Arrows")
fromyear = input(2018, defval = 2018, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
fromday = input(01, defval = 01, minval = 01, maxval = 31, title = "From day")
today = input(31, defval = 31, minval = 01, maxval = 31, title = "To day")
```