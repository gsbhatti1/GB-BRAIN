> Name

Dynamic-Envelope-Moving-Average-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/a374cd354cbddf7607.png)
[trans]
## Overview

This strategy is based on moving average and dynamic envelope lines to implement both long and short trading. It tracks price breakouts beyond envelope lines to establish positions and closes positions when price breaks back below the baseline moving average. This strategy works well for stocks and cryptocurrencies with obvious trends.

## Strategy Logic

Firstly, this strategy calculates the baseline moving average based on user-defined moving average type and length. Common moving averages include SMA, EMA etc.

Then, it calculates the upper and lower envelope lines based on user-defined percentage parameters. For example, 5% means establishing positions when price fluctuates 5% beyond baseline moving average. The number of envelope lines can be customized.

Regarding entry rules, go long when price breaks below the lower envelope line, go short when price breaks above the upper envelope line. The rules are simple and straightforward.

Lastly, close all positions when price breaks back below the baseline moving average. This is an exit point to trail the trend.

Notably, this strategy implements partial position establishment. If multiple envelope lines exist, capital will be allocated proportionately. This prevents the risk of one-sided bets.

## Advantage Analysis

The biggest pros of this strategy:

1. Automatic trend following. Using moving average to determine trend direction is a well-established method.
2. Filtering out some noise with envelope lines, preventing excessive sensitive trading. Reasonable parameter setting can greatly improve strategy profitability.
3. Partial position establishment enhances strategy resilience. Even if one side fails, the other side can keep running well. This optimizes overall risk-reward ratio.
4. Customizable moving average and envelope line number. This increases flexibility for parameter tuning based on different products.

## Risk Analysis

The main risks of this strategy:

1. Moving average system is not sensitive to golden cross signals. It may miss some opportunities if no obvious trend exists.
2. Too wide envelope line setting may increase trading frequency and slippage risk. Too narrow setting may miss larger moves. Finding the balance requires thorough testing.
3. This strategy likely encounters more whipsaws in ranging markets. So trending products are preferable.
4. Partial position establishment limits per trade profit. If seeking one-sided bets, further optimization is needed.

## Optimization Directions

The main directions to optimize this strategy:

1. Replace with other entry/exit indicators like KDJ etc. Or add filters with multiple indicators.
2. Add stop profit/loss logic. This locks in some profit and actively mitigates some risks.
3. Optimize parameters to find the best moving average and envelope combinations. Requires extensive backtesting and optimization.
4. Incorporate deep learning etc. for smart parameter tuning. Constantly learn and update over time.
5. Consider product and market differences, set multiple parameter sets suiting different trading environments. This greatly improves strategy robustness.

## Conclusion

In conclusion, this dynamic envelope moving average strategy works very well for trend trading. It is simple, efficient, easy to understand and optimize. As a basic strategy, it has great plasticity and extensibility. When combined with more complex systems, it can be further enhanced for higher returns and better risk-adjusted metrics. So it serves as an excellent foundation for quantitative trading strategies.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_bool_1|true|Long Positions|
|v_input_bool_2|true|Short Positions|
|v_input_1_ohlc4|0|(?Base MA)Source: ohlc4|high|low|open|hl2|hlc3|hlcc4|close|
|v_input_int_1|5|Baseline Moving Average Window|
|v_input_string_1|0|MA Type: 1. SMA|2. PCMA|3. EMA|4. WMA|5. DEMA|6. ZLEMA|7. HMA|
|v_input_float_1|0.05|(?Envelopes)Envelope 1|
|v_input_float_2|0.1|Envelope 2|
|v_input_float_3|0.15|Envelope 3|
|v_input_float_4|false|Envelope 4|
|v_input_float_5|false|Envelope 5|

> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-05 00:00:00
end: 2024-02-04 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Envelope Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital=1000, pyramiding = 5, commission_type=strategy.commission.percent, commission_value=0.0)
```