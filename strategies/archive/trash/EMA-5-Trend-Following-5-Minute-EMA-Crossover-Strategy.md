> Name

Trend-Following-5-Minute-EMA-Crossover-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/163948ecadbf5e6c6a7.png)
[trans]


## Overview

This is a 5-minute timeframe trend following strategy based on fast and slow EMA crossovers, with limit orders and trailing stop loss to automatically catch trends. It is suitable for medium-term trend trading, using EMA filter to determine overall trend direction and fast/slow EMA crossovers to pinpoint specific entry timing. Its advantages are accurate trend judgement and effective trend following. Disadvantages include occasional false breakouts and whipsaws.

## Strategy Logic

1. Use fast and slow EMA lines, go long when fast EMA crosses above slow EMA, go short when crossing below
2. Apply EMA macro filter, only take longs above EMA and shorts below EMA to avoid false signals
3. Enter trades with limit orders to ensure ideal entry price is met
4. Apply dynamic trailing stop loss after entry to lock in profits and cut losses

Specifically:

1. Calculate fast and slow EMA based on chosen periods
2. Only take long/short positions when price is above/below EMA if filter is enabled
3. Go long when fast EMA crosses above slow EMA, go short on downward crossover
4. Place limit buy orders for longs and limit sell orders for shorts
5. Initiate trailing stop loss based on highest high/lowest low after entry

The above covers the basic trading logic of this strategy.

## Advantages

1. EMA filters determine overall trend, prevents trading against major trend
2. Fast/slow EMA with limits prevents chasing tops/bottoms
3. Dynamic trailing stop locks in profits effectively
4. Good risk control with ~2% stop loss
5. Smaller drawdowns, good at following trends
6. Simple and easy to understand logic, optimizable

## Risks

1. Whipsaws and false breakout risks, possibility of being trapped
2. Incorrect EMA periods may cause missed trends
3. Stop loss too wide, may exceed normal volatility
4. Trailing stop too aggressive, could exit prematurely
5. Suboptimal stop loss/take profit ratios, missing big moves

Solutions:

1. Optimize EMA parameters to find best periods
2. Widen stops moderately to prevent excessive stops
3. Carefully determine trailing start point and trail percentage
4. Test different stop/take ratios to find optimum

## Optimization Opportunities

1. Optimize EMA periods to find best combinations
2. Try different EMA types like weighted moving average
3. Test other indicators like MACD for improved performance
4. Attempt EMA filtering on higher timeframes
5. Optimize limit order entry price range
6. Optimize stop loss and take profit points/ratios
7. Experiment with more advanced trailing methods
8. Add trend strength indicator for situational awareness
9. Consider more filters to further avoid false signals

## Conclusion

Overall this is a very effective medium-term trend following strategy. Its clear logic of using EMA crossovers for entries, limit orders to prevent chasing, and trailing stops to lock profits is simple and robust. With proper parameter tuning it can achieve higher win rates and profitability. Risks like improper EMA periods and excessive stops need to be monitored. But in general this is an efficient quantifiable trend trading system.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|20|(?EMA Settings)Fast Length|
|v_input_string_1|0|    Type: EMA|SMA|RMA|WMA|
|v_input_source_1_close|0|    Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_2|100|Slow Length|
|v_input_string_2|0|    Type: EMA|SMA|RMA|WMA|
|v_input_source_2_close|0|    Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_bool_1|false|(?Trade Filters)Use EMA Filter|
|v_input_timeframe_1||    Timeframe|
|v_input_int_3|300|    Length|
|v_input_source_3_hl2|0|    Source: hl2|high|low|open|close|hlc3|hlcc4|ohlc4|
|v_input_float_1|2|(?Entry Settings)Stop Loss (%)|
|v_input_float_2|2|Take Profit (%)|
|v_input_int_4|3|Long Entry Limit Lookback|
|v_input_int_5|3|Short Entry Limit Lookback|
|v_input_float_3|true|Start Trailing After (%)|
|v_input_float_4|true|Trail Behind (%)|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-11-09 00:00:00
end: 2023-11-15 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © jordanfray

//@version=5
strategy(title="5 Minute EMA Strategy", overlay=true, max_bars_back=500, default_qty_type=strategy.percent_of_equity, default_qty_value=100,initial_capital=100000, com
