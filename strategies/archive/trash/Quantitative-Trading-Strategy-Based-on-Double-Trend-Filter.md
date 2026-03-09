```markdown
> Name

Quantitative-Trading-Strategy-Based-on-Double-Trend-Filter

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/4519923478ba5e7f04.png)
[trans]

## Overview

This is a quantitative trading strategy that utilizes double trend filters. The strategy combines both global and local trend filters to ensure entering positions only when the trend direction is correct. In addition, multiple other filters such as RSI filter, price filter, slope filter are set up to further enhance the reliability of trading signals. On the exit side, preset stop loss and take profit prices are established. Overall, this is a stable and precise quantitative trading strategy.

## Strategy Logic

The core logic of this strategy is based on the double trend filters. The global trend filter judges overall market trends using high-period EMA, while the local trend filter uses low-period EMA to judge local trends. Only when both filters suggest the same trend direction will the strategy enter positions.

Specifically, the strategy calculates BTCUSDT's EMA to determine if the overall market is in an upward or downward trend. This serves as the global trend filter. At the same time, the strategy calculates EMA of the underlying contract to judge local trends. This is the local trend filter. Only when both filters agree on the same trend direction and other auxiliary filters are satisfied, will the strategy generate trading signals and preset stop loss and take profit prices for entering positions.

Once a tradable signal is determined, the strategy immediately places orders to enter positions. Meanwhile, preset stop loss and take profit prices are set. When price touches either of them, the strategy automatically exits with stop loss or take profit.

## Advantage Analysis

This is a stable and reliable quantitative trading strategy with several key advantages:

1. **Double Trend Filtering Mechanism**: This mechanism effectively filters out most false signals, making trading signals more reliable.
2. **Multiple Auxiliary Filters**: Combining RSI filter, price filter, and slope filter further improves signal quality.
3. **Automatic Calculation of Stop Loss and Take Profit Prices**: This reduces the risk of manual monitoring and helps minimize trading risks.
4. **Customizable Strategy Parameters**: Allows for adaptation to various trading instruments with better flexibility.
5. **Clear Strategy Logic and Easy Optimization**: The strategy is straightforward, making it easier to optimize and expand.

## Risk Analysis

Despite its many advantages, this strategy still faces some risks:

1. **Inaccurate Entry Timing Determination**: Double trend filters may not always determine the correct entry timing precisely. Parameter adjustments can help improve this.
2. **Incorrect Stop Loss and Take Profit Price Settings**: Inaccurately set stop loss or take profit prices might result in premature exits. Different parameter combinations should be tested to find the optimal settings.
3. **Improper Selection of Trading Instruments and Timeframes**: Incorrect selection may render the strategy ineffective. Parameters should be optimized separately for different trading instruments.
4. **Overfitting Risk**: More backtests in diverse market environments are needed to ensure robustness.

## Optimization Directions

The main directions for optimizing this strategy include:

1. **Adjusting Double Filter Parameters**: Find the best parameter combination through adjustments.
2. **Testing and Selecting Optimal Auxiliary Filters**.
3. **Optimizing Stop Loss and Take Profit Algorithms**: Make these algorithms more intelligent.
4. **Introducing Machine Learning Models for Dynamic Parameter Tuning**.
5. **Conducting More Backtests on Different Instruments and Longer Time Spans to Enhance Stability**.

## Conclusion

Overall, this is a stable, precise, and easily optimizable quantitative trading strategy. By combining double trend filters with multiple auxiliary filters, it effectively filters out noise and generates more reliable signals. Additionally, the preset stop loss and take profit prices help reduce trading risks. This is a highly practical strategy that can be directly applied in live trading after optimization and validation. It also has significant potential for further expansion and is worth in-depth research.

||

## Overview

This is a quantitative trading strategy that utilizes double trend filters. The strategy combines both global and local trend filters to ensure entering positions only when the trend direction is correct. In addition, multiple other filters such as RSI filter, price filter, slope filter are set up to further enhance the reliability of trading signals. On the exit side, preset stop loss and take profit prices are established. Overall, this is a stable and precise quantitative trading strategy.

## Strategy Logic

The core logic of this strategy is based on the double trend filters. The global trend filter judges overall market trends using high-period EMA, while the local trend filter uses low-period EMA to judge local trends. Only when both filters suggest the same trend direction will the strategy enter positions.

Specifically, the strategy calculates BTCUSDT's EMA to determine if the overall market is in an upward or downward trend. This serves as the global trend filter. At the same time, the strategy calculates EMA of the underlying contract to judge local trends. This is the local trend filter. Only when both filters agree on the same trend direction and other auxiliary filters are satisfied, will the strategy generate trading signals and preset stop loss and take profit prices for entering positions.

Once a tradable signal is determined, the strategy immediately places orders to enter positions. Meanwhile, preset stop loss and take profit prices are set. When price touches either of them, the strategy automatically exits with stop loss or take profit.

## Advantage Analysis

This is a stable and reliable quantitative trading strategy with several key advantages:

1. **Double Trend Filtering Mechanism**: This mechanism effectively filters out most false signals, making trading signals more reliable.
2. **Multiple Auxiliary Filters**: Combining RSI filter, price filter, and slope filter further improves signal quality.
3. **Automatic Calculation of Stop Loss and Take Profit Prices**: This reduces the risk of manual monitoring and helps minimize trading risks.
4. **Customizable Strategy Parameters**: Allows for adaptation to various trading instruments with better flexibility.
5. **Clear Strategy Logic and Easy Optimization**: The strategy is straightforward, making it easier to optimize and expand.

## Risk Analysis

Despite its many advantages, this strategy still faces some risks:

1. **Inaccurate Entry Timing Determination**: Double trend filters may not always determine the correct entry timing precisely. Parameter adjustments can help improve this.
2. **Incorrect Stop Loss and Take Profit Price Settings**: Inaccurately set stop loss or take profit prices might result in premature exits. Different parameter combinations should be tested to find the optimal settings.
3. **Improper Selection of Trading Instruments and Timeframes**: Incorrect selection may render the strategy ineffective. Parameters should be optimized separately for different trading instruments.
4. **Overfitting Risk**: More backtests in diverse market environments are needed to ensure robustness.

## Optimization Directions

The main directions for optimizing this strategy include:

1. **Adjusting Double Filter Parameters**: Find the best parameter combination through adjustments.
2. **Testing and Selecting Optimal Auxiliary Filters**.
3. **Optimizing Stop Loss and Take Profit Algorithms**: Make these algorithms more intelligent.
4. **Introducing Machine Learning Models for Dynamic Parameter Tuning**.
5. **Conducting More Backtests on Different Instruments and Longer Time Spans to Enhance Stability**.

## Conclusion

Overall, this is a stable, precise, and easily optimizable quantitative trading strategy. By combining double trend filters with multiple auxiliary filters, it effectively filters out noise and generates more reliable signals. Additionally, the preset stop loss and take profit prices help reduce trading risks. This is a highly practical strategy that can be directly applied in live trading after optimization and validation. It also has significant potential for further expansion and is worth in-depth research.

---

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Show WaveTrend|
|v_input_2|true|Show Buy dots|
|v_input_3|true|Show Gold dots|
|v_input_4|true|Show Sell dots|
|v_input_5|true|Show Div. dots|
|v_input_6|true|Show Fast WT|
|v_input_7|9|WT Channel Length|
|v_input_8|12|WT Average Length|
|v_input_9_hlc3|0|WT MA Source: hlc3|high|low|open|hl2|close|hlcc4|ohlc4|
|v_input_10|3|WT MA Length|
|v_input_11|53|WT Overbought Level 1|
|v_input_12|60|WT Overbought Level 2|
```