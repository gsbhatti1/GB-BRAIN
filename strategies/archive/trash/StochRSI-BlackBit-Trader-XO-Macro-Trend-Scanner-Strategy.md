> Name

Double Moving Average with StochRSI Crossover for Macro Trend Tracking Strategy - BlackBit-Trader-XO-Macro-Trend-Scanner-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/5e2cb6dcc20b4a140a.png)
 [trans]

## Overview

This strategy combines the use of double moving averages and StochRSI indicators to identify trend direction and entry points. The main feature is that it can enter the market at an early stage of a trend, while using the overbought/oversold characteristics of StochRSI to filter false breakouts.

## Strategy Logic

The strategy uses fast moving average EMA(12) and slow moving average EMA(25) to build a double moving average system. When the fast line crosses above the slow line, a buy signal is generated. When the fast line crosses below the slow line, a sell signal is generated. This is used to determine the major trend direction.

At the same time, the strategy incorporates StochRSI crossover to further identify entry timing. The StochRSI combines stochastic KDJ and RSI indicators. When the K line crosses above the D line from an oversold zone, a buy signal is generated. When the K line crosses below the D line from an overbought zone, a sell signal is generated.

Only when the double moving average produces a signal and StochRSI also generates a corresponding signal will this strategy open positions. This can effectively filter out some false breakouts and avoid invalid trades.

## Advantage Analysis

The biggest advantage of this strategy is being able to judge trend direction and potential entry points early. The moving average system can produce signals at the beginning of a trend, while the addition of StochRSI effectively filters false breakouts and avoids erroneous trades.

In addition, the strategy combines both trend analysis and overbought/oversold judgment, featuring the strengths of both trend following and mean-reversion. Whether tracking trends or buying low and selling high, this strategy can capture opportunities in all aspects.

## Risk Analysis

The main risk of this strategy lies in the lag of the double moving average system itself. When the market changes violently suddenly, the double moving average system often takes time to generate signals, easily missing the best entry timing.

In addition, StochRSI may also generate false signals, leading to unnecessary trades, especially in ranging markets where K and D lines can frequently crossover, posing risks of excessive invalid operations.

## Optimization Directions

The optimization of this strategy mainly focuses on several aspects:

1. Adjusting the parameters of double moving averages to adopt more favorable moving average periods for capturing trends;
2. Optimizing StochRSI parameters to develop a more sensible overbought/oversold criteria;
3. Increasing order size or adjusting stop loss/take profit levels to pursue higher returns;
4. Incorporating other indicators as filter conditions to further reduce invalid signals.

## Summary

Overall, this strategy is very suitable for capturing medium-to-long term trends with great profit potential at the early stage of trends. Combining StochRSI as an auxiliary judge can effectively filter misleading signals and avoid unnecessary losses. With improvements in parameter tuning and risk management, this strategy can become a powerful tool to obtain steady returns.

||

## Overview

This strategy combines double moving average and StochRSI indicators to identify trend direction and entry points. The main feature is that it can enter the market at an early stage of a trend, while using the overbought/oversold characteristics of StochRSI to filter false breakouts.

## Strategy Logic

The strategy uses fast moving average EMA(12) and slow moving average EMA(25) to build a double moving average system. When the fast line crosses above the slow line, a buy signal is generated. When the fast line crosses below the slow line, a sell signal is generated. This is used to determine the major trend direction.

At the same time, the strategy incorporates StochRSI crossover to further identify entry timing. The StochRSI combines stochastic KDJ and RSI indicators. When the K line crosses D line upward from an oversold zone, a buy signal is generated. When the K line crosses D line downward from an overbought zone, a sell signal is generated.

Only when the double moving average produces a signal and StochRSI also generates a corresponding signal will this strategy open positions. This can effectively filter out some false breakouts and avoid invalid trades.

## Advantage Analysis

The biggest advantage of this strategy is being able to judge trend direction and potential entry points early. The moving average system can produce signals at the beginning of a trend, while the addition of StochRSI effectively filters false breakouts and avoids erroneous trades.

In addition, the strategy combines both trend analysis and overbought/oversold judgment, featuring the strengths of both trend following and mean-reversion. Whether tracking trends or buying low and selling high, this strategy can capture opportunities in all aspects.

## Risk Analysis

The main risk of this strategy lies in the lag of the double moving average system itself. When the market changes violently suddenly, the double moving average system often takes time to generate signals, easily missing the best entry timing.

In addition, StochRSI may also generate false signals, leading to unnecessary trades, especially in ranging markets where K and D lines can frequently crossover, posing risks of excessive invalid operations.

## Optimization Directions

The optimization of this strategy mainly focuses on several aspects:

1. Adjusting the parameters of double moving averages to adopt more favorable moving average periods for capturing trends;
2. Optimizing StochRSI parameters to develop a more sensible overbought/oversold criteria;
3. Increasing order size or adjusting stop loss/take profit levels to pursue higher returns;
4. Incorporating other indicators as filter conditions to further reduce invalid signals.

## Summary

Overall, this strategy is very suitable for capturing medium-to-long term trends with great profit potential at the early stage of trends. Combining StochRSI as an auxiliary judge can effectively filter misleading signals and avoid unnecessary losses. With improvements in parameter tuning and risk management, this strategy can become a powerful tool to obtain steady returns.

||

> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_1_close|0|OHLC Type: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|12|Fast EMA|
|v_input_3|25|Slow EMA|
|v_input_4|25|Consolidated EMA|
|v_input_5|true|Show Both EMAs|
|v_input_int_1|3|K|
|v_input_int_2|3|D|
|v_input_int_3|14|RSI Length|
|v_input_int_4|14|Stochastic Length|
|v_input_int_5|80|(?Bands change this instead of length in Style for Stoch RSI colour to work properly)Upper Band|
|v_input_int_6|50|Middle Band|
|v_input_int_7|20|Lower Band|
|v_input_bool_1|false|(?Crossover Alerts)Crossover Alert Background Colour (Middle Level) [ON/OFF]|
|v_input_bool_2|false|Crossover Alert Background Colour (OB/OS Level) [ON/OFF]|
|v_input_bool_3|false|Crossover Alert >input [ON/OFF]|
|v_input_bool_4|false|Crossover Alert <input [ON/OFF]|
|v_input_string_1|0|(?Moving Average)MA Type: EMA|WMA|SMA|None|
|v_input_source_1_close|0|MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_8|200|MA Length|
|v_input_6|timestamp(2000-12-24T00:00:00)|(?---------TIME RANGE SETTINGS---------)startDate|
|v_input_7|timestamp(2029-02-26T00:00:00)|finishDate|
|v_input_8|200|(?EMA FILTER SETTINGS)EMA Filter Length|
|v_input_9_close|0|EMA Filter Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_10|26|(?MACD FILTER SETTINGS)Fast Length|
|v_input_11|100|Slow Length|
|v_input_12_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_9|9|Signal Smoothing|
|v_input_string_2|0|Oscillator MA Type: EMA|SMA|
|v_input_string_3|0|Signal Line MA Type: EMA|SMA|
|v_input_float_1|0.3|(?TP/SL CONDITION INPUTS HERE)Enter The Take Profit %|
|v_input_float_2|0.16|