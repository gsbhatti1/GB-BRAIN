> Source (PineScript)

``` pinescript
/*backtest
start: 2024-05-30 00:00:00
end: 2024-06-06 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License, version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at https://mozilla.org/MPL/2.0/.

//@version=5
strategy("Elliott-Wave-Stochastic-EMA Strategy", overlay=true)

// Parameters
length = input.int(5, minval=1, title="EMA Length")
src = input(close, title="Source High/Low")
kPeriod = input.int(14, minval=1, title="K Period")
dSmoothing = input.int(3, minval=1, title="D Smoothing")

// Calculate EMA
ema5 = ta.ema(close, length)

// Stochastic Oscillator Calculation
lowSrc = lowest(low, kPeriod)
highSrc = highest(high, kPeriod)
k = 100 * (src - lowSrc) / (highSrc - lowSrc + 0.001)
d = ta.sma(k, dSmoothing)

// Buy/Sell Conditions
buyCondition = ta.crossover(close, ema5)
sellCondition = ta.crossunder(close, ema5)

// Plotting
plot(ema5, color=color.blue, title="EMA(5)")
hline(70, "Overbought", color=color.red)
hline(30, "Oversold", color=color.green)
plotshape(series=buyCondition, location=location.belowbar, color=color.green, style=shape.triangleup, title="Buy Signal")
plotshape(series=sellCondition, location=location.abovebar, color=color.red, style=shape.triangledown, title="Sell Signal")

// Strategy Execution
if (buyCondition)
    strategy.entry("Long", strategy.long)

if (sellCondition)
    strategy.close("Long")
```

This Pine Script™ code implements the Elliott-Wave-Stochastic-EMA strategy on the Binance Futures exchange for Bitcoin/USDT pairs. The script uses Exponential Moving Averages and the Stochastic Oscillator to generate buy/sell signals based on the specified conditions.