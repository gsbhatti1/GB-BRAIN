> Name

Dynamic-Breakout-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1b0ff308dfa19dfa989.png)
[trans]

## Overview

This is a trend following breakout strategy based on dynamically calculated price levels. It tracks the stock's highest and lowest prices in real time. When the price breaks through the highest level of the recent period, it will go long; when the price breaks below the lowest level of the recent period, it will go short. The strategy also sets stop loss and take profit to control risks and ensure a fixed risk-reward ratio.

## Strategy Logic

The core logic of this strategy is to track and trade price breakout points of trends. Specifically, the strategy calculates the highest high (`highestHigh`) and lowest low (`lowestLow`) over the last 20 days. When today's closing price exceeds yesterday's `highestHigh`, it indicates an upward trend breakout signal and will go long; when today's closing price falls below yesterday's `lowestLow`, it suggests a downward trend breakout signal and will go short.

After going long or short, stop loss of 1% and take profit of 2% are set. This ensures a fixed risk-reward ratio of 2:1 for each trade, effectively controlling the risk of single trades.

## Advantages

The biggest advantage of this strategy is quickly capturing reversal points of price trends while controlling risks in each single trade. Main advantages include:

1. Dynamic calculation of highest and lowest prices, real-time tracking of price trend changes, which can quickly capture price reversal signals.
2. Using breakout methods for entries improves the quality of entries.
3. Setting stop loss and take profit to control risk-reward ratio effectively manages trade risks.
4. Simple and easy-to-understand logic, suitable for quant beginners.
5. Less code, making it easier for testing and optimization.

## Risks

There are also some risks associated with this strategy:

1. Following trends for entries may miss the best turning points of price reversals.
2. Fixed stop loss and take profit settings cannot adapt to market changes, which might lead to premature stops or profits.
3. No pyramiding logic for later additional entries, unable to keep following trends.
4. No consideration of big cycles, possibly conflicting with major trends leading to losses.
5. Lack of a position sizing module, no control over overall position management.

## Optimization Directions

There is still large room for optimization, mainly in the following directions:

1. Add dynamic stop loss and take profit settings based on market volatility.
2. Add trend direction filter based on moving averages to avoid conflicts with major trends.
3. Add trend strength indicators to ensure entries only when the trend is strong.
4. Add pyramiding logic to maximize profits by continuously following trends.
5. Combine with a position sizing module for dynamic adjustment of positions and risk control.

6. Optimize parameters to find the best parameter sets.

## Summary

Overall, this strategy is suitable for quant beginners to learn and practice. Its advantage lies in its simplicity and ease of understanding, also with stop loss and take profit logic to control risks. However, there are still many aspects that can be optimized, serving as a good opportunity for further learning. Generally speaking, this strategy is well-suited for beginners to master from the principles to application.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|20|Length|
|v_input_2|true|Stop Loss %|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-28 00:00:00
end: 2023-12-28 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Trend Following Breakout Strategy with 2:1 RRR", overlay=true)

// Define the calculation of previous high and low
length = input(20, minval=1, title="Length")
highestHigh = highest(high, length)
lowestLow = lowest(low, length)

// Define the conditions for buying and selling
longCondition = close > highestHigh[1] // Today's closing price is higher than yesterday's highestHigh
shortCondition = close < lowestLow[1]  // Today's closing price is lower than yesterday's lowestLow

// To ensure a risk-reward ratio of 2:1, we need to define stop loss and target prices
stopLoss = input(1, title="Stop Loss %") / 100
takeProfit = stopLoss * 2

// If the long condition is met, enter into a long position
if (longCondition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Long TP", "Long", profit=takeProfit * close, loss=stopLoss * close)

// If the short condition is met, enter into a short position
if (shortCondition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Short TP", "Short", profit=takeProfit * close, loss=stopLoss * close)

// Plot to display previous high and low
plot(highestHigh, color=color.green, title="Previous High")
plot(lowestLow, color=color.red, title="Previous Low")

```

> Detail

https://www.fmz.com/strategy/437048

> Last Modified

2023-12-29 17:32:10