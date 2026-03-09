> Name

Dynamic-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/c37256dd443057e129.png)

[trans]

### Overview

The main idea of this strategy is to dynamically track market trends by buying when the trend goes up and selling when the trend goes down. It combines multiple technical indicators to determine the trend direction, such as linear regression, modified Hull Moving Average, etc.

### Strategy Logic  

This strategy utilizes various technical indicators to determine the trend direction. First, it calculates a price channel, with the upper and lower limits based on the simple moving average of close and an input parameter. Then, it calculates the modified Hull Moving Average, which is considered better at depicting trends. In addition, the linear regression indicator is also calculated. It generates buy signals when the modified HMA crosses above the linear regression line, and sell signals when crossing below. This allows dynamically tracking changes in the trend.

To reduce false signals, the strategy also incorporates several filters, such as using EMA to determine if it's in a downtrend, and a windowed indicator to check for RSI divergence. These filters help avoid taking trades during choppy, sideways markets.

For entries and exits, the strategy records the price of the last open position, and sets take profit and stop loss percentages. For example, if the last long entry price is $100, it may set the take profit target at $102, and stop loss price at $95. This achieves dynamic tracking of the trends.

### Advantage Analysis

This strategy has the following advantages:

1. Dynamically tracking trend changes can smoothly catch longer-term directional moves.
2. Using multiple filters reduces noise and avoids over-trading during choppy markets.
3. Automatically adjusting stop loss and take profit levels achieves trend following.
4. Parameters can be optimized through backtesting to find the best combination automatically.

### Risk Analysis

There are also some risks with this strategy:

1. Still cannot completely avoid being caught in trend reversals, which may lead to larger floating losses when trends reverse.
2. Improper parameter settings may lead to poor strategy performance. Requires optimization to find the best parameters.
3. Long data processing time may cause signal delays. Need to optimize indicator calculation to be as real-time as possible.

To control risks, one can set stop loss, use trailing stops or options to lock in profits. Also, extensive testing of parameter combinations is necessary to find reliable ranges. Finally, execution time of indicators should be monitored to ensure timely signals.

### Optimization Directions

This strategy can be improved in the following aspects:

1. Test combinations of more indicators to find more reliable ways of determining trends.
2. Adjust parameter ranges to find optimal parameters.
3. Optimize signal filters to find balance between noise reduction and lagging.
4. Try machine learning approaches to automatically generate trading rules.

During optimization, backtesting and paper trading should be utilized extensively to evaluate signal quality and stability. Only well-validated optimizations should be applied in live trading.

### Conclusion

Overall this is a decent trend following strategy. It uses multiple indicators to gauge trends, sets up filters to reduce false signals, and can automatically adjust stops and targets to follow trends. With proper parameter tuning, it can smoothly catch mid to long-term trends. Next steps would be finding optimal parameters, and continue validating and improving the strategy.

||

### Overview  

The main idea of this strategy is to dynamically track market trends by buying when the trend goes up and selling when the trend goes down. It combines multiple technical indicators to determine the trend direction, such as linear regression, modified Hull Moving Average, etc.

### Strategy Logic  

This strategy utilizes various technical indicators to determine the trend direction. First, it calculates a price channel, with the upper and lower limits based on the simple moving average of close and an input parameter. Then, it calculates the modified Hull Moving Average, which is considered better at depicting trends. In addition, the linear regression indicator is also calculated. It generates buy signals when the modified HMA crosses above the linear regression line, and sell signals when crossing below. This allows dynamically tracking changes in the trend.

To reduce false signals, the strategy also incorporates several filters, such as using EMA to determine if it's in a downtrend, and a windowed indicator to check for RSI divergence. These filters help avoid taking trades during choppy, sideways markets.

For entries and exits, the strategy records the price of the last open position, and sets take profit and stop loss percentages. For example, if the last long entry price is $100, it may set the take profit target at $102, and stop loss price at $95. This achieves dynamic tracking of the trends.

### Advantage Analysis  

This strategy has the following advantages:

1. Dynamically tracking trend changes can smoothly catch longer-term directional moves.
2. Using multiple filters reduces noise and avoids over-trading during choppy markets.
3. Automatically adjusting stop loss and take profit levels achieves trend following.
4. Parameters can be optimized through backtesting to find the best combination automatically.

### Risk Analysis  

There are also some risks with this strategy:

1. Still cannot completely avoid being caught in trend reversals, which may lead to larger floating losses when trends reverse.
2. Improper parameter settings may lead to poor strategy performance. Requires optimization to find the best parameters.
3. Long data processing time may cause signal delays. Need to optimize indicator calculation to be as real-time as possible.

To control risks, one can set stop loss, use trailing stops or options to lock in profits. Also, extensive testing of parameter combinations is necessary to find reliable ranges. Finally, execution time of indicators should be monitored to ensure timely signals.

### Optimization Directions  

This strategy can be improved in the following aspects:

1. Test combinations of more indicators to find more reliable ways of determining trends.
2. Adjust parameter ranges to find optimal parameters.
3. Optimize signal filters to find balance between noise reduction and lagging.
4. Try machine learning approaches to automatically generate trading rules.

During optimization, backtesting and paper trading should be utilized extensively to evaluate signal quality and stability. Only well-validated optimizations should be applied in live trading.

### Conclusion  

Overall this is a decent trend following strategy. It uses multiple indicators to gauge trends, sets up filters to reduce false signals, and can automatically adjust stops and targets to follow trends. With proper parameter tuning, it can smoothly catch mid to long-term trends. Next steps would be finding optimal parameters, and continue validating and improving the strategy.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0|Strategy Direction: all|short|long|
|v_input_2|30|length of channel|
|v_input_3|5|upper percent|
|v_input_4|5|lower percent|
|v_input_5|3|Fast filter length |
|v_input_6|21|Slow filter length|
|v_input_7|1D|HTF|
|v_input_8|0|Timeframe: 1|5|15|30|60|120|240|360|720|D|W|
|v_input_9|50|Period|
|v_input_10|true|Shift|
|v_input_11|25|len|
|v_input_12|15|Min|
|v_input_13|2|Exit Profit %|
|v_input_14|true|buy Loss Long|
|v_input_15|5| rebuy %|
|v_input_16|true|filter|
|v_input_17|100|risk|
|v_input_18|true|leverage|
|v_input_19|5| stop loss|
|v_input_20|50| qty_percent1|
|v_input_21|50| qty_percent2|
|v_input_22|true| Take profit1|
|v_input_23|2| Take profit2|

> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-03 00:00:00
end: 2023-12-06 00:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to