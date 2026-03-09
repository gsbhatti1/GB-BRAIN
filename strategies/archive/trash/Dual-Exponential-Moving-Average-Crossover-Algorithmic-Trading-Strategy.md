``` pinescript
/*backtest
start: 2023-01-18 00:00:00
end: 2024-01-24 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © smottybugger 

//@version= 5
strategy("Dual Exponential Moving Average Crossover Algorithmic Trading Strategy", shorttitle="EMA Crossover Strategy", calc_on_order_fills=true, calc_on_every_tick=true, commission_type=strategy.commission.percent, commission_value=0.02, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital=100, margin_long=0, margin_short=0, overlay=true)
// Dual Vortex
period_1 = input(15, "short Time")
period_2 = input(25, "long time")
VMP = math.sum(math.abs(high - low[3]), period_1)
VMM = math.sum(math.abs(low - high[1]), period_2)
STR = math.sum(ta.atr(1), period_1)
STR2 = math.sum(ta.atr(1), period_2)
VXpower= (input(5, "Vortex Power")/10000)*close
shorterV =(VMP / STR)*VXpower
longerV = (VMM / STR2)*VXpower

// MACross
shortlen = input(20, "ShortMa")
longlen = input(29, "LongMA")
shorterMA = ta.sma(close, shortlen)
longerMA = ta.sma(close, longlen)

// Vortex "MACross Stabilized"
Varance = input(1, "Vortex Stabilize")
Vpercent = (Varance / 100)
shortV= ((((shorterMA-close)* Vpercent)+shorterV)/
```