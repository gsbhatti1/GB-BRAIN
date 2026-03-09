> Name

Trend-Following-Strategy-Based-on-Moving-Averages

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/af765d72dd4374e811.png)
 [trans]

## Overview

This strategy is a trend following strategy based on moving averages. It utilizes different period EMAs to construct multiple sets of trading signals, achieving trend tracking. When the price breaks below longer-term EMAs, it gradually builds long positions to lower the average cost. The strategy also sets stop loss conditions to exit in short-term reversals and secure profits.

## Strategy Logic

The strategy employs 5 EMA lines of different periods for constructing trading signals: 10-day, 20-day, 50-day, 100-day, and 200-day EMAs. The strategy defines four buying conditions based on the relationship between the price and these EMAs to implement pyramid trading.

When the price is below the 20-day EMA but above the 50-day EMA, the first buy signal is triggered. When it's below the 50-day EMA but above the 100-day EMA, the second buy signal is triggered. The third and fourth buy signals are triggered when the price drops below the 100-day EMA and 200-day EMA respectively. The position size also expands progressively from qt1 to qt4.

On the sell side, there are two groups of stop loss conditions. The first group stops out when the price surpasses the 10-day EMA while the 10-day EMA is above other EMAs. The second group exits when the price drops below the previous close of the 10-day EMA. These two conditions help secure short-term profits during trends.

## Advantage Analysis

The biggest advantage of this strategy lies in its ability to automatically track market trends for long-term holds. By using multiple entry conditions and progressive position building, it continuously lowers cost basis to yield excess returns. It also diversifies away the pricing risk associated with a single entry price level.

In stop loss terms, the strategy tracks short-term moving average turning points to quickly take profit and avoid further losses. This minimizes the downside risk.

## Risk Analysis

The biggest risk this strategy faces is being stuck in long-lasting consolidations or downtrends. When the overall market enters a ranging or downward channel, moving average signals become less reliable. This could lead to sustained losses from continued long builds.

Another risk point is that moving averages do not always pinpoint turns accurately. Price gaps or explosive moves could result in faulty signals. This calls for additional technical indicators for verification and optimization.

## Optimization Directions

Other technical indicators like volume or Bollinger Bands could be incorporated into the buying conditions to further improve entry accuracy.

The second layers of stop loss based on Bollinger Upper Band or key support areas could also be added. This helps avoid unnecessary small stops. Implementing adaptive stop loss to trail prices is another enhancement area to better protect profits.

## Conclusion

This strategy implements trend following trading via a moving average system. Through pyramid position building, it aims to maximize returns from sustained trends while securing capital preservation with dual stop loss mechanisms. This is a strategy worthy of further tracking and live testing. Parameters and models can be incrementally optimized based on practical performance.
[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_int_1|5|Quantity 1|
|v_input_int_2|10|Quantity 2|
|v_input_int_3|15|Quantity 3|
|v_input_int_4|20|Quantity 4|
|v_input_1|true|Profit Percentage|
|v_input_int_5|2|Pyramiding|


> Source (PineScript)

```pinescript
//@version=5
strategy("EMA_zorba1", shorttitle="zorba_ema", overlay=true)

// Input parameters
qt1 = input.int(5, title="Quantity 1", minval=1)
qt2 = input.int(10, title="Quantity 2", minval=1)
qt3 = input.int(15, title="Quantity 3", minval=1)
qt4 = input.int(20, title="Quantity 4", minval=1)
ema10 = ta.ema(close, 10)
ema20 = ta.ema(close, 20)
ema50 = ta.ema(close, 50)
ema100 = ta.ema(close, 100)
ema200 = ta.ema(close, 200)

// Date range filter
start_date = timestamp(year=2021, month=1, day=1)
end_date = timestamp(year=2024, month=10, day=27)
in_date_range = close_time >= start_date and close_time <= end_date

// Profit condition
profit_percentage = input(1, title="Profit Percentage")  // Adjust this value as needed

// Pyramiding setting
pyramiding = input.int(2, title="Pyramiding", minval=1, maxval=10)

// Buy conditions
buy_condition_1 = in_date_range and close < ema20 and close > ema50 and close < open and close < low[1]
buy_condition_2 = in_date_range and close < ema