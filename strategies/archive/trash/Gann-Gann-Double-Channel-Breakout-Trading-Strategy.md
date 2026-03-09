```pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-01-15 00:00:00
Period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("[VJ] Gann Double Band Buy Sell", overlay=true)
tim = input('375')
//skip buying near upper band and selling near lower band
out1 = security(syminfo.tickerid, tim, open)
out2 = security(syminfo.tickerid, tim, close)

//gann 81, 1 & 81, 2 as channel
length = input(81, minval=1)
src = input(close, title="Source")

Band1 = input(1.0, minval=0.001, maxval=10, step=0.1)
basis = sma(src, length)
dev = Band1 * stdev(src, length)
upper = basis + dev
lower = basis - dev

Band2 = input(2.0, minval=0.001, maxval=10, step=0.1)
dev2 = Band2 * stdev(src, length)
outer_upper = basis + dev2
outer_lower = basis - dev2

// Buy and Sell Logic
longCondition = close > lower and close[1] <= lower and longEntryPrice = out1
if (longCondition)
    strategy.entry("Long", strategy.long)

shortCondition = close < upper and close[1] >= upper and shortEntryPrice = out1
if (shortCondition)
    strategy.exit("Short Exit", "Long", stop=out2)

// Stop Loss and Take Profit
strategy.exit("Long Exit", "Long", stop=outer_lower, limit=outer_upper)
```

This updated Pine Script implements the logic described in the Chinese document. The script sets up two Gann channels based on moving averages and standard deviations to identify trend reversals and execute trades accordingly.