> Name

Incremental-Order-Size-Fibonacci-Retracement-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1a2a134a6be2b9cafd9.png)

[trans]


### Overview

This is a relatively complex momentum breakout strategy that incorporates multiple technical indicators for judgment and implements multi-staged pyramiding orders in different directions and phases to achieve the goal of scaling in and out. 

### Principles

The strategy mainly combines the momentum indicator MACD, overbought and oversold indicator RSI, and Bollinger Bands for directional judgment. When the MACD line is above 0 and the RSI is below the oversold line, it is a long signal. When the MACD line is below 0 and the RSI is above the overbought line, it is a short signal. It also incorporates breakout of Bollinger Bands upper and lower rail for further confirmation of trading signals.

In specific implementation, the strategy first judges the performance of MACD line and RSI to confirm fundamentals. Then according to the breakout of Bollinger Bands upper and lower rail, it takes pyramiding orders in different sizes. In a bullish phase, it will gradually long with increasing size near the Bollinger Bands lower rail. In a bearish phase, it will gradually short with increasing size near the Bollinger Bands upper rail. By scaling in and out at different directions and different prices, it can obtain bigger accumulated profit.

Meanwhile, the strategy also tracks the highest and lowest price to set stop loss and take profit, managing the orders accordingly. In general, this strategy combines multiple analytical tools and achieves better returns through staged pyramiding.

### Advantages

1. Combining multiple indicators avoids misjudgment of a single tool.
2. Scaling in with multiple stages can amplify profit margin.
3. Setting stop loss and take profit helps avoid loss from high spikes.
4. Controllable drawdown, won't see huge loss.

### Risks and Solutions

1. Breakout of Bollinger Bands upper and lower rail is not 100% reliable, may see some false signals. Can consider adding other indicators like candlestick patterns, volume for confirmation.
2. Staged pyramiding requires accurate grasp of market pace, rapid reversals may lead to huge loss. Can reduce scaling stages or set wider stop loss.
3. Need to watch for liquidity of trading instruments, low liquidity is not suitable for large batch pyramiding.
4. Backtest ≠ live, costs like spread and commission should be considered in live trading. Can loosen stop loss and take profit range.

### Optimization

1. Can test different parameter combinations like Bollinger period, STD multiplier, RSI parameters to find optimum.
2. Can explore other scaling techniques like fixed fraction, Kelly criterion etc.
3. Can implement dynamic optimization of parameters with machine learning etc.
4. Can incorporate more data sources like sentiment analysis, social data to assist judgement.
5. Can explore futures time price difference for arbitrage, further expand profit space.

### Summary

This strategy comprehensively uses multiple technical indicators, takes staged pyramiding, manages risks with stop loss and take profit, making it a relatively complete trend following strategy. But risks like false signals and rapid reversals should be alerted, properly adjusting parameters and position sizing can lead to more steady excess returns. Further optimization with machine learning etc. can improve strategy performance. It is worth long-term tracking and accumulating.

||

### Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|HA Candles|
|v_input_2|3|# of STDEV's|
|v_input_3|14|Pivot Length|
|v_input_4|100|Z-Index|
|v_input_5|false|Fibonacci|
|v_input_6|5|Resolution|
|v_input_7|false|Reverse Orders|
|v_input_8|99999|TS|
|v_input_9|30|TP|
|v_input_10|10|SL|

> Source (PineScript)

```pinescript
//@version=2
strategy(title="Incremental Order size +", shorttitle="Strategy", overlay=true, default_qty_value=1, pyramiding=10)

//Heiken Ashi
isHA = input(false, "HA Candles", bool)

//MACD
fastLength = 12
slowlength = 26
MACDLength = 9

MACD = ema(close, fastLength) - ema(close, slowlength)
aMACD = ema(MACD, MACDLength)
delta = MACD - aMACD

//Bollinger Bands Exponential
src = open
len = 18
e = ema(src, len)
evar = (src - e)*(src - e)
evar2 = (sum(evar, len))/len
std = sqrt(evar2)
Multiplier = input(3, minval=0.01, title="# of STDEV's")
upband = e + (Multiplier * std)
dnband = e - (Multiplier * std)

//EMA
ema3 = ema(close, 3)

//RSIplot
length = 45
overSold = 90
overBought = 10
price = close
rsi = rsi(price, length)
```