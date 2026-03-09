``` pinescript
/*backtest
start: 2022-09-30 00:00:00
end: 2023-10-06 00:00:00
period: 2d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy(title = "CS Basic Scripts - Stochastic Special (Strategy)", shorttitle = "Stochastic Special", overlay = false, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0)

// Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
usemar = input(false, defval = false, title = "Use Martingale")
capital = input(100, defval = 100, minval = 1, maxval = 10000, title = "Capital, %")
usesmi = input(true, defval = true, title = "Use SMI Strategy")
usersi = input(true, defval = true, title = "Use RSI Strategy")
usebod = input(true, defval = true, title = "Use Body-Filter")
a = input(5, "SMI Percent K Length")
b = input(3, "SMI Percent D Length")
limit = input(50, defval = 50, minval = 1, maxval = 100, title = "SMI Limit")

// Backtesting Input Range
fromyear = input(2017, defval = 2017, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
fromday = input(01, defval = 01, minval = 01, maxval = 31, title = "From day")
today = input(31, defval = 31, minval = 01, maxval = 31, title = "To day")

// Fast RSI
fastup = rma(max(change(close), 0), 7)
fastdown = rma(-min(change(close), 0), 7)
fastrsi = fastdown == 0 ? 100 : fastup / (fastup + fastdown) * 100

// SMI Calculation
src = close
k = sma(src, a)
d = sma(k, b)
smi = (src - d) / (src + d) * 100

// RSI Calculation
rsi = rsi(close, 14)

// Long Signal
longsignal = smi < -50 and rsi < 20

// Short Signal
shortsignal = smi > 50 and rsi > 80

// Body Filter
body = close - open
bodyfilter = (body / typicalprice(high, close, low) > 0.33 * sma(body, 10)) or (body / typicalprice(high, close, low) < -0.33 * sma(body, 10))

// Trade Execution
if (longsignal and bodyfilter)
    strategy.entry("Long", strategy.long, qty = capital)

if (shortsignal and bodyfilter)
    strategy.entry("Short", strategy.short, qty = capital)

// Optional Martingale
if (strategy.position_size < 0 and not bodyfilter and longsignal)
    strategy.close("Long")
    strategy.entry("Long", strategy.long, qty = capital * 2)

if (strategy.position_size > 0 and not bodyfilter and shortsignal)
    strategy.close("Short")
    strategy.entry("Short", strategy.short, qty = capital * 2)
```

This translation maintains the original code structure and formatting, including the use of code blocks and comments. The text describing the strategy and its parameters has been translated to English.