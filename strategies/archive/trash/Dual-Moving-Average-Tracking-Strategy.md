``` pinescript
/*backtest
start: 2022-12-18 00:00:00
end: 2023-12-24 00:00:00
period: 1d
basePeriod: 1h
exchange: Binance
args: v_input_1=10, v_input_float_1=3, v_input_2=7, v_input_3=7
*/

//@version=5
indicator("Dual-Moving-Average-Tracking-Strategy", overlay=true)

// Inputs
atrLength = input.int(10, title="ATR Length")
factor = input.float(3, title="Factor")
adxSmoothing = input.int(7, title="ADX Smoothing")
diLength = input.int(7, title="DI Length")

// Supertrend
[supertrend, _] = supertrend(close, atrLength, factor)

// RSI
rsiValue = rsi(close, 14)

// ADX
adxValue = ta.adx(high, low, close, adxSmoothing)

// Golden Cross
shortMA = ta.sma(close, 10)
longMA = ta.sma(close, 50)
goldenCross = ta.crossover(shortMA, longMA)

// Death Cross
deathCross = ta.crossunder(shortMA, longMA)

// Entry Conditions
bullish = goldenCross and rsiValue < 70 and adxValue > 20
bearish = deathCross and rsiValue > 30 and adxValue > 20

// Plot Supertrend
plot(supertrend, color=color.blue, title="Supertrend")

// Plot RSI
plot(rsiValue, color=color.red, title="RSI")

// Plot ADX
plot(adxValue, color=color.orange, title="ADX")

// Plot Golden Cross
plotshape(series=goldenCross, location=location.belowbar, color=color.green, style=shape.triangleup, title="Golden Cross")

// Plot Death Cross
plotshape(series=deathCross, location=location.abovebar, color=color.red, style=shape.triangledown, title="Death Cross")

// Long Signal
if (bullish)
    strategy.entry("Long", strategy.long)

// Close Long Position
if (bearish)
    strategy.close("Long")

// Plot Strategy
plotshape(series=bullish, location=location.belowbar, color=color.green, style=shape.triangleup, title="Buy Signal")

plotshape(series=bearish, location=location.abovebar, color=color.red, style=shape.triangledown, title="Sell Signal")
```

> Strategy Arguments

|Argument|Default|Description|
|---|---|---|
|v_input_1|10|ATR Length|
|v_input_float_1|3|Factor|
|v_input_2|7|ADX Smoothing|
|v_input_3|7|DI Length|