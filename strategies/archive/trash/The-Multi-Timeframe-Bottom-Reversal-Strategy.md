``` pinescript
/*backtest
start: 2022-10-11 00:00:00
end: 2023-10-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// the original indicator is Noro's BottomSensivity v0.6
//@version=4
strategy("Noro's BottomSensivity v0.6 strategy + rsi + Alarm", shorttitle="Bottom 0.6 StRsiAlarm", overlay=true)

overSold = input(35)
overBought = input(70)
botsens = input(defval = 3, minval = 1, maxval = 4, title = "Bottom-Sensivity")
smalen = input(defval = 25, minval = 20, maxval = 200, title = "SMA Length")
bars = input(defval = 3, minval = 2, maxval = 4, title = "Bars of Locomotive")
useloc = input(true, title = "Use bottom-pattern Locomotive?")
usepin = input(true, title = "Use bottom-pattern Pin-bar?")
usecvi = input(true, title = "Use bottom-indicator CVI?")
useucs = input(true, title = "Use bottom-indicator UCS?")
usevix = input(true, title = "Use bottom-indicator WVF?")
usersi = input(true, title = "Use bottom-indicator RSI?")
usered = input(false, title = "Only red candles?")
usesma = input(true, title = "Use SMA Filter?")
showsma = input(false, title = "Show SMA Filter?")

//SMA Filter
sma = sma(close, smalen)
colsma = showsma == true ? red : na
plot(sma, color = colsma)

//VixFix method
//Start of ChrisMoody's code
pd = 22
bbl = 20
mult = 2
lb = 50
ph = .85
pl = 1.01
hp = false
sd = false
wvf = ((highest(close, pd)-low)/(highest(close, pd)))*100
sDev = mult * stdev(wvf, bbl)
midLine = sma(wvf, bbl)
lowerBand = midLine - sDev
upperBand = midLine + sDev
rangeHigh = (highest(wvf, lb)) * ph
rangeLow = (lowest(wvf, lb)) * pl
//End of ChrisMoody's code

//Locomotive method
bar = close > open ? 1 : close < open ? -1 : 0
locob = bar == 1 and bar[1] == -1 and bar[2] == -1 and (bar[3] == -1 or bars < 3) and (bar[4] == -1 or bars < 4) ? 1 : 0

//PIN BAR
body = abs(close - open)
upshadow = open > close? (high - open) : (high - close)
downshadow = open > close ? (close - low) : (open - low)
pinbar = open[1] > close[1] ? (body[1] > body ? (downshadow > 0.5 * body ? (downshadow > 2 * upshadow ? 1 : 0 ) : 0 ) : 0 ) : 0

//CVI method
//Start of LazyBear's code
ValC=sma(hl2, 3)
bull=-.51
bear=.43
vol=sma(atr(3), 3)
cvi = (close-ValC) / (vol*sqrt(3))
cb= cvi <= bull ? green : cvi >=bear ? red : cvi > bull ? blue : cvi < bear ? blue : na
bull1 = cvi <= bull
bear1 = cvi >= bear
bull2 = bull1[1] and not bull1
bear2 = bear1[1] and not bear1
//End of LazyBear's code

//UCS method
//Start of UCS's code
ll = lowest(low, 5)
hh = highest(high, 5)
diff = hh - ll
rdiff = close - (hh+ll)/2
avgrel = ema(em
```