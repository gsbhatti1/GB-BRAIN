> Name

Quantitative-Trading-Strategy-Based-on-Ichimoku-with-Multiple-Signals

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1d5d669b93c6f8669d7.png)
[trans]

### Overview

This strategy integrates Ichimoku Kinko Hyo indicators and multiple other technical indicators to combine various trading signals, in order to leverage the advantages of the Ichimoku system while confirming entries with multiple signals to effectively filter out false signals and control risks while pursuing high win rate.

### Strategy Logic

The key components of this strategy are:

1. Calculation of Ichimoku Kinko Hyo indicators, including Tenkan-sen, Kijun-sen, Senkou Span A, Senkou Span B, and Kumo.

2. Multiple filters, including Kumo cloud filter, Kijun baseline filter, MACD filter, RSI filter, Bill Williams ARGUMENTS fractals filter, SuperTrend filter, Parabolic SAR filter, and ADX filter. These filters are used to confirm trend direction and avoid trades affected by volatile markets.

3. Multiple trading signals, including price breakouts, Chikou span relationships with price or cloud, Tenkan-sen relationships with Kijun-sen or cloud, totaling 23 Ichimoku original trading signals. Additionally, various other technical indicator signals are included, such as MACD, RSI, Fractals, etc. These signals are used to identify potential trading opportunities.

4. Two-stage filters for entry signals to effectively filter out false signals. One filter is selected as the first stage and another as the second stage to avoid being trapped at entry.

5. Two-stage filters for exit signals. Similar to the entry filters.

6. Combination of selected trading signals and filter confirmations as final entry and exit signals. Based on the user's selected trading signals, combined with the first and second stage entry filters and exit filters, to form final trading decisions.

7. Take profit and stop loss settings. Options are provided to enable or disable and set specific take profit and stop loss levels.

8. Backtest period settings. Options to set the start and end time of the backtest period.

### Strategy Advantages

This strategy has the following advantages:

1. Combining the advantages of Ichimoku's multiple indicators and trading signals, balancing trend following and signal filtering.

2. Avoiding false signals at entry through two-stage filters and effective risk control.

3. Providing multiple trading signals to choose from, allowing for optimization based on different market conditions.

4. Offering multiple filter options to optimize based on individual stock characteristics.

5. Setting take profit and stop loss levels to help lock in profits and control risks.

6. Setting different backtest periods to validate the strategy, making it easier to optimize.

### Strategy Risks

This strategy also has some risks:

1. Ichimoku system may be slower in determining buy/sell signals, potentially missing short-term trading opportunities. Shorter periods can be adjusted.

2. Multiple filters may be overly cautious, leading to uncertain entries. Testing and adjusting filter parameters may be necessary.

3. A single stop loss level may not be flexible enough to handle complex market scenarios. Dynamic stop loss may be considered.

4. Backtest period settings may not precisely simulate live market conditions. Multiple iterations are needed for validation.

### Strategy Optimization Directions

This strategy can be optimized in the following ways:

1. Adjust Ichimoku system parameters, such as shortening the Tenkan-sen period to adapt to shorter-term trading.

2. Test different signal combinations to identify the best signals for individual stocks.

3. Optimize filter parameters to balance filtering effectiveness and entry certainty.

4. Try dynamic stop loss methods to better align with market changes.

5. Use longer backtest periods or tick data for more accurate simulations.

6. Add a position sizing module to optimize capital utilization.

7. Implement automatic parameter optimization for more intelligent adjustments.

### Conclusion

This strategy combines Ichimoku's indicators and signals with additional filters and confirmations from other technical indicators, realizing a quantitative system that fuses trend following and breakout signals. It fully leverages Ichimoku's strengths while using parameterized modules for adjustments and optimizations to adapt to changing markets. Continuous testing and optimization are expected to lead to high stability and profitability.

||

### Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Backtest (no comment-string)|
|v_input_2|0|Long/Short Entry: Both|Long|Short|
|v_input_3|false|Shared Filter and Entry Parameters :|
|v_input_4|2|Fractals Period (Filter/Entry)|
|v_input_5|14|RSI Period (Filter/Entry)|
|v_input_6|2|SuperTrend Multiplier (Filter/Entry)|
|v_input_7|5|SuperTrend Length (Filter/Entry)|
|v_input_8|10|ADX Period (Filter/Entry)|
|v_input_9|25|ADX Threshold (Filter/Entry)|
|v_input_10|0|Signal: Price X Kumo sig|Inside Bar sig|Outside Bar sig|Sandwich Bar sig|Bar sig|SMA50 sig|RSI50 sig|Fractals sig|Parabolic SAR sig|SuperTrend sig|Price X Kijun sig|---|Kumo flip sig|Price filtered Kumo flip sig|Chikou X Price sig|Chikou X Kumo sig|Price X Tenkan sig|Tenkan X Kumo sig|Tenkan X Kijun sig|Kumo filtered Tenkan X Kijun sig|CB/CS sig|IB/IS sig|B1/S1 sig|B2/S2 sig|
|v_input_11|0|Entry filt