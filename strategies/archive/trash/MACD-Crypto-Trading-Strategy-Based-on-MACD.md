``` pinescript
/*backtest
start: 2023-09-11 00:00:00
end: 2023-09-12 04:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
// Revision:        5
// Author:          @Hugo_Moriceau
//study("Thesis_EMLYON_Withdate-strategies-Daily_Crypto_Moriceau_indicator",overlay=true)

// Pyramide 10 order size 100, every tick

strategy("Daily_Crypto_Moriceau_indicator",overlay=true)

// === GENERAL INPUTS ===

fast = 12, slow = 26
fastMA = ema(close, fast)
slowMA = ema(close, slow)

macd = fastMA - slowMA
signal = sma(macd, 9)
rsi = rsi(close,14)

// === Strategy Arguments ===

tradeInvert     = input(defval = false, title = "Invert Trade Direction?")

// === LOGIC ===

// is fast ma above slow ma?
aboveBelow = fastMA >= slowMA ? true : false

// are we inverting our trade direction?
tradeDirection = tradeInvert ? aboveBelow ? false : true : aboveBelow ? true : false

// === Plot Setting ===

//plot(fastMA,color=red)
//plot(slowMA,color=blue)
//barcolor(color=iff(fastMA > slowMA, yellow, na))
//barcolor(color=iff(fastMA < slowMA, black, na))
barcolor(color=iff(macd > 0.12*close , fuchsia, na))
barcolor(color=iff(macd < -0.1*close , lime, na))
dataS= macd > 0.125 and rsi>81 and fastMA > slowMA
dataB= macd < -0.1  and rsi<27 and fastMA< slowMA

plotchar(dataB, char='B',color=black,size = size.tiny,location = location.belowbar,transp= 0)  
plotchar(dataS, char='S',color=black,size = size.tiny,location = location.abovebar,transp= 0)

// === BACKTEST RANGE ===
FromMonth = input(defval = 01, title = "From Month", minval = 1)
FromDay   = input(defval = 01, title = "From Day", minval = 1)
FromYear  = input(defval = 2017, title = "From Year", minval = 2014)
ToMonth   = input(defval = 2, title = "To Month", minval = 1)
ToDay     = input(defval = 10, title = "To Day", minval = 1)
ToYear    = input(defval = 2019, title = "To Year", minval = 2014)
```