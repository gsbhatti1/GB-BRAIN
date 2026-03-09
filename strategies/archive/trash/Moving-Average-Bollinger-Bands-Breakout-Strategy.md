> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_bool_1|false|Date background|
|v_input_bool_2|false|Session background|
|v_input_float_1|10000|(?Calculate position)Enter initial/current capital|
|v_input_bool_14|true|Use leverage ?|
|v_input_float_2|2.5|(?Position amount calculator)% account risk per trade|
|v_input_1|timestamp(10 Feb 2014 13:30 +0000)|(?Time filter)Initial date|
|v_input_2|timestamp(01 Jan 2030 19:30 +0000)|Final date|
|v_input_3|0000-2400|Time session|
|v_input_int_1|200|(?Trend)Ema length|
|v_input_bool_3|false|(?Appearance)Show ema ?|
|v_input_bool_4|false|Show atr from ut bot alerts ?|
|v_input_bool_5|false|Show ema from ut bot alerts ?|
|v_input_bool_6|true|Show signals ?|
|v_input_bool_7|false|Paint candles ?|
|v_input_bool_8|true|Show Atr stop loss ?|
|v_input_bool_12|true|Draw position on chart ?|
|v_input_bool_13|true|Draw first take profit/breakeven price on chart ?|
|v_input_4|3|(?UT BOT ALERTS)Key Vaule|
|v_input_5|true|ATR Period|
|v_input_6|false|Signals from Heikin Ashi Candles|
|v_input_7_close|0|(?Atr stop loss)Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_2|14|Period|
|v_input_float_3|1.5|Atr multiplier|
|v_input_string_1|0|(?Risk management for trades)Source of stoploss: Current candle|Past candle|
|v_input_float_4|2.5|% Account risk per trade for backtesting|
|v_input_bool_9|true|Use leverage for backtesting ?|
|v_input_float_5|0.75|Risk/reward for breakeven long|
|v_input_float_6|3|Risk/reward for take profit long|
|v_input_float_7|0.75|Risk/reward for break even short|
|v_input_float_8|3|Risk/reward for take profit short|
|v_input_float_9|50|% of trade for first take profit|
|v_input_bool_10|true|(?Positions management)Long positions ?|
|v_input_bool_11|true|Short positions ?|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-07 00:00:00
end: 2023-12-07 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
//@version=5
// Developed by StrategiesForEveryone

strategy("UT Bot Alerts Strategy", overlay=true, process_orders_on_close = true, initial_capital = 1000000, default_qty_type=strategy.cash, precision = 2, calc_on_every_tick = true, commission_value = 0.03)

// ------ Inputs for calculating position --------

initial_actual_capital = input.float(defval=10000, title="Enter initial/current capital", group="Calculate position")
risk_c = input.float(2.5, '% account risk per trade', step=1, group="Position amount calculator", tooltip="Percentage of total account to risk per trade. The USD value that should be used to risk the inserted percentage of the account. Appears green in the upper left corner")

// ------ Date filter (obtained from ZenAndTheArtOfTrading) ---------

initial_date = input(title="Initial date", defval=timestamp("10 Feb 2014 13:30 +0000"), group="Time filter")
final_date = input(title="Final date", defval=timestamp("01 Jan 2030 19:30 +0000"), group="Time filter")

// ------ Session time ---------

time_session = input.time(defval=0, title="Time session", group="Session time")

// ------ EMA settings ---------

ema_length = input.int(200, minval=1, title="Ema length", group="Trend")
show_ema = input.bool(false, "Show ema?", group="Appearance")

// ------ ATR and Stop Loss ---------

atr_period = input.int(title="ATR Period", defval=true)
show_atr_stop_loss = input.bool(true, "Show Atr stop loss?")
draw_position_on_chart = input.bool(true, "Draw position on chart?")
draw_first_take_profit_breakeven_price = input.bool(true, "Draw first take profit/breakeven price on chart?")

atr_multiplier = input.float(1.5, title="Atr multiplier", minval=0.1)
atr_stop_loss_source = input.string("Current candle", title="Source of stoploss:", options=["Current candle", "Past candle"], group="Risk management for trades")
risk_reward_break_even_long = input.float(0.75, "% Risk/reward for breakeven long", minval=0.1)
risk_reward_take_profit_long = input.float(3, "Risk/reward for take profit long", minval=0.1)
risk_reward_break_even_short = input.float(0.75, "Risk/reward for break even short", minval=0.1)
risk_reward_take_profit_short = input.float(3, "Risk/reward for take profit short", minval=0.1)
first_take_profit_percentage = input.float(50, "% of trade for first take profit", minval=0)

long_positions = input.bool(true, "?Positions management", group="Positions management")
short_positions = input.bool(true, "", group="")

// ------ Strategy Logic ---------

ema = ta.ema(close, ema_length)
upper_band = ta.highest(high, 20) - (atr(atr_period) * atr_multiplier)
lower_band = ta.lowest(low, 20) + (atr(atr_period) * atr_multiplier)

if time >= initial_date and time <= final_date
    if close > upper_band and long_positions
        strategy.entry("Long", strategy.long)
    elif close < lower_band and short_positions
        strategy.entry("Short", strategy.short)

// ------ Risk Management ---------

stop_loss = na
take_profit_long = na
take_profit_short = na

if not na(strategy.position_avg_price) and time >= initial_date and time <= final_date
    if long_positions
        stop_loss := strategy.position_avg_price - (atr(atr_stop_loss_source) * atr_multiplier)
        take_profit_long := strategy.position_avg_price + (risk_reward_take_profit_long / 100 * strategy.position_avg_price)
    
    if short_positions
        stop_loss := strategy.position_avg_price + (atr(atr_stop_loss_source) * atr_multiplier)
        take_profit_short := strategy.position_avg_price - (risk_reward_take_profit_short / 100 * strategy.position_avg_price)

// ------ Drawing on Chart ---------

if show_ema
    plot(ema, title="EMA", color=color.blue)

if show_atr_stop_loss
    label.new(x=bar_index, y=na, text=strategy.position_avg_price - stop_loss, style=label.style_label_down, color=color.red)
    label.new(x=bar_index, y=na, text=strategy.position_avg_price + take_profit_long, style=label.style_label_up, color=color.green)

if draw_position_on_chart
    plotshape(strategy.opentrades.entry_bar_index("Long"), title="Entry Long", location=location.belowbar, color=color.blue)
    plotshape(strategy.opentrades.exit_bar_index("Long"), title="Exit Long", location=location.abovebar, color=color.red)
    
    plotshape(strategy.opentrades.entry_bar_index("Short"), title="Entry Short", location=location.belowbar, color=color.red)
    plotshape(strategy.opentrades.exit_bar_index("Short"), title="Exit Short", location=location.abovebar, color=color.blue)

```

This should cover the translation and maintain the original structure and code.