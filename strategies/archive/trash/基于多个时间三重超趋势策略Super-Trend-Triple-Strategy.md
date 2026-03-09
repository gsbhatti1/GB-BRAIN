> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|3|Supertrend 1 Period|
|v_input_int_2|12|Supertrend 1 Multiplier|
|v_input_int_3|2|Supertrend 2 Period|
|v_input_int_4|11|Supertrend 2 Multiplier|
|v_input_int_5|true|Supertrend 3 Period|
|v_input_int_6|10|Supertrend 3 Multiplier|
|v_input_int_7|100|EMA Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-20 00:00:00
end: 2023-12-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Triple Supertrend Strategy", shorttitle = "TSS", overlay = true, pyramiding = 1) // Added pyramiding = 1

// Define input settings for Supertrend indicators
supertrend1_period = input.int(3, title = "Supertrend 1 Period")
supertrend1_multiplier = input.int(12, title = "Supertrend 1 Multiplier")
supertrend2_period = input.int(2, title = "Supertrend 2 Period")
supertrend2_multiplier = input.int(11, title = "Supertrend 2 Multiplier")
supertrend3_period = input.int(1, title = "Supertrend 3 Period")
supertrend3_multiplier = input.int(10, title = "Supertrend 3 Multiplier")
ema_length = input.int(100, title = "EMA Length")

// Calculate Supertrend 1
[supertrend1_upperband, supertrend1_lowerband] = supertrend(supertrend1_period, supertrend1_multiplier)

// Calculate Supertrend 2
[supertrend2_upperband, supertrend2_lowerband] = supertrend(supertrend2_period, supertrend2_multiplier)

// Calculate Supertrend 3
[supertrend3_upperband, supertrend3_lowerband] = supertrend(supertrend3_period, supertrend3_multiplier)

// Calculate EMA
ema = ta.ema(close, ema_length)

// Generate buy signal
buy_signal = close > supertrend1_upperband and close > supertrend2_upperband and close > supertrend3_upperband and close > ema

// Generate sell signal
sell_signal = close < supertrend1_lowerband and close < supertrend2_lowerband and close < supertrend3_lowerband and close < ema

// Place trades
if (buy_signal)
    strategy.entry("Buy", strategy.long)

if (sell_signal)
    strategy.close("Buy")

// Plot Supertrend lines and EMA
plot(supertrend1_upperband, title = "Supertrend 1 Upperband", color=color.blue, style=plot.style_dashed)
plot(supertrend1_lowerband, title = "Supertrend 1 Lowerband", color=color.blue, style=plot.style_dashed)
plot(supertrend2_upperband, title = "Supertrend 2 Upperband", color=color.red, style=plot.style_dashed)
plot(supertrend2_lowerband, title = "Supertrend 2 Lowerband", color=color.red, style=plot.style_dashed)
plot(supertrend3_upperband, title = "Supertrend 3 Upperband", color=color.green, style=plot.style_dashed)
plot(supertrend3_lowerband, title = "Supertrend 3 Lowerband", color=color.green, style=plot.style_dashed)
plot(ema, title = "EMA", color=color.orange)
```

Note: The `supertrend` function and its parameters need to be properly defined or imported for the strategy to work correctly. If `supertrend` is not a built-in function, you may need to define it or use an equivalent function.