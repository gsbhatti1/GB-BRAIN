> Name

Three-EMA-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/b940064ababd737a51.png)
[trans]

## Overview

The Three-EMA-Trend-Following-Strategy uses the calculation of EMA moving averages with different periods to determine price trend direction and follows the trend. This strategy is simple to implement, particularly effective in trending instruments.

## Strategy Principle

This strategy calculates three EMAs with specific periods: 10-period, 20-period, and 30-period EMA. The code uses the `ema` function to compute these three EMAs.

The core logic involves judging the direction consistency of the three EMAs. If all three EMAs are rising together, a long signal is generated; if all three are falling together, a short signal is generated.

For specific long and short signals, if `ema1`, `ema2`, and `ema3` rose in the last bar, `enter_long` becomes true, generating a long signal. If they fell in the last bar, `enter_short` becomes true, generating a short signal.

Based on these signals, the strategy opens corresponding long and short positions. The exit logic is opposite to the entry signals: if `ema1`, `ema2`, and `ema3` do not rise together in the current bar, `exit_long` becomes true, closing the long position; if they do not fall together in the current bar, `exit_short` becomes true, closing the short position.

By judging the direction consistency of these three EMAs, overall price trend can be determined and followed.

## Strategy Advantages

- Using three EMA lines allows for more accurate judgment of trend direction. Compared to a single line, using three EMAs results in fewer incorrect signals.
- EMA is more sensitive to price changes, enabling timely reflection of trend reversals compared to SMA and other moving averages.
- Combining different period EMAs helps balance short-term and mid-to-long-term trends: 10-period for short-term, 20-period and 30-period for mid-to-long term.
- The strategy logic is simple and easy to understand, suitable for beginners. It also offers significant parameter adjustment space for various instruments.
- The strategy operates solely on EMA lines, requiring fewer resources and being suitable for high-concurrency scenarios.

## Strategy Risks

- Consistency in the direction of three EMAs is a necessary but not sufficient condition for trend judgment. Incorrect signals can occur during false breakouts.
- Lagging of EMAs in trend reversals means they cannot timely reflect turning points, potentially leading to losses.
- The sensitivity of EMA to price changes results in frequent opening and closing of positions, increasing transaction costs.
- In highly volatile markets where EMA lines fluctuate frequently, the strategy may not perform well.
- Increasing the period difference between three EMAs can reduce incorrect signals. Alternatively, adding other indicators can help filter false breakouts.

- Incorporating momentum indicators to confirm real trends and identify turning points can reduce losses. Loosening stop-loss levels could also be considered.
- Extending EMA periods reduces position opening and closing frequency. Alternatively, using other MA indicators might be more appropriate.
- Suspending the strategy in a range-bound market avoids unnecessary trades.

## Optimization Directions

- Period Tuning: Adjust the three EMA period parameters to adapt to different instruments' characteristics.
- Add Filters: Integrate MA, BOLL, etc., to avoid false breakouts of EMAs.
- Stop Loss Strategy: Implement trailing stop-loss mechanisms to protect profits.
- Risk Management: Optimize position sizing to limit the impact of single losses on overall performance.
- Market Regime Judgement: Use volatility indicators to gauge market oscillation and control strategy engagement.
- Adaptive Parameters: Automatically optimize EMA period parameters based on market changes for improved robustness.

## Summary

The Three-EMA-Trend-Following-Strategy uses EMA line directions to identify price trends, enabling automatic tracking of trends for trading. This strategy is simple and practical with significant parameter adjustment potential, allowing for optimization according to the characteristics of different instruments. However, it also carries certain risks such as false breakouts and range-bound market impacts. With continuous optimizations, this strategy can become a robust trend-following solution.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|10|EMA1 Period|
|v_input_2|20|EMA2 Period|
|v_input_3|30|EMA3 Period|
|v_input_4|false|Long Only|
|v_input_5|5|Stop-loss (%)|
|v_input_6|false|Use Stop-Loss|


> Source (PineScript)

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
```