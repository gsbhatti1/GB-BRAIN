``` pinescript
/*backtest
start: 2022-11-22 00:00:00
end: 2023-11-22 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//Author Josef Tainsh PhD 6Sept2020


//USE STUDY FOR ALERTS WITH AUTO TRADING BOT
//study(title = "Open Close Crossover for BOT Alerts", shorttitle = "OCC for BOT Alerts",overlay = true)
//USE STRATEGY TO FIT THE MOVING AVERAGE AND THE TREND FITS BY MINIMISING LOSS (OR MAXIMISING PROFITS)
//NOT THAT STRATEGIES RARELY SHOW A PROFIT ALSO THE STRATEGIES USE THE CROSS OVER ON THE MOVING AVERAGE TO ENTER A POSITION
strategy(title = "OCC Trend Combo 1 day BTC Moonflag", overlay = true, initial_capital=1000, commission_type=strategy.commission.percent, commission_value=0.2, default_qty_type = strategy.percent_of_equity, default_qty_value=100, pyramiding=0, calc_on_order_fills=false)
//CalcOnTick = true
//calc_on_every_tick = false

// Function for coders who want to offer their users a repainting/no-repainting version of the HTF data.
// It has the advantage of using only one `security()` call for both.
f_security(_symbol, _res, _src, _repaint) => security(_symbol, _res, _src[_repaint ? 0 : barstate.isrealtime ? 1 : 0])[_repaint ? 0 : barstate.isrealtime ? 0 : 1]


/////////////////////////////////////////////////////////////////////////////
// === BASE FUNCTIONS ===
/////////////////////////////////////////////////////////////////////////////
//This function returns true if execution is at the start of a new bar (so the last bar is previous close where alerts are determined)
is_newBar(stratRes) =>
```