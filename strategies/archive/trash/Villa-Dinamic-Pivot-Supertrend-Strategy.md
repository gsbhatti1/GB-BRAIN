```pinescript
/*backtest
start: 2022-02-01 00:00:00
end: 2022-02-11 23:59:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © evillalobos1123

//@version=5
strategy("Villa Dinamic Pivot Supertrend Strategy", overlay=true, calc_on_every_tick = true)

//INPUTS

ema_b = input.bool(false, "Use Simple EMA Filter", group = "Strategy Inputs")
ema_b_ang = input.bool(true, "Use DEMA Angle Filter", group = "Strategy Inputs")
dema_b = input.bool(true, "Use DEMA Filter", group = "Strategy Inputs")
st_sig = input.bool(false, "Take Every Supertrend Signal" , group = "Strategy Inputs")
take_p = input.bool(true, "Stop Loss at Supertrend", group = "Strategy Inputs")
din_tp = input.bool(false, "2 Steps Take Profit", group = "Strategy Inputs")
move_sl = input.bool(true, "Move SL", group = "Strategy Inputs")
sl_atr = input.float(2.5, "Stop Loss ATR Multiplier", group = "Strategy Inputs")
tp_atr = input.float(4, "Take Profit ATR Multiplier", group = "Strategy Inputs")
din_tp_qty = input.int(50, "2 Steps TP qty%", group = "Strategy Inputs")
dema_a_filter = input.float(0, "DEMA Angle Threshold (+ & -)", group = "Strategy Inputs")
dema_a_look = input.int(1, "DEMA Angle Lookback", group = "Strategy Inputs")
dr_test = input.string("All", "Testing", options = ["Backtest", "Forwardtest", "All"], group = "Strategy Inputs")
test_act = input.string('Forex', 'Market', options = ['Forex', 'Stocks'], group = "Strategy Inputs")

not_in_trade = strategy.position_size == 0

//Backtesting date range

start_year = input.int(2021, "Backtesting start year", group = "BT Date Range")
start_month = input.int(1, "Backtesting start month", group = "BT Date Range")
start_date = input.int(1, "Backtesting start day", group = "BT Date Range")
end_year = input.int(2021, "Backtesting end year", group = "BT Date Range")
end_month = input.int(12, "Backtesting end month", group = "BT Date Range")
end_date = input.int(31, "Backtesting end day", group = "BT Date Range")

bt_date_range = (time >= timestamp(syminfo.timezone, start_year,
         start_month, start_date, 0, 0)) and
     (time < timestamp(syminfo.timezone, end_year, end_month, end_date, 0, 0))

//Forward testing date range

start_year_f = input.int(2022, "Forwardtesting start year", group = "FT Date Range")
start_month_f = input.int(1, "Forwardtesting start month", group = "FT Date Range")
start_date_f = input.int(1, "Forwardtesting start day", group = "FT Date Range")
end_year_f = input.int(2022, "Forwardtesting end year", group = "FT Date Range")
end_month_f = input.int(3, "Forwardtesting end month", group = "FT Date Range")
end_date_f = input.int(26, "Forwardtesting end day", group = "FT Date Range")

ft_date_range = (time >= timestamp(syminfo.timezone, start_year_f,
         start_month_f, start_date_f, 0, 0)) and
     (time < timestamp(syminfo.timezone, end_year_f, end_month_f, end_date_f, 0, 0))

//Pivot Supertrend parameters

pvt_st_piv = input.int(200, "PVT ST Pivot Point Period", group = "Pivot Supertrend")
st_atr = input.float(3.0, "PVT ST ATR Factor", group = "Pivot Supertrend")
st_period = input.int(9, "PVT ST ATR Period", group = "Pivot Supertrend")

//D-EMAs parameters

dema_len = input.int(21, "DEMA Len", group = "D-EMAs")
source_dema = input.source(close, "D-EMAs Source", group = "D-EMAs")
ema_1 = ta.ema(close, 21)
ema_2 = ta.ema(close, 50)
ema_3 = ta.ema(close, 200)

//Normal Supertrend parameters

st_atr_period = input.int(20, "ST ATR Period", group = "Normal Supertrend")
source_st = input.source(hl2, "ST Supertrend Source", group = "Normal Supertrend")
multiplier_st = input.float(2.5, "ST ATR Multiplier", group = "Normal Supertrend")

//Strategy logic

if (bt_date_range or ft_date_range)
    // Backtest and Forwardtest logic
else if (not_in_trade) 
    // Entry conditions
    if (ema_b and ta.crossover(ema_1, ema_2) and ta.crossover(ema_2, ema_3))
        strategy.entry("Long", strategy.long)

    if (dema_b)
        angle = ta.angle(dema_a_filter, dema_a_look)
        if (angle > 0.5 or angle < -0.5)
            strategy.entry("Long", strategy.long)

    if (st_sig and not st_prev and ta.crossover(source_st, ta.sma(source_st, st_period) * (1 + multiplier_st)))
        strategy.entry("Long", strategy.long)

if take_p
    // Take Profit logic
    tp_qty = din_tp_qty / 100
    if (strategy.position_size > 0)
        target_price = close - (close * (tp_atr / 100))
        strategy.exit("Take Profit", from_entry="Long", limit=target_price)

if move_sl
    // Stop Loss logic
    sl_qty = din_tp_qty / 100
    if (strategy.position_size > 0)
        stop_loss_level = close + (close * (sl_atr / 100))
        strategy.exit("Stop Loss", from_entry="Long", stop=stop_loss_level)

```

> Source (PineScript)