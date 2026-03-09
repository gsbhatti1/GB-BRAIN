> Name

Momentum-Trend-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/133197733f0fc1530f2.png)
 [trans]

#### Overview

This strategy combines various technical indicators such as moving average, relative strength index (RSI), volume fluctuation indicator (VFI), and true strength index (TSI) to determine the overall momentum and trend of the market and capture mid-to-long term price movements.

#### Strategy Logic

1. Calculate the moving averages of fast line RSI (7-day), normal line RSI (14-day), and slow line RSI (50-day) to determine the RSI trend and momentum.
  
2. Calculate VFI and the moving averages VFI EMA (25-day) and VFI SMA (25-day) to gauge funds inflow and outflow.

3. Calculate the ratio of the long term moving average and short term moving average of TSI to determine the strength of the market trend.

4. Integrate the results of RSI, VFI, and TSI to derive the overall market momentum direction.

5. Take a short position when downward momentum is identified. Close the short position when momentum reversal is detected.

#### Advantage Analysis

1. The combination of multiple indicators allows for a more comprehensive and accurate measurement of overall market momentum and trend.

2. VFI reflects market funds flow, avoiding trading against the trend.

3. TSI filters out market choppiness, making signals more reliable.

4. Overall, the strategy has high reliability and a good win rate.

#### Risk Analysis

1. Complex parameter tuning is required for optimal results from the multi-indicator setup.

2. Simple entry and exit rules may fail to fully capitalize on the information provided by the indicators, leading to short-term reversal losses.

3. Susceptible to false signals and small pullback losses in ranging, choppy markets.

#### Optimization Directions

1. Optimize indicator combinations to find the best parameters.

2. Enhance exit rules based on indicator conditions to catch reversals.

3. Build profit protection mechanisms to reduce losses from choppiness.

#### Summary

This strategy combines multiple indicators to gauge overall market momentum and takes short positions when downward momentum is identified. It has relatively high reliability but simple entry/exit rules that do not fully utilize indicator information. Further enhancements to parameters and exit logic can improve stability and profitability.

|Argument|Default|Description|
|---|---|---|
|v_input_1|50|length|
|v_input_2|50|overSold|
|v_input_3|65|overBought|
|v_input_4|12|fastLength|
|v_input_5|26|slowlength|
|v_input_6|9|MACDLength|
|v_input_7|7|v_input_7|
|v_input_8|14|v_input_8|
|v_input_9|50|v_input_9|
|v_input_10|true|Exponential MA|
|v_input_11|true|Exponential MA|
|v_input_12|true|Exponential MA|
|v_input_13|130|VFI length|
|v_input_14|0.2|coef|
|v_input_15|2.5|Max. vol. cutoff|
|v_input_16|10|signalLength|
|v_input_17|100|signalLength2|
|v_input_18|false|smoothVFI|
|v_input_19|24|Long Length|
|v_input_20|7|Short Length|
|v_input_21|13|Signal Length|

> Source (PineScript)

```pinescript
//@version=2
// credit to LazyBear, Lewm444, and others for direct and indirect inputs/////////////////////////////////
// script is very rough, publishing more for collaborative input value than as a finished product/////////
strategy("Momo", overlay=true)
length = input(50)
overSold = input(50)
overBought = input(65)
price = ohlc4

/////////////////////////////////////////////////////macd/////////////////////////////////////////////////

fastLength = input(12)
slowlength = input(26)
MACDLength = input(9)

fast = 12, slow = 26
fastMA = ema(close, fast)
slowMA = ema(close, slow)
MACD = (fastMA - slowMA)
Msignal = (sma(MACD, 9))*40
//plot(Msignal, color=blue, linewidth=3)

/////////////////////////////////////////////////rsi spread/////////////////////////////////////////////////

source = price

RSIFast  = rsi(source, input(7))
RSINorm  = rsi(source, input(14))
RSISlow = rsi(source, input(50))

//plot(RSIFast, color=silver, style=area, histbase=50)
//plot(RSINorm, color=#98b8be, style=area, histbase=50)
//plot(RSISlow, color=#be9e98, style=area, histbase=50)

//plot(RSIFast, color=gray, style=line, linewidth=1)
//plot(RSINorm, color=purple, style=line, linewidth=2)
//plot(RSISlow, color=black, style=line, linewidth=3)

exponential = input(true, title="Exponential MA")

src = (RSIFast)

ma05 = exponential ? ema(src, 5) : sma(src, 5)
ma30 = exponential ? ema(src, 30) : sma(src, 30)
ma50 = exponential ? ema(src, 50) : sma(src, 50)
ma70 = exponential ? ema(src, 70) : sma(src, 70)
ma90 = exponential ? ema(src, 90) : sma(src, 90)
ma100 = exponential ? ema(src, 100) : sma(src, 100)

exponential1 = input(true, title="Exponential MA")

src1 = (RSINorm)

ma051 = exponential1 ? ema(src1, 5) : sma(src1, 5)
ma301 = exponential1 ? ema(src1, 30) : sma(src1, 30)
ma501 = exponential1 ? ema(src1, 50) : sma(src1, 50)
ma701 = exponential1 ? ema(src1, 70) : sma(src1, 70)
ma901 = exponential1 ? ema(src1, 90) : sma(src1, 90)
ma1001 = exponential1 ? ema(src1, 100) : sma(src1, 100)

exponential2 = input(true, title="Exponential MA")

src2 = (RSINorm)

ma052 = exponential2 ?