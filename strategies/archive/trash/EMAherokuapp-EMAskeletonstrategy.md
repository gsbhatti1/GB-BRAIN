> Name

Dynamic EMA HerokuApp Overview Strategy EMA-skeleton-strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/8e1d42a028dbd88749.png)

---

## Overview

This strategy combines the EMA and RSI indicators to identify short-term adjustment opportunities in Bitcoin. It mainly uses the EMA as the main graphical tool and the RSI as an auxiliary judgment indicator, finding obvious adjustment patterns. Trading signals are generated when the price breaks below or climbs back above the EMA line. It also has stop loss and take profit controls that can be parameterized.

## Strategy Principle

The strategy mainly utilizes a 50-period EMA line and a 25-period RSI indicator. The EMA line is regarded as the main graphical indicator, while the RSI is used to determine overbought and oversold conditions and assist in generating trading signals. A sell signal is generated when the price falls below the EMA line, and a buy signal is generated when the price breaks above the EMA line and the RSI shows a non-overbought signal (RSI value less than 70). To reduce the chance of wrong entries, the strategy also incorporates a longer-period EMA line (such as 70 periods) as an additional filter condition.

After entering a trade, the strategy also sets stop loss and take profit levels. The stop loss distance is adjustable, defaulting to 5.1%; the take profit distance is also adjustable, defaulting to 9.6%. This effectively limits the maximum loss per trade.

In summary, the strategy mainly relies on EMA line patterns, supplemented by RSI indicators to avoid overbought and oversold conditions, while having stop loss and take profit controls. It is suitable for capturing short-term BT Bitcoin adjustments.

## Advantage Analysis

The main advantages of this strategy are:

1. The strategy signals are relatively clear without too many random wrong entries. The combination of EMA and RSI makes the signals more reliable rather than relying solely on a single indicator.
2. Built-in stop loss and take profit control. This effectively limits the loss per trade and is a very important risk control tool.
3. Strategy parameters can be optimized. EMA length, RSI length, and other parameters are adjustable, allowing users to find the optimal parameter sets for different market conditions.
4. Backtesting enabled. The strategy allows setting a backtest date range internally to verify performance.

## Risk Analysis

The strategy also has some risks, mainly from:

1. BT Bitcoin has volatile moves, stops may be run. Although stops are set, BTC often has large price swings that can take out stops leading to larger-than-expected losses.
2. Drawdown risk. The strategy does not consider overall drawdown control. It may experience drawdowns during prolonged adjustment periods.
3. Weaker signals in strong trends. BTC trends can become quite extended during certain market conditions, and the short-term signals tend to underperform, leading to being stopped out of good trades.

To control and mitigate these risks:

1. Allow wider stop loss ranges. During strong trending conditions, the stop loss range can be widened, such as to 10%, to avoid being stopped out prematurely.
2. Add other indicator filters. Trend-following indicators can be added to avoid taking trades during prolonged consolidation periods.
3. Optimize parameters. Test parameter sets across different market conditions and create multiple parameter templates to switch between in real-time based on current conditions.

## Optimization Directions

There is further room to optimize this strategy:

1. Add overall drawdown control. Could set a maximum drawdown percentage, such as 20%, that pauses trading when reached to limit losses.
2. Limit entry frequency. Can restrict the number of trades per unit time, such as 2 trades per hour max, to prevent over-trading.
3. Optimize parameters. Test parameter combinations for different market conditions and create multiple parameter templates to switch between in real-time based on current conditions.
4. Combine with other indicators. Integrate trend, volatility, and other metrics to create more comprehensive trading system entry rules.

## Summary

Overall, the strategy mainly relies on short-term BTC adjustment patterns, using EMA and RSI to generate clear trading signals while having stop loss and take profit controls. It can effectively capture short-term slippage opportunities but is better suited as a short-term auxiliary tool when combined with other strategies for more stable excess returns.

|