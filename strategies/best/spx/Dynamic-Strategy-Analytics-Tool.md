> Name

Dynamic Strategy Analytics Tool

> Author

ChaoZhang

> Strategy Description

[trans]

## Overview

The main idea of this strategy is to simulate real-time trading, collect weekly trading data, and present the statistics in a table for more intuitive review of the strategy's performance. It can help us quickly evaluate the profit and loss of the strategy, identify periods of poor performance, and optimize the strategy accordingly.

## Strategy Logic

1. Set the start and end time for the calculation period.
2. Set the precision of statistics and the number of weeks in each group.
3. Simulate RSI strategy for entries and exits.
4. Define variables for the statistics table.
5. Calculate the result for the current period.
6. If the period changes and trading is enabled, record the time and result for this period.
7. If it's the last bar and trading is enabled, record the time and result for the current period.
8. If the period changes and trading is disabled, record the time and result for the previous period.
9. Find the highest and lowest period results.
10. Render the statistics table.

- First calculate the total number of statistical periods
- Iterate through each period, render headers, time, and results
- Cumulatively calculate the result for each group
- Color code positive and negative results

## Advantage Analysis

- Can observe weekly results in real time for quick strategy evaluation
- Intuitive presentation of results for clear insights
- Helps identify periods of poor performance for strategy adjustment
- Convenient to track cumulative gains for long-term strategies
- Can compare trading styles across different time periods
- Customizable precision and groups to meet different needs
- Simple and clear code, easy to understand and extend

## Risk Analysis

- The strategy is based on RSI, which has inherent trend following limitations
- Trading costs can significantly impact actual results
- Backtest data may not reflect actual market conditions
- Default capital in backtest may not match real account size
- Avoid overfitting by blindly tuning parameters based on statistics

Can incorporate more indicators for trend and optimize entries and exits to improve basic RSI strategy. Use actual trading costs in live trading. Add randomness to capital size in backtest. Maintain skepticism instead of over-tuning based on statistics.

## Optimization Directions

- Consider adding stop loss to limit downside
- Optimize RSI parameters like overbought and oversold levels
- Try different trading frequencies, such as intraday or monthly holding
- Incorporate more indicators for trend and timing
- Add profit taking logic
- Optimize statistical parameter settings
- Expand to track multiple assets

Stops can better manage risk/reward. RSI tuning improves win rate. More indicators and frequencies make strategy robust. Statistical tuning highlights important data. Expanding to multiple assets gives a complete view.

## Summary

The goal is to collect periodic results for intuitive statistical visualization to quickly judge performance across time. This provides data to optimize strategies. Strengths include real-time weekly results, clarity, and extensibility. Be wary of over-reliance and curve-fitting with statistical outputs. Use rationally along with core strategy logic for insights, not as basis for changes. Overall, it is a convenient way to assess performance and crucial for optimization.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|timestamp(01 Jan 2019 00:00 UTC)|Trade after|
|v_input_2|timestamp(31 Dec 2024 23:59 UTC)|Trade before|
|v_input_int_1|true|(?Statistic visualisation)Statistic precision|
|v_input_int_2|12|Statistic group size|


> Source (PineScript)

``` pinescript
//@version=5
// strategy('Strategy weekly results as numbers v1', overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=25, commission_type=strategy.commission.percent, commission_value=0.04)

after = input(title='Trade after', defval=timestamp('01 Jan 2019 00:00 UTC'), tooltip="Strategy will be executed after this timestamp. The statistic table will include only periods after this date.")
before = input(title='Trade before', defval=timestamp('31 Dec 2024 23:59 UTC'), tooltip="Strategy will be executes before this timestamp. The statistic table will include only periods before this date.")

statisti