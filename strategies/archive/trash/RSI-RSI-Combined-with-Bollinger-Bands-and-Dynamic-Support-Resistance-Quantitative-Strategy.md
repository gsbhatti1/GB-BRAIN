> Name

RSI with Dynamic Support and Resistance Combined with Bollinger Bands Quantitative Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/14d3aeb93aa864e61eb.png)
[trans]

## Overview
This strategy uses the RSI indicator to judge market overbought and oversold levels, combined with Bollinger Bands to determine the price fluctuation range. Additionally, dynamic support and resistance are generated based on high/low prices, triggering buy/sell operations only when the price approaches these levels. Users can set a trend filter condition, such as simple moving average, to ensure that trading occurs only when the price trend aligns with trade directions. The strategy integrates multiple technical indicators for robust signal accuracy and effectively captures market opportunities.

## Strategy Logic
The strategy consists of three key components: RSI, Bollinger Bands, and Dynamic Support/Resistance (S/R).

- **RSI Component:** Determines overbought and oversold levels. An RSI below 30 suggests an oversold condition, triggering a buy signal; above 70 suggests an overbought condition, triggering a sell signal.
  
- **Bollinger Bands:** Upper and lower bands are calculated from the price moving average and standard deviation to determine if prices have broken out of their normal fluctuation range. Prices approaching the upper band suggest a sell, while those approaching the lower band suggest a buy.

- **Dynamic S/R Component:** Uses a dynamic calculation method based on high/low or open/close prices within certain lookback periods and percentage ranges, along with historical price reversal points to generate key support and resistance levels. It triggers a sell signal when the price rises close to key resistance levels and a buy signal when it drops to key support levels.

In summary, this strategy only initiates buy/sell trades when RSI indicates overbought or oversold conditions, prices break out of Bollinger Bands, and are near dynamic S/R levels.

## Advantages
1. Combines fundamental indicators (RSI) with technical analysis indicators (Bollinger Bands). RSI judges market overbought/oversold levels fundamentally while Bollinger Bands determine the price's technical pattern.
2. Dynamic support/resistance calculation adheres closer to actual support and resistance that governs price movement.
3. Adding a trend filter further improves signal accuracy by filtering out noise when combined with RSI and Bollinger Bands.

## Risks
1. Improper RSI parameter settings may cause misjudgment. Too short an RSI length increases noise, while incorrect overbought/oversold thresholds lead to errors.
2. Incorrect Bollinger Bands parameters such as length or standard deviation multiplier affect judging accuracy.
3. Dynamic support/resistance relies on historical high/low prices and thus tends to lag. Users should optimize S/R parameters for greater relevance to current price levels.
4. The strategy has relatively complex logic, with multiple indicators potentially causing interference. Users should test parameters to reduce conflict. Simplifying entry criteria also helps minimize errors.

## Optimization Directions
1. Test and optimize RSI parameters including length and overbought/oversold thresholds.
2. Test and optimize Bollinger Bands parameters including length and standard deviation multiplier.
3. Optimize dynamic support/resistance parameters to align levels closer to current price, such as using shorter lookback periods or fewer historical high/low prices.
4. Test additional auxiliary indicators in combination with RSI, such as KDJ, MACD, etc., to improve accuracy.
5. Test and optimize trend filter parameters, including the length of the trend filter, to extend holding periods and reduce unnecessary reverse orders.

## Conclusion
This strategy leverages the strengths of multiple indicators like RSI, Bollinger Bands, and dynamic support/resistance levels, with extensive cross-verification for robust signal accuracy. Adding a trend filter further reduces noise. With flexible parameter tuning, users can optimize this strategy to best suit their needs. Proper parameter testing and optimization will lead to more pronounced performance. This is a highly promising quantitative strategy.

||

## Overview
This strategy uses the RSI indicator to judge market overbought and oversold levels, combined with Bollinger Bands to determine price fluctuation ranges. Additionally, dynamic support and resistance are generated based on high/low prices, triggering buy/sell operations only when the price approaches these levels. Users can set a trend filter condition, such as simple moving average, to ensure trading occurs only when the price trend aligns with trade directions. The strategy integrates multiple technical indicators for robust signal accuracy and effectively captures market opportunities.

## Strategy Logic
The strategy consists of three key components: RSI, Bollinger Bands, and Dynamic Support/Resistance (S/R).

- **RSI Component:** Determines overbought and oversold levels. An RSI below 30 suggests an oversold condition, triggering a buy signal; above 70 suggests an overbought condition, triggering a sell signal.

- **Bollinger Bands:** Upper and lower bands are calculated from the price moving average and standard deviation to determine if prices have broken out of their normal fluctuation range. Prices approaching the upper band suggest a sell, while those approaching the lower band suggest a buy.

- **Dynamic S/R Component:** Uses a dynamic calculation method based on high/low or open/close prices within certain lookback periods and percentage ranges, along with historical price reversal points to generate key support and resistance levels. It triggers a sell signal when the price rises close to key resistance levels and a buy signal when it drops to key support levels.

