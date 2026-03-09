``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title="Triple SMA with Entries Based on Close Prices", shorttitle="TRIPLE SMA STRATEGY", overlay=true) // resolution=""
len = input(200, minval=1, title="SMA 1 length")
len1 = input(400, minval=1, title="SMA 2 length")
len2 = input(600, minval=1, title="SMA 3 length")
src = input(close, title="Source")
////////////////////////////////////////////
smma = 0.0
smma := na(smma[1]) ? sma(src, len) : (smma[1] * (len - 1) + src) / len

up = smma > smma [1]
down = smma < smma[1]
mycolor = up ? #64b5f6 : down ? #d32f2f : na
fastma = sma(hl2, 1)

fastplot = plot(fastma, color=#000000, transp=100, title='SMA on Candle')
slowplot = plot(smma, color=mycolor, transp=55, title='SMA1')

////////////////////////////////////////////
smma1 = 0.0
smma1 := na(sm
```