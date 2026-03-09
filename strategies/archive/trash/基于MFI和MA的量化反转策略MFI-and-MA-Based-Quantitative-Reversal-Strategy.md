``` pinescript
// A function to check whether the bar or price session is within the market session
inSession = na(time(timeframe.period, i_marketSession)) ? false : session.in_range(time(timeframe.period, i_marketSession), session.regular)

// ********** Supporting functions - End **********


// ********** Main Strategy Logic - Start **********

// Calculate MFI
mfi = ta.mfi(i_MFI)

// Check for overbought and oversold conditions
isOverbought = mfi > OB
isOversold = mfi < OS

// Calculate MA
ma = ta.sma(close, i_MALen)

// Determine long and short signals
longCondition = isOversold and close > ma
shortCondition = isOverbought and close < ma

// Execute trades
if (inSession)
    if (longCondition)
        strategy.entry("Long", strategy.long)
        strategy.exit("Long Exit", "Long", stop=close * (1 - shortLossPerc), limit=close * (1 + longProfitPerc))
    if (shortCondition)
        strategy.entry("Short", strategy.short)
        strategy.exit("Short Exit", "Short", stop=close * (1 + shortLossPerc), limit=close * (1 - shortProfitPerc))

// ********** Main Strategy Logic - End **********


// ********** Plotting - Start **********

// Plot MFI
plot(mfi, title="MFI", color=color.blue, linewidth=2)

// Plot MA
plot(ma, title="MA", color=color.red, linewidth=2)

// Plot signal lines
plotshape(series=longCondition, title="Long Entry", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=shortCondition, title="Short Entry", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// ********** Plotting - End **********
```

This Pine Script translates the provided trading strategy into a format that can be executed on trading platforms like TradingView. It incorporates the necessary inputs and logic as described in the document.