``` pinescript
/*backtest
start: 2023-11-23 00:00:00
end: 2023-11-30 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 25/04/2019
// This is a combined strategy for getting 
// a cumulative signal. The result signal will return 1 if both strategies are long, -1 if all strategies are short and 0 if signals of the strategies are not equal.
//
// First Strategy:
// This system was created from the book "How I Tripled My Money In The Futures Market" by Ulf Jensen, Page 183. It is a reverse type strategy.
// The strategy buys at market when the close price is higher than the previous close for two consecutive days and the 9-day Stochastic Slow Oscillator is below 50.
// The strategy sells at market when the close price is lower than the previous close for two consecutive days and the 9-day Stochastic Fast Oscillator is above 50.
//
// Second Strategy:
// The Accelerator Oscillator was developed by Bill Williams as an extension of the Awesome Oscillator. It represents the 
// difference between the Awesome Oscillator and its 5-period moving average, showing the speed of change in the Awesome Oscillator,
// which can help identify trend reversals before they are evident in the Awesome Oscillator.
//
// WARNING:
// - For educational purposes only
// - This strategy is not guaranteed to generate profitable trades. Users should thoroughly test and validate this strategy 
//   with their own data and risk management practices.

//@input Length, title="Length", defval=14
//@input KSmoothing, title="K Smoothing", defval=true
//@input DLength, title="D Length", defval=3
//@input Level, title="Level", defval=50
//@input Length Slow, title="Length Slow", defval=34
//@input Length Fast, title="Length Fast", defval=5
//@input TradeReverse, title="Trade Reverse", defval=false

// First Strategy - 123 Reversal Strategy
length := input(14)
kSmoothing := input(true)
dLength := input(3)
level := input(50)
lengthSlow := input(34)
lengthFast := input(5)
tradeReverse := input(false)

buySignal = close > nz(close[1]) and nz(close[2]) > nz(close[1]) and stochslow(close, length, dLength, level) < 50
sellSignal = close < nz(close[1]) and nz(close[2]) < nz(close[1]) and stochfast(close, lengthSlow, lengthFast) > 50

// Second Strategy - Accelerator Oscillator
oscillator = (awesomeOscillator(close, lengthFast, lengthSlow))
ma5 = sma(oscillator, 5)
accelerator = oscillator - ma5

// Combine signals
combinedSignal = na(buySignal) ? 0 : buySignal ? 1 : sellSignal ? -1

plot(combinedSignal, title="Combined Signal", color=color.blue)

// Trading Logic
strategy.entry("Buy", strategy.long, when=buySignal and not tradeReverse)
strategy.close("Buy", when=sellSignal and not tradeReverse)
strategy.exit("Sell", from_entry="Buy", loss=50, profit=100)  // Example stop loss and take profit

```
```