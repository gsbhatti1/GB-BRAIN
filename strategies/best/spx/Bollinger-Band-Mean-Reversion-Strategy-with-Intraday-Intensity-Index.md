```pinescript
/*backtest
start: 2024-01-20 00:00:00
end: 2024-02-19 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/

// Bollinger Bands Strategy with Intraday Intensity Index
// by ChaoZhang

// For Educational Purposes
// Results can differ on different markets and can fail at any time. Profit is not guaranteed.
strategy(title="Bollinger Bands Strategy with Intraday Intensity Index", shorttitle="Bollinger Bands Strategy", overlay=true)

BBlength = input(20, title="Bollinger Bands length")
BBmaType = input("SMA", title="Bollinger Bands MA type", type=input.type.string)
BBmaType == "SMA" ? sma(close, BBlength) : ema(close, BBlength)

BBdev = input(2, title="Bollinger Bands Standard Deviation")
source = input(close, title="source", type=input.type.string)
intradayIndexLen = input(21, title="Intraday Intensity Index length")

// Calculate Bollinger Bands
src = close
if BBmaType == "EMA"
    src := ema(src, BBlength)
bb = ta.bband(src, BBlength, BBdev)

// Calculate Intraday Intensity Index
intradayIndex = ta.hlc3

// Strategy Logic
longCondition = ta.crossover(bb[1].low, src) and (intradayIndex >= 0)
shortCondition = ta.crossunder(bb[1].high, src) and (intradayIndex <= 0)

if longCondition
    strategy.entry("Long", strategy.long)
if shortCondition
    strategy.entry("Short", strategy.short)

// Stop Loss
stopLossLength = input(10, title="Time-based stop length")
stopLoss = strategy.position_avg_price * (1 - stopLossLength / 100)
strategy.exit("Stop Loss", "Long", stoploss=stopLoss)
strategy.exit("Stop Loss", "Short", stoploss=stopLoss)

// Plotting
plot(bb[1].low, color=color.red, title="Bollinger Bands Lower Band")
plot(bb[1].high, color=color.green, title="Bollinger Bands Upper Band")
```