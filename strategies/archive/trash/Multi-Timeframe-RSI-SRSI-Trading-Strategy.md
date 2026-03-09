> Name

Multi-Timeframe RSI-SRSI Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13c6d14e89a7fa34ca7.png)
[trans]
## Overview

This trading strategy combines the use of Relative Strength Index (RSI) and Stochastic Relative Strength Index (Stochastic RSI) technical indicators to generate trading signals. Additionally, it leverages the price trend of cryptocurrencies in higher timeframes to confirm the trend and enhance signal reliability.

## Strategy Name

Multi Timeframe RSI-SRSI Trading Strategy

## Strategy Logic

The strategy determines overbought and oversold conditions based on RSI values. An RSI below 30 indicates an oversold signal, while an RSI above 70 indicates an overbought signal. The Stochastic RSI indicator observes the fluctuation of RSI values. A Stochastic RSI below 5 indicates an oversold signal, while a Stochastic RSI above 50 indicates an overbought signal.

The strategy also incorporates the price trend of cryptocurrencies in higher timeframes (e.g., weekly). Only when the higher time frame RSI is above a threshold (e.g., 45), does a long signal trigger. This filters out non-persistent oversold signals during overall downward trends.

Buy and sell signals need confirmation over a certain period (e.g., 8 bars) to avoid misleading signals.

## Advantages

- Utilizes the classic technical analysis method using RSI to identify overbought/oversold levels
- Incorporates Stochastic RSI to detect reversals in RSI
- Applies multi-timeframe techniques to filter out misleading signals and improve signal quality

## Risks and Solutions

- RSI is prone to generating false signals
  - Combine with other indicators to filter out misleading signals
  - Apply trend confirmation techniques
- Improper threshold settings can lead to too many trading signals
  - Optimize parameter combinations to find the best settings
- Signals require confirmation time
  - Balance confirmation periods to filter out misleading signals without missing opportunities

## Enhancement Directions

- Test more indicator combinations to generate stronger signals
  - For example, incorporate the Moving Average Convergence Divergence (MACD) indicator
- Utilize machine learning methods to find optimal parameters
  - Use genetic algorithms/evolutionary algorithms for automated optimization
- Add stop loss strategies to control single trade risks
  - Set stop loss when the price breaks support levels

## Conclusion

The strategy primarily relies on the two classic technical indicators, RSI and Stochastic RSI, to generate trading signals. The introduction of trend confirmation from higher timeframes effectively filters out misleading signals and improves signal quality. Further performance improvements can be achieved by optimizing parameters, adding stop loss strategies, and other means. The logic is simple and straightforward, serving as a good starting point for quantitative trading.

||

## Overview

This trading strategy combines the use of the Relative Strength Index (RSI) and Stochastic Relative Strength Index (Stochastic RSI) technical indicators to generate trading signals. Additionally, it leverages the price trend of cryptocurrencies in higher timeframes to confirm the trend and enhance signal reliability.

## Strategy Name

Multi Timeframe RSI-SRSI Trading Strategy

## Strategy Logic

The strategy judges overbought and oversold conditions based on RSI values. An RSI below 30 is considered an oversold signal, while an RSI above 70 is considered an overbought signal. The Stochastic RSI indicator observes the fluctuation of RSI values. A Stochastic RSI below 5 is considered an oversold signal, while a Stochastic RSI above 50 is considered an overbought signal.

The strategy also incorporates the price trend of cryptocurrencies in higher timeframes (e.g., weekly). Only when the higher time frame RSI is above a threshold (e.g., 45), does a long signal trigger. This filters out non-persistent oversold signals during overall downward trends.

Buy and sell signals need confirmation over a certain period (e.g., 8 bars) to avoid misleading signals.

## Advantages

- Utilizes the classic technical analysis method using RSI to identify overbought/oversold levels
- Incorporates Stochastic RSI to detect reversals in RSI
- Applies multi-timeframe techniques to filter out misleading signals and improve signal quality

## Risks and Solutions

- RSI is prone to generating false signals
  - Combine with other indicators to filter out misleading signals
  - Apply trend confirmation techniques
- Improper threshold settings can lead to too many trading signals
  - Optimize parameter combinations to find the best settings
- Signals require confirmation time
  - Balance confirmation periods to filter out misleading signals without missing opportunities

## Enhancement Directions

- Test more indicator combinations to generate stronger signals
  - For example, incorporate the Moving Average Convergence Divergence (MACD) indicator
- Utilize machine learning methods to find optimal parameters
  - Use genetic algorithms/evolutionary algorithms for automated optimization
- Add stop loss strategies to control single trade risks
  - Set stop loss when the price breaks support levels

## Conclusion

The strategy primarily relies on the two classic technical indicators, RSI and Stochastic RSI, to generate trading signals. The introduction of trend confirmation from higher timeframes effectively filters out misleading signals and improves signal quality. Further performance improvements can be achieved by optimizing parameters, adding stop loss strategies, and other means. The logic is simple and straightforward, serving as a good starting point for quantitative trading.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|14|RSI Length|
|v_input_2|14|Stochastic Length|
|v_input_3|3|K Smooth|
|v_input_4|3|D Smooth|
|v_input_5|5|Low SRSI|
|v_input_6|50|High SRSI|
|v_input_7|5|difference|
|v_input_8|30|Low RSI|
|v_input_9|60|High RSI|
|v_input_10|45|High higher time frame RSI|
|v_input_11|8|Trigger duration|
|v_input_12|20|Monitoring last low|
|v_input_13|BTC_USDT:swap|Input Ticker (leave empty for current)|
|v_input_14|2019|Start Year|
|v_input_15|true|Start Month|
|v_input_16|true|Start Day|
|v_input_17|2030|End Year|
|v_input_18|true|End Month|
|v_input_19|true|End Day|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-02-11 00:00:00
end: 2024-02-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI and Stochastic Strategy", overlay=true, use_bar_magnifier = false)


/////// Inputs ///////////////

// RSI and SRSI
rsiLength = input(14, title="RSI Length") 
stochLength = input(14, title="Stochastic Length")
kSmooth = input(3, title="K Smooth")
dSmooth = input(3, title="D Smooth")


//////// thresholds ///////////////
st_low = input(5, title="Low SRSI") // stochastic RSI low -- prepare to sell
st_hi = input(50, title="High SRSI") // stochastic RSI high -- prepare to buy
diff = input(5, title="difference") // minimum change in RSI
// inval_diff = input(12, title="difference") // invalidation difference: change in the opposite direction that invalidates rsi falling/rising
rsi_low = input(30, title="Low RSI") // RSI considered low
rsi_hi = input(60, title="High RSI") // RSI considered high
rsi_ht_hi = input(45, title="High higher time frame RSI") // RSI in higher time frame considered high


/// buy trigger duration 
tr_dur = input(8, title="Trigger duration")
low_dur = input(20, title="Monitoring last low")


///////////////// Higher time frame trend ///////////////////
// higher time frame resolution
res2 = input.timeframe("W", title="Higher time-frame")
// Input for the ticker symbol, default is an empty string
// F