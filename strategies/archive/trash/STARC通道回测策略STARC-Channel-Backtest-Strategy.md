> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|5|LengthMA|
|v_input_2|15|LengthATR|
|v_input_3|1.33|K|
|v_input_4|false|Trade reverse|


> Source (PineScript)

```pinescript
//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 23/04/2018
// A type of technical indicator that is created by plotting two bands around 
// a short-term simple moving average (SMA) of an underlying asset's price. 
// The upper band is created by adding a value of the average true range 
// (ATR) - a popular indicator used by technical traders - to the moving average. 
// The lower band is created by subtracting a value of the ATR from the SMA.
// STARC is an acronym for Stoller Average Range Channels. The indicator is 
// named after its creator, Manning Stoller.
//
// You can change long to short in the Input Settings
// WARNING:
//  - For purpose educate only
//  - 

// Strategy Description
strategy("STARC Channel Backtest Strategy", overlay=false)

// Inputs
lengthMA = input(5, title="LengthMA")
lengthATR = input(15, title="LengthATR")
kValue = input(1.33, title="K")
tradeReverse = input(false, title="Trade reverse")

// Calculate SMA and ATR
src = close
sma = sma(src, lengthMA)
atr = atr(lengthATR)

// Upper and Lower Bands
upperBand = sma + kValue * atr
lowerBand = sma - kValue * atr

// Buy and Sell Conditions
buyCondition = close > upperBand
sellCondition = close < lowerBand

// Trading Logic
if (tradeReverse)
    strategy.entry("Buy", strategy.long, when=buyCondition)
    strategy.close("Sell", when=sellCondition)
else
    strategy.entry("Buy", strategy.long, when=buyCondition)
    strategy.close("Buy", when=sellCondition)

// Plotting Bands
plot(sma, color=color.blue, linewidth=2)
plot(upperBand, color=color.red, linewidth=2)
plot(lowerBand, color=color.green, linewidth=2)
```

This Pine Script code implements the STARC Channel Backtest Strategy described in the document. It includes the necessary inputs and logic to generate trading signals based on the calculated upper and lower bands.