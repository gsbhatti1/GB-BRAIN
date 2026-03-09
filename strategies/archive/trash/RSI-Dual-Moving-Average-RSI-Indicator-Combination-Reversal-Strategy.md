> Name

Dual-Moving-Average-RSI-Indicator-Combination-Reversal-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1a1891ae0ee82932bf0.png)
[trans]


## Overview

This strategy uses a combination of dual moving averages, relative strength index (RSI), and parabolic stop-and-reverse (PSAR) indicators to identify price reversal points. It then makes buy and sell decisions at these points based on the identified reversals, making it a reversal trading strategy.

## Principles 

The strategy mainly uses the following technical indicators to determine price reversal points:

1. Dual Moving Average: Calculate fast moving average (MA Fast Line) and slow moving average (MA Slow Line). When the fast line crosses above the slow line, it indicates a bull market and goes long. When the fast line crosses below the slow line, it indicates a bear market and goes short.

2. RSI Indicator: RSI judges overbought and oversold conditions by calculating the average closing gain and average closing loss over a period of time. RSI above 70 indicates an overbought zone, while RSI below 30 indicates an oversold zone.

3. PSAR Indicator: Parabolic SAR indicates the trend direction. SAR points below price indicate a bull market; above price indicate a bear market.

4. ADX Indicator: ADX measures the strength of a trend by calculating directional movement. ADX above 20 signals a trending market, while ADX below 20 signals consolidation.

The logic for buy and sell signals is as follows:

- Buy Signal: Fast MA crosses above slow MA, RSI below 30 (oversold), SAR points above price, ADX above 20.
- Sell Signal: Fast MA crosses below slow MA, RSI above 70 (overbought), SAR points below price, ADX above 20.

When a buy or sell signal occurs, take a position with 10% of equity respectively. Close the position timely when the reversal signal fails.

## Advantages

- Dual MAs determine major trend direction, while RSI and PSAR filter out false signals, making it possible to accurately identify reversal points.
- Combining multiple indicators prevents wrong signals from a single indicator.
- Setting stop losses effectively controls risk.
- The strategy is simple and easy to implement.
- It works for both uptrend and downtrend markets.

## Risks and Solutions

- Dual MAs may generate false breakout signals. Consider using longer MA periods or adding Bollinger Bands to confirm true breakouts.
- RSI may produce incorrect signals if not properly set. Fine-tune the RSI parameters and add other indicators to confirm RSI signals.
- Suspend trading when ADX is below 20 to avoid reversal trading in directionless markets. Alternatively, shorten the ADX period.
- SetStringry stop losses can cause unnecessary loss. Adjust stop losses based on market volatility.
- High trading frequency may be an issue. Adjust MA periods to lower trading frequency.

## Improvement

- Test different lengths of MAs to find the best combination.
- Test different RSI parameters for better overbought/oversold judgment.
- Add other indicators like Bollinger Bands, KDJ to enrich the logic.
- Set dynamic stop losses based on different products and markets.
- Implement position sizing to better follow trends.
- Test different ADX parameters to find the best value to determine trend strength.
- Add an auto stop loss function.

## Conclusion

This strategy uses dual moving averages to identify major trend directions, and RSI, PSAR for additional signal filtering. After optimizing parameters, it can effectively identify reversal points and catch trends around reversals. In practice, risk management by proper stop losses and ongoing parameter optimization are crucial. Overall, the strategy combines indicators with clear logic and easy operation, making it a reliable reversal trading strategy.

||

## Overview

This strategy combines dual moving averages, relative strength index (RSI), and parabolic SAR (PSAR) to identify price reversal points and make buy/sell decisions accordingly. It falls under the category of reversal trading strategies.

## Principles 

The strategy mainly uses the following technical indicators to determine price reversal points:

1. Dual Moving Average: Calculate fast moving average (MA Fast Line) and slow moving average (MA Slow Line). When the fast line crosses above the slow line, it indicates a bull market and goes long. When the fast line crosses below the slow line, it indicates a bear market and goes short.

2. RSI Indicator: RSI judges overbought and oversold conditions by calculating the average closing gain and average closing loss over a period of time. RSI above 70 indicates an overbought zone, while RSI below 30 indicates an oversold zone.

3. PSAR Indicator: Parabolic SAR indicates the trend direction. SAR points below price indicate a bull market; above price indicate a bear market.

4. ADX Indicator: ADX measures the strength of a trend by calculating directional movement. ADX above 20 signals a trending market, while ADX below 20 signals consolidation.

The logic for buy and sell signals is as follows:

- Buy Signal: Fast MA crosses above slow MA, RSI below 30 (oversold), SAR points above price, ADX above 20.
- Sell Signal: Fast MA crosses below slow MA, RSI above 70 (overbought), SAR points below price, ADX above 20.

When a buy or sell signal occurs, take a position with 10% of equity respectively. Close the position timely when the reversal signal fails.

## Advantages

- Dual MAs determine major trend direction, while RSI and PSAR filter out false signals, making it possible to accurately identify reversal points.
- Combining multiple indicators prevents wrong signals from a single indicator.
- Setting stop losses effectively controls risk.
- The strategy is simple and easy to implement.
- It works for both uptrend and downtrend markets.

## Risks and Solutions

- Dual MAs may generate false breakout signals. Consider using longer MA periods or adding Bollinger Bands to confirm true breakouts.
- RSI may produce incorrect signals if not properly set. Fine-tune the RSI parameters and add other indicators to confirm RSI signals.
- Suspend trading when ADX is below 20 to avoid reversal trading in directionless markets. Alternatively, shorten the ADX period.
- SetStringry stop losses can cause unnecessary loss. Adjust stop losses based on market volatility.
- High trading frequency may be an issue. Adjust MA periods to lower trading frequency.

## Improvement

- Test different lengths of MAs to find the best combination.
- Test different RSI parameters for better overbought/oversold judgment.
- Add other indicators like Bollinger Bands, KDJ to enrich the logic.
- Set dynamic stop losses based on different products and markets.
- Implement position sizing to better follow trends.
- Test different ADX parameters to find the best value to determine trend strength.
- Add an auto stop loss function.

## Conclusion

This strategy uses dual moving averages to identify major trend directions, and RSI, PSAR for additional signal filtering. After optimizing parameters, it can effectively identify reversal points and catch trends around reversals. In practice, risk management by proper stop losses and ongoing parameter optimization are crucial. Overall, the strategy combines indicators with clear logic and easy operation, making it a reliable reversal trading strategy.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0.02|start|
|v_input_2|0.02|increment|
|v_input_3|0.2|maximum|
|v_input_4|30|ADX Smoothing|
|v_input_5|30|DI Length|
|v_input_6|50|length|
|v_input_7|0.5|Mult Factor|
|v_input_8|0.1|alertLevel|
|v_input_9|0.75|impulseLevel|
|v_input_10|false|showRange|


> Source (PineScript)

```pinescript
//@version=2
// Based on Senpai BO 3
strategy(title="Senpai_Strat_3", shorttitle="Senpai_Strat_3", overlay=false, default_qty_type=strategy.percent_of_equity, default_qty_value=100)
src = close

// PSAR 
start = input(0.02)
increment = input(0.02)
maximum = input(0.2)
psar = sar(start, increment, maximum)

// ADX Init
adxlen = input(30, title="ADX Smoothing")	
dilen = input(30, title="DI Length")	
dirmov(
```