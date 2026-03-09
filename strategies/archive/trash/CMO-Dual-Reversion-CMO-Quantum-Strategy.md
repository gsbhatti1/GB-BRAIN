```pinescript
//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 19/08/2019
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
//    This indicator plots Chandre Momentum Oscillator and its WMA on the 
//    same chart. This indicator plots the absolute value of CMO.
//    The CMO is closely related to, yet unique from, other momentum oriented 
//    indicators such as Relative Strength Index, Stochastic, Rate-of-Change, 
//    etc. It is most closely related to Welles Wilder?s RSI, yet it differs 
//    in several ways:
//    - It uses data for both up days and down days in the numerator, thereby 
//        directly measuring momentum;
//    - The calculations are applied on unsmoothed data. Therefore, short-term 
//        extreme movements in price are not hidden. Once calculated, smoothing 
//        can be applied to the CMO, if desired;
//    - The scale is bounded between +100 and -100, thereby allowing you to clearly 
//        see changes in net momentum using the 0 level. The bounded scale also allows 
//        you to conveniently compare values across different securities.
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

CMOWMA(Length, LengthWMA) =>
    cmo = chaikin_momentum_oscillator(close, high, low, volume)
    wma_cmo = wma(cmo, LengthWMA)
    color_bar = na
    if (cmo > wma_cmo and cmo > 0)
        color_bar := green
    else if (cmo < wma_cmo and cmo < 0)
        color_bar := red
    color_bar

strategy("Dual-Reversion-CMO-Quantum-Strategy", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 10, initial_capital = 10000)

length = input(14, title="Length")
kSmoothing = input(True, title="KSmoothing")
dLength = input(3, title="DLength")
level = input(50, title="Level")
cmoLength = input(14, title="CMO Length")
wmaLength = input(13, title="WMA Length")
tradeReverse = input(False, title="Trade reverse")

// First strategy logic
reversalSignal = Reversal123(length, kSmoothing, dLength, level)

// Second strategy logic
cmoValue = chaikin_momentum_oscillator(close, high, low, volume)
wmaCmo = wma(cmoValue, wmaLength)
cmowmaSignal = cmoValue > wmaCmo

// Combined signal
signal = (reversalSignal == 1 and cmowmaSignal) or (reversalSignal == -1 and not cmowmaSignal)

if (signal)
    strategy.entry("Long", strategy.long)
if (not(signal))
    strategy.close("Long")

plotshape(series=signal, location=location.belowbar, color=color.blue, style=shape.labelup, text="Entry Signal")
plotshape(series=(reversalSignal == -1 and not cmowmaSignal), location=location.abovebar, color=color.red, style=shape.labeldown, text="Exit Signal")

// Color bars based on CMO and WMA
var color barColor = na
if (cmoValue > wmaCmo)
    barColor := green
else if (cmoValue < wmaCmo)
    barColor := red
barcolor(barColor)

```