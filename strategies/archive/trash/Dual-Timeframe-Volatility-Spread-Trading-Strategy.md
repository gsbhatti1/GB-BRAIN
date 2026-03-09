> Name

Dual-Timeframe-Volatility-Spread-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/14596ddc1192b4d3687.png)
[trans]
## Overview

The dual-timeframe volatility spread trading strategy judges the overbought/oversold status of the market by calculating the spread between RSI indicators of two different time cycles, to implement low-risk trend trading.

## Strategy Principle

The core indicators of this strategy are `shortTermXtrender` and `longTermXtrender`. `shortTermXtrender` calculates the RSI spread on the short-term timeframe, and `longTermXtrender` calculates the RSI spread on the long-term timeframe.

The short-term timeframe adopts the price difference between 7-day EMA and 4-day LMA to calculate RSI, and then the price difference with 50 constitutes `shortTermXtrender`. The long-term timeframe adopts the price difference between RSI of 4-day EMA and 50 to constitute `longTermXtrender`.

When `shortTermXtrender` crosses above 0, go long; when `longTermXtrender` crosses above 0, also go long. The stop loss principle after going long is to stop loss when `shortTermXtrender` crosses below 0; when `longTermXtrender` crosses below 0, stop loss too.

In this way, by judging on dual timeframes, more false breakouts can be filtered out.

## Advantage Analysis

The biggest advantage of this strategy is that the trend judgment is accurate. The combination of dual timeframes can effectively filter out noise and lock in the target trend direction. This provides a guarantee for low-risk trend tracking trading.

In addition, the strategy provides room for parameter optimization. Users can adjust parameters such as SMA cycle and RSI parameters according to different varieties and time cycles to optimize strategy results.

## Risk Analysis

The main risk of this strategy is the wrong judgment of long and short. In oscillating markets, it is easy to generate wrong signals. If the position is still opened at this time, there will be the risk of loss.

In addition, improper parameter settings can also lead to poor results. If the time cycle parameter is set too short, the probability of misjudgment will increase; if the time cycle parameter is set too long, the opportunity for the trend will be missed. This requires users to test and optimize parameters for different markets.

## Optimization Directions

The strategy can be optimized in the following aspects:

1. Increase profit taking mechanism. Currently, there is no profit taking setting in the strategy. Profit can be taken in time after reaching the target profit.
2. Increase position management. Positions can be dynamically adjusted based on capital size, volatility, and other indicators.
3. Test parameter settings for different varieties. Users can test the optimal parameter combination by backtesting different timeframes such as daily and 60 minutes.
4. Increase machine learning assisted judgment. Models can be trained to determine market conditions and dynamically adjust strategy parameters to improve win rate.

## Summary

The dual-timeframe volatility spread trading strategy achieves efficient trend capturing by constructing dual-timeframe indicators. The strategy has large optimization space. Users can optimize through parameter adjustment, profit taking management, position management, etc., to obtain better strategy results. This strategy is suitable for users with some trading experience.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|7|ShortTermSMA|
|v_input_2|4|ShortTermLMA|
|v_input_3|2|ShortTermRSI|
|v_input_4|4|LongTermMA|
|v_input_5|2|LongTermRSI|
|v_input_6|true|UseFactors|
|v_input_7|true|TradeShortTerm|
|v_input_8|true|TradeLongTerm|
|v_input_9|true|From Day|
|v_input_10|true|From Month|
|v_input_11|2018|From Year|
|v_input_12|true|To Day|
|v_input_13|true|To Month|
|v_input_14|2020|To Year|


> Source (PineScript)

```pinescript
//@version=4
//study("MavXtrender")
strategy("MavXtrender")

ShortTermSMA = input(7)
ShortTermLMA = input(4)
ShortTermRSI = input(2)

LongTermMA  = input(4)
LongTermRSI  = input(2)

UseFactors = input(true)
TradeShortTerm = input(true)
TradeLongTerm = input(true)

count = TradeShortTerm == true ? 1 : 0
count := TradeLongTerm == true ? count + 1 : count
// set position size
Amount = strategy.equity / (close * count)

ShortTermLMA := UseFactors == true ? round(ShortTermSMA * ShortTermLMA) : ShortTermLMA
ShortTermRSI := UseFactors == true ? round(ShortTermSMA * ShortTermRSI) : ShortTermRSI
LongTermMA := UseFactors == true ? round(ShortTermSMA * LongTermMA) : LongTermMA
LongTermRSI := UseFactors == true ? round(ShortTermSMA * LongTermRSI) : LongTermRSI
```