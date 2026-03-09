``` pinescript
/*backtest
start: 2023-08-26 00:00:00
end: 2023-09-07 00:00:00
period: 12h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © str1nger
//@version=4

// strategy(title="BTC - 4hr - Long/Short", shorttitle="BTC - 4hr - Long/Short", overlay=true, initial_capital=1000, default_qty_type=strategy.percent_of_equity, default_qty_value=75,commission_type=strategy.commission.percent, commission_value=0.075)//////<---Uses a percentage of starting equity

//DATE RANGE//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
startDate = input(title="Start Date", type=input.integer,
     defval=1, minval=1, maxval=31)
startMonth = input(title="Start Month", type=input.integer,
     defval=1, minval=1, maxval=12)
startYear = input(title="Start Year", type=input.integer,
     defval=2020, minval=2000, maxval=2100)
endDate = input(title="End Date", type=input.integer,
     defval=1, minval=1, maxval=31)
endMonth = input(title="End Month", type=input.integer,
     defval=12, minval=1, maxval=12)
endYear = input(title="End Year", type=input.integer,
     defval=2021, minval=2000, maxval=2100)

inDateRange =  true


//EMAs//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//LONG
//11,33,3,40
lof= input(11, title="Long Open - Fast", step=1)
los= input(33, title="Long Open - Slow", step=1)
lcf= input(3, title="Long Close - Fast", step=1)
lcs= input(40, title="Long Close - Slow", step=1)
ema_long_open_fast = ema(close, lof)
ema_long_open_slow = ema(close, los)
ema_long_close_fast= ema(close, lcf)
ema_long_close_slow = ema(close, lcs)
//SHORT
//5,11,4,7
sof= input(5, title="Short Open - Fast", step=1)
sos= input(11, title="Short Open - Slow", step=1)
scf= input(4, title="Short Close - Fast", step=1)
scs= input(7, title="Short Close - Slow", step=1)
ema_short_open_fast = ema(close, sof)
ema_short_open_slow = ema(close, sos)
ema_short_close_fast = ema(close, scf)
ema_short_close_slow = ema(close, scs)


//CONDITIONS///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//LONG
openlong = crossover(ema_long_open_fast, ema_long_open_slow)
closelong = crossover(ema_long_close_slow, ema_long_close_fast)
//1.7%
long_loss_percent = input(title="Long Stop Loss (%)", type=input.float, minval=0.1, maxval=10, step=0.1, defval=1.7)
short_loss_percent = input(title="Short Stop Loss (%)", type=input.float, minval=0.1, maxval=10, step=0.1, defval=0.4)
//LONG STOP LOSS
long_stop_loss = valuewhen(inDateRange, close, 0) * (1 - long_loss_percent / 100)
//SHORT STOP LOSS
short_stop_loss = valuewhen(inDateRange, close, 0) * (1 + short_loss_percent / 100)
//ENTRY
long_entry = na(openlong) ? na : valuewhen(openlong, close, 0)
short_entry = na(closelong) ? na : valuewhen(closelong, close, 0)
//EXIT
long_exit = na(closelong) ? na : valuewhen(closelong, close, 0)
short_exit = na(openlong) ? na : valuewhen(openlong, close, 0)
//POSITION MANAGEMENT
strategy.entry("Long", strategy.long, when=openlong)
strategy.exit("Close Long", "Long", stop=long_stop_loss, limit=long_exit)
strategy.entry("Short", strategy.short, when=closelong)
strategy.exit("Close Short", "Short", stop=short_stop_loss, limit=short_exit)
```

This script implements the described strategy, including date range inputs, EMA parameters, and stop loss conditions.