```pinescript
/*backtest
start: 2023-12-17 00:00:00
end: 2024-01-16 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 15/09/2020
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
// The name ‘Floor-Trader Pivot,’ came from the fact that Pivot points can 
// be calculated quickly, on the fly using price data from the previous day 
// as an input. Although time-frames of less than a day can be used, Pivots are 
// commonly plotted on the Daily Chart; using price data from the previous day’s 
// trading activity. 
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

FPP() =>
    pos = 0
    xHigh  = security(syminfo.tickerid,"D", high[1])
    xLow   = security(syminfo.tickerid,"D", low[1])
    xClose = security(syminfo.tickerid,"D", close[1])
    vPP = (xHigh+xLow+xClose) / 3
    vR1 = (vPP * 2) - xLow
    vS1 = (vPP * 2) - xHigh
    pos := iff(close > vR1, 1,
             iff(close < vS1, -1, nz(pos[1], 0))) 
    pos

strategy(title="Combo Backtest 123 Reversal & Floor Pivot Points", shorttitle="Combo", overlay = true)
Length = input(15, minval=1)
KSmoothing = input(1, minval=1)
DLength = input(3, minval=1)
Level = input(50, minval=1)
TradeReverse = input(false, title="Trade reverse")

plotshape(series=crossover(stoch(close, high, low, Length), Level) and close > close[2] and vFast < vSlow, location=location.belowbar, color=color.green, style=shape.triangleup, title="Buy Signal")
plotshape(series=crossunder(stoch(close, high, low, Length), Level) and close < close[2] and vFast > vSlow, location=location.abovebar, color=color.red, style=shape.triangledown, title="Sell Signal")

if (TradeReverse)
    strategy.entry("Buy", strategy.long, when=crossover(stoch(close, high, low, Length), Level) and close > close[2] and vFast < vSlow)
    strategy.exit("Close Buy", "Buy", stop=vS1)
else
    strategy.entry("Sell", strategy.short, when=crossunder(stoch(close, high, low, Length), Level) and close < close[2] and vFast > vSlow)
    strategy.exit("Close Sell", "Sell", stop=vR1)

if (TradeReverse)
    plotshape(series=Reversal123(Length, KSmoothing, DLength, Level) == 1, location=location.belowbar, color=color.green, style=shape.triangleup, title="Buy Signal from Reversal")
else
    plotshape(series=FPP() == 1, location=location.belowbar, color=color.green, style=shape.triangleup, title="Buy Signal from Floor Pivot")

if (TradeReverse)
    strategy.entry("Buy", strategy.long, when=Reversal123(Length, KSmoothing, DLength, Level) == 1 and close > vR1)
else
    strategy.entry("Sell", strategy.short, when=FPP() == 1 and close < vS1)

```