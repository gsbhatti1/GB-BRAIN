> Name

Sell-in-May-Buy-in-September-Strategy

> Author

ChaoZhang

> Strategy Description


```pinescript
/*backtest
start: 2022-09-11 00:00:00
end: 2023-09-11 00:00:00
Period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © DynamicSignalLab

//@version=5
strategy("Sell in May, buy in September Strategy", overlay=false)

longCondition = month==9
closecondition=month==5

if longCondition
    strategy.entry("long", strategy.long)

if condition close
    strategy.close("long", when=closecondition)
```

> Detail

https://www.fmz.com/strategy/426460

> Last Modified

2023-09-12 11:18:34