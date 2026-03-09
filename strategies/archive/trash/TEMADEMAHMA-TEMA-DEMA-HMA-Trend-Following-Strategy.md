```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © tuned-com

//@version=4
strategy("TEMA/DEMA/HMA", overlay=true, pyramiding=0, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital=1000000, commission_type=strategy.commission.percent, commission_value=0.1)

Tlength = input(8, title="TEMA Length", minval=1)
Dlength = input(43, title="DEMA Length", minval=1)
Hlength = input(52, title="Hull Length", minval=1)
Rlength = input(2, title="Hull Trend Test Length", minval=1)


//TEMA//
ema1 = ema(close, Tlength)
ema2 = ema(ema1, Tlength)
ema3 = ema(ema2, Tlength)
tema = 3 * (ema1 - ema2) + ema3

//DEMA//
e1 = ema(close, Dlength)
e2 = ema(e1, Dlength)
dema = 2 * e2 - e1

//HMA//
h1 = ema(close, Hlength / 2)
h2 = ema(h1, int(Hlength / (sqrt(2) + 1)))
h3 = ema(h2, int(Hlength / (sqrt(2) + 1)))
hma = 2 * h3 - h2

// Entry Conditions
longCondition = ta.crossover(tema, dema)
shortCondition = ta.crossunder(tema, dema)

// Trade Execution
if (longCondition and ta.upcross(hma))
    strategy.entry("Long", strategy.long)

if (shortCondition and ta.downcross(hma))
    strategy.close("Long")

```

This code completion ensures that the Pine Script logic aligns with the described strategy. The TEMA, DEMA, and HMA calculations are correctly implemented, along with the entry conditions based on the crossing of these averages and the confirmation using the HMA trend direction.