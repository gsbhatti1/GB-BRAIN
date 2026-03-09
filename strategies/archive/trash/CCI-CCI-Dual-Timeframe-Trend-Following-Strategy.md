``` pinescript
/*backtest
start: 2023-10-24 00:00:00
end: 2023-11-23 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy(title="CCI-Dual-Timeframe-Trend-Following-Strategy", calc_on_order_fills=true, currency=currency.USD, default_qty_type=strategy.percent_of_equity, commission_type=strategy.commission.percent)


source = close
shortlength=input(14)
longlength=input(56)
aa=input(2)
Ss=input(75)

// CCI part
ci1 = cci(source, shortlength)   // 14-period CCI
ci2 = cci(source, longlength)   // 56-period CCI

// Orian Teacher's WT + Ichimoku
len = input(10)
lenTurn = input(9)
lenStd = input(26)

wtm_e(so, l) =>
    esa = ema(so, l)
    d = ema(abs(so - esa), l)
    ci = (so - esa) / (0.015 * d)
    ema(ci, l*2+1)

alh(len) => avg(lowest(len), highest(len))
alh_src(src, len) => avg(lowest(src, len), highest(src, len))

wt = wtm_e(close, len)
turn = alh_src(wt, lenTurn)
std = alh_src(wt, lenStd)

cnt = 0
if wt > turn
    cnt := cnt + 1
if wt > std
    cnt := cnt + 1


// 100 and -100 lines
h0 = hline(100)
h1 = hline(-100)

plot(ci1, color=green)
plot(ci2, color=red)

plot(0, color=black)
plot(100, color=black)
plot(-100, color=black)

fill(h0, h1, color=purple, transp=95)

bgcolor(cnt == 0 ? red : cnt == 1 ? blue : cnt == 2 ? green
```