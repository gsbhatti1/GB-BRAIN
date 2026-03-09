``` pinescript
/*backtest
start: 2022-12-04 00:00:00
end: 2023-12-10 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © KivancOzbilgic
//developer: @KivancOzbilgic
//author: @enesyetkin

strategy("Y-Profit Maximizer Strategy with Exit Points", shorttitle="Y-PMax Strategy with Exit Points", overlay=true, default_qty_type=strategy.cash, default_qty_value=10000, initial_capital=10000, currency=currency.USD, commission_value=0.1, commission_type=strategy.commission.percent)
baslik1 = input(title="-------------------- PMax Settings --------------------", defval=false)
src = i
```