```pinescript
/*backtest
start: 2022-11-14 00:00:00
end: 2023-11-20 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © phobo3s

//@version=4
strategy("Dynamic Stop Loss Trail Strategy", shorttitle="DSLS", initial_capital=1000, overlay=true, default_qty_type=strategy.percent_of_equity, pyramiding=5, default_qty_value=20, commission_type=strategy.commission.cash_per_order, commission_value=1, calc_on_every_tick=true)

daysBack = input(defval=120, title="Days Back", type=input.integer)
sellCoeff = input(defval=1.5, title="Selling Coefficent For ATR", type=input.float, minval=0.01, step=0.1)
buyCoeff = input(defval=1.2, title="Buying Coefficent For ATR", type=input.float, minval=0.01, step=0.1)

fromDate = timenow - (daysBack * 24 * 60 * 60 * 1000)
toDate = timenow

ATR = atr(14)
stopLossPoint = ATR *
```