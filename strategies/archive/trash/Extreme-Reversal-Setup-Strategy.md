---
> Name

Extreme Reversal Setup Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1135cf284cbff8d898f.png)
[trans]
## Overview

The extreme reversal setup strategy is a trading strategy that utilizes extreme K-line reversals. It generates trade signals based on the size of the latest K-line's实体 and average value, producing a signal when the entity size exceeds the average value and there is a reversal.

## Strategy Principle  

This strategy primarily assesses the size of the current K-line's实体 and overall size.

It records the size (difference between open and close) of the most recent K-line's实体 and the overall size of the K-line (difference between high and low).

Then, it uses the Average True Range Moving Average (RMA) to calculate the average entity size and K-line size over the last 20 K-lines.

When the latest K-line rises, and the entity size is greater than the average entity size, and the overall K-line size is more than twice the average K-line size, a long signal is generated.

Conversely, when the latest K-line falls, and the entity size also meets these conditions, a short signal is generated.

This means that trading signals are triggered when extreme K-lines reverse by comparing them with averages.

## Advantage Analysis

The main advantages of this strategy include:

1. Utilizing extreme K-line characteristics for easy reversals
2. Comparing extreme values of entity and overall K-line size to identify anomalies
3. Using RMA to calculate dynamic averages, making it adaptable to market changes
4. Combining reversal patterns for more reliable signals

## Risk Analysis  

This strategy also has some risks:

1. Extreme K-lines may not reverse and continue running
2. Improper parameter settings can lead to overly sensitive or insensitive responses
3. Requires sufficient market volatility as support, unsuitable for consolidation periods
4. May generate frequent trading signals, increasing transaction costs and slippage risks

To reduce these risks, parameters can be adjusted appropriately, or stop losses can be added to control potential losses.

## Optimization Directions

This strategy can be optimized in the following ways:

1. Adding a volume filter to avoid false breakouts
2. Using volatility indicators to dynamically optimize parameter settings
3. Combining trend indicators to avoid reverse long and short positions
4. Incorporating machine learning models to predict K-line reversals
5. Adding stop loss mechanisms

## Summary  

The extreme reversal setup strategy generates trading signals when reversals occur by judging the latest K-line's实体 size. It leverages the advantage of using exceptional extreme K-line characteristics, but also has certain risks. Better performance can be achieved through parameter optimization and risk control measures.

||

## Overview

The extreme reversal setup strategy is a trading strategy that utilizes extreme K-line reversals. It generates trade signals based on the size of the latest K-line's实体 and average value, producing a signal when the entity size exceeds the average value and there is a reversal.

## Strategy Principle  

This strategy primarily assesses the size of the current K-line's实体 and overall size.

It records the size (difference between open and close) of the most recent K-line's实体 and the overall size of the K-line (difference between high and low).

Then, it uses the Average True Range Moving Average (RMA) to calculate the average entity size and K-line size over the last 20 K-lines.

When the latest K-line rises, and the entity size is greater than the average entity size, and the overall K-line size is more than twice the average K-line size, a long signal is generated.

Conversely, when the latest K-line falls, and the entity size also meets these conditions, a short signal is generated.

This means that trading signals are triggered when extreme K-lines reverse by comparing them with averages.

## Advantage Analysis

The main advantages of this strategy include:

1. Utilizing extreme K-line characteristics for easy reversals
2. Comparing extreme values of entity and overall K-line size to identify anomalies
3. Using RMA to calculate dynamic averages, making it adaptable to market changes
4. Combining reversal patterns for more reliable signals

## Risk Analysis  

This strategy also has some risks:

1. Extreme K-lines may not reverse and continue running
2. Improper parameter settings can lead to overly sensitive or insensitive responses
3. Requires sufficient market volatility as support, unsuitable for consolidation periods
4. May generate frequent trading signals, increasing transaction costs and slippage risks

To reduce these risks, parameters can be adjusted appropriately, or stop losses can be added to control potential losses.

## Optimization Directions

This strategy can be optimized in the following ways:

1. Adding a volume filter to avoid false breakouts
2. Using volatility indicators to dynamically optimize parameter settings
3. Combining trend indicators to avoid reverse long and short positions
4. Incorporating machine learning models to predict K-line reversals
5. Adding stop loss mechanisms

## Summary  

The extreme reversal setup strategy generates trading signals when reversals occur by judging the latest K-line's实体 size. It leverages the advantage of using exceptional extreme K-line characteristics, but also has certain risks. Better performance can be achieved through parameter optimization and risk control measures.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|0.75|bodySize|
|v_input_2|20|Lookback Period|
|v_input_3|2|Bar ATR Multiplier|


> Source (PineScript)

```pinescript
/*backtest
start: 2024-02-13 00:00:00
end: 2024-02-20 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Extreme Reversal Setup", overlay=true)

bodySize = input(defval=0.75)
barsBack = input(title="Lookback Period", type=input.integer, defval=20, minval=0)
bodyMultiplier = input(title="Bar ATR Multiplier", type=input.float, defval=2.0, minval=0)

myBodySize = abs(close - open)
averageBody = rma(myBodySize, barsBack)
myCandleSize = abs(high - low)
averageCandle = rma(myCandleSize, barsBack)

signal_long = open[1]-close[1] >= bodySize*(high[1]-low[1]) and 
   high[1]-low[1] > averageCandle*bodyMultiplier and 
   open[1]-close[1] > averageBody and close > open
signal_short = close[1]-open[1] >= bodySize*(high[1]-low[1]) and 
   high[1]-low[1] > averageCandle*bodyMultiplier and 
   close[1]-open[1] > averageBody and open > close

plotshape(signal_long, "LONG", shape.triangleup, location.belowbar, size=size.normal)
plotshape(signal_short, "SHORT", shape.triangledown, location.belowbar, size=size.normal)

strategy.entry("LONG", strategy.long, when=signal_long)
strategy.entry("SHORT", strategy.short, when=signal_short)
```

> Detail

https://www.fmz.com/strategy/442365

> Last Modified

2024-02-21 14:08:09
---