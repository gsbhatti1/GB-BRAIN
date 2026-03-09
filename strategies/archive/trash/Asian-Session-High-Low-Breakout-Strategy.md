``` pinescript
/*backtest
start: 2024-02-27 00:00:00
end: 2024-03-28 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Asian Session High-Low Breakout Strategy", overlay=true)

var hourSessionStart = input(19, "Asia session start hour", minval=0, maxval=23)
var hourSessionStop  = input(1, "Asia session end hour", minval=0, maxval=23)
var offsetHours = input(3, "Offset hours after Asia session end")

var float hi              = na
var float lo              = na
var float plotHi          = na
var float plotLo          = na

var bool  inSession       = na
var bool  enteringSession = na
var bool  exitingSession  = na

inSession       := (hour >= hourSessionStart or hour < hourSessionStop)
enteringSession := inSession and not inSession[1]
exitingSession  := not inSession and inSession[1]

if enteringSession
    plotLo := na
    plotHi := na

if inSession
    lo := min(low,  nz(lo, 1.0e23))
    hi := max(high, nz(hi))

if exitingSession
    plotLo := lo
    plotHi := hi
    lo     := na
    hi     := na

bgcolor(inSession ? color.blue : na)

plot(plotLo, "Asian session Low",  color.red,   style=plot.style_linebr)
plot(plotHi, "Asian session High", color.green, style=plot.style_linebr)
```