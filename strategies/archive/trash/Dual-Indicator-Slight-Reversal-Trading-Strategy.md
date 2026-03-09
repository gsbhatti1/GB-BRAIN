> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|32|r|
|v_input_6|5|s|
|v_input_7|5|u|
|v_input_8|3|SmthLen|
|v_input_9|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-09 00:00:00
end: 2023-10-16 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 28/07/2020
// This is combo strategies for get a cumulative signal. 
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close during 2 days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market, if close price is lower than the previous close during 2 days and the meaning of 9-days Stochastic Fast Oscillator is above 50.
//

strategy("Dual Indicator Slight Reversal Trading Strategy", overlay=true)

length1 = input(14, title="Length")
kSmoothing = input(true, title="KSmoothing")
dLength = input(3, title="DLength")
level = input(50, title="Level")
r = input(32, title="r")
s = input(5, title="s")
u = input(5, title="u")
smthLen = input(3, title="SmthLen")
tradeReverse = input(false, title="Trade reverse")

// 123 Reversal Strategy
var float[] buyPriceArray = array.new_float(0)
var int[] buyIndexArray = array.new_int(0)

isBuySignal = false
for i = 0 to bar_index - 1
    if close[i+2] < close[i+1] and close[i+1] > close[i] and stoch(dLength, smthLen, kSmoothing)[i] < level
        isBuySignal := true
        array.push(buyPriceArray, close[i])
        array.push(buyIndexArray, i)

if not na(close[1]) and close[1] < close[0] and stoch(dLength, smthLen, kSmoothing)[2] > level
    strategy.entry("Buy", strategy.long)

// Ergodic Indicator Strategy
var float[] sellPriceArray = array.new_float(0)
var int[] sellIndexArray = array.new_int(0)

isSellSignal = false
for i = 0 to bar_index - 1
    if close[i+2] > close[i+1] and close[i+1] < close[i] and stoch(dLength, smthLen, kSmoothing)[i] >= level
        isSellSignal := true
        array.push(sellPriceArray, close[i])
        array.push(sellIndexArray, i)

if not na(close[2]) and close[2] > close[1] and stoch(dLength, smthLen, kSmoothing)[3] < level
    strategy.exit("Sell", from_entry="Buy")

// Plot signals
plotshape(series=isBuySignal ? high : na, location=location.abovebar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=isSellSignal ? low : na, location=location.belowbar, color=color.red, style=shape.labeldown, text="SELL")

// Additional parameters and logic can be added as needed
```

```