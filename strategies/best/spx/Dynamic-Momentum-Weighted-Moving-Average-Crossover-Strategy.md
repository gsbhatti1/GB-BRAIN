``` pinescript
/*backtest
start: 2023-12-12 00:00:00
end: 2024-01-11 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// © informanerd
//@version=4

strategy("MultiType Shifting Predictive MAs Crossover", shorttitle = "MTSPMAC + MBHB Strategy", overlay = true)

//inputs

predict = input(true, "Show MA Prediction Tails")
trendFill = input(true, "Fill Between MAs Based on Trend")
crossSignals = input(true, "Show Cross Direction Signals")
showFastMA = input(true, "[ Show Fast Moving Average ]══════════")
fastMAType = input(0, "Fast MA Type: MAEMA (Momentum Adjusted Exponential)", type=input.string)
fastMATypeOptions = ["MAEMA (Momentum Adjusted Exponential)", "DEMA (Double Exponential)", "EMA (Exponential)", "HMA (Hull)", "LSMA (Least Squares)", "RMA (Adjusted Exponential)", "SMA (Simple)", "SWMA (Symmetrically Weighted)", "TEMA (Triple Exponential)", "TMA (Triangular)", "VMA / VIDYA (Variable Index Dynamic Average)", "VWMA (Volume Weighted)", "WMA (Weighted)"]
fastMAType = input.fuzzy(fastMAType, fastMATypeOptions)
fastMASource = input(0, "Fast MA Source: high", type=input.string)
fastMASources = ["high", "close", "low", "open", "hl2", "hlc3", "hlcc4", "ohlc4"]
fastMASource = input.fuzzy(fastMASource, fastMASources)
fastMALen = input(80, "Fast MA Length")
fastMAShift = input(false, "Fast MA Shift")
fastMAThick = input(2, "Fast MA Thickness")
colorTrendFastMA = input(false, "Color Fast MA Based on Detected Trend")
showFastMARangeBand = input(false, "Show Fast MA Range Band")
fastBandATRLookback = input(20, "Fast Band ATR Lookback Period")
fastBandATRMult = input(3, "Fast Band ATR Multiplier")
showSlowMA = input(true, "[ Show Slow Moving Average ]══════════")
slowMAType = input(0, "Slow MA Type: MAEMA (Momentum Adjusted Exponential)", type=input.string)
slowMATypeOptions = fastMATypeOptions
slowMAType = input.fuzzy(slowMAType, slowMATypeOptions)
slowMASource = input.close, "Slow MA Source: close", type=input.string
slowMASources = fastMASources
slowMASource = input.fuzzy(slowMASource, slowMASources)
slowMALen = input(144, "Slow MA Length")
slowMAShift = input(false, "Slow MA Shift")
slowMAThick = input(2, "Slow MA Thickness")
colorTrendSlowMA = input(false, "Color Slow MA Based on Detected Trend")
showSlowMARangeBand = input(false, "Show Slow MA Range Band")
slowBandATRLookback = input(20, "Slow Band ATR Lookback Period")
slowBandATRMult = input(3, "Slow Band ATR Multiplier")
useEMABase = input(false, "Use EMA Basis?")
bollLength = input(80, "Bollinger Length")
bollSource = input.close, "Bollinger Source: close", type=input.string
bollSources = fastMASources
bollSource = input.fuzzy(bollSource, bollSources)
baseMult = input(true, "Base Multiplier")
multiInc = input(true, "Multiplier Increment")
breakoutMult = input(3, "Breakout Multiplier")
highBreakSrc = input(0, "High Break Source: high", type=input.string)
highBreakSources = fastMASources
highBreakSrc = input.fuzzy(highBreakSrc, highBreakSources)
lowBreakSrc = input(0, "Low Break Source: low", type=input.string)
lowBreakSources = bollSources
lowBreakSrc = input.fuzzy(lowBreakSrc, lowBreakSources)

// calculations

fastMA = ta.valtype(fastMAType) ? ta.ema(fastMASource, fastMALen) : na
slowMA = ta.valtype(slowMAType) ? ta.ema(slowMASource, slowMALen) : na

plot(fastMA, title="Fast MA", color=color.new(color.blue, 0), linewidth=2, showLast=showFastMA)
plot(slowMA, title="Slow MA", color=color.new(color.red, 0), linewidth=2, showLast=showSlowMA)

if (predict and not na(fastMA) and not na(slowMA))
    plot(predict ? fastMA + ta.atr(fastBandATRLookback) * fastBandATRMult : fastMA - ta.atr(fastBandATRLookback) * fastBandATRMult, color=color.blue)
    plot(predict ? slowMA + ta.atr(slowBandATRLookback) * slowBandATRMult : slowMA - ta.atr(slowBandATRLookback) * slowBandATRMult, color=color.red)

if (crossSignals and not na(fastMA) and not na(slowMA))
    plotshape(cross(fastMA, slowMA), title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
    plotshape(cross(slowMA, fastMA), title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

if (colorTrendFastMA and not na(fastMA))
    if (ta.crossover(fastMA, slowMA) or ta.crossunder(fastMA, slowMA))
        bgcolor(ta.crossover(fastMA, slowMA) ? color.new(color.blue, 90) : color.new(color.red, 90), transp=75)

if (colorTrendSlowMA and not na(slowMA))
    if (ta.crossover(slowMA, fastMA) or ta.crossunder(slowMA, fastMA))
        bgcolor(ta.crossover(slowMA, fastMA) ? color.new(color.blue, 90) : color.new(color.red, 90), transp=75)

// Bollinger Bands
bollUpper = bollLength and not useEMABase ? ta.sma(bollSource, bollLength) + ta.atr(20) * baseMult + multiInc : na
bollLower = bollLength and not useEMABase ? ta.sma(bollSource, bollLength) - ta.atr(20) * baseMult - multiInc : na

plot(bollUpper, title="Bollinger Upper Band", color=color.new(color.blue, 0), linewidth=1)
plot(bollLower, title="Bollinger Lower Band", color=color.new(color.red, 0), linewidth=1)

// Breakout condition
longCondition = ta.crossover(fastMA, slowMA) and lowBreakSrc <= bollLower
shortCondition = ta.crossunder(fastMA, slowMA) and highBreakSrc >= bollUpper

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.exit("Short", "Long")
```

This script includes the necessary Pine Script code to implement the strategy as described. It defines all inputs and calculates the required moving averages, including their predictions and crossover signals. The Bollinger Bands and breakout conditions are also included for additional context.