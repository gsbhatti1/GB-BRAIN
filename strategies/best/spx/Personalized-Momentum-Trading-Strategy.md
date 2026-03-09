> Name

Personalized-Momentum-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/b02e38bb7efb8d3d5a.png)

[trans]

## Overview
This is a personalized trading strategy that combines momentum indicators and candlestick entity filtering. It integrates the use of Stochastic Momentum Index (SMI), fast RSI, and candlestick entity filtering to implement a momentum-based trading strategy while considering overbought and oversold conditions.

## Trading Logic
The strategy uses the following three indicators for trading signal judgment:

1. **Stochastic Momentum Index (SMI):** It combines the spacing between candlestick entities with the relative position of the closing price to determine the strength or weakness of price momentum. A buy signal is generated when SMI crosses above the boundary line, and a sell signal is generated when it crosses below the boundary line.

2. **Fast RSI (7-day line):** It evaluates overbought and oversold conditions. An RSI below 20 indicates oversold conditions and triggers a buy signal; an RSI above 80 indicates overbought conditions and triggers a sell signal.

3. **Candlestick Entity Filter:** Calculate the average candlestick entity size over the past 10 days. Only enable the signal if today's candlestick entity exceeds one-third of that average to avoid invalid signals.

The strategy first evaluates the signals from SMI and RSI. If either indicator’s signal requirement is met, it then combines the candlestick entity filter to determine whether that signal is valid. A trading signal is generated only if the signal is deemed valid.

## Advantage Analysis
This strategy has the following advantages:

1. Multiple indicators combined for more precise and reliable judgments.
2. Adding a candlestick entity filter reduces invalid signals.
3. Combining overbought/oversold conditions makes it easier to capture signals at trend reversal points.
4. Dual-directional long/short trading increases profit opportunities.
5. Partial position trading limits the risk of excessive single-time losses.

## Risk Analysis
The strategy also has some risks:

1. Indicators can generate false signals leading to losses. Parameter optimization can reduce false signals.
2. Partial position trading cannot fully utilize trend opportunities in each direction. Higher returns can be achieved by amplifying trading position size.
3. SMI, as the main indicator, is sensitive to parameter settings; improper configuration may miss trading opportunities or increase false signals.
4. Frequent dual-directional trading increases transaction costs.

## Optimization Directions
The strategy can be further optimized in the following aspects:

1. Optimize parameters for SMI and RSI to find the best parameter combinations.
2. Increase position sizing and position management mechanisms to achieve higher returns during trends.
3. Add stop loss strategies to reduce single-time loss risk.
4. Combine more indicators to judge signal reliability and reduce false signals.
5. Adopt efficient contracts to reduce transaction costs.

## Conclusion
This strategy comprehensively utilizes SMI, fast RSI, and candlestick entity filtering indicators to implement a momentum-based, overbought/oversold-aware personalized trading strategy. It has advantages such as precise judgment, identification of valid signals, combination of overbought/oversold conditions, and dual-directional trading, but also risks like parameter sensitivity, inability to fully capitalize on trends, and frequent operations. By continuously optimizing parameters, increasing position sizing and stop loss management, reducing false signals, etc., the strategy can achieve better trading performance.

||

## Overview
This is a personalized trading strategy that combines momentum indicators and candlestick entity filtering. It comprehensively uses three technical indicators - Stochastic Momentum Index (SMI), fast RSI, and candlestick entity filtering to implement a momentum-based trading strategy while considering overbought and oversold conditions.

## Trading Logic
The strategy uses the following three indicators for trading signal judgment:

1. **Stochastic Momentum Index (SMI):** It combines the spacing between candlestick entities with the relative position of the closing price to determine the strength or weakness of price momentum. A buy signal is generated when SMI crosses above the boundary line, and a sell signal is generated when it crosses below the boundary line.

2. **Fast RSI (7-day line):** It evaluates overbought and oversold conditions. An RSI below 20 indicates oversold conditions and triggers a buy signal; an RSI above 80 indicates overbought conditions and triggers a sell signal.

3. **Candlestick Entity Filter:** Calculate the average candlestick entity size over the past 10 days. Only enable the signal if today's candlestick entity exceeds one-third of that average to avoid invalid signals.

The strategy first evaluates the signals from SMI and RSI. If either indicator’s signal requirement is met, it then combines the candlestick entity filter to determine whether that signal is valid. A trading signal is generated only if the signal is deemed valid.

## Advantage Analysis
This strategy has the following advantages:

1. Judgment is more precise and reliable with a combination of multiple indicators.
2. Adding a candlestick entity filter avoids invalid signals.
3. By combining overbought/oversold conditions, it is easier to capture signals at trend reversal points.
4. Increased profit opportunities with dual-directional long/short trading.
5. Partial position trading avoids excessive single-time loss.

## Risk Analysis
The strategy also has some risks:

1. Indicators can generate false signals leading to losses. Parameter optimization can reduce false signals.
2. Partial position trading cannot fully utilize the trend opportunities in each direction. Higher returns can be achieved by amplifying trading position size.
3. As the main indicator, SMI is sensitive to parameter settings; improper configuration may miss trading opportunities or increase false signals.
4. Frequent dual-directional trading increases transaction costs.

## Optimization Directions
The strategy can be further optimized in the following aspects:

1. Optimize parameters for SMI and RSI to find best parameter combinations.
2. Increase position sizing and position management mechanisms to achieve higher returns during trends.
3. Add stop loss strategies to reduce single-time loss risk.
4. Combine more indicators to judge signal reliability and reduce false signals.
5. Adopt efficient contracts to reduce transaction costs.

## Conclusion
This strategy comprehensively utilizes SMI, fast RSI, and candlestick entity filtering indicators to implement a momentum-based, overbought/oversold-aware personalized trading strategy. It has advantages like precise judgment, identification of valid signals, combination of overbought/oversold conditions, and dual-directional trading but also risks such as parameter sensitivity, inability to fully capitalize trends, and frequent operations. By continuously optimizing parameters, increasing position sizing and stop loss management, reducing false signals, etc., the strategy can achieve better trading performance.

||

## Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|false|Use Martingale|
|v_input_4|100|Capital, %|
|v_input_5|true|Use SMI Strategy|
|v_input_6|true|Use RSI Strategy|
|v_input_7|true|Use Body-Filter|
|v_input_8|5|SMI Percent K Length|
|v_input_9|3|SMI Percent D Length|
|v_input_10|50|SMI Limit|
|v_input_11|2017|From Year|
|v_input_12|2100|To Year|
|v_input_13|true|From Month|
|v_input_14|12|To Month|
|v_input_15|true|From day|
|v_input_16|31|To day|

> Source (PineScript)

```pinescript
//@version=2
strategy(title = "Noro's Stochastic Strategy v1.2", shorttitle = "Stochastic str 1.2", overlay = false, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0)

//Settings 
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
usemar = input(false, defval = false, title = "Use Martingale")
```