> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|100|donLength|
|v_input_2|10|Slow ATR period|
|v_input_3|3|Slow ATR multiplier|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-03-16 00:00:00
end: 2024-03-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Donchian Channel Breakout Strategy with ATRSL Trailing Stop", overlay = true)
donLength = input(100, minval=1)

//Donchian Channel
donLower = lowest(donLength)
donUpper = highest(donLength)
donBasis = avg(donUpper, donLower)

// ATRSL
SC = close

// Slow ATR
AP2 = input(10, title="Slow ATR period")  // ATR Period
AF2 = input(3, title="Slow ATR multiplier")  // ATR Factor
SL2 = AF2 * atr(AP2)  // Stop Loss
Trail2 = 0.0
iff_3 = SC > nz(Trail2[1], 0) ? SC - SL2 : SC + SL2
iff_4 = SC < nz(Trail2[1], 0) and SC[1] < nz(Trail2[1], 0) ? min(nz(Trail2[1], 0), SC + SL2) : iff_3
Trail2 := SC > nz(Trail2[1], 0) and SC[1] > nz(Trail2[1], 0) ? max(nz(Trail2[1], 0), SC - SL2) : iff_4

// Long and Short Conditions
longCondition = crossover(close, donUpper)
shortCondition = below(close, Trail2)

// Strategy Actions
if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.close("Long")

// Plotting
plot(donLower, color=color.red)
plot(donUpper, color=color.green)
plot(Trail2, color=color.blue)
```

This script defines a Donchian Channel Breakout Strategy with an ATRSL trailing stop. The strategy uses Donchian Channels to identify potential entry points and an ATR-based trailing stop to manage risk.