> Name

Three-SMA-Crossover-Momentum-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1409ce1608b12ef217c.png)
[trans]

## Overview

The Three SMA Crossover Momentum strategy is a typical technical indicator strategy that tracks market trends. It combines 16-period, 36-period, and 72-period simple moving averages to determine market trends through their bullish and bearish crossovers. Kaufman’s Adaptive Moving Average (KAMA) serves as a filter, activating SMA crossover signals only when the trend direction is clear.

## Strategy Logic

The core indicators of this strategy are the 16-, 36-, and 72-period simple moving averages. When the shorter-period Simple Moving Average (SMA) crosses over the longer-period one upwards, it indicates an uptrend; conversely, a downward crossover signals a downtrend. For instance, when the 16-SMA crosses above both the 36-SMA and 72-SMA, this is a bullish signal. Conversely, when the 16-SMA crosses below both the 36-SMA and 72-SMA, it indicates a bearish signal.

Kaufman’s Adaptive Moving Average (KAMA) acts as a filter to avoid false signals in uncertain trend scenarios. SMA crossover signals are only activated when KAMA is in a non-accelerating or non-decelerating mode (i.e., during the linear phase).

The strategy monitors the crossover situations of SMAs, taking long or short positions based on clear trend indications. The long condition is met if the 16-SMA crosses above both the 36-SMA and 72-SMA with a KAMA in its linear state; the short condition is triggered when the 16-SMA crosses below both the 36-SMA and 72-SMA, also during the linear phase of KAMA.

## Advantage Analysis

The strategy has several advantages:

1. Combining multi-period SMAs can effectively track medium- to long-term market trends.
2. Incorporating adaptive moving average as a filter helps reduce false signals in uncertain trend scenarios.
3. Simple implementation makes it suitable for automated or program trading.

## Risk Analysis

This strategy also poses some risks:

1. Frequent ineffective signals may occur during range-bound markets due to frequent SMAs crossovers.
2. No stop-loss mechanism is set, leading to potential loss expansion.
3. Designed for high-volatility crypto markets; it may underperform in less volatile markets.

These risks can be mitigated by tuning SMA parameters, setting up stop-loss constraints, or applying the strategy only in highly volatile markets.

## Optimization Directions

The strategy can be optimized through:

1. Testing different combinations of SMA parameters to find the optimal settings.
2. Adding trading volume or volatility indicators as supplementary filter conditions.
3. Setting up a stop-loss mechanism.
4. Combining other indicators to determine entry timing more accurately.
5. Optimizing position sizing, gradually adjusting risk levels by adding and reducing positions.

## Conclusion

Overall, the Three SMA Crossover Momentum strategy is a classic and practical trend-following approach. It leverages multi-period SMAs to identify medium- to long-term market trends while effectively filtering out noise. It can serve as a reference for timing trades but requires further enhancements and optimizations to perform well across a broader range of markets.

||

## Overview

The Three SMA Crossover Momentum strategy is a typical technical indicator strategy that tracks market trends. It combines 16-, 36- and 72-period simple moving averages, using their bullish and bearish crossovers to determine market trends. Kaufman’s Adaptive Moving Average (KAMA) serves as a filter, only activating SMA crossover signals when the trend direction is clear.

## Strategy Logic

The core indicators of this strategy are the 16-, 36- and 72-period simple moving averages. When the shorter-period Simple Moving Average (SMA) crosses over the longer-period one upwards, it indicates an uptrend; conversely, a downward crossover signals a downtrend. For example, when the 16-SMA crosses above both the 36-SMA and 72-SMA, this is a bullish signal. Conversely, when the 16-SMA crosses below both the 36-SMA and 72-SMA, it indicates a bearish signal.

Kaufman’s Adaptive Moving Average (KAMA) acts as a filter to avoid false signals in uncertain trend scenarios. SMA crossover signals are only activated when KAMA is in a non-accelerating or non-decelerating mode (i.e., during the linear phase).

The strategy monitors the SMA crossover situations, taking long or short positions based on clear trend indications. The long condition is met if the 16-SMA crosses above both the 36-SMA and 72-SMA with a KAMA in its linear state; the short condition is triggered when the 16-SMA crosses below both the 36-SMA and 72-SMA, also during the linear phase of KAMA.

## Advantage Analysis

The advantages of this strategy are:

1. Combining multi-period SMAs can effectively track medium- to long-term market trends.
2. Incorporating adaptive moving average as a filter helps reduce false signals in uncertain trend scenarios.
3. Simple implementation makes it suitable for automated or program trading.

## Risk Analysis

This strategy also poses some risks:

1. Frequent ineffective signals may occur during range-bound markets due to frequent SMAs crossovers.
2. No stop-loss mechanism is set, leading to potential loss expansion.
3. Designed for high-volatility crypto markets; it may underperform in less volatile markets.

These risks can be mitigated by tuning SMA parameters, setting up stop-loss constraints, or applying the strategy only in highly volatile markets.

## Optimization Directions

The strategy can be optimized through:

1. Testing different combinations of SMA parameters to find the optimal settings.
2. Adding trading volume or volatility indicators as supplementary filter conditions.
3. Setting up a stop-loss mechanism.
4. Combining other indicators to determine entry timing more accurately.
5. Optimizing position sizing, gradually adjusting risk levels by adding and reducing positions.

## Conclusion

Overall, the Three SMA Crossover Momentum strategy is a classic and practical trend-following approach. It leverages multi-period SMAs to identify medium- to long-term market trends while effectively filtering out noise. It can serve as a reference for timing trades but requires further enhancements and optimizations to perform well across a broader range of markets.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_4|100|  Trend SMA |
|v_input_int_5|50|   KAMA Lenght|
|v_input_bool_1|true|  Self Powered|
|v_input_int_1|16|(?SMA)  1-SMA Lenght|
|v_input_int_2|36|  2-SMA Lenght|
|v_input_int_3|72|  3-SMA Lenght|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-24 00:00:00
end: 2023-12-24 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Wielkieef


//@version=5
strategy(title='Three SMA-crossover strategy [30min] ', overlay=true, pyramiding=1, initial_capital=10000, default_qty_type=strategy.cash, default_qty_value=10000, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.03)

src = close

Length1 = input.int(16, title='  1-SMA Lenght', minval=1, group='SMA')
Length2 = input.int(36, title='  2-SMA Lenght', minval=1, group='SMA')
Length3 = input.int(72, title='  3-SMA Lenght', minval=1, group='SMA')
SMA1 = ta.sma(close, Length1)
SMA2 = ta.sma(close, Length2)
SMA3 = ta.sma(close, Length3)

Long_ma = SMA1 > SMA2 and SMA2 > SMA3
Short_ma = SMA1 < SMA2 and SMA2 < SMA3

LengthMainSMA = input.int(100, title='  Trend SMA ', minval=1)

SMAas = ta.sma(src, LengthMainSMA)

//  Powered Kaufman Adaptive Moving Average by alexgrover (modificated by Wielkieef)
lengthas = input.int(50, title='   KAMA Lenght')
sp = input.bool(true, title='  Self Powered')

er = math.abs(ta.change(close, lengthas)) / math.sum(math.abs(ta.change(close)), lengthas)
``` 

The script is truncated and does not include the full Kaufman’s Adaptive Moving Average (KAMA) calculation. The code continues with the logic for KAMA but is incomplete as shown in the snippet provided. You can complete it by adding the necessary lines to calculate KAMA based on the given `lengthas` parameter and other required variables. If you need further assistance or completion of this part, feel free to ask!