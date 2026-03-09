``` pinescript
/*backtest
start: 2022-11-16 00:00:00
end: 2023-11-22 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © lepstick-TC
//@version=4
strategy("Trend-Tracking-Strategy-Based-on-Multi-indicator", overlay=true)
length = input(5, minval=1)
src = input(close, title="Source")
mult = input(1.5, minval=0.001, maxval=50)
basis = sma(src, length)
dev = mult * stdev(src, length)
upper = basis + dev
lower = basis - dev
plot(basis, color=color.red)

p1 = plot(upper, color=color.blue, title="Upper Bollinger Band")
p2 = plot(lower, color=color.blue, title="Lower Bollinger Band")

rsiLength = input(7)
rsiSource = input(close, title="RSI Source")
upTrendSignal = close < ref(basis, 1) and close < ref(upper, 1) and rsi(rsiSource, rsiLength) < v_input_5
downTrendSignal = close > ref(basis, 1) and close > ref(lower, 1) and rsi(rsiSource, rsiLength) > v_input_4

// Buy signal for relatively ascending trend
if (upTrendSignal)
    strategy.entry("Buy", strategy.long)

// Sell signal for relatively descending trend
if (downTrendSignal)
    strategy.entry("Sell", strategy.short)

plotshape(series=upTrendSignal, location=location.belowbar, color=color.green, style=shape.labelup, title="Up Trend Signal")
plotshape(series=downTrendSignal, location=location.abovebar, color=color.red, style=shape.labeldown, title="Down Trend Signal")

```

This translation keeps the code blocks and formatting as in the original while translating all human-readable text into English.