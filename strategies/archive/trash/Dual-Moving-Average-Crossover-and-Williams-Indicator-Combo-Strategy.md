```pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 20/06/2019
// This is a combined strategy for getting a cumulative signal.
//
// First Strategy:
// Generates a buy signal when yesterday's close price is higher than the previous day's close and 
// the fast 9-day Stochastic Oscillator is lower than the slow 3-day Stochastic Oscillator D-line.
// Generates a sell signal when yesterday's close price is lower than the previous day's close and
// the fast Stochastic Oscillator is higher than the slow Stochastic Oscillator D-line.

// Second Strategy:
// Calculates the difference between the 5-day and 34-day price fluctuations, then computes moving averages of that difference.
// A buy signal is generated when the current value is above the previous period.
// A sell signal is generated when the current value is below the previous period.

// The two strategy signals are combined by taking their intersection. 
// Long positions are taken when both strategies give a buy signal, and short positions are taken when both strategies give a sell signal.

// Strategy Arguments
strategy("Dual-Moving-Average-Crossover-and-Williams-Indicator-Combo-Strategy", overlay=true)

v_input_1 = input(14, title="Length")
v_input_2 = input(true, title="KSmoothing")
v_input_3 = input(3, title="DLength")
v_input_4 = input(50, title="Level")
v_input_5 = input(34, title="Length Slow")
v_input_6 = input(5, title="Length Fast")
v_input_7 = input(15, title="MA")
v_input_8 = input(15, title="EMA")
v_input_9 = input(15, title="WMA")
v_input_10 = input(true, title="Show and trading WMA")
v_input_11 = input(false, title="Show and trading MA")
v_input_12 = input(false, title="Show and trading EMA")
v_input_13 = input(false, title="Trade reverse")

// First Strategy
var float sma9 = na
sma9 := ta.sma(close, v_input_6)
var float sma3 = na
sma3 := ta.sma(close, v_input_3)

buy_signal_1 = not na(sma9) and not na(sma3) and close[1] > open[1] and sma9 < sma3[v_input_3]
sell_signal_1 = not na(sma9) and not na(sma3) and close[1] < open[1] and sma9 > sma3[v_input_3]

// Second Strategy
var float diff = na
diff := (close - ta.sma(close, v_input_5)) - (ta.sma(close, v_input_6))
var float ma_diff = na
ma_diff := ta.sma(diff, v_input_7)

buy_signal_2 = not na(ma_diff) and ma_diff > ma_diff[1]
sell_signal_2 = not na(ma_diff) and ma_diff < ma_diff[1]

// Combined Signal
long_signal = buy_signal_1 and buy_signal_2
short_signal = sell_signal_1 and sell_signal_2

if (long_signal)
    strategy.entry("Long", strategy.long)

if (short_signal)
    strategy.entry("Short", strategy.short)

plotshape(series=long_signal, location=location.belowbar, color=color.green, style=shape.triangleup, title="Buy Signal")
plotshape(series=short_signal, location=location.abovebar, color=color.red, style=shape.triangledown, title="Sell Signal")

```
```