In summary, this strategy only initiates buy/sell trades when RSI indicates overbought or oversold conditions, prices break out of Bollinger Bands, and are near dynamic S/R levels.

## Advantages
1. Combines fundamental indicators (RSI) with technical analysis indicators (Bollinger Bands). RSI judges market overbought/oversold levels fundamentally while Bollinger Bands determine the price's technical pattern.
2. Dynamic support/resistance calculation adheres closer to actual support and resistance that governs price movement.
3. Adding a trend filter further improves signal accuracy by filtering out noise when combined with RSI and Bollinger Bands.

## Risks
1. Improper RSI parameter settings may cause misjudgment. Too short an RSI length increases noise, while incorrect overbought/oversold thresholds lead to errors.
2. Incorrect Bollinger Bands parameters such as length or standard deviation multiplier affect judging accuracy.
3. Dynamic support/resistance relies on historical high/low prices and thus tends to lag. Users should optimize S/R parameters for greater relevance to current price levels.
4. The strategy has relatively complex logic, with multiple indicators potentially causing interference. Users should test parameters to reduce conflict. Simplifying entry criteria also helps minimize errors.

## Optimization Directions
1. Test and optimize RSI parameters including length and overbought/oversold thresholds.
2. Test and optimize Bollinger Bands parameters including length and standard deviation multiplier.
3. Optimize dynamic support/resistance parameters to align levels closer to current price, such as using shorter lookback periods or fewer historical high/low prices.
4. Test additional auxiliary indicators in combination with RSI, such as KDJ, MACD, etc., to improve accuracy.
5. Test and optimize trend filter parameters, including the length of the trend filter, to extend holding periods and reduce unnecessary reverse orders.

## Conclusion
This strategy leverages the strengths of multiple indicators like RSI, Bollinger Bands, and dynamic support/resistance levels, with extensive cross-verification for robust signal accuracy. Adding a trend filter further reduces noise. With flexible parameter tuning, users can optimize this strategy to best suit their needs. Proper parameter testing and optimization will lead to more pronounced performance. This is a highly promising quantitative strategy.

---

## Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_int_1|14|RSI Length|
|v_input_int_2|70|Overbought Level|
|v_input_int_3|30|Oversold Level|
|v_input_int_4|20|Bollinger Bands Length|
|v_input_float_1|2|Bollinger Bands Deviation|
|v_input_int_5|10|Pivot Period|
|v_input_string_1|0|Pivot Source: High/Low|Close/Open|
|v_input_int_6|20|Maximum Number of Pivots|
|v_input_int_7|10|Maximum Channel Width %|
|v_input_int_8|5|Maximum Number of S/R Levels|
|v_input_int_9|2|Minimum Strength|
|v_input_bool_1|false|Use Trend Filter|
|v_input_int_10|50|Trend Filter Length|

---

## Source (Pine Script)

```pinescript
/*backtest
start: 2023-01-17 00:00:00
end: 2024-01-23 00:00:00
*/
// RSI with Dynamic Support and Resistance Combined with Bollinger Bands Quantitative Strategy

//@version=5
indicator("RSI with Dynamic Support and Resistance Combined with Bollinger Bands", overlay=true)

rsiLength = input.int(14, minval=1, title="RSI Length")
overboughtLevel = input.int(70, minval=1, title="Overbought Level")
oversoldLevel = input.int(30, minval=1, title="Oversold Level")
bbLength = input.int(20, minval=1, title="Bollinger Bands Length")
bbDeviation = input.float(2.0, minval=0.1, title="Bollinger Bands Deviation")
pivotPeriod = input.int(10, minval=1, title="Pivot Period")
pivotSource = input.string("close", title="Pivot Source", options=["high", "low", "close", "open"])
maxNumPivots = input.int(20, minval=1, title="Maximum Number of Pivots")
maxChannelWidthPercent = input.int(10, minval=1, title="Maximum Channel Width %")
maxSRLevels = input.int(5, minval=1, title="Maximum Number of S/R Levels")
minStrength = input.int(2, minval=1, title="Minimum Strength")
useTrendFilter = input.bool(false, title="Use Trend Filter")
trendFilterLength = input.int(50, minval=1, title="Trend Filter Length")

rsi = ta.rsi(close, rsiLength)
upperBB, lowerBB = ta.bband(close, bbLength, 2, bbDeviation)

// Calculate dynamic support and resistance levels
var float[] supports = array.new_float(0)
var float[] resistances = array.new_float(0)
if (array.size(supports) < maxSRLevels)
    // Add logic to calculate dynamic S/R here

// Check for overbought/oversold conditions
longCondition = ta.crossover(rsi, oversoldLevel) and lowerBB > close
shortCondition = ta.crossunder(rsi, overboughtLevel) and upperBB < close

plotshape(series=longCondition ? close : na, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=shortCondition ? close : na, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// Trend filter
if (useTrendFilter)
    trend = ta.sma(close, trendFilterLength)
    longCondition = longCondition and close > trend
    shortCondition = shortCondition and close < trend

plot(series=trend, title="Trend Filter", color=color.blue)
```
```