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
// This is combo strategies for get a cumulative signal. 
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close for two consecutive days, and the 9-day moving average of the slow K-line is below 50.
// It sells short if close price is lower than the previous close for two consecutive days, and the 9-day moving average of the fast K-line is above 50.
//

// STARC Bands Strategy
// This strategy judges trend direction by plotting bands around a short-term simple moving average of the price.
// The upper band is constructed by adding average true range (ATR) above the moving average.
// The lower band is constructed by subtracting ATR from the moving average.
// Breaking above the upper band indicates an uptrend, while breaking below the lower band indicates a downtrend.
// STARC stands for Stoller Average Range Channels. The indicator is named after its creator, Manning Stoller.

// Initialize variables
var float fastK = na
var float slowK = na
var float upperBand = na
var float lowerBand = na

// 123 Reversal Strategy
if (close[0] > close[1] and close[1] > close[2] and sma(close, v_input_2)[0] < v_input_5)
    strategy.entry("Buy", strategy.long)
else if (close[0] < close[1] and close[1] < close[2] and sma(close, v_input_2)[0] > v_input_5)
    strategy.entry("Sell", strategy.short)

// STARC Bands Strategy
lenMA = input(5, title="Length MA")
lenATR = input(15, title="Length ATR")
k = input(1.33, title="K")
atr = ta.atr(lenATR)
ma = ta.sma(close, lenMA)

upperBand = ma + k * atr
lowerBand = ma - k * atr

// Check for trend direction based on price breakouts
if (close > upperBand)
    strategy.entry("Buy", strategy.long)
if (close < lowerBand)
    strategy.entry("Sell", strategy.short)

// Set Stop Loss and Take Profit (Optional)
stopLoss = input(title="Stop Loss", type=input.price, defval=100)
takeProfit = input(title="Take Profit", type=input.price, defval=200)

strategy.exit("Exit Long", from_entry="Buy", stop=stopLoss, limit=takeProfit)
strategy.exit("Exit Short", from_entry="Sell", stop=stopLoss, limit=takeProfit)
```

This Pine Script code implements the 123 Reversal and STARC Bands combination strategy, as described in the document.