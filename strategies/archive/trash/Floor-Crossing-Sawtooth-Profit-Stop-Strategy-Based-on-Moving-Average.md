> Name

Floor-Crossing-Sawtooth-Profit-Stop-Strategy-Based-on-Moving-Average

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16550a719cc025b8aed.png)
[trans]

## Overview

This strategy opens positions based on the golden cross and death cross of moving averages, and sets take profit and stop loss in a floor-crossing manner. Its main features are:

1. Use moving average system to filter shock markets.
2. Adopt moving take profit and stop loss for dynamic capital management.
3. Configurable position filtering to avoid one-way opening.

## Strategy Principle

The strategy consists of four parts:

1. Moving Average System

   Use golden cross and death cross of moving averages to determine trends and filter shock markets.

2. Moving Take Profit and Stop Loss

   Use take profit and stop loss with a certain percentage to lock in profits and control risks, realizing dynamic capital management.

3. Position Filtering

   Can configure whether to enable position filtering. If the previous position is long, the next signal must be short to open position, avoiding unilateral holding.

4. ATR Stop Loss

   Use ATR to limit the maximum range of stop loss and avoid excessive stop loss.

Specifically, the strategy first calculates the moving average, longs on golden cross, and shorts on death cross. After entry, set the moving take profit and stop loss lines with a certain percentage. If price touches the take profit line, then take profit; if touches the stop loss line or exceeds the ATR stop loss range, then stop loss.

## Advantages

The main advantages of this strategy are:

1. High Configurability

   Many parameters in the strategy are configurable for users to adjust based on their trading styles.

2. Good Capital Management

   The adoption of moving take profit and stop loss and ATR stop loss can effectively control the amplitude of a single stop loss and achieve excellent capital management.

3. Suitable for Trending Market

   The moving average strategy itself is more suitable for strong trending markets to filter shock markets effectively.

## Risks and Countermeasures

There are also some risks in this strategy:

1. Trend Misjudgement

   The judgment of moving averages on complex markets is not perfect, and misjudgements may occur. At this time, moving average parameters should be adjusted accordingly, or other indicators can be combined to judge trends.

2. Excessive Stop Loss

   Moving stop loss may be negated in shocks. ATR parameters should be combined to set the stop loss range.

3. One-way Opening Risks

   Enabling position filtering will have some impact on trading frequency. Prolonged one-way holding may bring additional risks.

## Optimization Directions

The main optimization directions are:

1. Parameter Optimization

   Adjust the moving average cycle, ATR parameters, take profit and stop loss ratios and other parameters to optimize strategy performance.

2. Adding Indicators

   Add indicators like CMF, OBV to judge capital flow and avoid excessive stop loss.

3. Combining with Other Strategies

   Combine with breakout strategies to follow trends after the trend stabilizes to achieve better results.

## Summary

In summary, through the moving average filter and moving take profit and stop loss, this strategy realizes dynamic capital management based on trends. It has high configurability, suitable for rational investors to adjust and use according to their own styles. As a universal quantitative strategy, it still has great potential for optimization and is worth in-depth research.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_int_1|52|Leading Period|
|v_input_int_2|true|Displacement|
|v_input_bool_1|true|Apply Position Order Filter|
|v_input_float_1|true|Stop Loss %|
|v_input_float_2|2|Take Profit %|
|v_input_float_3|0.3|ATR Factor|
|v_input_float_4|0.01|ATR Upper Limit|
|v_input_float_5|0.06|ATR Lower Limit|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-20 00:00:00
end: 2023-12-11 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © MGULHANN

//@version=5

// Ichimoku Leading Span 2 Calculation and Entries
strategy("Stairs Gain Strategy - MG", overlay=true, margin_long=100, margin_short=100)
laggingSpan2Periods = input.int(52, minval=1, title="Leading Period")
displacement = input.int(1, minval=1, title="Displacement")
donchian(len) => math.avg(ta.lowest(len), ta.highest(len))
leadLine2 = donchian(laggingSpan2Periods)
p2 = plot(leadLine2, offset = displacement - 1, color=#EF9A9A, title="Leading Span B")

// Filter Repeated Operations
filtreUygula = input.bool(true, title="Apply Position Order Filter")
```