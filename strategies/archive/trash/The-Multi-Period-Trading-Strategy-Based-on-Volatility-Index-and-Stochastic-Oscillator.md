> Name

The-Multi-Period-Trading-Strategy-Based-on-Volatility-Index-and-Stochastic-Oscillator

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1a48274ed19b654a7fa.png)

[trans]

### Overview

This strategy combines the volatility index VIX and stochastic oscillator RSI through a composition of indicators across different time periods, in order to achieve efficient breakout entries and overbought/oversold exits. The strategy has large room for optimizations and can be adapted to different market environments.

### Strategy Principles  

1. Calculate the VIX volatility index: Take the highest and lowest prices over the past 20 days to compute volatility. High VIX indicates market panic, while low VIX suggests market complacency.
   
2. Compute the RSI stochastic oscillator: Take the price changes over the past 14 days. RSI above 70 suggests overbought conditions, and RSI below 30 suggests oversold conditions.

3. Combine the two indicators. Go long when VIX breaches the upper band or the highest percentile. Close longs when RSI goes above 70.

### Strategy Advantages 

1. Integrates multiple indicators for comprehensive market timing assessment.
2. Indicators across timeframes verify each other and improve decision accuracy.
3. Customizable parameters can be optimized for different trading instruments.

### Risk Analysis  

1. Improper parameter tuning may cause multiple false signals.
2. A single exit indicator may miss price reversals.

#### Optimization Suggestions

1. Incorporate more confirming indicators like moving averages and Bollinger bands to time entries.
2. Add more exit indicators such as reversal candlestick patterns.

### Summary 

This strategy utilizes the VIX to gauge market timing and risk levels, and filters out unfavorable trades using overbought/oversold readings from the RSI, in order to enter at opportune moments and exit timely with stops. There is ample room for optimization to suit wider market conditions.

||

Overview
This strategy combines the volatility index VIX and stochastic oscillator RSI through a composition of indicators across different time periods, in order to achieve efficient breakout entries and overbought/oversold exits. The strategy has large room for optimizations and can be adapted to different market environments.  

Principles
1. Calculate the VIX volatility index: Take the highest and lowest prices over the past 20 days to compute volatility. High VIX indicates market panic, while low VIX suggests market complacency.

2. Compute the RSI stochastic oscillator: Take the price changes over the past 14 days. RSI above 70 suggests overbought conditions, and RSI below 30 suggests oversold conditions.

3. Combine the two indicators. Go long when VIX breaches the upper band or the highest percentile. Close longs when RSI goes above 70.

Advantages 
1. Integrates multiple indicators for comprehensive market timing assessment.
2. Indicators across timeframes verify each other and improve decision accuracy.
3. Customizable parameters can be optimized for different trading instruments.

Risks
1. Improper parameter tuning may cause multiple false signals.
2. A single exit indicator may miss price reversals.

Optimization Suggestions
1. Incorporate more confirming indicators like moving averages and Bollinger bands to time entries.
2. Add more exit indicators such as reversal candlestick patterns.

Summary
This strategy utilizes the VIX to gauge market timing and risk levels, and filters out unfavorable trades using overbought/oversold readings from the RSI, in order to enter at opportune moments and exit timely with stops. There is ample room for optimization to suit wider market conditions.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|14|lookback length of Stochastic|
|v_input_int_2|80|Stochastic overbought condition|
|v_input_int_3|20|Stochastic oversold condition|
|v_input_1|3|smoothing of Stochastic %K |
|v_input_2|3|moving average of Stochastic %K|
|v_input_int_4|14|lookback length of RSI|
|v_input_int_5|70|RSI overbought condition|
|v_input_int_6|30|RSI oversold condition|
|v_input_3|22|LookBack Period Standard Deviation High|
|v_input_4|20|Bolinger Band Length|
|v_input_float_1|2|Bollinger Band Standard Devaition Up|
|v_input_5|50|Look Back Period Percentile High|
|v_input_6|0.85|Highest Percentile - 0.90=90%, 0.95=95%, 0.99=99%|
|v_input_7|false|-------Text Plots Below Use Original Criteria-------|
|v_input_8|false|Show Text Plot if WVF WAS True and IS Now False|
|v_input_9|false|Show Text Plot if WVF IS True|
|v_input_10|false|-------Text Plots Below Use FILTERED Criteria-------|
|v_input_11|true|Show Text Plot For Filtered Entry|
|v_input_12|true|Show Text Plot For AGGRESSIVE Filtered Entry|
|v_input_float_2|40|Long-Term Look Back Current Bar Has To Close Below This Value OR Medium Term--Default=40|
|v_input_float_3|14|Medium-Term Look Back Current Bar Has To Close Below This Value OR Long Term--Default=14|
|v_input_int_7|3|Entry Price Action Strength--Close > X Bars Back---Default=3|
|v_input_13|false|-------------------------Turn On/Off ALERTS Below---------------------|
|v_input_14|false|----To Activate Alerts You HAVE To Check The Boxes Below For Any Alert Criteria You Want----|
|v_input_15|false|Show Alert WVF = True?|
|v_input_16|false|Show Alert WVF Was True Now False?|
|v_input_17|false|Show Alert WVF Filtered?|
|v_input_18|false|Show Alert WVF AGGRESSIVE Filter?|

> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-20 00:00:00
end: 2023-12-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © timj

strategy('Vix FIX / StochRSI Strategy', overlay=true, pyramiding=9, margin_long=100, margin_short=100)

Stochlength = input.int(14, minval=1, title="lookback length of Stochastic")
StochOverBought = input.int(80, title="Stochastic overbought condition")
StochOverSold = input.int(20, title="Stochastic oversold condition")
smoothK = input(3, title="smoothing of Stochastic %K ")
smoothD = input(3, title="moving average of Stochastic %K")
k = ta.sma(ta.stoch(close, high, low, Stochlength), smoothK)
d = ta.sma(k, smoothD)

///////////// RSI 
RSIlength = input.int( 14, minval=1 , title="lookback length of RSI")
RSIOverBought = input.int( 70  , title="RSI overbought condition")
RSIOverSold = input.int( 30  , title="RSI oversold condition")
RSIprice = close
vrsi = ta.rsi(RSIprice, RSIlength)

///////////// Double strategy: RSI strategy + Stochastic strategy

pd = input(22, title="LookBack Period Standard Deviation High")
bbl = input(20, title="Bolinger Band Length")
mult = input.float(2.0    , minval=1, maxval=5, title="Bollinger Band Standard Devaition Up")
lb = input(50  , title="Look Back Period Percentile High")
ph = input(.85, title="Highest Percentile - 0.90=90%, 0.95=95%, 0.99=99%")
new = input(false, title="-------Text Plots Below Use Original Criteria-------" )
```