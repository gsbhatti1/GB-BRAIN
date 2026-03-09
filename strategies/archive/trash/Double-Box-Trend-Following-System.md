> Strategy Name

Double-Box-Trend-Following-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1abc0fa4702b6eca3c3.png)

[trans]

## Overview

The Trend Following System is a trend tracking strategy based on a double box system. It uses a long-term box to determine the overall trend direction and takes signals that align with the major trend when the short-term box triggers. This strategy follows trends while managing risks.

## Strategy Logic

The strategy uses two boxes to determine the trend. The long-term box uses a longer period to judge the major trend direction, and the short-term box uses a shorter period to generate trading signals.

First, the strategy calculates the highest and lowest prices of the long-term box to determine the major trend direction. The trend direction can be:

- If the highest price crosses above the highest price of the previous bar, it is defined as an uptrend, assigned a value of 1
- If the lowest price crosses below the lowest price of the previous bar, it is defined as a downtrend, assigned a value of -1
- Otherwise, maintain the original trend direction

After determining the major trend, the strategy starts taking positions based on the short-term box signals. Specifically:

- When the major trend is up and the short-term box's lowest price equals the previous bar's lowest price and is lower than the current short-term box's lowest price, go long.
- When the major trend is down and the short-term box's highest price equals the previous bar's highest price and is higher than the current short-term box's highest price, go short.

In addition, stop loss and take profit are configured:

- Long stop loss is the lowest price of the long-term box, short stop loss is the highest price of the long-term box
- Long take profit is the highest price of the short-term box, short take profit is the lowest price of the short-term box

When the major trend reverses, close all positions.

## Advantage Analysis

The advantages of this strategy include:

1. The double box system effectively identifies trend directions and reduces incorrect trades.
2. Only taking reversal signals that align with the major trend avoids being misled by short-term market noise.
3. The combination of long and short periods ensures capturing major trends while maintaining position adjustment flexibility.
4. Reasonable stop loss and take profit points control risk while following trends.
5. Quickly flattening all positions when the major trend reverses minimizes losses.

## Risk Analysis

The risks of this strategy include:

1. Improper long and short period settings may cause overtrading or missing opportunities.
2. Short-term reversals may not represent long-term trend changes, still posing loss risks.
3. Stop loss too close may get stopped out prematurely.
4. Take profit too loose may not maximize profits.
5. Wrong judgment of the major trend leads to losses.
6. Solutions include adjusting periods, optimizing stops/targets, adding filters, etc.

## Optimization Directions

The strategy can be improved by:

1. Adding filters to avoid false breakouts.
2. Optimizing long and short periods for different products.
3. Dynamically adjusting stop loss and take profit levels.
4. Incorporating position sizing rules.
5. Using volume, etc., to judge the reliability of trend changes.
6. Utilizing machine learning to auto-optimize parameters and filters.

## Summary

The Trend Following System is a practical trend trading strategy combining trend determination and short-term adjustments. With continuous optimizations, it can become a robust automated system that tracks trends while controlling risks. It contains the core philosophies of trend trading and is worth in-depth studying.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|80|Longterm Period|
|v_input_2|21|Shortterm Period|
|v_input_3|true|Show Target|
|v_input_4|true|Show Trend|


> Source (PineScript)

```pinescript
//@version=4
strategy("Double-Box-Trend-Following-System", overlay = true)
flb = input(defval = 80, title = "Longterm Period", minval = 1)
slb = input(defval = 21, title = "Shortterm Period", minval = 1)
showtarget = input(defval = true, title = "Show Target")
showtrend = input(defval = true, title = "Show Trend")

major_resistance = highest(high, flb)
major_support = lowest(low, flb)
minor_resistance = highest(high, slb)
minor_support = lowest(low, slb)
```