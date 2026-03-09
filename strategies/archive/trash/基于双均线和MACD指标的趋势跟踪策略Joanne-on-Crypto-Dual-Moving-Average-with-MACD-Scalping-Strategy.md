> Name

Dual Moving Average with MACD Scalping Strategy on Crypto - Joanne-on-Crypto-Dual-Moving-Average-with-MACD-Scalping-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/b82e03f96ff5eb4862.png)
[trans]


## Overview

The core idea of this strategy is to combine dual moving averages and the MACD indicator to determine the trend direction for trend-following trading. When the short-term moving average crosses above the long-term moving average, it signals a bullish opportunity. Conversely, when the short-term moving average crosses below the long-term moving average, it signals a bearish opportunity. The MACD histogram is used to determine specific entry and exit points: going long when it crosses above 0 and going short when it crosses below 0.

## Strategy Logic

1. Calculate the fast EMA (12-day), slow EMA (26-day), and signal EMA (9-day) of MACD.
2. Calculate the MACD histogram (fast EMA - slow EMA) and the MACD signal line (9-day EMA of the MACD histogram).
3. Calculate the 50-day and 200-day MAs as trend indicators.
4. A MACD histogram crossing above 0 is a bullish signal, while a MACD histogram crossing below 0 is a bearish signal.
5. A fast EMA crossing above the slow EMA, combined with a short-term MA crossing above a long-term MA, gives a bullish signal.
6. A fast EMA crossing below the slow EMA, combined with a short-term MA crossing below a long-term MA, gives a bearish signal.
7. Limit the number of trades after each MA crossover using the `Max trades after EMA cross` parameter.
8. Use stop loss and take profit to exit trades.

## Advantages

1. Dual MAs determine the overall trend to avoid counter-trend trades.
2. MACD identifies entry and exit points to capture trend shifts.
3. Combining dual MAs and MACD provides good entry timing in the direction of the trend.
4. Limit the number of trades after crossovers to avoid chasing trends.
5. Stop loss and take profit mechanisms control risk.
6. Parameters can be optimized for better performance.

## Risks

1. Incorrect trend determination can lead to counter-trend losses. Widen the MA difference requirement to firmly establish the trend.
2. MACD signals can lag price action, leading to premature or late entries. Adjust MACD parameters or add filters.
3. Improper stop loss and take profit levels can result in excessive stops or insufficient profits. Requires parameter optimization for each instrument.
4. Parameter optimization can be challenging. Different parameter combinations may be needed for different products and timeframes. Extensive upfront testing is required.

## Enhancement Opportunities

1. Test other trend indicators like KD to determine the overall trend.
2. Add other indicators to filter MACD signals, such as Bollinger Bands or ATR for stop losses.
3. Optimize stop loss and take profit parameters for each product.
4. Use walkforward and random optimization methods to find better parameter combinations.
5. Add mechanisms to reduce trade frequency, such as MACD zones around the zero line.
6. Automate parameter and combination optimization across multiple products.

## Summary

This strategy combines the strengths of dual moving averages for trend direction and MACD for entry timing to create a robust trend-following system. Additional performance gains are possible through parameter optimization and indicator combinations. Overall, it has strong risk management and profit potential and is worth considering for live trading. However, parameter testing is still required for each product to ensure robustness.

||

## Overview

The core idea of this strategy is to combine dual moving averages and the MACD indicator to determine the trend direction for trend-following trading. When the fast MA crosses above the slow MA, it signals an uptrend opportunity. When the fast MA crosses below the slow MA, it signals a downtrend opportunity. The MACD histogram is used to determine specific entry and exit points by going long when it crosses above 0 and going short when it crosses below 0.

## Strategy Logic

1. Calculate the fast EMA (12-day), slow EMA (26-day), and signal EMA (9-day) of MACD.
2. Calculate the MACD histogram (fast EMA - slow EMA) and the MACD signal line (9-day EMA of the MACD histogram).
3. Calculate the 50-day and 200-day MAs as trend indicators.
4. A MACD histogram crossing above 0 is the bullish signal, and crossing below 0 is the bearish signal.
5. A fast EMA crossing above the slow EMA, combined with a short-term MA crossing above a long-term MA, gives a bullish signal.
6. A fast EMA crossing below the slow EMA, combined with a short-term MA crossing below a long-term MA, gives a bearish signal.
7. Limit the number of trades after each MA crossover using the `Max trades after EMA cross` parameter.
8. Use stop loss and take profit to exit trades.

## Advantages

1. Dual MAs determine the overall trend to avoid counter-trend trades.
2. MACD identifies entry and exit points to capture trend shifts.
3. Combining dual MAs and MACD provides good entry timing in the direction of the trend.
4. Limit the number of trades after crossovers to avoid chasing trends.
5. Stop loss and take profit mechanisms control risk.
6. Parameters can be optimized for better performance.

## Risks

