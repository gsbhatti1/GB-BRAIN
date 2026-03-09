> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|---- 123 Reversal ----|
|v_input_2|14|Length|
|v_input_3|true|KSmoothing|
|v_input_4|3|DLength|
|v_input_5|50|Level|
|v_input_6|true|---- STARC Bands ----|
|v_input_7|5|LengthMA|
|v_input_8|15|LengthATR|
|v_input_9|1.33|K|
|v_input_10|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-26 00:00:00
end: 2023-12-03 00:00:00
period: 45m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 28/07/2021
// This is a combo strategy for generating cumulative signals.
//
// First Strategy
// This system was created from the book "How I Tripled My Money In The Futures Market" by Ulf Jensen, Page 183. It's a reversal type of strategy.
// The strategy buys at market if the close price is higher than the previous day's close for two consecutive days and the 9-day moving average of the slow K-line is below 50.
//
// Second Strategy
// This system uses STARC Bands to determine trend direction. It plots bands around a short-term simple moving average of the price.
// The upper band is constructed by adding the Average True Range (ATR) above the moving average, and the lower band by subtracting ATR from the moving average.
// Breaking above the upper band indicates an uptrend, while breaking below the lower band indicates a downtrend.
//
// STARC stands for Stoller Average Range Channels. The indicator is named after its creator, Manning Stoller.

study("123 Reversal & STARC Bands Combo Strategy", shorttitle="123Revs-STARC-Bands")

lenMA = input(5, title="Length MA")
lenATR = input(15, title="Length ATR")
k = input(1.33, title="K")
longLevel = input(50, title="Level")
smoothK = input(true, title="KSmoothing")

inLong = crossover(close[1], close[2]) and sma(close, 9) < longLevel
inShort = crossunder(close[1], close[2]) and sma(close, 9) > longLevel

// STARC Bands
atrLength = input(14, title="Length ATR")
lenMA = input(5, title="Length MA")

smaFast = sma(close, 3)
smaSlow = sma(close, 9)

upperBand = sma(close, lenMA) + k * atr(lenATR)
lowerBand = sma(close, lenMA) - k * atr(lenATR)

// Long condition
longCondition1 = inLong and not tradeReverse
if longCondition1
    strategy.entry("Buy", strategy.long)

// Short condition
shortCondition1 = inShort and not tradeReverse
if shortCondition1
    strategy.entry("Sell", strategy.short)
```

This script combines the 123 Reversal strategy with the STARC Bands strategy to generate cumulative trading signals.