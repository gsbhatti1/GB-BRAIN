``` pinescript
/*backtest
start: 2023-02-25 00:00:00
end: 2024-02-25 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("ZendicatoR", overlay=true)
dt = input(defval=0.001, title="Decision Threshold", type=float, step=0.0001)
keh = input(title="Double HullMA Cross", defval=7, minval=1)
che1 = input(title="MA 1", defval=34, minval=1)
che2 = input(title="MA 2", defval=144, minval=1)
che3 = input(title="MA 3", defval=377, minval=1)
amnt = input(title="TP ($)", defval=4200, minval=1)
wma1 = wma(close, che1)
wma2 = wma(close, che2)
wma3 = wma(close, che3)
tms = 10000000000000
A = request.security(syminfo.tickerid, 'D', close) * tms
B = request.security(syminfo.tickerid, 'D', close[1]) * tms
C = A > B ? green : red
D = wma2 > wma3 ? green : red
plot(wma1, style=line, color=C, linewidth=4)
p1 = plot(wma2, style=line, color=D)
p2 = plot(wma3, style=line, color=D)
fill(p1, p2, color=D, transp=75)
n2ma = 2 * wma(close, round(keh / 2))
nma = wma(close, keh)
diff = n2ma - nma
n2ma1 = 2 * wma(close[2], round(keh / 2))
nma1 = wma(close[2], keh)
diff1 = n2ma1 - nma1
n1 = wma(diff, sqn) * tms
n2 = wma(diff1, sqn) * tms
closelong = A * tms < B * tms and n2 * tms > n1 * tms and strategy.openprofit > amnt
if (closelong)
    strategy.close("Long")
closeshort = A * tms > B * tms and n1 * tms > n2 * tms and strategy.openprofit > amnt
if (closeshort)
    strategy.close("Short")
longCondition = A * tms > B * tms and n1 * tms > n2 * tms
if (longCondition)
    strategy.entry("Long", strategy.long, when=longCondition)
```