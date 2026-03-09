``` pinescript
/*backtest
start: 2023-04-22 00:00:00
end: 2024-04-27 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI Trend Reversal", overlay=true, max_bars_back = 4999, calc_on_every_tick = false)


// INPUTS 
rsi_length = input.int(8, title="RSI Length")
multiplier = input.float(1.5, title="Multiplier")
delay = input.bool(true, title="Delay to prevent idealization")
min_diff = input.float(10, title="Minimum Difference")
source = input.source(close, title="Source Input: close|high|low|open|hl2|hlc3|hlcc4|ohlc4")


// FUNCTIONS 
highest_custom(high, length) =>
    highest_price = ta.highest(high, length)
    highest_price

lowest_custom(low, length) =>
    lowest_price = ta.lowest(low, length)
    lowest_price


// CALCULATIONS
rsi = ta.rsi(source, rsi_length)
atr = ta.atr(14)

upper_band = highest_custom(high, rsi_length) * (1 - (atr / close + 1 / (rsi[2] * multiplier)))
lower_band = lowest_custom(low, rsi_length) * (1 + (atr / close + 1 / (rsi[2] * multiplier)))

if (delay)
    upper_band := upper_band
    lower_band := lower_band


// ENTRY AND EXIT 
long_condition = ta.crossover(close, upper_band)
short_condition = ta.crossunder(close, lower_band)

if (long_condition)
    strategy.entry("Long", strategy.long)
if (short_condition)
    strategy.entry("Short", strategy.short)


// PLOTTING
plot(upper_band, color=color.red, title="Upper Band")
plot(lower_band, color=color.blue, title="Lower Band")


// END OF CODE
```

This code snippet defines the RSI Trend Reversal strategy with the specified inputs and logic. It includes the necessary functions for calculating the upper and lower bands based on the user-defined parameters and plots them on the chart.