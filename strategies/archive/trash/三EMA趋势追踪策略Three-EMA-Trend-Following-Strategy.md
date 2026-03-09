> Name

Three-EMA-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/b940064ababd737a51.png)
[trans]

## Overview

The Three-EMA-Trend-Following-Strategy uses the calculation of EMA lines with different periods to determine the price trend direction and follows the trend. This strategy is simple and easy to implement, and it performs well in instruments with clear trends.

## Strategy Principle

The strategy calculates three EMA lines with specific periods: 10, 20, and 30. The `ema` function in the code generates these EMA lines.

The main logic is to judge the direction consistency of the three EMA lines. If all three EMA lines are rising, a long signal is generated. If all three EMA lines are falling, a short signal is generated.

For long and short signals, if `ema1`, `ema2`, and `ema3` all rose in the last bar, `enter_long` becomes true, and a long signal is generated. If `ema1`, `ema2`, and `ema3` all fell in the last bar, `enter_short` becomes true, and a short signal is generated.

Based on the long and short signals, the strategy will open corresponding long and short positions. The exit logic is the opposite of the entry signals. If `ema1`, `ema2`, and `ema3` do not rise together in the current bar, `exit_long` becomes true, and the long position will be closed. If `ema1`, `ema2`, and `ema3` do not fall together in the current bar, `exit_short` becomes true, and the short position will be closed.

By judging the direction consistency of the three EMA lines, the overall trend can be determined, allowing for trend following.

## Strategy Advantages

- Using three EMA lines can more accurately judge the trend direction compared to a single line. The probability of false signals is lower.

- EMA is more sensitive to price changes and can reflect trend reversals in time. It is more suitable for trend judgment compared to SMA and other MA lines.

- Combining different period EMA lines can balance short-term and mid-to-long-term trends. The 10-period EMA is for short-term trends, while the 20 and 30-period EMAs are for mid-to-long-term trends.

- The strategy logic is simple and easy to understand, making it suitable for beginners. Also, the parameters have a large optimization space for different instruments.

- The strategy is based solely on EMA lines, requiring fewer resources and suitable for high concurrency.

## Strategy Risks

- The consistency of the direction of the three EMA lines is a necessary but not sufficient condition for trend judgment. False signals may occur during EMA line false breakouts.

- EMA lines lag in trend reversals and cannot reflect turning points in time, which may lead to losses.

- EMA is sensitive to price changes, and frequent long-short position flips may increase transaction costs.

- The strategy performs poorly in volatile markets where the EMA lines fluctuate frequently.

- The period difference of the three EMA lines can be optimized to reduce false signals. Alternatively, other indicators can be added to filter false breakouts.

- Momentum indicators can be added to confirm the real trend and identify turning points, reducing losses. Also, the stop loss point can be loosened.

- The period of the EMA lines can be increased to reduce the frequency of position flips. Alternatively, other MA indicators can be used.

- The strategy should be suspended when a range market is identified to avoid unnecessary trades.

## Optimization Directions

- Period Tuning: Adjust the EMA periods to adapt to different instruments.

- Add Filters: Add MA, BOLL, etc. to avoid EMA false breakouts.

- Stop Loss: Use trailing stop to lock profits.

- Risk Management: Optimize position sizing to limit single loss impact.

- Market Regime: Use volatility indicators to gauge oscillation and control strategy engagement.

- Adaptive Parameters: Automatically optimize EMA periods based on market changes to improve robustness.

## Conclusion

The Three-EMA-Trend-Following-Strategy trades by identifying the trend direction via EMA lines. It is simple and practical with a large optimization space. Risks such as false breakouts and oscillations should be noted. With continuous optimizations, this strategy can become a robust trend following solution.

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
/*backtest
start: 2023-10-10 00:00:00
end: 2023-11-09 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
```