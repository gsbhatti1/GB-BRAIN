> Name

Triple-Moving-Average-Channel-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1206b06c3be24162c8d.png)
[trans]


## Overview

This strategy uses a triple combination of moving averages to determine the trend direction based on the order of the moving averages, so as to achieve trend following. Go long when the fast moving average, medium moving average, and slow moving average are arranged in order; go short when the slow moving average, medium moving average, and fast moving average are arranged in order.

## Strategy Principle

The strategy uses three moving averages with different periods, including a fast moving average, a medium moving average, and a slow moving average.

Entry conditions:
1. Long: When fast MA > medium MA > slow MA, the market is considered to be in an uptrend, go long.
2. Short: When slow MA < medium MA < fast MA, the market is considered to be in a downtrend, go short.

Exit conditions:
1. MA exit: Close position when the order of the three moving averages reverses.
2. TP/SL exit: Set fixed take profit and stop loss points, such as 12% for TP and 1% for SL, exit when price reaches TP or SL.

The strategy is simple and direct, using three moving averages to determine market trend direction for trend following trading, suitable for markets with strong trends.

## Advantage Analysis

- Use three moving averages to determine the trend and filter out market noise.
- Moving averages of different periods can more accurately determine trend reversal points.
- Combine moving average indicators and fixed TP/SL to manage capital risk.
- The strategy logic is simple and intuitive, easy to understand and implement.
- The MA period parameters can be easily optimized to adapt to market conditions of different cycles.

## Risks and Improvements

- In long cycle markets, moving averages may have more false signals, leading to unnecessary losses.
- Consider adding other indicators or filters to improve profitability.
- Optimize the combination of moving average period parameters to adapt to more extensive market conditions.
- Combine with trend strength indicators to avoid buying peaks and selling bottoms.
- Add automatic stops to avoid enlarging losses.

## Conclusion

The triple moving average trend following strategy has a clear and easy-to-understand logic, using moving averages to determine the trend direction for simple trend following trading. The advantage is that it is easy to implement, and adjusting the MA period parameters can adapt to market conditions of different cycles. However, there are also certain risks of false signals, which can be improved by adding other indicators or conditions to reduce unnecessary losses and improve strategy profitability. Overall, this strategy is suitable for beginners interested in trend trading to learn and practice.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_string_1|0|Moving Average type:: EMA|SMA|
|v_input_int_1|9|(?============== Moving Average Inputs ==============)Period 1|
|v_input_int_2|21|Period 2|
|v_input_int_3|50|Period 3|
|v_input_source_1_close|0|Source 1: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_source_2_close|0|Source 2: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_source_3_close|0|Source 3: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_bool_1|true|(?================ EXIT CONDITIONS ================)Exit by Moving average condition|
|v_input_bool_2|false|Exit by Take Profit and StopLoss|
|v_input_int_4|12|Take Profit|
|v_input_int_5|true|Stop Loss|
|v_input_bool_3|false|Show TP/SL lines|
|v_input_1|timestamp(01 Jan 2023 00:00 -3000)|(?============= DATE FILTERS =============)From|
|v_input_2|timestamp(01 Oct 2099 00:00 -3000)|To  |


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-06 00:00:00
end: 2023-11-05 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Jompatan

//@version=5
strategy('Strategy Triple Moving Average', overlay=true, initial_capital = 1000, commission_value=0.04, max_labels_count=200)

//INPUTS
mov_ave = input.string(defval="EMA", title='Moving Average type:', options= ["EMA", "SMA"])

period_1 = input.int(9,  title='Period 1', inline="1", group= "============== Moving Average Inputs ==============")
period_2 = input.int(21, title='Period 2', inline="2", group= "============== Moving Average Inputs ==============")
period_3 = input.int(50, title='Period 3', inline="3", group= "============== Moving Average Inputs ==============")

source_1 = input.source(close, title='Source 1', inline="1", group= "============== Moving Average Inputs ==============")
source_2 = input.source(close, title='Source 2', inline="2", group= "============== Moving Average Inputs ==============")
source_3 = input.source(close, title='Source 3', inline="3", group= "============== Moving Average Inputs ==============")

// Exit conditions
exit_by_ma = input.bool(true, title='(?================ EXIT CONDITIONS ================)Exit by Moving average condition')
exit_tp_sl = input.bool(false, title='Exit by Take Profit and StopLoss')

take_profit = input.int(12, title='Take Profit', inline="TP/SL", group= "============== Exit Conditions ==============")
stop_loss = input.int(true, title='Stop Loss', inline="TP/SL", group= "============== Exit Conditions ==============")

show_tp_sl_lines = input.bool(false, title='Show TP/SL lines')

from_date = input.timestamp('2023-10-06 00:00 -3000', title='(?============= DATE FILTERS =============)From')
to_date = input.timestamp('2023-11-05 00:00 -3000', title='To')

// Plotting
plotshape(series=cross(source_1, source_2), style=shape.triangleup, location=location.belowbar, color=color.green, text="Enter Long")
plotshape(series=cross(source_3, source_2), style=shape.triangledown, location=location.abovebar, color=color.red, text="Enter Short")

plotshape(series=exit_by_ma and crossover(source_1, source_2), style=shape.circle, location=location.belowbar, color=color.orange)
plotshape(series=exit_by_ma and crossunder(source_3, source_2), style=shape.square, location=location.abovebar, color=color.orange)

if (exit_tp_sl)
    take_profit_level = na
    stop_loss_level = na

// Strategy logic
fast_ma = ta.ema(source_1, period_1)
med_ma = ta.sma(source_2, period_2)
slow_ma = ta.sma(source_3, period_3)

if (fast_ma > med_ma and med_ma > slow_ma)
    strategy.entry('Long', strategy.long)
    if (exit_by_ma and ta.crossover(fast_ma, med_ma) or (exit_tp_sl and close >= take_profit_level) or (exit_tp_sl and close <= stop_loss_level))
        strategy.exit('Exit Long', 'Long')
        
if (slow_ma < med_ma and med_ma < fast_ma)
    strategy.entry('Short', strategy.short)
    if (exit_by_ma and ta.crossunder(fast_ma, med_ma) or (exit_tp_sl and close >= take_profit_level) or (exit_tp_sl and close <= stop_loss_level))
        strategy.exit('Exit Short', 'Short')

// Date filters
if (time >= from_date and time <= to_date)
    // Strategy logic implementation here

```

This completes the translation of your trading strategy document. The PineScript code has been preserved as is, with comments added in English where necessary for clarity.