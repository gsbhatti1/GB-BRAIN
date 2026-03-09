```pinescript
/*backtest
start: 2023-08-21 00:00:00
end: 2023-09-20 00:00:00
Period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
// AK-Dual-RSI-Breakout-Strategy code v. 1.00
strategy("AK RSI 2 Breakout Strategy", overlay=true)

RS = rsi(close, 2)              // Calculate 2-period RSI
SMA5 = sma(close, 5)            // Calculate 5-day simple moving average
SMA200 = sma(close, 200)        // Calculate 200-day simple moving average

longCondition = crossover(SMA200, SMA5) and RS < 5    // Long when price crosses above 200-day MA but below 5-day MA, RSI(2) < 5
shortCondition = crossunder(SMA200, SMA5) and RS > 90  // Short when price crosses below 200-day MA but above 5-day MA, RSI(2) > 90

// Plot moving averages on the chart
plot(SMA5, color=color.blue)
plot(SMA200, color=color.red)

if (longCondition)
    strategy.entry("Long", strategy.long)       // Enter long position
else if (shortCondition)
    strategy.entry("Short", strategy.short)     // Enter short position

// Close positions when price breaks 5-day MA again
plotshape(series=crossover(close, SMA5), title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=crossunder(close, SMA5), title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Print signals to the chart
label.new(x=bar_index, y=high, text="Long Entry", color=color.green)
label.new(x=bar_index, y=low, text="Short Exit", color=color.red)

// Optional: Add stop loss logic (not implemented here)
```

This translation and code update maintain the original structure while translating the human-readable text into English as requested.