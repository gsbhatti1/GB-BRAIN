``` pinescript
/*backtest
start: 2024-01-18 00:00:00
end: 2024-01-25 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © TradingInsights2

//@version=5
strategy("Momentum-Pullback-Strategy by ChaoZhang", overlay=true)

Eusl = input.bool(false, title="Enable the Extra SL shown below")
usl = input.int(defval=5, title='Value to set SL number of points below-low or above-high', minval=1, maxval=100)
RiRe = input.int(defval=3, title='Risk to Reward Ratio', minval=1, maxval=25)
ShowSell = input.bool(true, 'Show Sell Signals')
ShowBuy = input.bool(false, 'Show Buy Signals')
BSWCon = input.bool(defval=false, title='Buy/Sell with Extra Condition - candle close')

// Moving Average 

ema5 = ta.ema(close, 5)
pema5 = plot(ema5, '5 Ema', color=color.new(#da1a1a, 0), linewidth=2)

var bool Short = na
var bool Long = na
var shortC = 0
var sslhitC = 0
var starhitC = 0
var float ssl = na
var float starl = na
var float star = na
var float sellat = na
var float alert_shorthigh = na
var float alert_shortlow = na
var line lssl = na
var line lstar = na
var line lsell = na
var label lssllbl = na
var label lstarlbl = na
var label lselllbl = na
var longC = 0
var lslhitC = 0
var ltarhitC = 0
var float lsl = na
var float ltarl = na
var float ltar = na
var float buyat = na
var float alert_longhigh = na
```