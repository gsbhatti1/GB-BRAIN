``` pinescript
xXY) - xX * sum(xSeria, Length)) / xDivisor
xLRI = (sum(xSeria, Length) - xSlope * xX) / Length
if (close > xLRI and not reverse)
	strategy.entry("Long", strategy.long)
else if (close < xLRI and not reverse)
	strategy.entry("Short", strategy.short)
else if (close < xLRI and reverse)
	strategy.entry("Short", strategy.short)
else if (close > xLRI and reverse)
	strategy.entry("Long", strategy.long)
```

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_3|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-28 00:00:00
end: 2023-12-28 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 21/03/2018
// Linear Regression Intercept is one of the indicators calculated by using the 
// Linear Regression technique. Linear regression indicates the value of the Y 
// (generally the price) when the value of X (the time series) is 0. Linear 
// Regression Intercept is used along with the Linear Regression Slope to create 
// the Linear Regression Line. The Linear Regression Intercept along with the Slope 
// creates the Regression line.
//
// You can change long to short in the Input Settings
// WARNING:
//  - For purpose educate only
//  - This script to change bars colors.
////////////////////////////////////////////////////////////
strategy(title="Linear Regression Intercept Strategy", overlay = true)
Length = input(14, minval=1)
xSeria = input(title="Source", defval="close")
reverse = input(false, title="Trade reverse")

xX = Length * (Length - 1) * 0.5
xDivisor = xX * xX - Length * Length * (Length - 1) * (2 * Length - 1) / 6
xXY = 0
for i = 0 to Length-1
    xXY := xXY + (i * xSeria[i])
xSlope = (Length * xXY - xX * sum(xSeria, Length)) / xDivisor
xLRI = (sum(xSeria, Length) - xSlope * xX) / Length

if (close > xLRI and not reverse)
    strategy.entry("Long", strategy.long)
else if (close < xLRI and not reverse)
    strategy.entry("Short", strategy.short)
else if (close < xLRI and reverse)
    strategy.entry("Short", strategy.short)
else if (close > xLRI and reverse)
    strategy.entry("Long", strategy.long)
```