``` pinescript
/*backtest
start: 2023-11-24 00:00:00
end: 2023-12-24 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Noro
// 2017

//@version=2
strategy(shorttitle = "Squeeze str 1.0", title="Noro's Squeeze Momentum Strategy v1.0", overlay = false, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0)

// Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
length = input(20, title="BB Length")
mult = input(2.0, title="BB MultFactor")
lengthKC = input(20, title="KC Length")
multKC = input(1.5, title="KC MultFactor")
useTrueRange = true
usecolor = input(true, defval = true, title = "Use color of candle")
usebody = input(true, defval = true, title = "Use EMA Body")
needbg = input(false, defval = false, title = "Show trend background")
fromyear = input(1900, defval = 1900, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
fromday = input(01, defval = 01, minval = 01, maxval = 31, title = "From day")
today = input(31, defval = 31, minval = 01, maxval = 31, title = "To day")

// Calculate BB
source = close
basis = sma(source, length)
dev = mult * atr(length)
lower = basis - dev
upper = basis + dev

// Calculate KC
kc_length = lengthKC
kc_mult = multKC
kc_upper = sma(high, kc_length) + kc_mult * sma(abs(high - low), kc_length)
kc_lower = sma(low, kc_length) - kc_mult * sma(abs(high - low), kc_length)

// Determine Trend
isCompressed = close > lower and close < upper
isExpanding = close < lower or close > upper
isTrendUp = close > open
isTrendDown = close < open
trendColor = close > open ? color.green : color.red
trendBody = close > open ? close - open : open - close

// Generate Signals
longSignal = isCompressed and isTrendUp and usecolor and usebody and trendBody > avgBody(30)
shortSignal = isCompressed and isTrendDown and usecolor and usebody and trendBody > avgBody(30)

// Plotting
plotshape(series = longSignal, title = "Long Signal", location = location.belowbar, color = color.blue, style = shape.triangleup, text = "Long")
plotshape(series = shortSignal, title = "Short Signal", location = location.abovebar, color = color.red, style = shape.triangledown, text = "Short")

// Plot BB and KC Channels
plot(lower, color=color.new(color.gray, 90), title="Lower Bollinger Band")
plot(upper, color=color.new(color.gray, 90), title="Upper Bollinger Band")
plot(kc_upper, title="KC Upper Channel", color=color.orange)
plot(kc_lower, title="KC Lower Channel", color=color.orange)

// Plot Trend Background
if (needbg)
    bgcolor(isCompressed ? color.gray : na, title="Background Color")

// Functions
avgBody(len) =>
    sum = 0.0
    for i = 0 to len - 1
        sum += abs(open[i] - close[i])
    sum / len

// Strategy Logic
if (longSignal)
    strategy.entry("Long", strategy.long)
elif (shortSignal)
    strategy.entry("Short", strategy.short)

// Plotting Parameters
plotshape(series = isCompressed, title = "Compressed", location = location.middle, color = color.gray, style = shape.labeldown, text = "Compressed")

```