```pinescript
/*backtest
start: 2024-01-19 00:00:00
end: 2024-02-18 0:00:00
Period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © melihtuna

//@version=2
strategy("Jim's MACD", overlay=true)

Tendies = input(true, title="Check here for tendies")

// === MACD Setup ===
[macdLine, signalLine, histLine] = macd(close, 12, 26, 9)

// EMA
ma = ema(close, 34)
plot(ma, title="34-period EMA", color=color.red)

// Entry
if (close > ma and macdLine > signalLine and macdLine > 0)
    strategy.entry("Buy", strategy.long)

if (close < ma and macdLine < signalLine and macdLine < 0)
    strategy.entry("Sell", strategy.short)

// Exit
strategy.exit("Take Profit", "Buy", limit=close + 10 * point_size)
strategy.exit("Stop Loss", "Buy", stop=close - 10 * point_size)

strategy.exit("Take Profit", "Sell", limit=close - 10 * point_size)
strategy.exit("Stop Loss", "Sell", stop=close + 10 * point_size)

// Plot MACD lines
plot(macdLine, title="MACD Line", color=color.blue)
plot(signalLine, title="SIGNAL Line", color=color.orange)
plot(histLine, title="Histogram", color=color.green, style=plot.style_histogram)

// Add Stop Loss and Take Profit Levels
plotshape(series=macdLine > signalLine and close > ma, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=macdLine < signalLine and close < ma, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)
```