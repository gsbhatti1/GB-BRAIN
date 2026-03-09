``` pinescript
/*backtest
start: 2024-03-01 00:00:00
end: 2024-03-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Q_D_Nam_N_96

//@version=5
strategy("Long BTC Strategy", overlay=true, 
     default_qty_type = strategy.percent_of_equity, 
     default_qty_value = 100, initial_capital = 1000, currency = currency.USD)

Volume_Q