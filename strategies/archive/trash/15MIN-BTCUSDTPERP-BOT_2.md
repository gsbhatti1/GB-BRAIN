```pinescript
/*backtest
start: 2022-05-20 00:00:00
end: 2022-06-18 23:59:00
period: 45m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © ChaoZhang

//@version=4
strategy("15MIN-BTCUSDTPERP-BOT", overlay=true, pyramiding=1, initial_capital = 10000, default_qty_type=strategy.percent_of_equity, default_qty_value = 100, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0)

//SOURCE ==================================================================================================================================================================================================================================================================

src = input(ohlc4)

// INPUTS ==================================================================================================================================================================================================================================================================

v_input_1_ohlc4 = input(0, "Source", type=input.source)
v_input_2 = input(true, "AVERAGE DIRECTIONAL INDEX")
v_input_3 = input(0, "ADX OPTION: MASANAKAMURA, CLASSIC")
v_input_4 = input(11, "ADX LENGTH")
v_input_5 = input(12, "ADX THRESHOLD")
v_input_6 = input(13, "Range Filter length")
v_input_7 = input(true, "Range Filter mult")
v_input_8 = input(false, "SAR Start")
v_input_9 = input(0.006, "SAR Increment")
v_input_10 = input(true, "SAR Maximum")
v_input_11 = input(true, "SAR Point Width")
v_input_12 = input(70, "RSI length")
v_input_13_close = input(0, "RSI Source: close", type=input.source)
v_input_14 = input(10, "TWAP Smoothing")
v_input_15 = input(0, "TWAP Timeframe")
v_input_16_close = input(0, "JMA Source: close", type=input.source)
v_input_17 = input("", "JMA Resolution")
v_input_18 = input(false, "JMA Allow Repainting?")
v_input_19 = input(4, "JMA Length")
v_input_20 = input(25, "MACD Fast Length")
v_input_21 = input(50, "MACD Slow Length")
v_input_22 = input(9, "MACD Signal Smoothing")
v_input_23 = input(45, "Delta Length")
v_input_24 = input(100, "Volume Weight Length")
v_input_25 = input(0, "Volume Weight Type: SMA, EMA, HMA, WMA, DEMA")
v_input_26 = input(1.5, "Volume To Trigger Signal")
v_input_27 = input(51, "MA Length")
v_input_28 = input(5, "AvgType")
v_input_29 = input(45, "Momentum Length")
v_input_30 = input(12, "Momentum Calc length")
v_input_31 = input(9, "Momentum Smooth length")
v_input_32 = input(true, "BACKTEST")
v_input_33 = input(180, "BACKTEST DAYS")
v_input_34 = input(0, "ENTRY TYPE: % EQUITY, CASH, CONTRACTS")
v_input_35 = input(3.6, "Stop Loss % [plotshape]")
v_input_36 = input(0.8, "Take Profit % [plotshape]")
v_input_37 = input(3.6, "stop loss [BT]")
v_input_38 = input(100, "qty percent")
v_input_39 = input(0.8, "Take profit [BT]")

// INDICATORS ==============================================================================================================================================================================================================================================================

adx = ta.adx(src, v_input_4, v_input_5)
range_filter = ta.rma(src, v_input_6) * (v_input_7 ? 1 : -1)
sar = ta.sar(v_input_8 ? close : na, v_input_9, v_input_10, v_input_11 ? 2 : 1)
rsi = ta.rsi(src, v_input_12, v_input_13_close ? close : na)
twap = ta.wma(src, v_input_14 * (v_input_15 ? 60 : 5), v_input_15 ? 60 : 5)
jma = strategy.jma(v_input_16_close ? close : na, v_input_17, v_input_18, v_input_19, "EMA")
macd_line = ta.macd(src)[1]
macd_signal = ta.macd_signal(src)[1]
delta_length = v_input_23
volume_delta = ta.cvdelta(v_input_24)
volume_weight = strategy.rwma(volume_delta, v_input_25 ? 0 : v_input_26, v_input_27, v_input_28, "EMA")
speed_ma = ta.sma(src, v_input_29, v_input_30, v_input_31)
stochastic_k, stochastic_d = ta.stoch(close, high, low, v_input_32, v_input_33)

// STRATEGY LOGIC =======================================================================================================================================================================================================================================================

long_condition = adx > 25 and range_filter < rsi[1] and not sar and macd_line > macd_signal and volume_weight > v_input_26
short_condition = adx < -25 and range_filter > rsi[1] and not sar and macd_line < macd_signal and volume_weight > v_input_26

if (long_condition)
    strategy.entry("Long", strategy.long)

if (short_condition)
    strategy.entry("Short", strategy.short)

// STOP LOSS AND TAKE PROFIT ================================================================================================================================================================================================================================================

stop_loss = 0.03 * (v_input_38 ? close : na)
take_profit = 0.015 * (v_input_39 ? close : na)

strategy.exit("Stop Loss", "Long", stop=stop_loss, limit=na)
strategy.exit("Take Profit", "Long", stop=na, limit=take_profit)

// PLOTTING ================================================================================================================================================================================================================================================================

plotshape(series=adx > 25 and range_filter < rsi[1] and not sar and macd_line > macd_signal and volume_weight > v_input_26, location=location.belowbar, color=color.green, style=shape.labelup, text="Long Signal")
plotshape(series=adx < -25 and range_filter > rsi[1] and not sar and macd_line < macd_signal and volume_weight > v_input_26, location=location.abovebar, color=color.red, style=shape.labeldown, text="Short Signal")
```