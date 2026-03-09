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

// Parameters for MACD
macdLength = input.int(12, title="MACD Length")
signalSmoothing = input.int(9, title="MACD Signal Smoothing")
src = input(close, title="Source")

// Calculation of MACD
[macdLine, signalLine, _] = ta.macd(src, macdLength, 26, signalSmoothing)
macdHist = macdLine - signalLine

// Parameters for RSI
rsiLength = input.int(14, title="RSI Length")
overboughtLevel = input.int(70, title="Overbought Level")
oversoldLevel = input.int(30, title="Oversold Level")

// Calculation of RSI
rsiValue = ta.rsi(src, rsiLength)

// Parameters for SMA
sma50Period = input.int(50, title="SMA 50 Period")
sma200Period = input.int(200, title="SMA 200 Period")

// Calculation of SMA
sma50 = ta.sma(src, sma50Period)
sma200 = ta.sma(src, sma200Period)

// Long Entry Condition
longCondition = ta.crossover(macdLine, signalLine) and rsiValue < overboughtLevel and sma50 > sma200

// Long Exit Condition
longExitCondition1 = ta.crossunder(macdLine, signalLine)
longExitCondition2 = rsiValue > overboughtLevel
longExitCondition = longExitCondition1 or longExitCondition2

// Short Entry Condition
shortCondition = ta.crossunder(macdLine, signalLine) and rsiValue > oversoldLevel and sma50 < sma200

// Short Exit Condition
shortExitCondition1 = ta.crossover(macdLine, signalLine)
shortExitCondition2 = rsiValue < oversoldLevel
shortExitCondition = shortExitCondition1 or shortExitCondition2

// Plotting MACD histogram and RSI on the chart
plot(macdHist, title="MACD Histogram", color=color.blue, linewidth=2)
hline(overboughtLevel, "Overbought Level", color=color.red)
hline(oversoldLevel, "Oversold Level", color=color.green)

// Entry and Exit Rules for Strategy
if (longCondition)
    strategy.entry("Long", strategy.long)

if (longExitCondition)
    strategy.close("Long")

if (shortCondition)
    strategy.entry("Short", strategy.short)

if (shortExitCondition)
    strategy.close("Short")
```

This Pine Script code implements the trading strategy described, with clear entry and exit rules based on MACD, RSI, and SMA conditions. The script sets up the necessary parameters for each indicator and defines the conditions under which to enter or exit trades.