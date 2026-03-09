> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|10|LengthShortEMA|
|v_input_2|20|LengthLongEMA|
|v_input_3|false|Trade reverse|


> Source (PineScript)

```pinescript
//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 30/05/2017
// The Absolute Price Oscillator displays the difference between two exponential 
// moving averages of a security's price and is expressed as an absolute value.
// How this indicator works
//    APO crossing above zero is considered bullish, while crossing below zero is bearish.
//    A positive indicator value indicates an upward movement, while negative readings 
//      signal a downward trend.
//    Divergences form when a new high or low in price is not confirmed by the Absolute

// Strategy Description
study("The Dual EMA Price Swing Strategy", shorttitle="Dual EMA PS", overlay=false)

LengthShortEMA = input(10, title="Short EMA Length")
LengthLongEMA = input(20, title="Long EMA Length")
TradeReverse = input(false, title="Trade Reverse")

// Calculate APO
xShortEMA = ema(close, LengthShortEMA)
xLongEMA = ema(close, LengthLongEMA)
xAPO = xShortEMA - xLongEMA

plot(xAPO, color=apo > 0 ? green : red, title="Absolute Price Oscillator (APO)")

// Signal generation
longCondition = crossover(xAPO, 0)
shortCondition = crossunder(xAPO, 0)

if (longCondition and not TradeReverse or (TradeReverse and not inLong))
    strategy.entry("Buy", strategy.long)

if (shortCondition and not TradeReverse or (TradeReverse and not inShort))
    strategy.entry("Sell", strategy.short)

inLong = strategy.position_size > 0
inShort = strategy.position_size < 0

```

Note: The Pine Script provided is a simplified version to match the text description. You may need to further customize it based on specific requirements or test results.