> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|13|LengthBP|
|v_input_6|false|Trigger|
|v_input_7|false|Trade reverse|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-10-21 00:00:00
end: 2023-11-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 15/06/2020
// This is a combo strategy to generate a cumulative signal.
//
// First Strategy
// This system was created from the book "How I Tripled My Money In The Futures Market" by Ulf Jensen, page 183. It is a reversal type of strategy.
// The strategy buys at market if the close price is higher than the previous close for two consecutive days and the meaning of the 9-day Stochastic Slow Oscillator is below 50.
// The strategy sells at market if the close price is lower than the previous close for two consecutive days and the meaning of the 9-day Stochastic Fast Oscillator is above 50.
//
// Second Strategy
// Developed by Dr. Alexander Elder, the Elder-ray indicator measures buying and selling pressure in the market. It is often used as part of the Triple Screen trading system but can also be used on its own.
// Dr. Elder uses a 13-day Exponential Moving Average (EMA) to indicate the market consensus of value. Bull Power measures the ability of buyers to drive prices above the consensus of value, while Bear Power reflects the ability of sellers to drive prices below the consensus of value.
//
// The threshold for the bull power indicator in this strategy is set to 0, meaning any value greater than 0 generates a trading signal.
//
// Combined Signals
// A final trading signal is generated when both the reversal and bull power signals align in the same direction. Long signals are triggered when both the reversal and bull power signals indicate long positions. Short signals are triggered when both signals indicate short positions.
```

The provided Pine Script continues without further context, so it's presented as-is below:

```pinescript
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 15/06/2020
// This is a combo strategy to generate a cumulative signal.

//@version=4

// Define variables for the first strategy
length = input(14, title="Length")
kSmoothing = input(true, title="KSmoothing")
dLength = input(3, title="DLength")
level = input(50, title="Level")
lengthBP = input(13, title="LengthBP")

// Define variables for the second strategy
trigger = input(false, title="Trigger")
tradeReverse = input(false, title="Trade reverse")

// First Strategy: Reversal Part
longCondition = close[2] > close[1] and close > close[1] and stochasticsD(9) < level
shortCondition = close[2] < close[1] and close < close[1] and stochasticsK(9) > level

// Second Strategy: Bull Power Part
emaValue = ema(close, lengthBP)
bullPower = highest(high - emaValue, 1)
bearPower = lowest(low - emaValue, 1)

// Combined Signals
combinedLongCondition = longCondition and bullPower > 0
combinedShortCondition = shortCondition and bearPower < 0

plotshape(series=combinedLongCondition ? close : na, title="Combined Long Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=combinedShortCondition ? close : na, title="Combined Short Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// Placeholder for additional logic
```