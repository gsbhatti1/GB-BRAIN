``` pinescript
/*backtest
start: 2023-10-01 00:00:00
end: 2023-10-13 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © 03.freeman

//@version=4
strategy("FRAMA strategy", overlay=true, precision=6, initial_capital=1000, calc_on_every_tick=true, pyramiding=0, default_qty_type=strategy.fixed, default_qty_value=10000, currency=currency.EUR)
ma_src = input(title="MA FRAMA Source", type=input.source, defval=close)
ma_frama_len = input(title="MA FRAMA Length", type=input.integer, defval=200)
res = input(title="Resolution", type=input.resolution, defval="1W")
frama_only_fc = input(title="Fractal Adjusted (FRAMA) Only - FC", type=input.bool, defval=false)
frama_only_sc = input(title="Fractal Adjusted (FRAMA) Only - SC", type=input.integer, defval=200)
use_supertrend_enter = input(title="Use supertrend for enter", type=input.bool, defval=false)
use_supertrend_exit = input(title="Use supertrend for exit", type=input.bool, defval=false)
factor = input(title="Factor", type=input.integer, defval=3)
pd = input(title="Pd", type=input.integer, defval=7)
take_profit_points = input(title="Take Profit Points", type=input.bool, defval=false)
stop_loss_points = input(title="Stop Loss Points", type=input.bool, defval=false)
trailing_stop_loss_points = input(title="Trailing Stop Loss Points", type=input.bool, defval=false)
trailing_stop_offset_points = input(title="Trailing Stop Loss Offset Points", type=input.bool, defval=false)
custom_backtesting_dates = input(title="Custom Backtesting Dates", type=input.bool, defval=false)
backtest_start_year = input(title="Backtest Start Year", type=input.integer, defval=2020)
backtest_start_month = input(title="Backtest Start Month", type=input.bool, defval=true)
backtest_start_day = input(title="Backtest Start Day", type=input.bool, defval=true)
backtest_start_hour = input(title="Backtest Start Hour", type=input.bool, defval=false)
backtest_stop_year = input(title="Backtest Stop Year", type=input.integer, defval=2020)
backtest_stop_month = input(title="Backtest Stop Month", type=input.integer, defval=12)
backtest_stop_day = input(title="Backtest Stop Day", type=input.integer, defval=31)
backtest_stop_hour = input(title="Backtest Stop Hour", type=input.integer, defval=23)
```