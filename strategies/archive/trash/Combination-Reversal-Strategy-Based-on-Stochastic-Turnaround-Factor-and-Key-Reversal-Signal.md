> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|true|Enter the number of bars over which to look for a new low in prices.|
|v_input_6|false|Trade reverse|


> Source (PineScript)

```pinescript
//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 22/12/2020
// This is combo strategies for get a cumulative signal. 
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close 
// during 2 days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market, if close price is lower than the previous close price 
// during 2 days and the meaning of 9-days Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
// A key reversal is a one-day trading pattern that may signal the reversal of a trend. 
// In a bull market, after the price hits a new high, if the closing price is near the lowest price of the previous day, it constitutes a key reversal long signal.
// In a bear market, after the price hits a new low, if the closing price is near the highest price of the previous day, it constitutes a key reversal short signal.
//
// Combined Strategy
// This combined strategy uses both the stochastic turnaround factor and key reversal signal to generate trading signals.
// It first uses the stochastic turnaround factor to determine whether the price shows signs of a potential reversal.
// Then it incorporates the key reversal signal to filter out false reversals, ensuring the capture of true reversal opportunities, thereby reducing trading risk.
//
// Parameters
// Length: The length of the stochastic slow and fast oscillator.
// KSmoothing: The smoothing factor for the stochastic oscillator.
// DLength: The length of the D (signal) line in the stochastic oscillator.
// Level: The threshold level for the stochastic oscillator.
// v_input_5: The number of bars over which to look for a new low in prices.
// v_input_6: Whether to trade in the opposite direction of the key reversal signal.
//
// Example Usage
// length: 14
// kSmoothing: true
// dLength: 3
// level: 50
// v_input_5: true
// v_input_6: false
//
// This script is designed to be used in TradingView PineScript environment.
// It combines two reversal strategies to improve the accuracy of trading signals and reduce false signals.
// It can be further optimized and customized as needed.
//
// This script is provided "as is" and without any warranty, express or implied.
// The author disclaims all liability for any loss or damage that may arise from the use of this script.
//
// This script is for educational purposes and should be used at your own risk.
//
// Please note that this script is a draft and may require further development and testing.
// It is recommended to backtest and validate the strategy thoroughly before using it in live trading.
//
// Happy Trading!
```

```pinescript
//@version=4
strategy("Combination-Reversal-Strategy-Based-on-Stochastic-Turnaround-Factor-and-Key-Reversal-Signal", overlay=true)

// Input parameters
length = input(14, title="Length")
kSmoothing = input(True, title="KSmoothing")
dLength = input(3, title="DLength")
level = input(50, title="Level")
newLowBars = input(True, title="Enter the number of bars over which to look for a new low in prices.")
tradeReverse = input(False, title="Trade reverse")

// Calculate Stochastic
[stochK, stochD] = sma(close, 14, 3) - sma(close, 14, 3 * 3)
stochSlow = sma(stochK, 3)
stochFast = sma(stochK, 3 * 3)

// Determine buy and sell signals
buySignal = close[2] > close[1] and stochSlow < 50
sellSignal = close[2] < close[1] and stochFast > 50

// Key Reversal Signal
var float prevHigh = na
var float prevLow = na
var bool isBullish = na
var bool isBearish = na
bullish = close > open and close > prevHigh and close[1] < prevHigh
bearish = close < open and close < prevLow and close[1] > prevLow

if (bullish and close < open[1])
    prevHigh := high
    isBullish := true
    isBearish := false
else if (bearish and close > open[1])
    prevLow := low
    isBullish := false
    isBearish := true

// Generate signals
if (buySignal and not isBullish) or (not tradeReverse and isBullish)
    strategy.entry("Buy", strategy.long)

if (sellSignal and not isBearish) or (not tradeReverse and isBearish)
    strategy.entry("Sell", strategy.short)

// Plot signals
plotshape(series=buySignal, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="Buy")
plotshape(series=sellSignal, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="Sell")
```

This script implements the combination of stochastic turnaround factor and key reversal signal to generate trading signals. It includes detailed comments to explain each part of the script and how the strategy works.