``` pinescript
/*backtest
start: 2023-09-23 00:00:00
end: 2023-10-23 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
// Created by ChaoZhang
strategy(title="CamarillaStrategyV1", shorttitle="CZ_Camarilla_StrategyV1", overlay=true)

// EMA
EMA = ema(close, 8)

// Camarilla Channels
pivot = (high + low + close) / 3.0
range = high - low
h5 = close + (high - low) * 1.1 / 2.0
h4 = close + (high - low) * 1.1 / 4.0
h3 = close + (high - low) * 1.1 / 6.0
h2 = close + (high - low) * 1.1 / 12.0
h1 = close + (high - low) * 1.1 / 24.0
l1 = close - (high - low) * 1.1 / 24.0
l2 = close - (high - low) * 1.1 / 12.0
l3 = close - (high - low) * 1.1 / 6.0
l4 = close - (high - low) * 1.1 / 4.0
h6 = h5 + 1.168 * (h5 - h4)
l5 = close - (h5 - close)
l6 = close - (h6 - close)

// Daily line breaks
//sopen = request.security(syminfo.tickerid, "D", open [1])
//shigh = request.security(syminfo.tickerid, "D", high [1])
//slow = request.security(syminfo.tickerid, "D", low [1])
//sclose = request.security(syminfo.tickerid, "D", close [1])

// Color
//dcolor = sopen != sopen[1] ? na : black
//dcolor1 = sopen != sopen[1] ? na : red
//dcolor2 = sopen != sopen[1] ? na : green

// Daily Pivots
dtime_pivot = request.security(syminfo.tickerid, 'D', pivot[1])
dtime_h6 = request.security(syminfo.tickerid, 'D', h6[1])
dtime_h5 = request.security(syminfo.tickerid, 'D', h5[1])
dtime_h4 = request.security(syminfo.tickerid, 'D', h4[1])
dtime_h3 = request.security(syminfo.tickerid, 'D', h3[1])
dtime_h2 = request.security(syminfo.tickerid, 'D', h2[1])
dtime_h1 = request.security(syminfo.tickerid, 'D', h1[1])
dtime_l1 = request.security(syminfo.tickerid, 'D', l1[1])
dtime_l2 = request.security(syminfo.tickerid, 'D', l2[1])
dtime_l3 = request.security(syminfo.tickerid, 'D', l3[1])
dtime_l4 = request.security(syminfo.tickerid, 'D', l4[1])

// Strategy Logic
longCondition = close > h4 and open < h4
shortCondition = close < l4 and open > l4

// Enter long position
if (longCondition)
    strategy.entry("Long", strategy.long)
    // Stop Loss
    strategy.exit("Long Exit", from_entry="Long", stop=dtime_pivot)
    // Take Profit
    strategy.exit("Long TP", from_entry="Long", limit=dtime_h5)

// Enter short position
if (shortCondition)
    strategy.entry("Short", strategy.short)
    // Stop Loss
    strategy.exit("Short Exit", from_entry="Short", stop=dtime_pivot)
    // Take Profit
    strategy.exit("Short TP", from_entry="Short", limit=dtime_l5)

// Plot EMA and Camarilla Channels
plot(EMA, color=color.blue, title="EMA")
plot(h5, color=color.red, title="H5")
plot(h4, color=color.orange, title="H4")
plot(h3, color=color.yellow, title="H3")
plot(h2, color=color.green, title="H2")
plot(h1, color=color.cyan, title="H1")
plot(l1, color=color.blue, title="L1")
plot(l2, color=color.orange, title="L2")
plot(l3, color=color.yellow, title="L3")
plot(l4, color=color.green, title="L4")
plot(h6, color=color.red, title="H6")
plot(l5, color=color.cyan, title="L5")
plot(l6, color=color.green, title="L6")

// Plot daily pivots
plot(dtime_pivot, color=color.red, title="Daily Pivot")
plot(dtime_h6, color=color.blue, title="H6")
plot(dtime_h5, color=color.orange, title="H5")
plot(dtime_h4, color=color.yellow, title="H4")
plot(dtime_h3, color=color.green, title="H3")
plot(dtime_h2, color=color.cyan, title="H2")
plot(dtime_h1, color=color.red, title="H1")
plot(dtime_l1, color=color.blue, title="L1")
plot(dtime_l2, color=color.orange, title="L2")
plot(dtime_l3, color=color.yellow, title="L3")
plot(dtime_l4, color=color.green, title="L4")
```