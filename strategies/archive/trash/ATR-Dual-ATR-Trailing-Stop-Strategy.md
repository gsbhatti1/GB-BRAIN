``` pinescript
//@version=4
strategy("ATR Trailing Stop Strategy by ceyhun", overlay=true)

/////////notes////////////////////////////////////////
// This is based on the ATR trailing stop indicator //
// with an addition of two levels of stops and      //
// different interpretation.                        //
// This is a fast-reacting system and is better     //
// suited for higher volatility markets             //
//////////////////////////////////////////////////////

SC = input(close, "Source", input.source)

// Fast Trail //
AP1 = input(5, "Fast ATR period", input.integer)  // ATR Period
AF1 = input(0.5, "Fast ATR multiplier", input.float)  // ATR Factor
SL1 = AF1 * atr(AP1)  // Stop Loss
Trail1 = 0.0
Trail1 := iff(SC > nz(Trail1[1], 0) and SC[1] > nz(Trail1[1], 0), max(nz(Trail1[1], 0), SC - SL1), iff(SC < nz(Trail1[1], 0) and SC[1] < nz(Trail1[1], 0), min(nz(Trail1[1], 0), SC + SL1), iff(SC > nz(Trail1[1], 0), SC - SL1, SC + SL1)))

// Slow Trail //
AP2 = input(10, "Slow ATR perod", input.integer)  // ATR Period
AF2 = input(2, "Slow ATR multiplier", input.float)  // ATR Factor
SL2 = AF2 * atr(AP2)  // Stop Loss
Trail2 = 0.0
Trail2 := iff(SC > nz(Trail2[1], 0) and SC[1] > nz(Trail2[1], 0), max(nz(Trail2[1], 0), SC - SL2), iff(SC < nz(Trail2[1], 0) and SC[1] < nz(Trail2[1], 0), min(nz(Trail2[1], 0), SC + SL2), iff(SC > nz(Trail2[1], 0), SC - SL2, SC + SL2)))

// Bar color for trade signal //
Green = Trail1 > Trail2 and close > Trail2 and low > Trail2
Blue = Trail1 > Trail2 and close > Trail2 and low < Trail2
Red = Trail2 > Trail1 and close < Trail2 and high < Trail2
Yellow = Trail2 > Trail1 and close < Trail2 and high > Trail2

// Signals //
Bull = iff(close[1] >= Trail2 and close > Trail2, true, false)
Bear = iff(close[1] <= Trail1 and close < Trail1, true, false)

plotshape(series=Green, location=location.belowbar, color=color.green, style=shape.labelup, text="BUY", title="Buy Signal")
plotshape(series=Red, location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL", title="Sell Signal")

// Plot trail lines //
plot(Trail1, "Fast ATR Trail", color=color.blue)
plot(Trail2, "Slow ATR Trail", color=color.orange)

```