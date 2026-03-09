> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Take Profit pip|
|v_input_2|20|Stop Loss pip|

> Source (PineScript)

```pinescript
//@version=3
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 12/02/2019
//    This is a three candlestick bullish reversal pattern consisting of a 
//    bullish harami pattern formed by the first 2 candlesticks then followed 
//    by up candlestick with a higher close than the prior candlestick.
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
/////////////////////////////////////////
study("Three Inside Up Reversal Strategy", shorttitle="3INSUPR", overlay=true)

// Inputs
takeProfitPips = input(20, title="Take Profit pip")
stopLossPips = input(20, title="Stop Loss pip")

// Define the pattern conditions
longCondition1 = (close[2] < open[2]) and (open[1] > close[1])
longCondition2 = (close[1] > open[1]) and (close[1] < open[2])
longCondition3 = (close > open[1]) and (close > max(open[0], close[1]))

// Detect the pattern
threeInsideUpPattern = na
if longCondition1 and longCondition2
    threeInsideUpPattern := 1

if threeInsideUpPattern == 1 and longCondition3
    strategy.entry("Three Inside Up", strategy.short, when=bar_index)

// Set Stop Loss and Take Profit levels
strategy.exit("Profit Target", "Three Inside Up", profit=takeProfitPips * pointsize, loss=stopLossPips * pointsize)

// Plot the bars for visual reference
plotshape(series=threeInsideUpPattern == 1, title="3INSUPR", location=location.abovebar, color=color.red, style=shape.triangledown, text="3INSUPR")
```

This PineScript code implements the "Three Inside Up Reversal Strategy" based on the defined conditions and inputs. It detects the specific candlestick pattern and executes a short position when the pattern is identified, setting predefined stop loss and take profit levels.