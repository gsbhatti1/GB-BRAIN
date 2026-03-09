``` pinescript
/*backtest
start: 2022-12-01 00:00:00
end: 2023-12-07 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © mohanee

//@version=4
//ADX strategy
SmoothedTrueRange=0.00
SmoothedDirectionalMovementPlus=0.00
SmoothedDirectionalMovementMinus=0.00


strategy(title="ADX Crossover Trend Trading Strategy", overlay=false, pyramiding=3, default_qty_type=strategy.fixed, default_qty_value=3, initial_capital=10000, currency=currency.USD)

len = input(11, title="ADX Length", minval=1)
threshold = input(30, title="Threshold", minval=5)

fastEma=input(13, title="Fast EMA",minval=1, maxval=50)
slowEma=input(55, title="Slow EMA",minval=10, maxval=200)
stopLoss =input(8, title="Stop Loss",minval=1)   //


TrueRange = max(max(high-low, abs(high-nz(close[1]))), abs(low-nz(close[1])))
DirectionalMovementPlus = high-nz(high[1]) > nz(low[1])-low ? max(high-nz(high[1]), 0): 0
DirectionalMoveme
```