> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|14|r|
|v_input_6|10|s|
|v_input_7|5|u|
|v_input_8|45|OS|
|v_input_9|-45|OB|
|v_input_10|false|Trade reverse|


> Source (PineScript)

```pinescript
//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 19/02/2020
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
// This technique was described by William Blau in his book "Momentum,
// Direction and Divergence" (1995). His book focuses on three key aspects 
// of trading: momentum, direction and divergence. Blau, who was an electrical 
// engineer before becoming a trader, thoroughly examines the relationship between 
// price and momentum in step-by-step examples. From this grounding, he then looks 
// at the deficiencies in other oscillators and introduces some innovative techniques, 
// including a fresh twist on Stochastics. On directional issues, he analyzes the 
// intricacies of ADX and offers a unique approach to help define trending and 
// non-trending periods.
// Directional Trend Index (DTI)
//
// Combined Strategy
// The combined strategy uses both the 123 Reversal Indicator and DTI to determine 
// trading signals. It first identifies potential reversals using the 123 Indicator, 
// then confirms these reversals using the DTI.
//
// Input Parameters:
// length: Length of the moving average
// kSmoothing: Smoothing parameter for K line
// dLength: Length of D line
// level: Level to compare with
// r: Parameter for Stochastic Fast Oscillator
// s: Parameter for Stochastic Slow Oscillator
// u: Upper threshold
// os: Overbought level
// ob: Oversold level
// tradeReverse: Boolean flag to indicate if the strategy should trade in reverse

strategy("Combo-Trend-Tracking-Strategy", shorttitle="CTTS", overlay=true)

length = input(14, title="Length")
kSmoothing = input(true, title="KSmoothing")
dLength = input(3, title="DLength")
level = input(50, title="Level")
r = input(14, title="r")
s = input(10, title="s")
u = input(5, title="u")
os = input(45, title="OS")
ob = input(-45, title="OB")
tradeReverse = input(false, title="Trade reverse")

// 123 Reversal Indicator
[longCond, shortCond] = twelfthirtythree(close, dLength, level)

// Directional Trend Index (DTI)
dti = ta.sma(ta.abs(close - close[1]), length) / ta.ema(close, r)
overboughtLine = hline(os, "Overbought Line", os + 50, color=color.red)
oversoldLine = hline(ob, "Oversold Line", ob - 50, color=color.green)

// Combined Strategy
if (longCond and dti < level) or (shortCond and dti > level)
    strategy.entry("Long", strategy.long)
else if (shortCond and dti < level) or (longCond and dti > level)
    strategy.close("Long")

plotshape(series=longCond, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=shortCond, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Parameters for the combined strategy
if tradeReverse
    if (shortCond and dti < level)
        strategy.entry("Short", strategy.short)
    else if (longCond and dti > level)
        strategy.close("Short")
```