``` pinescript
/*backtest
start: 2023-09-29 00:00:00
end: 2023-10-29 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("VB Strategy", overlay=true)

length = input(130, title="交易量长度")
coef = input(0.2, title="系数")
vcoef = input(2.5, title="最大系数")
signalLength=input(5)
smoothVFI=input(false, type=bool, title="平滑")
//布林带
length2 = input(20, minval=1, title="布林带长度")

ma(x,y) => smoothVFI ? sma(x,y) : x

typical=hlc3
inter = log( typical ) - log( typical[1] )
vinter = stdev(inter, 30 )
cutoff = coef * vinter * close
vave = sma( volume, length )[1]
vmax = vave * vcoef
vc = iff(volume < vmax, volume, vmax)
mf = typical - typical[1]
vcp = iff( mf > cutoff, vc, 
```