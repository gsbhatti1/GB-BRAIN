``` pinescript
/*backtest
start: 2022-11-10 00:00:00
end: 2023-11-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © zxcv55602
//@version=4
strategy(shorttitle="BB+EMA", title="Bollinger Bands", overlay=true)
date1 = input(title="Start Date", type=input.time, defval=timestamp("2020-01-01T00:00:00"))
date2 = input(title="Stop Date", type=input.time, defval=timestamp("2030-01-01T00:00:00"))
length = input(40, minval=1)
src = input(close, title="Source")
mult = input(2.0, title="StdDev", step=0.1)
basis = sma(src, length)
dev = mult * stdev(src, length)
upper = basis + dev
lower = basis - dev
//offset = input(0, "Of
```