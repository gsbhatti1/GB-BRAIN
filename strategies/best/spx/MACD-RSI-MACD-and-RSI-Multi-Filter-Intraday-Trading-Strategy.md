``` pinescript
/*backtest
start: 2024-05-07 00:00:00
end: 2024-06-06 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Day Trading Strategy", overlay=true)

// MACD Parameters
macdLength = input.int(12, title="MACD Length")
signalSmoothing = input.int(9, title="MACD Signal Smoothing")
src = input(close, title="Source")

// Calculating MACD
[macdLine, signalLine, _] = ta.macd(src, macdLength, 26, signalSmoothing)
macdHist = macdLine - signalLine

// RSI Parameters
rsiLength = input.int(14, title="RSI Length")
overboughtLevel = 70
oversoldLevel = 30

// Calculating RSI
rsiValue = ta.rsi(src, rsiLength)

// SMA Conditions
sma50 = ta.sma(close, 50)
sma200 = ta.sma(close, 200)

// Entry and Exit Rules
longCondition = macdHist > 0 and rsiValue < overboughtLevel and sma50 > sma200
shortCondition = macdHist < 0 and rsiValue > oversoldLevel and sma50 < sma200

// Long Entry
if (longCondition)
    strategy.entry("Long", strategy.long)

// Long Exit
if (macdLine < signalLine or rsiValue >= overboughtLevel)
    strategy.close("Long")

// Short Entry
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Short Exit
if (macdLine > signalLine or rsiValue <= oversoldLevel)
    strategy.close("Short")
```

This Pine Script code implements the described trading strategy using MACD, RSI, and SMA indicators. The script includes the necessary parameters for each indicator and defines entry and exit rules based on the conditions provided in the description.