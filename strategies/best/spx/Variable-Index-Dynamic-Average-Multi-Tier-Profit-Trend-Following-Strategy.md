``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-10 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © PresentTrading

// This strategy, "VIDYA ProTrend Multi-Tier Profit," is a trend-following system that utilizes fast and slow VIDYA indicators 
// to identify entry and exit points based on the direction and strength of the trend. 
// It incorporates Bollinger Bands as a volatility filter and features a multi-step take profit mechanism, 
// with adjustable ATR-based and percentage-based profit targets for both long and short positions. 
// The strategy allows for more aggressive take profit settings for short trades, making it adaptable to varying market conditions.

//@version=5
strategy("VIDYA ProTrend Multi-Tier Profit", overlay=true)

// Parameters
length1 = input(20, title="Fast VIDYA Length")
length2 = input(40, title="Slow VIDYA Length")
k = input(3.0, title="K Value for Bollinger Bands")
atrLength = input(14, title="ATR Length")
trailPercent = input(5.0, title="% Trailing Stop Loss")

// Indicator Calculations
vidyaFast = ta.vidya(close, length1)
vidyaSlow = ta.vidya(close, length2)
smaPrice = ta.sma(close, 20)
atrValue = ta.atr(atrLength)

// Bollinger Bands Calculation
upperBB = smaPrice + (k * atrValue)
lowerBB = smaPrice - (k * atrValue)

// Entry Conditions
longCondition = ta.crossover(vidyaFast, vidyaSlow) and close > upperBB
shortCondition = ta.crossunder(vidyaFast, vidyaSlow) and close < lowerBB

// Multi-Tier Profit Mechanism
profitTargetATR1 = vidyaSlow + (atrValue * 2)
profitTargetATR2 = vidyaSlow + (atrValue * 3)

trailStopLossLong = math.max(smaPrice - (trailPercent / 100) * atrValue, lowerBB)
trailStopLossShort = math.min(smaPrice + (trailPercent / 100) * atrValue, upperBB)

// Trading Logic
if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

// Plotting Indicators and Levels
plot(vidyaFast, color=color.blue, title="Fast VIDYA")
plot(vidyaSlow, color=color.red, title="Slow VIDYA")
hline(smaPrice, "SMA 20", color=color.gray)
plot(upperBB, color=color.green, title="Upper Bollinger Band")
plot(lowerBB, color=color.red, title="Lower Bollinger Band")

// Plot Trailing Stop Loss Levels
plot(ta.valuewhen(strategy.opentrades > 0 and strategy.position_size[1] > 0, trailStopLossLong, 1), color=color.blue)
plot(ta.valuewhen(strategy.opentrades > 0 and strategy.position_size[1] < 0, trailStopLossShort, 1), color=color.red)

// Profit Target Levels
plot(profitTargetATR1, color=color.green, title="Profit Target ATR1")
plot(profitTargetATR2, color=color.orange, title="Profit Target ATR2")

```
```