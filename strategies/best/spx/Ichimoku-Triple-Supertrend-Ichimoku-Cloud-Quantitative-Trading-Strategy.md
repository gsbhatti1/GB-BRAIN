> Name

Triple-Supertrend-Ichimoku-Cloud-Quantitative-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f612903c646a621ebc.png)
[trans]

## Overview

This strategy is a quantitative trading strategy that combines the Triple Supertrend indicator, Ichimoku Cloud indicator, Average True Range (ATR) indicator, and Exponential Moving Average (EMA). It uses the Triple Supertrend to determine market trend direction, Ichimoku Cloud for support and resistance, ATR for stop loss, and EMA for trend confirmation to form a relatively complete trading system.

## Strategy Principle

The core logic of this strategy is based on the judgment of the Triple Supertrend indicator. The Supertrend indicator determines the trend direction by comparing the price with the average true range within a certain period. When the price is above the upper band, it is a bullish signal; when the price is below the lower band, it is a bearish signal. This strategy adopts three Supertrend indicators with different parameters. Trading signals are generated when all three give buy or sell signals simultaneously.

In addition, the Ichimoku Cloud thickness helps determine the strength of the current trend to filter out some false signals. The ATR indicator is used to set the stop loss. The EMA indicator confirms intermediate and long-term trends.

Specifically, go long when the price is above the upper band of all three Supertrend indicators; go short when below the lower band of all three. Also require the price to be above or below the Ichimoku Cloud to filter uncertain signals. The stop loss is set to the entry price minus the ATR value for a dynamic trailing stop.

## Advantages

1. The triple Supertrend with different settings can effectively filter market noise and determine trend direction more accurately.
2. Ichimoku Cloud determines trend strength to avoid false breakouts. ATR stop loss setting is reasonable to minimize potential losses.
3. EMA assists in confirming intermediate and long-term trends, verifying signals from Supertrend to further improve reliability.
4. Combining multiple indicators allows for cross-verification of signals, providing a more reliable market trend judgment.

## Risks

1. Although Ichimoku Cloud is added, there is still the risk of entering an invalid zone if cloud thickness is penetrated. The ATR would cap losses to some extent.
2. When volatility is high, stop loss set by ATR could be triggered directly, increasing the loss rate. Parameters can be adjusted or stop loss range increased.
3. Invalid signals may occur frequently if Supertrend parameters are set inappropriately. Extensive backtesting is needed to find the best parameter combination.

## Enhancement

1. Additional indicators like Volatility Index and Bollinger Bands can be added to assist in filtering signals and improving reliability.
2. Improve ATR calculation to dynamically adjust stop loss ranges during high volatility to reduce loss rates.
3. Add a machine learning model trained on historical data to judge trading signals instead of manual parameter setting, which would improve signal accuracy.

## Conclusion

This strategy combines four parts including Triple Supertrend, Ichimoku Cloud, ATR, and EMA. Signals are verified across indicators when determining market trends. Ichimoku Cloud and ATR stop loss control risk. EMA confirms intermediate and long-term trends. Signals from this strategy are relatively reliable for intermediate to long-term holding. Stop loss mechanisms can be further optimized, and additional assisting indicators can be added to obtain better performance.

||


## Summary

This strategy is a quantitative trading strategy that combines the Triple Supertrend indicator, Ichimoku Cloud indicator, Average True Range (ATR) indicator, and Exponential Moving Average (EMA). It uses the Triple Supertrend to determine market trend direction, Ichimoku Cloud for support and resistance, ATR for stop loss, and EMA for trend confirmation to form a relatively complete trading system.

## Strategy Principle

The core logic of this strategy is based on the judgment of the Triple Supertrend indicator. The Supertrend indicator determines the trend direction by comparing the price with the average true range within a certain period. When the price is above the upper band, it is a bullish signal; when the price is below the lower band, it is a bearish signal. This strategy adopts three Supertrend indicators with different parameters. Trading signals are generated when all three give buy or sell signals simultaneously.

In addition, the Ichimoku Cloud thickness helps determine the strength of the current trend to filter out some false signals. The ATR indicator is used to set the stop loss. The EMA indicator confirms intermediate and long-term trends.

Specifically, go long when the price is above the upper band of all three Supertrend indicators; go short when below the lower band of all three. Also require the price to be above or below the Ichimoku Cloud to filter uncertain signals. The stop loss is set to the entry price minus the ATR value for a dynamic trailing stop.

## Advantages

1. The triple Supertrend with different settings can effectively filter market noise and determine trend direction more accurately.
2. Ichimoku Cloud determines trend strength to avoid false breakouts. ATR stop loss setting is reasonable to minimize potential losses.
3. EMA assists in confirming intermediate and long-term trends, verifying signals from Supertrend to further improve reliability.
4. Combining multiple indicators allows for cross-verification of signals, providing a more reliable market trend judgment.

## Risks

1. Although Ichimoku Cloud is added, there is still the risk of entering an invalid zone if cloud thickness is penetrated. The ATR would cap losses to some extent.
2. When volatility is high, stop loss set by ATR could be triggered directly, increasing the loss rate. Parameters can be adjusted or stop loss range increased.
3. Invalid signals may occur frequently if Supertrend parameters are set inappropriately. Extensive backtesting is needed to find the best parameter combination.

## Enhancement

1. Additional indicators like Volatility Index and Bollinger Bands can be added to assist in filtering signals and improving reliability.
2. Improve ATR calculation to dynamically adjust stop loss ranges during high volatility to reduce loss rates.
3. Add a machine learning model trained on historical data to judge trading signals instead of manual parameter setting, which would improve signal accuracy.

## Conclusion

This strategy combines four parts including Triple Supertrend, Ichimoku Cloud, ATR, and EMA. Signals are verified across indicators when determining market trends. Ichimoku Cloud and ATR stop loss control risk. EMA confirms intermediate and long-term trends. Signals from this strategy are relatively reliable for intermediate to long-term holding. Stop loss mechanisms can be further optimized, and additional assisting indicators can be added to obtain better performance.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_int_1|2|percentage of portfolio per order|
|v_input_int_2|9|(?ichimoku) Conversion Line Length|
|v_input_int_3|26|Base Line Length|
|v_input_int_4|52|Leading Span B Length|
|v_input_int_5|26|Lagging Span|
|v_input_1|10|(?SuperTrend) ATR Length1|
|v_input_float_1|true|Factor1|
|v_input_2|11|ATR Length2|
|v_input_float_2|2|Factor2|
|v_input_3|12|ATR Length2|
|v_input_float_3|3|Factor2|
|v_input_int_6|14|(?ATR) Length (ATR)|
|v_input_string_1|0|Smoothing (ATR): RMA |SMA |EMA |WMA|
|v_input_int_7|200|(?EMA) Length of EMA|
|v_input_4_close|0|Source of EMA: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_8|false|Offset (EMA)|
|v_input_string_2|0|Method (EMA): SMA |EMA |SMMA (RMA) |WMA |VWMA|
|v_input_int_9|5|Smoothing Length (EMA)|


> Source (PineScript)

```pinescript
//@version=5
strategy(title="HyperTrend", shorttitle="HyperTrend", overlay=true )
```