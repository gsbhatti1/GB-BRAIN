> Name

Parameter-Optimized-Trend-Following-Quantitative-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/a800a2f343d0bc3580.png)
[trans]

## Overview

The main idea of this strategy is to combine the percentrank indicator and parameter optimization to judge and track price trends. The strategy generates trading signals by comparing the current price with the percentage of prices over a certain historical period, aiming to capture the intermediate mirror effect, follow trends, and thereby achieve excess returns.

## Strategy Principle

The strategy uses the percentrank indicator to determine price trends. Percentrank represents the relative strength of the current price within the viewed period. The parameter len indicates the length of the historical period to view.

The range of percentrank values is from 0 to 100. When the percentrank value approaches 0, it means the current price is close to the lowest price in the viewed period and is in an undervalued area; when it approaches 100, it indicates that the current price is near the highest price in the viewed period and is in an overvalued area.

The strategy also introduces a scale parameter as an offset. This shifts the 0 to 100 range to the scale to 100+scale range. Two signal lines level_1 and level_2 are set, where level_1 indicates the long level and level_2 indicates the short level.

When the price percentrank indicator crosses from below level_1 upwards, a long signal is generated; when it crosses level_2 downwards, a short signal is generated. The exit conditions are opposite of the entry signals.

## Advantages of the Strategy

1. Use the percentrank indicator to determine the strength of price trends, avoiding being trapped or chasing highs
2. Apply parameter optimization methods to adjust the offset scale and signal line thresholds for different products and cycles, improving stability
3. Combine trend following and mean reversion trading ideas, tracking trends in a timely manner after breaking through the signal lines

## Risk Analysis

1. Incorrect judgment of trends leading to unnecessary losses
2. Prone to generating wrong signals when price volatility and trends are unclear
3. Improper parameter settings may result in too frequent trading or insufficient trading volume

To address these risks, parameters like len, scale, level can be adjusted for optimization; additionally, other indicators can be incorporated as confirmation to avoid erroneous trades.

## Optimization Directions

The strategy still has room for further improvement:

1. Introduce stop loss points to reduce single trade loss
2. Incorporate indicators such as moving averages for confirmation, filtering out some wrong signals
3. Use machine learning methods to automatically optimize parameters
4. Run in parallel across multiple time frames

## Conclusion

The overall idea of the strategy is clear, employing quantitative methods of parameter optimization to judge and track price trends. It has practical value but still needs further testing and optimization to reduce risks and enhance stable profitability.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|10|lookback - Period of comparison|
|v_input_3|50|scale offset - Scale offset|
|v_input_4|30|sygnal line 1|
|v_input_5|-30|sygnal line 2|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-12-02 00:00:00
end: 2024-01-01 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Alex_Dyuk

//@version=4
strategy(title="percentrank", shorttitle="percentrank")
src = input(close, title="Source")
len = input(title="lookback - Period of comparison", type=input.integer, defval=10, minval=2)
scale = input(title="scale offset - Scale offset", type=input.integer, defval=50, minval=0, maxval=100)
level_1 = input(title="sygnal line 1", type=input.integer, defval=30)
level_2 = input(title="sygnal line 2", type=input.integer, defval=-30)

prank = percentrank(src, len) - scale
plot(prank, style=plot.style_columns)
plot(level_2, style=plot.style_line, color=color.red)
plot(level_1, style=plot.style_line, color=color.green)

longCondition = crossunder(level_1, prank) == true
if (longCondition)
    strategy.entry("Long", strategy.long)
longExitCondition = crossover(level_2, prank) == true
if (longExitCondition)
    strategy.close("Long")
    
shortCondition = crossover(level_2, prank) == true
if (shortCondition)
    strategy.entry("Short", strategy.short)
shortexitCondition = crossunder(level_1, prank) == true
if (shortexitCondition)
    strategy.close("Short")
```

> Detail

https://www.fmz.com/strategy/437383

> Last Modified

2024-01-02 11:0