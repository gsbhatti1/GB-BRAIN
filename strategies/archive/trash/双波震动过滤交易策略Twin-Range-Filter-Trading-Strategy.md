> Name

Twin-Range-Filter-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/9d60a6061247fbea15.png)
[trans]

## Overview

The Twin Range Filter strategy is a trading strategy based on price volatility. It utilizes two average range indicators with different parameter settings, combined with the relationship between price and range, to generate trading signals. This strategy is suitable for highly volatile digital assets like Bitcoin.

## Strategy Logic

This strategy uses two smooth range indicators with different period lengths: a fast range indicator (default period 27) and a slow range indicator (default period 55). The range indicator formula is: exponential moving average of current period price range multiplied by a factor (such as 1.6).

The Twin Range Filter strategy compares the price with the two range indicators to determine if it is currently within a certain oscillation range. Trading signals are generated when the price breaks through this oscillation range.

Specifically, the strategy uses a median line as the benchmark, which is the average of the two range indicators. A long signal is generated when the price is above the median line by one fast range; a short signal is generated when the price falls below the median line by one fast range.

To filter false signals, it also adds a condition: a signal is only generated when the current price move is consistent with the previous period. For example, a long signal is only triggered when the price rises and exceeds the median line by one range.

In summary, this strategy identifies the oscillation range with twin range indicators, and generates orders when the price breaks through the range. Price direction filters are added to reduce false signals.

## Advantages

The advantages of the Twin Range Filter strategy:

1. Utilizes price volatility features, adaptable to highly volatile assets like Bitcoin. The twin range indicators can locate price ranges more precisely.
2. The twin range indicators contain different timeframes. The fast one catches short-term opportunities, while the slow one considers long-term trends.
3. Adding price direction filters reduces false signals from short-term fluctuations.
4. Simple and clear logic, easy to understand and implement, suitable for algo trading.

## Risks

Some risks of the strategy to note:

1. Relies on volatility indicators, may underperform in low volatility environments.
2. Range parameters need to be optimized for different products, otherwise trading opportunities may be missed or false signals occur.
3. Divergence between price and volatility is not considered. False signals may occur if volatility rises without corresponding price increase.
4. Stop loss levels may need adjustment in high volatility environments. Overly tight stops cause excessive stop outs.

## Enhancement

The strategy can be enhanced in several aspects:

1. Test and optimize range parameters to find optimal combinations for different products and timeframes.
2. Add dynamic stop loss mechanisms based on recent volatility, to optimize stop loss strategy.
3. Add filters based on price-volatility divergence to avoid false signals.
4. Incorporate other indicators like volume changes to increase entry certainty.
5. Test and add appropriate profit taking exit mechanisms suitable for the strategy.

## Summary

Overall, the Twin Range Filter is an effective trading strategy for highly volatile assets. It utilizes price volatility characteristics well and generates simple and clear trading logic. With further improvements like parameter optimization and risk management, it can become a valuable component in a quant trading system. It also provides insight into algorithmic trading based on market volatility features.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|27|Fast period|
|v_input_3|1.6|Fast range|
|v_input_4|55|Slow period|
|v_input_5|2|Slow range|
|v_input_6|false|Following conditions and backtest algorithm are added by @greenmask9 ?, original script is written by @colinmck ?. Read both of their's release notes for more info on how this script works.|
|v_input_7|false|Disable greenmask9's ATR conditions|
|v_input_8|32|ATR1|
|v_input_9|0|Smoothing: SMA|RMA|EMA|WMA|
|v_input_10|64|ATR2|
|v_input_11|0|Smoothing: RMA|SMA|EMA|WMA|
|v_input_12|900|Ticks profit|
|v_input_13|300|Ticks stoploss|
|v_input_14|17|Time stoploss|

> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-05 00:00:00
end: 2023-11-12 00:00:00
period: 30m
basePeriod: 15m
exchanges: [
```