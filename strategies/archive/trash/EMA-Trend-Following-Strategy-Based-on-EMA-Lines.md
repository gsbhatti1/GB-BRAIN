> Name

Trend-Following-Strategy-Based-on-EMA-Lines

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1f5e9e12cd4244e49e4.png)
[trans]
## Overview

This strategy is based on 3 EMA lines of different periods. It judges the current trend direction by whether the price is above the EMA lines. When the short-term EMA line crosses above the long-term EMA line, a buy signal is generated. When the short-term EMA line crosses below the long-term EMA line, a sell signal is generated. This strategy tracks the trend runs and closes positions in time when trend reverses.

## Strategy Logic

The strategy uses 3 EMA lines, which are 10-day, 20-day, and 50-day respectively. The judging rules are:

1. When both 10-day EMA and 20-day EMA are above 50-day EMA, it is defined as an uptrend;
2. When both 10-day EMA and 20-day EMA are below 50-day EMA, it is defined as a downtrend;
3. When short-term EMA lines (10-day and 20-day) cross above long-term EMA line (50-day), a buy signal is generated;  
4. When short-term EMA lines (10-day and 20-day) cross below long-term EMA line (50-day), a sell signal is generated;
5. Hold long position during uptrend and hold short position during downtrend;  
6. Close current directional position when trend reverses (short-term EMA crosses long-term EMA).

The strategy captures profit by timely closing positions to lock in gains and alternating between long and short positions.

## Advantage Analysis

The advantages of this strategy are:

1. The rules are simple and clear, easy to understand and implement;
2. Using EMA lines to determine trend avoids interference from short-term market fluctuations;
3. Timely closing positions to track trend runs avoids expanding losses;
4. No need to predict market direction with high winning rate by tracking trends.

## Risk Analysis

There are also some risks in this strategy:

1. During range-bound markets, EMA lines may crossover frequently, resulting in high trading costs from frequently opening and closing positions;
2. Trend determination by EMA may fail after price gap, missing good entry opportunities.

To optimize the risks, some methods can be used:

1. Open position rules can be relaxed properly when EMAs are close to avoid over-trading; 
2. Determine trend combining other indicators to avoid EMA failure.

## Optimization Directions

The strategy can be optimized from the following aspects:

1. Parameter optimization. Test different EMA period combinations to find the optimal parameters;  
2. Trading cost optimization. Optimize open position rules properly to reduce unnecessary frequent trading;

3. Stop loss strategy optimization. Set reasonable stop loss level to control single loss;
4. Combine other indicators. Use MACD, KDJ and other indicators to assist in determining optimal entry timing.

## Summary

In general, this strategy is quite simple and practical. It uses EMA to determine trend direction with proper stop loss strategy to effectively control risks. There are also rooms for optimization. By combining parameter optimization, stop loss strategy, and other indicators, the performance of this strategy can be further improved.

||

## Overview

This strategy is based on 3 EMA lines of different periods. It judges the current trend direction by whether the price is above the EMA lines. When the short-term EMA line crosses above the long-term EMA line, a buy signal is generated. When the short-term EMA line crosses below the long-term EMA line, a sell signal is generated. This strategy tracks the trend runs and closes positions in time when trend reverses.

## Strategy Logic

The strategy uses 3 EMA lines, which are 10-day, 20-day, and 50-day respectively. The judging rules are:

1. When both 10-day EMA and 20-day EMA are above 50-day EMA, it is defined as an uptrend;
2. When both 10-day EMA and 20-day EMA are below 50-day EMA, it is defined as a downtrend;
3. When short-term EMA lines (10-day and 20-day) cross above long-term EMA line (50-day), a buy signal is generated;  
4. When short-term EMA lines (10-day and 20-day) cross below long-term EMA line (50-day), a sell signal is generated;
5. Hold long position during uptrend and hold short position during downtrend;  
6. Close current directional position when trend reverses (short-term EMA crosses long-term EMA).

The strategy captures profit by timely closing positions to lock in gains and alternating between long and short positions.

## Advantage Analysis

The advantages of this strategy are:

1. The rules are simple and clear, easy to understand and implement;
2. Using EMA lines to determine trend avoids interference from short-term market fluctuations;
3. Timely closing positions to track trend runs avoids expanding losses;
4. No need to predict market direction with high winning rate by tracking trends.

## Risk Analysis

There are also some risks in this strategy:

1. During range-bound markets, EMA lines may crossover frequently, resulting in high trading costs from frequently opening and closing positions;
2. Trend determination by EMA may fail after price gap, missing good entry opportunities.

To optimize the risks, some methods can be used:

1. Open position rules can be relaxed properly when EMAs are close to avoid over-trading; 
2. Determine trend combining other indicators to avoid EMA failure.

## Optimization Directions

The strategy can be optimized from the following aspects:

1. Parameter optimization. Test different EMA period combinations to find the optimal parameters;  
2. Trading cost optimization. Optimize open position rules properly to reduce unnecessary frequent trading;

3. Stop loss strategy optimization. Set reasonable stop loss level to control single loss;
4. Combine other indicators. Use MACD, KDJ and other indicators to assist in determining optimal entry timing.

## Summary

In general, this strategy is quite simple and practical. It uses EMA to determine trend direction with proper stop loss strategy to effectively control risks. There are also rooms for optimization. By combining parameter optimization, stop loss strategy, and other indicators, the performance of this strategy can be further improved.

[/trans]

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|true|infoBox|
|v_input_2|false|infoBox2|
|v_input_3|false|Buy & SellSignal|
|v_input_4|0|infoBoxSize: size.large|size.tiny|size.small|size.normal|size.auto|size.huge|
|v_input_5|10|ema1Value|
|v_input_6|20|ema2Value|
|v_input_7|59|ema3Value|
|v_input_8|3000|maxLoss|

> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-28 00:00:00
end: 2024-01-31 04:00:00
period: 45m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © mattehalen

//@version=4
//study("EMA 10,20 59",overlay=true)
strategy("EMA 10,20 59", overlay=true)
infoBox     = input(true, title="infoBox", type=input.bool)
infoBox2    = input(false, title="infoBox2", type=input.bool)
BuySellSignal_Bool = input(false, title="Buy & SellSignal", type=input.bool)
infoBoxSize = input(title="infoBoxSize", defval=size.large, options=[size.auto, size.tiny, size.small, size.normal, size.large, size.huge])
ema1Value   = input(10)
ema2Value   = input(20)
ema3Value   = input(59)
maxLoss     = input(3000)
ema1        = ema(close, ema1Value)
ema2        = ema(close, ema2Value)
ema3        = ema(close, ema3Value)
objcnt      = 0
buyTitle    = tostring(close[1])
myProfit    = float(0)

plot(ema1, title="ema1", color=color.red, linewidth=2)
plot(ema2, title="ema2", color=color.green, linewidth=2)
plot(ema3, title="ema3", color=color.black, linewidth=2)

Buytrend = (ema1 and ema2 > ema3) and (ema1[1] and ema2[1] > ema3[1])
```