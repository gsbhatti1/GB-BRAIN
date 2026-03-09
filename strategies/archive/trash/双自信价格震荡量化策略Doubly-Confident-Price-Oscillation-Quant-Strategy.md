``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 22/04/2019
// This is a combo strategy to get a cumulative signal. The final signal will return 1 if both sub-strategies are long, -1 if both are short, and 0 if the signals are inconsistent.
//
// First sub-strategy
// This system was created from the book "How I Tripled My Money In The Futures Market" by Ulf Jensen, Page 183. It is a reversal type of strategy.
// The strategy buys at market if the close price is higher than the previous close for two consecutive days and the 9-day Stochastic Slow Oscillator is below 50.
// The strategy sells at market if the close price is lower than the previous close for two consecutive days and the 9-day Stochastic Fast Oscillator is above 50.
//
// Second sub-strategy
// The Absolute Price Oscillator (APO) displays the difference between two exponential moving averages of a security's price and is expressed as an absolute value.
// How this indicator works
//    APO crossing above zero is considered bullish, while crossing below zero is bearish.
//    A positive value indicates an upward movement, while a negative value signals a downward trend.
//    Divergences form when a new high or low in the price does not match the corresponding high or low in the APO.
//
// Combining the two sub-strategies
// If both sub-strategies give the same signal, follow that signal. Otherwise, do not operate.
// 
// Advantages
// This strategy combines short-term reversal signals and medium-to-long term trend signals, effectively identifying turning points. Compared to using 123 Reversals or APO alone, it can greatly improve the reliability of signals and reduce erroneous signals.
// 
// Risk Analysis
// The biggest risk is when the 123 Reversal and APO emit conflicting signals. In such cases, the operator needs to judge based on experience which signal is more reliable. Wrong judgements may lead to missing trading opportunities or losses.
// 
// Optimization Directions
// 1. Optimize sub-strategy parameters for more reliable signals, e.g. moving average periods.
// 2. Add other auxiliary indicators to form a voting mechanism. Consistent signals from multiple indicators are more reliable.
// 3. Add stop loss strategies. Timely stop loss on adverse price moves avoids further losses.
// 4. Optimize entry and stop loss levels based on historical backtesting.
//
// Conclusion
// This strategy uses multiple technical indicators to judge the market, avoiding single indicator dependency risks to some extent and improving signal accuracy. There is also room for optimization based on investor requirements. Overall, the Doubly Confident Price Oscillation Quant Strategy provides reliable trade signals and is worth researching further.
////////////////////////////////////////////////////////////
study("Doubly-Confident-Price-Oscillation-Quant-Strategy", shorttitle="DC-POQS", precision=0)

// Inputs
length = input(14, title="Length")
kSmoothing = input(true, title="KSmoothing")
dLength = input(3, title="DLength")
level = input(50, title="Level")
lengthShortEMA = input(10, title="LengthShortEMA")
lengthLongEMA = input(20, title="LengthLongEMA")
tradeReverse = input(false, title="Trade reverse")

// 123 Reversal Strategy
longCondition = close[1] < close[2] and close[2] < close[3] and stochosc(close, length, 5, 3, 3) < 50
shortCondition = close[1] > close[2] and close[2] > close[3] and stochosc(close, length, 5, 3, 3) > 50

// Absolute Price Oscillator (APO)
shortEMA = ema(close, lengthShortEMA)
longEMA = ema(close, lengthLongEMA)
apo = abs(shortEMA - longEMA)

// Signal Combination
longSignal = (longCondition and (apo > 0) and (apo[1] <= 0)) or (tradeReverse and shortCondition and (apo > 0) and (apo[1] <= 0))
shortSignal = (shortCondition and (apo < 0) and (apo[1] >= 0)) or (tradeReverse and longCondition and (apo < 0) and (apo[1] >= 0))

// Final Signal
finalSignal = 0
if (longSignal)
    finalSignal := 1
else if (shortSignal)
    finalSignal := -1

// Plotting
plot(finalSignal, title="Final Signal", color=color.green, style=plot.style_histogram)

// Alert
alertcondition(finalSignal != 0, title="Trade Alert", message="Signal Generated: " + str.tostring(finalSignal))
```