``` pinescript
/*backtest
start: 2023-02-13 00:00:00
end: 2024-02-19 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("CDC Action Zone [TS Trader]", overlay=true)

// CDC ActionZone V2 29 Sep 2016
// CDC ActionZone is based on a simple 2MA and is most suitable for use with medium volatility market
// 11 Nov 2016 : Ported to Trading View with minor UI enhancement

src = input(title="Data Array", type=input.source, defval=ohlc4)
prd1 = input(title="Short MA period", type=input.integer, defval=12)
prd2 = input(title="Long MA period", type=input.integer, defval=26)

AP = ema(src, 2)
Fast = ema(AP, prd1)
Slow = ema(AP, prd2)

// === INPUT BACKTEST RANGE ===
FromYear = input(defval = 2019, title = "From Year", minval = 2009)
FromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
FromDay = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
ToYear = input(defval = 9999, title = "To Year", minval = 2009)
ToMonth = input(defval = 12, title = "To Month", minval = 1, maxval = 12)
ToDay = input(defval = 31, title = "From Day", minval = 1, maxval = 31)

// === FUNCTION EXAMPLE ===
start = timestamp(FromYear, FromMonth, FromDay, 00, 00)  // backtest start window
finish = timestamp(ToYear, ToMonth, ToDay, 23, 59)        // backtest finish window
window() => true
Bullish = Fast > Slow
Bearish = Fast < Slow

Green = Bullish and AP > Fast
Red = Bearish and AP < Fast
Yellow = Bullish and AP < Fast
Blue = Bearish and AP > Fast

//Long Signal
Buy = Green and Green[1] == 0
Sell = Red and Red[1] == 0

//Short Signal
Short = Red and Red[1] == 0
Cover = Red[1] and Red == 0

//Plot
l1 = plot(Fast, color=color.green, title="Fast MA")
l2 = plot(Slow, color=color.red, title="Slow MA")

plotshape(series=Buy, location=location.belowbar, color=color.green, style=shape.triangleup, title="Buy Signal")
plotshape(series=Sell, location=location.abovebar, color=color.red, style=shape.triangledown, title="Sell Signal")

// Strategy logic
if (window())
    strategy.entry("Long", strategy.long, when=Buy)
    strategy.close("Long", when=Sell or Cover)

```