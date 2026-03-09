``` pinescript
/*backtest
start: 2024-02-21 00:00:00
end: 2024-10-01 00:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("SuperTrend + Stochastic Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// SuperTrend Settings
superTrendFactor = input.float(3.0, title="SuperTrend Factor")
atrPeriod = input.int(10, title="ATR Period")

// Stochastic Oscillator Settings
kPeriod = input.int(14, title="%K Period", minval=1)
dSmoothing = input.int(3, title="%D Smoothing", minval=1)
overboughtLevel = 80
oversoldLevel = 20

// SuperTrend Calculation
[supertrend, supertrendDirection] = superTrend(close, atrPeriod, superTrendFactor)

// Stochastic Oscillator Calculation
[kValue, dValue] = stoch(high, low, close, kPeriod, dSmoothing)

plotshape(series=cross(supertrend, oversoldLevel) and (supertrendDirection == 1), title="Long Entry", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=cross(oversoldLevel, supertrend) and (supertrendDirection == -1), title="Short Entry", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// Long Condition
longCondition = crossover(supertrend, oversoldLevel) and (supertrendDirection == 1)
if (longCondition)
    strategy.entry("Long", strategy.long)

// Short Condition
shortCondition = crossunder(oversoldLevel, supertrend) and (supertrendDirection == -1)
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Exit Conditions
exitLongCondition = crossover(supertrend, oversoldLevel) or crossunder(kValue, overboughtLevel)
if (exitLongCondition)
    strategy.close("Long")

exitShortCondition = crossunder(supertrend, oversoldLevel) or crossover(kValue, oversoldLevel)
if (exitShortCondition)
    strategy.close("Short")
```

This Pine Script implements the described strategy using SuperTrend and Stochastic Oscillator indicators. The script sets up long and short entry conditions based on the crossovers between the SuperTrend line and the overbought/oversold levels of the Stochastic Oscillator, ensuring clear and executable trading signals.