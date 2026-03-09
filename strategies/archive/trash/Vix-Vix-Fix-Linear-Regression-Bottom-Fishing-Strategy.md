``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © HeWhoMustNotBeNamed

//@version=4
strategy("VixFixLinReg-Strategy", shorttitle="VixFixLinReg - Strategy",
                     overlay=false, initial_capital = 100000, 
                     default_qty_type = strategy.percent_of_equity, default_qty_value = 100, commission_type = strategy.commission.percent, pyramiding = 1, 
                     commission_value = 0.01)
pd = input(22, title="LookBack Period Standard Deviation High")
bbl = input(20, title="Bolinger Band Length")
mult = input(2.0    , minval=1, maxval=5, title="Bollinger Band Standard Devaition Up")
lb = input(50  , title="Look Back Period Percentile High")
ph = input(.85, title="Highest Percentile - 0.90=90%, 0.95=95%, 0.99=99%")
pl = input(1.01, title="Lowest Percentile - 1.10=90%, 1.05=95%, 1.01=99%")
hp = input(false, title="Show High Range - Based on Percentile and LookBack Period?")
sd = input(false, title="Show Standard Deviation Line?")
showBBColor = input(true, title="Show Bollinger Bands Color?")
vixFixClose = input(false, title="Consider Vix Fix Close?")
kcLen = input(20, title="KC Length")
kcMult = input(1.5, title="KC Multiplier")
atrLen = input(22, title="ATR Length")
atrMult = input(5, title="ATR Multiplier")
initialStopBar = input(5, title="Initial Stop Bar")
waitForCloseBeforeStop = input(true, title="Wait for Close Before Stop?")
```