1. Incorrect trend determination can lead to counter-trend losses. Widen the MA difference requirement to firmly establish the trend.
2. MACD signals can lag price action, leading to premature or late entries. Adjust MACD parameters or add filters.
3. Improper stop loss and take profit levels can result in excessive stops or insufficient profits. Requires parameter optimization for each instrument.
4. Parameter optimization can be challenging. Different parameter combinations may be needed for different products and timeframes. Extensive upfront testing is required.

## Enhancement Opportunities

1. Test other trend indicators like KD to determine the overall trend.
2. Add other indicators to filter MACD signals, such as Bollinger Bands or ATR for stop losses.
3. Optimize stop loss and take profit parameters for each product.
4. Use walkforward and random optimization methods to find better parameter combinations.
5. Add mechanisms to reduce trade frequency, such as MACD zones around the zero line.
6. Automate parameter and combination optimization across multiple products.

## Summary

This strategy combines the strengths of dual moving averages for trend direction and MACD for entry timing to create a robust trend-following system. Additional performance gains are possible through parameter optimization and indicator combinations. Overall, it has strong risk management and profit potential and is worth considering for live trading. However, parameter testing is still required for each product to ensure robustness.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|50|EMA Trend 1|
|v_input_2|200|EMA Trend 2|
|v_input_3|12|MACD Fast Length|
|v_input_4|26|MACD Slow Length|
|v_input_int_1|9|MACD Signal Smoothing|
|v_input_5_close|0|MACD Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_string_1|0|Tick Highlight: Moving average|Fixed value|
|v_input_string_2|0|Tick Source: Highest bar|Average|Last bar|
|v_input_int_2|72|Upticks Avg. Length|
|v_input_int_3|72|Downticks Avg. Length|
|v_input_float_1|2|Ticks Avg. Multiplier|
|v_input_int_4|3|Max trades after EMA cross|
|v_input_6|30|Fixed Uptick Value|
|v_input_7|-30|Fixed Downtick Value|
|v_input_float_2|0.005|Limit Price Difference|
|v_input_float_3|0.005|Take Profit|
|v_input_float_4|0.004|Stop Loss|
|v_input_float_5|100|Min EMA difference|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-10-02 00:00:00
end: 2023-11-01 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title="ComiCo - Joel on Crypto - MACD Scalping", shorttitle="ComiCo - Joel on Crypto - MACD Scalping")
// Getting inputs
slow_length1 = input(title="EMA Trend 1", defval=50)
slow_length2 = input(title="EMA Trend 2 ", defval=200)
fast_length = input(title="MACD Fast Length", defval=12)
slow_length = input(title="MACD Slow Length", defval=26)
signal_length = input.int(title="MACD Signal Smoothing",  minval = 1, maxval = 50, defval=9)
source = input(source(close), title="MACD Source")
i_switch = input.string(title="Tick Highlight", defval="Moving average")
i_tick_source = input.string(title="Tick Source", defval="Last bar")
i_ua_length = input.int(title="Upticks Avg. Length", defval=72)
i_da_length = input.int(title="Downticks Avg. Length", defval=72)
i_avg_multiplier = input.float(title="Ticks Avg. Multiplier", defval=2.0)
max_trades_after_ema_cross = input.int(title="Max trades after EMA cross", defval=3)
fixed_up_tick_value = input.float(title="Fixed Uptick Value", defval=30.0)
fixed_down_tick_value = input.float(title="Fixed Downtick Value", defval=-30.0)
price_diff_limit = input.float(title="Limit Price Difference", defval=0.005)
take_profit = input.float(title="Take Profit", defval=0.005)
stop_loss = input.float(title="Stop Loss", defval=0.004)
min_ema_difference = input.float(title="Min EMA Difference", defval=100.0)

// Calculate EMA
ema1 = ta.ema(close, slow_length1)
ema2 = ta.ema(close, slow_length2)
ema_signal = ta.ema(close, signal_length)

// Calculate MACD
macd = ema1 - ema2
macd_signal = ta.ema(macd, signal_length)
macd_hist = macd - macd_signal

// Trend signals
bullish_signal = ta.crossover(macd_hist, 0)
bearish_signal = ta.crossunder(macd_hist, 0)

// Trade logic
var int trade_counter = 0
if bullish_signal
    if trade_counter < max_trades_after_ema_cross
        trade_counter := trade_counter + 1
        strategy.entry("Bullish", strategy.long)
if bearish_signal
    if trade_counter < max_trades_after_ema_cross
        trade_counter := trade_counter + 1
        strategy.entry("Bearish", strategy.short)

// Stop loss and take profit
if strategy.position_size > 0
    strategy.exit("Take Profit Long", "Bullish", stop=close + take_profit * close, limit=close + stop_loss * close)
if strategy.position_size < 0
    strategy.exit("Take Profit Short", "Bearish", stop=close - take_profit * close, limit=close - stop_loss * close)
```