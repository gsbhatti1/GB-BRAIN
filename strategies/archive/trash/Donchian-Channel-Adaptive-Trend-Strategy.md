``` pinescript
/*backtest
start: 2022-10-19 00:00:00
end: 2023-10-25 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Noro
//2020

//@version=4
strategy(title = "Noro's Donchian Strategy", shorttitle = "Donchian str", overlay = true, default_qty_type = strategy.percent_of_equity, initial_capital = 100, default_qty_value = 100, commission_value = 0.1)

//Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
tp = input(defval = 10, minval = 1, title = "Take profit")
lotsize = input(100, defval = 100, minval = 1, maxval = 10000, title = "Lot, %")
pclen = input(50, minval = 1, title = "Price Channel Length")
showll = input(true, defval = true, title = "Show lines")
showbg = input(false, defval = false, title = "Show Background")
showof = input(true, defval = true, title = "Show Offset")
fromyear = input(1900, defval = 1900, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
fromday = input(01, defval = 01, minval = 01, maxval = 31, title = "From day")
today = input(31, defval = 31, minval = 01, maxval = 31, title = "To day")

//Price Channel
h = highest(high, pclen)
l = lowest(low, pclen)
center = (h + l) / 2
tpl = h * (100 + tp) / 100
tps = l * (100 - tp) / 100

//Lines
tpcol = showll ? color.lime : na
pccol = showll ? color.blue : na
slcol = showll ? color.red : na
offset = showof ? 1 : 0
plot(tpl, offset = offset, color = tpcol, linewidth = 1, title = "Take Profit Level")
plot(l, offset = offset, color = pccol, linewidth = 1, title = "Lower Channel Line")
plot(h, offset = offset, color = pccol, linewidth = 1, title = "Upper Channel Line")

//Trading Logic
if (needlong and high > h)
    strategy.entry("Long", strategy.long)
if (needshort and low < l)
    strategy.entry("Short", strategy.short)

//Stop Loss and Take Profit
strategy.exit("Take Profit Long", from_entry = "Long", limit = tpl)
strategy.exit("Take Profit Short", from_entry = "Short", limit = tps)

//Offset Plot
if (showof)
    plot(offset, color = slcol, linewidth = 1, title = "Offset")
```

The translated and formatted Pine Script is provided above. The text and code blocks are kept as close as possible to the original while ensuring the translation is accurate and clear.