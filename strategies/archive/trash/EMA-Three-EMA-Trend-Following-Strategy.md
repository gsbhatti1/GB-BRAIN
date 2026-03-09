> Name

Three-EMA-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/b940064ababd737a51.png)
[trans]

## Overview

The Three-EMA Trend Following Strategy tracks price trends by calculating different period EMAs and following the trend. This strategy is simple to implement and performs well in clearly trending instruments.

## Strategy Logic

This strategy calculates three EMA lines with specific periods: 10-period, 20-period, and 30-period EMA. The `ema` function in the code generates these three EMAs.

The main logic involves judging the direction of the three EMA lines. If all three EMAs are rising together, a long signal is generated; if they are falling together, a short signal is generated.

Specifically, if `ema1`, `ema2`, and `ema3` were all increasing in the previous bar, `enter_long` becomes true and generates a long signal. Conversely, if they were all decreasing in the previous bar, `enter_short` becomes true and generates a short signal.

Based on these signals, the strategy opens corresponding long or short positions. The exit logic is opposite to entry signals: If `ema1`, `ema2`, and `ema3` are not rising together in the current bar, `exit_long` becomes true, closing the long position; if they are not falling together, `exit_short` becomes true, closing the short position.

By judging the direction consistency of these three EMA lines, one can determine the overall trend and follow it automatically.

## Advantages

- Using three EMAs allows for more accurate trend direction determination compared to a single EMA. The probability of false signals is lower.
- EMA reacts more sensitively to price changes and reflects trend reversals quickly. It is more suitable for trend judgment than SMA or other MA indicators.
- Combining different period EMAs accommodates both short-term and mid-to-long-term trends: 10-period EMA for short-term, while 20-period and 30-period EMAs track mid-to-long term trends.
- The strategy logic is simple and easy to understand, making it suitable for beginners. It also has a large parameter optimization space for different instruments.
- The strategy relies solely on EMAs, requiring fewer resources and being suitable for high concurrency.

## Risks

- EMA direction consistency alone is necessary but not sufficient for trend judgment. False signals can occur during false breakouts of EMA lines.
- EMA lags in reflecting trend reversals, which may delay the identification of turning points and result in losses.
- Frequent long-short position switching due to sensitivity to price changes increases transaction costs.
- The strategy is less effective in volatile markets where EMAs frequently change direction.

## Optimization

- Period Tuning: Adjust EMA periods to better fit different instrument characteristics.
- Add Filters: Incorporate additional indicators like MA or BOLL to filter out false breakouts.
- Stop Loss Strategy: Implement trailing stop loss to protect profits.
- Risk Management: Optimize position sizing to limit the impact of single trades on overall risk.
- Market Regime Identification: Use volatility metrics to determine market conditions and adjust strategy engagement accordingly.
- Adaptive Parameters: Allow EMA periods to adapt automatically based on market changes to enhance robustness.

## Conclusion

The Three-EMA Trend Following Strategy identifies trends by analyzing the direction of EMAs and follows them accordingly. It is simple, practical, and has a large scope for optimization tailored to specific instrument characteristics. However, risks such as false breakouts and volatility need careful management. Continuous optimization can make this strategy more robust and reliable.

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