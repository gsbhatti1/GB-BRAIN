---
> Name

Dual MA Indicator Oscillating Price Tracking Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16e566fe96e1d0694f0.png)
[trans]

This strategy is named "Dual MA Indicator Oscillating Price Tracking Strategy." It utilizes the combination of SMA, EMA, and other MA (Moving Average) indicators to track market prices in real time. When there is oscillation in the market, it can provide trading signals.

Strategy Overview:
The strategy builds three groups of MA indicator lines with different parameters, representing the fast, medium, and slow trends of the market. Meanwhile, filter indicators are used to filter out false signals and form the basis for long and short judgments. The strategy has diverse logical optimization and filtering methods, using technical indicators such as moving average crossovers, RSI (Relative Strength Index), and Bollinger Bands breakouts for composite judgment. It can effectively determine the buying and selling points of price extremes and capture oscillating trends while reducing market risks. The strategy has significant advantages.

Strategy Principles:  
1. Set up a group of fast (21 periods), medium (55 periods), and slow (89 periods) three MA indicator lines representing average price levels at different time lengths;
2. Determine whether the current trend is in an upward or downward phase by judging the arrangement relationship of the three MA indicator lines (fast > medium > slow or fast < medium < slow);
3. Assist with judgments such as SuperTrend to increase signal accuracy;
4. Issue buy/sell signals based on changes in the status of these signals and filter indicators.

Advantages of the Strategy:
1. Use multiple MA combinations to judge long and short term market trends for more accurate judgments;
2. Adopt multiple filtering methods to optimize the selection of buying and selling points and increase profit probability;
3. Apply technical indicators such as Bollinger Bands and RSI to assist breakouts and grasp key support levels and reversal opportunities;  
4. Select the buying and selling direction according to the direction change of the fast MA without the need to be greedy for reversals, chase oscillating trends, and achieve profits;
5. Trading signals displayed clearly through visualizable arrows and markings, easy to grasp and convenient to operate.

Risks and Prevention:  
1. MA strategies have weaker resistance to false breakout probabilities;
2. There may be time differences between combined indicators, leading to lagging signal risks;  
3. After a break-in buy, further judgment of the strength of the subsequent market is needed to prevent being trapped;
4. Consider adding stop loss and take profit in live trading to control maximum loss per trade.   

Strategy Optimization:  
1. Test different types and parameters of MA to find the optimal combination;
2. Enhance reversal judgment modules such as improving the use of the KD indicator;  
3. Incorporate trading volume indicators to determine true trends;  
4. Expand BIAS indicators to determine overbought and oversold areas.

Conclusion:  
In the ever-fluctuating cryptocurrency market, this strategy takes advantage of the opportunities during the ups and downs of market waves. By setting up the MA indicators and auxiliary filtering judgments for switching between long and short positions, it grasps the key reversal timing of the market. It can also be further optimized by adding stop loss modules to reduce single losses and obtain long-term positive returns through strategy automation.

||

The strategy is named "Dual MA Indicator Oscillating Price Tracking Strategy." It utilizes the combination of SMA, EMA, and other MA (Moving Average) indicators to track market prices in real time. When there is oscillation in the market, it can provide trading signals.

Strategy Overview:
The strategy builds three groups of MA indicator lines with different parameters, representing the fast, medium, and slow trends of the market. Meanwhile, filter indicators are used to filter out false signals and form the basis for long and short judgments. The strategy has diverse logical optimization and filtering methods, using technical indicators such as moving average crossovers, RSI overbought and oversold, and Bollinger Bands breakouts for composite judgment. It can effectively determine the buying and selling points of price extremes and capture oscillating trends while reducing market risks. The strategy has significant advantages.

Strategy Principles:  
1. Set up a group of fast (21 periods), medium (55 periods), and slow (89 periods) three MA indicator lines representing average price levels at different time lengths;
2. Determine whether the current trend is in an upward or downward phase by judging the arrangement relationship of the three MA indicator lines (fast > medium > slow or fast < medium < slow);
3. Assist with judgments such as SuperTrend to increase signal accuracy;
4. Issue buy/sell signals based on changes in the status of these signals and filter indicators.

Advantages of the Strategy:
1. Use multiple MA combinations to judge long and short term market trends for more accurate judgments;
2. Adopt multiple filtering methods to optimize the selection of buying and selling points and increase profit probability;
3. Apply technical indicators such as Bollinger Bands and RSI to assist breakouts and grasp key support levels and reversal opportunities;  
4. Select the buying and selling direction according to the direction change of the fast MA without the need to be greedy for reversals, chase oscillating trends, and achieve profits;
5. Trading signals displayed clearly through visualizable arrows and markings, easy to grasp and convenient to operate.

Risks and Prevention:  
1. MA strategies have weaker resistance to false breakout probabilities;
2. There may be time differences between combined indicators, leading to lagging signal risks;  
3. After a break-in buy, further judgment of the strength of the subsequent market is needed to prevent being trapped;
4. Consider adding stop loss and take profit in live trading to control maximum loss per trade.

Strategy Optimization:  
1. Test different types and parameters of MA to find the optimal combination;
2. Enhance reversal judgment modules such as improving the use of the KD indicator;  
3. Incorporate trading volume indicators to determine true trends;  
4. Expand BIAS indicators to determine overbought and oversold areas.

Conclusion:  
In the ever-fluctuating cryptocurrency market, this strategy takes advantage of the opportunities during the ups and downs of market waves. By setting up the MA indicators and auxiliary filtering judgments for switching between long and short positions, it grasps the key reversal timing of the market. It can also be further optimized by adding stop loss modules to reduce single losses and obtain long-term positive returns through strategy automation.

---

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_string_1|0|Coloured MA Type: : HullMA|EMA|WMA|VWMA|SMMA|DEMA|TEMA|SMA|ZEMA|TMA|SSMA|
|v_input_int_1|18|Coloured MA - Length|
|v_input_1_close|0|Coloured MA - Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_string_2|0|Fast MA Type: : EMA|SMA|WMA|VWMA|SMMA|DEMA|TEMA|HullMA|ZEMA|TMA|SSMA|
|v_input_int_2|21|Fast MA - Length|
|v_input_string_3|0|Medium MA Type: : EMA|SMA|WMA|VWMA|SMMA|DEMA|TEMA|HullMA|ZEMA|TMA|SSMA|
|v_input_int_3|55|Medium MA - Length|
|v_input_string_4|0|Slow MA Type: : EMA|SMA|WMA|VWMA|SMMA|DEMA|TEMA|HullMA|ZEMA|TMA|SSMA|
|v_input_int_4|89|Slow MA Length|
|v_input_2_close|0|3xMA and Bollinger Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_string_5|0|Signal Filter Option : : SuperTrend|3xMATrend|SuperTrend+3xMA|ColouredMA|No Alerts|MACross|MACross+ST|MACross+3xMA|OutsideIn:MACross|OutsideIn:MACross+ST|OutsideIn:MACross+3xMA|
|v_input_3|false|hideMALines|
|v_input_4|true|hideSuperTrend|
|v_input_5|true|hideBollingerBands|
|v_input_6|true|hideTrendDirection|
|v_input_7|false|disableFastMAFilter|
|v_input_8|false|disableMediumMAFilter|
|v_input_9|false|disableSlowMAFilter|
|v_input_int_5|20|Bollinger Bands Length|
|v_input_float_1|2|Bollinger Bands StdDevs|
|v_input_10|8|Bollinger Outside In LookBack|
|v_input_float_2|3.