``` pinescript
/*backtest
start: 2023-11-05 00:00:00
end: 2023-12-05 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Noro
// 2018

//@version=2
strategy(title = "BB%/MFI/RSI", shorttitle = "BB%/MFI/RSI", default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 100)

// Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(false, defval = false, title = "Short")
capital = input(100, defval = 100, minval = 1, maxval = 10000, title = "Lot, %")
fromyear = input(1900, defval = 1900, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(1, defval = 1, minval = 1, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 1, maxval = 12, title = "To Month")
fromday = input(1, defval = 1, minval = 1, maxval = 31, title = "From Day")
today = input(31, defval = 31, minval = 1, maxval = 31, title = "To Day")

source = hlc3
length = input(14, minval=1), mult = input(2.0, minval=0.001, maxval=50), bblength = input(50, minval=1, title="BB Period")
DrawRSI_f = input(true, title="Draw RSI?", type=bool)
DrawMFI_f = input(false, title="Draw MFI?", type=bool)
HighlightBreaches = input(true, title="Highlight Oversold/Overbought?", type=bool)

DrawMFI = (not DrawMFI_f) and (not DrawRSI_f) ? true : DrawMFI_f
DrawRSI = (DrawMFI_f and DrawRSI_f) ? false : DrawRSI_f
// RSI
rsi_s = DrawRSI ? rsi(source, length) : na
plot(DrawRSI ? rsi_s : na, color=maroon, linewidth=2)

// MFI
upper_s = DrawMFI ? sum(volume * (change(source) <= 0 ? 0 : source), length) : na
lower_s = DrawMFI ? sum(volume * (change(source) >= 0 ? 0 : source), length) : na
mf = DrawMFI ? rsi(upper_s, lowe
```