``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 24/11/2020
// This is combo strategies for get a cumulative signal. 
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close 
// during 2 days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market, if close price is lower than the previous close price 
// during 2 days and the meaning of 9-days Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
// As the name suggests, High low bands are two bands surrounding the underlying’s 
// price. These bands are generated from the triangular moving averages calculated 
// from the underlying’s price. The triangular moving average is, in turn, shifted 
// up and down by a fixed percentage. The bands, thus formed, are termed as High 
// low bands. The main theme and concept of High low bands is based upon the triangular 
// moving average. 
//
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
////////////////////////////////////////////////////////////
Reversal123(Length, KSmoothing, DLength, Level) =>
    vFast = sma(stoch(close, high, low, Length), KSmoothing) 
    vSlow = sma(vFast, DLength)
    pos = 0.0
    pos := iff(close[2] < close[1] and close > close[1] and vFast < vSlow and vFast > Level, 1,
	           iff(close[2] > close[1] and close < close[1] and vFast > vSlow and vFast < Level, -1, nz(pos[1], 0))) 
    pos

HLB(Length, PercentShift) =>
    pos = 0.0
    xTMA = sma(sma(close, Length), Length)
    xHighBand = xTMA + (xTMA * PercentShift / 100)
    xLowBand = xTMA - (xTMA * PercentShift / 100)
    pos := iff(close > xHighBand, 1,
	           iff(close < xLowBand, -1, nz(pos[1], 0))) 
    pos

strategy(title="Combo Backtest 123 Reversal & High Low Bands", shorttitle="Combo", overlay = true)
Length = input(14, minval=1)
KSmoothing = input(1, minval=1)
DLength = input(3, minval=1)
Level = input(50, minval=1)
//-------------------------
Length_HLB = input(14, minval=1)
PercentShift = input(true, title="KSmoothing")
TradeReverse = input(false, title="Trade reverse")
plotshape(series=Reversal123(Length, KSmoothing, DLength, Level) == 1, style=shape.triangleup, location=location.belowbar, color=color.green, title="Buy Signal")
plotshape(series=Reversal123(Length, KSmoothing, DLength, Level) == -1, style=shape.triangledown, location=location.abovebar, color=color.red, title="Sell Signal")
hline(50, "Overbought/Oversold", color=color.orange)
hline(0, "Midpoint", color=color.black)

```