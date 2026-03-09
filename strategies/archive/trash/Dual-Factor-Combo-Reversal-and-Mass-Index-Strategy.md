> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|---- 123 Reversal ----|
|v_input_2|14|Length|
|v_input_3|true|KSmoothing|
|v_input_4|3|DLength|
|v_input_5|50|Level|
|v_input_6|true|---- MASS Index ----|
|v_input_7|9|Length1|
|v_input_8|25|Length2|
|v_input_9|26.5|Trigger|
|v_input_10|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-25 00:00:00
end: 2023-12-25 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 22/02/2021
// This is a combo strategy to achieve a cumulative signal. 
//
// First strategy
// This system was created from the book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is a reversal type of strategy.
// The strategy buys at the market if the close price is higher than the previous close 
// during two days and the 9-day Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at the market if the close price is lower than the previous close 
// during two days and the 9-day Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
// The Mass Index was designed to identify trend reversals by measuring 
// the narrowing and widening of the range between the high and low prices. 
// As this range widens, the Mass Index increases; as the range narrows 
// the Mass Index decreases.
// The Mass Index was developed by Donald Dorsey.
//
// WARNING:
// - This script is for educational purposes only.
// - It is used to change the bar colors.
////////////////////////////////////////////////////////////
Reversal123(Length, KSmoothing, DLength, Level) =>
    vFast = sma(stoch(close, high, low, Length), KSmoothing) 
    vSlow = sma(vFast, DLength)
    pos = 0.0
    pos := iff(close[2] < close[1] and close > close[1] and vFast < vSlow and vFast > Level, 1,
	         iff(close[2] > close[1] and close < close[1] and vFast > vSlow and vFast < Level, -1, nz(pos[1], 0))) 
    pos

MASS(Length1, Length2, Trigger) =>
    pos = 0.0
    xPrice = high - low
    xEMA = ema(xPrice, Length1)
    xSmoothXAvg = ema(xEMA, Length1)
    nRes = sum(iff(xSmoothXAvg != 0, xEMA / xSmoothXAvg, 0), Length2)
    pos := iff(nRes > Trigger, -1,
	         iff(nRes < Trigger, 1, nz(pos[1], 0))) 
```