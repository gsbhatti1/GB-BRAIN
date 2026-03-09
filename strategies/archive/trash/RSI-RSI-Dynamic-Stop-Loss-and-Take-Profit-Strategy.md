> Strategy Overview:
The strategy is based on the relationship between the RSI indicator and price, optimizing trading performance by dynamically adjusting take profit and stop loss levels. The main idea of the strategy is to utilize the overbought and oversold characteristics of the RSI indicator, combined with changes in price and trading volume, to take profit in a timely manner when the RSI diverges, while controlling risk through dynamic stop loss.

> Strategy Principle:
1. Calculate the value of the RSI indicator and determine the overbought and oversold thresholds based on the input parameters.
2. Judge whether a peak formation (isPeak) or bottom formation (isBottom) appears by comparing the current RSI value with the RSI values of the previous few candles.
3. When a peak formation appears, if the current price is higher than the high of the previous peak and the trading volume is smaller than the trading volume of the previous peak, a sell signal is generated.
4. When a bottom formation appears, if the current price is lower than the low of the previous bottom and the trading volume is smaller than the trading volume of the previous bottom, a buy signal is generated.
5. After a buy signal is triggered, take profit when the price retraces to the low of the previous bottom or the trading volume is smaller than the trading volume of the previous bottom.
6. After a sell signal is triggered, take profit when the price rebounds to the high of the previous peak or the trading volume is smaller than the trading volume of the previous peak.
7. After opening a position, set the stop loss price to a certain percentage (2%) of the opening price to control risk.

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|14|RSI Length|
|v_input_2|70|Overbought Level|
|v_input_3|30|Oversold Level|


> Source (PineScript)

``` pinescript
//@version=4
strategy("RMM_byMR", overlay=true)

// RSI length input
rsiLength = input(14, title="RSI Length")

// Overbought and oversold levels inputs
overboughtLevel = input(70, title="Overbought Level")
oversoldLevel = input(30, title="Oversold Level")

// RSI calculation
rsiValue = rsi(close, rsiLength)

// Detect the last peak points // Detect the last bottom points
```