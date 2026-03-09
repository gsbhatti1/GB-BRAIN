> Name

Threefold-Overlapping-SuperTrend-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/17997fae09a4a0064ba.png)
[trans]
## Overview
This is a trading strategy that utilizes three overlapping SuperTrend indicators to make trading decisions. It can capture larger directional opportunities in trending markets.

## Strategy Logic
The strategy uses the `ta.supertrend()` function to calculate three SuperTrend indicators with different parameter settings, namely:

- **SuperTrend1**: 10-day period and a multiplier of 3.
- **SuperTrend2**: 14-day period and a multiplier of 2.
- **SuperTrend3**: 20-day period and a multiplier of 2.5.

A buy signal is generated when the price crosses above all three SuperTrend lines. A sell signal is generated when the price crosses below all three SuperTrend lines.

The SuperTrend indicator combines with the ATR (Average True Range) to effectively track price trend changes. The strategy of three overlapping SuperTrends makes signals more reliable, thereby capturing greater profits in trending markets.

## Advantages
1. **Triple Filter Mechanism**: Avoids false signals and improves signal quality.
2. **Built-in Noise Reduction**: The SuperTrend itself has good noise reduction capabilities.
3. **Flexible Hyperparameter Configuration**: Multiple combinations of hyperparameters can be set to suit different market environments.
4. **Good Historical Performance**: High return-to-risk ratio.

## Risks
1. **Multiple Filter Signals May Miss Opportunities**: Missing some trades due to multiple filtering.
2. **Poor Performance in Ranging Markets**: Not effective during consolidation phases.
3. **Need for Hyperparameter Optimization**: Requires fine-tuning of three sets of hyperparameters.
4. **Risk from Concentrated Trading Time**: Susceptible to sudden events.

To mitigate these risks, consider:
1. Adjusting filter conditions by keeping one or two SuperTrends.
2. Adding a stop loss strategy.
3. Optimizing hyperparameters to improve win rate.

## Optimization Directions
1. Test more parameter combinations to find the optimal set of hyperparameters.
2. Incorporate machine learning algorithms for real-time parameter optimization.
3. Add stop loss strategies to control single trade losses.
4. Integrate other indicators to identify trends and ranges.
5. Extend trading time periods to avoid risks at specific times.

## Conclusion
This strategy makes decisions based on three overlapping SuperTrends, which can effectively identify trend direction. It has advantages such as high signal quality and flexible parameter configurations. However, it also comes with certain risks that require adjustment of parameters and exit timing to adapt to different market environments. Overall, the strategy performs exceptionally well and is worth further research and application.

||

## Overview
This is a trading strategy that utilizes three overlapping SuperTrend indicators to make trading decisions. It can capture larger directional opportunities in trending markets.

## Strategy Logic
The strategy uses the `ta.supertrend()` function to calculate three SuperTrend indicators with different parameter settings, namely:

- **SuperTrend1**: 10-day period and a multiplier of 3.
- **SuperTrend2**: 14-day period and a multiplier of 2.
- **SuperTrend3**: 20-day period and a multiplier of 2.5.

A buy signal is generated when the price crosses above all three SuperTrend lines. A sell signal is generated when the price crosses below all three SuperTrend lines.

The SuperTrend indicator combines with the ATR (Average True Range) to effectively track price trend changes. The strategy of three overlapping SuperTrends makes signals more reliable, thereby capturing greater profits in trending markets.

## Advantages
1. **Triple Filter Mechanism**: Avoids false signals and improves signal quality.
2. **Built-in Noise Reduction**: The SuperTrend itself has good noise reduction capabilities.
3. **Flexible Hyperparameter Configuration**: Multiple combinations of hyperparameters can be set to suit different market environments.
4. **Good Historical Performance**: High return-to-risk ratio.

## Risks
1. **Multiple Filter Signals May Miss Opportunities**: Missing some trades due to multiple filtering.
2. **Poor Performance in Ranging Markets**: Not effective during consolidation phases.
3. **Need for Hyperparameter Optimization**: Requires fine-tuning of three sets of hyperparameters.
4. **Risk from Concentrated Trading Time**: Susceptible to sudden events.

To mitigate these risks, consider:
1. Adjusting filter conditions by keeping one or two SuperTrends.
2. Adding a stop loss strategy.
3. Optimizing hyperparameters to improve win rate.

## Optimization Directions
1. Test more parameter combinations to find the optimal set of hyperparameters.
2. Incorporate machine learning algorithms for real-time parameter optimization.
3. Add stop loss strategies to control single trade losses.
4. Integrate other indicators to identify trends and ranges.
5. Extend trading time periods to avoid risks at specific times.

## Conclusion
This strategy makes decisions based on three overlapping SuperTrends, which can effectively identify trend direction. It has advantages such as high signal quality and flexible parameter configurations. However, it also comes with certain risks that require adjustment of parameters and exit timing to adapt to different market environments. Overall, the strategy performs exceptionally well and is worth further research and application.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|10|ATR Length 1|
|v_input_2|3|Factor 1|
|v_input_3|14|ATR Length 2|
|v_input_4|2|Factor 2|
|v_input_5|20|ATR Length 3|
|v_input_6|2.5|Factor 3|


> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy('Combined Supertrend Strategy - Ajit Prasad', overlay=true)

// Function to calculate Supertrend
supertrendFunc(atrLength, factor) =>
    [supertrend, direction] = ta.supertrend(factor, atrLength)
    [supertrend, direction]

// Input parameters for the first Supertrend
atrPeriod1 = input(10, 'ATR Length 1')
factor1 = input(3, 'Factor 1')

// Calculate the first Supertrend
[supertrend1, direction1] = supertrendFunc(atrPeriod1, factor1)

// Input parameters for the second Supertrend
atrPeriod2 = input(14, 'ATR Length 2')
factor2 = input(2, 'Factor 2')

// Calculate the second Supertrend
[supertrend2, direction2] = supertrendFunc(atrPeriod2, factor2)

// Input parameters for the third Supertrend
atrPeriod3 = input(20, 'ATR Length 3')
factor3 = input(2.5, 'Factor 3')

// Calculate the third Supertrend
[supertrend3, direction3] = supertrendFunc(atrPeriod3, factor3)

// Define market opening and closing times
marketOpenHour = 9
marketOpenMinute = 15
marketCloseHour = 15
marketCloseMinute = 30
exitTimeHour = 15
exitTimeMinute = 10

// Fetch historical close values using security function
histClose = request.security(syminfo.tickerid, "D", close)

// Buy condition
buyCondition = close > supertrend1 and close > supertrend2 and close > supertrend3 and close[1] <= supertrend1[1]

// Sell condition
sellCondition = close < supertrend1 and close < supertrend2 and close < supertrend3 and close[1] >= supertrend1[1]

// Exit conditions
buyExitCondition = close < supertrend1[1] or close < supertrend2[1] or close < supertrend3[1]
sellExitCondition = close > supertrend1[1] or close > supertrend2[1] or close > supertrend3[1]

// Execute orders with market timing
if true
    // Buy condition without 'and not'
    strategy.entry('Buy', strategy.long, when = buyCondition)

    // Sell condition without 'and not'
    strategy.entry('Sell', strategy.short, when = sellCondition)

    // Close conditions
    strategy.close('Buy', when = buyExitCondition)
    strategy.close('Sell', when = sellExitCondition)
```