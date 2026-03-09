> Name

EMAC Index Moving Average Cross Optimized Strategy (EMAC-Exponential-Moving-Average-Cross-Optimized-Strategy)

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/186996b0c8ff3d15ac5.png)
[trans]

## Overview

The EMAC Index Moving Average Cross Optimized Strategy is an optimized version of the basic EMAC strategy. It integrates trend judgment, multiple moving average filtering, and stop loss/take profit exits to follow mid-to-long term trends.

## Strategy Logic

1. Judge recent trend direction: calculate the increase/decrease percentage of close price over past 26 weeks to determine uptrend, downtrend or sideways.

2. Multiple moving average filter: calculate 10-period, 20-period, 34-period EMA and wait for them to cross above 50-period SMA to trigger buy signals.

3. ATR stop loss: when entry signal appears, set stop loss at entry bar's low or high minus 2.5ATR.

4. Trailing stop loss: gradually move up stop loss line as price rises.

5. Take profit: when entry signal appears, set target at close price plus 3ATR.

6. MA pullback exit: actively exit when price breaks back below 10-day EMA.

## Advantages

1. Multiple MA filter increases signal reliability, avoiding false breakouts.

2. ATR stop loss allows reasonable stop distance based on market volatility.

3. Trailing stop locks in some profits as it moves up.

4. Reasonable profit target avoids giving back too much profit.

5. MA pullback exit allows timely exit when trend reverses.

## Risks and Solutions

1. EMA crosses may whipsaw in sideways markets, causing consecutive losses. Can increase EMA periods or add MA crossover filter.

2. Large ATR values can cause stops too far away, increasing loss risk. Can optimize with ATR moving averages or reduction coefficients.

3. Overnight gap risk not considered. Can add logic to avoid signals during non-trading periods.

4. Market regime not considered. Can add market trend filter as a strategy switch.

## Optimization Directions 

1. Test EMA combinations to find optimal lengths for different products.

2. Test ATR moving averages or reduction coefficients to optimize stop distance.

3. Add logic to avoid signals during non-trading periods.

4. Add market trend filter as a strategy switch when market is unfavorable.

5. Backtest parameter combinations over many years to find optimal stability.

## Summary

The EMAC Index Moving Average Cross Optimized Strategy combines trend judgment, multiple MA filtering and dynamic stops to follow mid-to-long term trends. Compared to the original version it has undergone parameter optimization to improve real-trading performance. But further optimizations and enhancements are needed by adding more logic to handle different market situations, reducing risks and improving stability and profitability.

|||

## Overview

The EMAC Exponential Moving Average Cross Optimized Strategy is an optimized version based on the basic EMAC strategy. It incorporates trend judgment, multiple moving average filtering, and stop loss/take profit exits, aiming to follow mid-to-long term trends.

## Strategy Logic

1. Judge recent trend direction: calculate the increase/decrease percentage of close price over past 26 weeks to determine uptrend, downtrend or sideways.

2. Multiple moving average filter: calculate 10-period, 20-period, 34-period EMA and wait for them to cross above 50-period SMA to trigger buy signals.

3. ATR stop loss: when entry signal appears, set stop loss at entry bar's low or high minus 2.5ATR.

4. Trailing stop loss: gradually move up stop loss line as price rises.

5. Take profit: when entry signal appears, set target at close price plus 3ATR.

6. MA pullback exit: actively exit when price breaks back below 10-day EMA.

## Advantages

1. Multiple MA filter increases signal reliability, avoiding false breakouts.

2. ATR stop loss allows reasonable stop distance based on market volatility.

3. Trailing stop locks in some profits as it moves up.

4. Reasonable profit target avoids giving back too much profit.

5. MA pullback exit allows timely exit when trend reverses.

## Risks and Solutions

1. EMA crosses may whipsaw in sideways markets, causing consecutive losses. Can increase EMA periods or add MA crossover filter.

2. Large ATR values can cause stops too far away, increasing loss risk. Can optimize with ATR moving averages or reduction coefficients.

3. Overnight gap risk not considered. Can add logic to avoid signals during non-trading periods.

4. Market regime not considered. Can add market trend filter as a strategy switch.

## Optimization Directions 

1. Test EMA combinations to find optimal lengths for different products.

2. Test ATR moving averages or reduction coefficients to optimize stop distance.

3. Add logic to avoid signals during non-trading periods.

4. Add market trend filter as a strategy switch when market is unfavorable.

5. Backtest parameter combinations over many years to find optimal stability.

## Summary

The EMAC Exponential Moving Average Cross Optimized Strategy combines trend judgment, multiple MA filtering and dynamic stops to follow mid-to-long term trends. Compared to the original version it has undergone parameter optimization to improve real-trading performance. But further optimizations and enhancements are needed by adding more logic to handle different market situations, reducing risks and improving stability and profitability.

|||

## Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|2015|Start Year|
|v_input_2|0|R Static or Percent: Percent|Static|
|v_input_3|2000|R Size Static|
|v_input_4|3|R Size Percent|
|v_input_5|W|Trend Timeframe|
|v_input_6|26|# of Bars for Trend|
|v_input_7|15|Trend Growth %|
|v_input_8|0|Trend Required: Red|Yellow|Orange|Green|
|v_input_9|10|MA1 Period|
|v_input_10|0|MA1 Type: EMA|SMA|WMA|
|v_input_11|20|MA2 Period|
|v_input_12|0|MA2 Type: EMA|SMA|WMA|
|v_input_13|34|MA3 Period|
|v_input_14|0|MA3 Type: EMA|SMA|WMA|
|v_input_15|100|MA4 Period|
|v_input_16|0|MA4 Type: SMA|EMA|WMA|
|v_input_17|200|MA5 Period|
|v_input_18|0|MA5 Type: SMA|EMA|WMA|
|v_input_19|0|Enable Short MA Cross Filter: No|Yes|
|v_input_20|0|Enable Long MA Cross Filter: No|Yes|
|v_input_21|2.5|Stop ATR Multiple|
|v_input_22|3|Target Multiple|
|v_input_23|0|Enable ATR Stops: No|Yes|
|v_input_24|0|Enable Stops: No|Yes|
|v_input_25|0|Enable Targets: No|Yes|
|v_input_26|0|Enable Early Exit: Yes|No|

## Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-01 00:00:00
end: 2023-10-31 23:59:59
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//Author = Dustin Drummond https://www.tradingview.com/u/Dustin_D_RLT/
//Strategy based in part on original 10ema Basic Swing Trade Strategy by Matt Delong: https://www.tradingview.com/u/MattDeLong/
//Link to original 10ema Basic Swing Trade Strategy: https://www.tradingview.com/script/8yhGnGCM-10ema-Basic-Swing-Trade-Strategy/
//This is the Original EMAC - Exponential Moving Average Cross Strategy built as a class for reallifetrading dot com and so has all the default settings and has not been optimized
//I would not recomend using this strategy with the default settings and is for educational purposes only
//For the fully optimized version please come back around the same time tomorrow 6/16/21 for the EMAC - Exponential Moving Average Cross - Opti
```