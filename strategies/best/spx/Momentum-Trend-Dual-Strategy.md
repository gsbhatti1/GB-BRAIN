> Name

Momentum-Trend-Dual-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/874d90cb2e7e47c812.png)
 [trans]
## Overview

This strategy combines the Relative Strength Index (RSI) and Bollinger Bands indicators to implement a dual confirmation logic for entries and exits. It generates trading signals only when both RSI and Bollinger Bands show overbought or oversold signals at the same time. This can effectively reduce false signals and improve the stability of the strategy.

## Strategy Logic

1. **RSI Judgment Logic**
   - RSI crossing above 45 is considered an oversold signal.
   - RSI crossing below 55 is considered an overbought signal.
2. **Bollinger Bands Judgment Logic**
   - Price crossing above Bollinger Lower Band is considered oversold.
   - Price crossing below Bollinger Upper Band is considered overbought.
3. **Dual Confirmation Logic**
   - A long position is opened only when both RSI and Bollinger Bands show an oversold signal.
   - A short position is opened only when both RSI and Bollinger Bands show an overbought signal.

The above logic implements a stable dual confirmation strategy for entries and exits.

## Advantage Analysis

1. The dual confirmation mechanism can filter out many noise trades, avoid unnecessary trades, reduce trading costs, and improve profitability.
2. RSI is effective in identifying trends and reversals. Bollinger Bands are effective in judging supports and resistances. The two indicators complement each other perfectly.
3. Flexible parameter settings allow adjustment based on different products and trading preferences, making the strategy highly adaptable.

## Risk Analysis

1. In ranging markets, RSI and Bollinger Bands may give out wrong signals at the same time, causing unnecessary losses. Optimizing parameters can reduce misjudgment probabilities.
2. The dual confirmation mechanism slightly increases entry delay, possibly missing very short-term trading opportunities. This strategy is not suitable for those highly sensitive to delays.
3. The strategy is highly sensitive to parameter settings. Inappropriate parameter settings may significantly decrease profitability. Sufficient backtesting and review are needed to find the optimal combination.

## Optimization Directions

1. Test RSI indicators with different periods to find the best matching period parameter to improve efficiency.
2. Add stop loss logic, setting reasonable moving or fixed stop losses to control single trade risk.
3. Test Bollinger bandwidth parameters to optimize channel ranges and enhance recognition accuracy.
4. Test different price inputs such as close, high, low, etc., to identify the most stable input for the strategy.

## Summary

The strategy successfully combines RSI and Bollinger Bands indicators with a dual confirmation logic, ensuring sufficient trading opportunities while effectively reducing noise trades. With proper parameter optimization and risk control, it can become a very stable and reliable trend tracking and trading strategy.
[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|16|RSI Period Length|
|v_input_2|45|RSI Value Range|
|v_input_3|20|Bollinger Bands SMA Period Length|
|v_input_4|2|Bollinger Bands Standard Deviation|
|v_input_5|true|Enable Bar Color?|
|v_input_6|true|Enable Background Color?|


> Source (PineScript)

```pinescript
//@version=2
strategy("Momentum-Trend-Dual-Strategy", shorttitle="MTDS", overlay=true)

// RSI and Bollinger Bands, Dual Strategy by ChartArt
//
// Version 1.0
// Idea by ChartArt on January 14, 2015.
//
// This strategy uses a modified RSI to sell when the RSI increases over the value of 55 or to buy when the value falls below 45,
// with the classic Bollinger Bands strategy to sell when the price is above the upper Bollinger Band and to buy when this value is below the lower band.
//
// This simple strategy only triggers when both RSI and Bollinger Bands indicators are at the same time in an overbought or oversold condition.
//
// List of my work:
// https://www.tradingview.com/u/ChartArt/
//


///////////// RSI
RSIlength = input(16, title="RSI Period Length")
RSIvalue = input(45, title="RSI Value Range")
RSIoverSold = 0 + RSIvalue
RSIoverBought = 100 - RSIvalue
price = close
vrsi = rsi(price, RSIlength)

///////////// Bollinger Bands
BBlength = input(20, minval=1, title="Bollinger Bands SMA Period Length")
BBmult = input(2.0, minval=0.001, maxval=50, title="Bollinger Bands Standard Deviation")
BBbasis = sma(price, BBlength)
BBdev = BBmult * stdev(price, BBlength)
BBupper = BBbasis + BBdev
BBlower = BBbasis - BBdev

// Entry and Exit Logic
longCondition = vrsi < RSIoverSold and price > BBlower
shortCondition = vrsi > RSIoverBought and price < BBupper

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

// Plotting
plot(vrsi, color=color.blue, title="RSI")
hline(RSIoverSold, "OverSold Level", color=color.red)
hline(RSIoverBought, "OverBought Level", color=color.green)

plot(BBlower, color=color.orange, title="Bollinger Lower Band")
plot(BBupper, color=color.orange, title="Bollinger Upper Band")

// Optional: Enable bar and background colors
if (v_input_5)
    bgcolor(color.new(color.blue, 90), transp=true)
else
    bgcolor(none)

if (v_input_6)
    barcolor(vrsi < RSIoverSold ? color.green : vrsi > RSIoverBought ? color.red : color.gray)
```