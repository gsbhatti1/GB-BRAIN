``` pinescript
/*backtest
start: 2024-05-07 00:00:00
end: 2024-06-06 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("MACD and RSI Multi-Filter Intraday Trading Strategy", overlay=true)

// MACD Parameters
macdLength = input.int(12, title="MACD Length")
signalSmoothing = input.int(9, title="MACD Signal Smoothing")
src = input(close, title="Source")

// Calculating MACD
[macdLine, signalLine, _] = ta.macd(src, macdLength, 26, signalSmoothing)
macdHist = macdLine - signalLine

// RSI Parameters
rsiLength = input.int(14, title="RSI Length")
overboughtLevel = input.int(70, title="Overbought Level")
oversoldLevel = input.int(30, title="Oversold Level")

// Calculating RSI
rsi = ta.rsi(src, rsiLength)

// SMA Parameters
sma50Length = input.int(50, title="SMA 50 Length")
sma200Length = input.int(200, title="SMA 200 Length")

// Calculating SMA
sma50 = ta.sma(src, sma50Length)
sma200 = ta.sma(src, sma200Length)

// Strategy Conditions
var float longEntryPrice = na
var float shortEntryPrice = na

longCondition = ta.crossover(macdLine, signalLine) and rsi < overboughtLevel and sma50 > sma200
if (longCondition)
    strategy.entry("Long", strategy.long)
    longEntryPrice := close

shortCondition = ta.crossunder(macdLine, signalLine) and rsi > oversoldLevel and sma50 < sma200
if (shortCondition)
    strategy.entry("Short", strategy.short)
    shortEntryPrice := close

// Exit Conditions
longExitCondition = ta.crossunder(macdLine, signalLine) or rsi > overboughtLevel
if (longExitCondition)
    strategy.close("Long")

shortExitCondition = ta.crossover(macdLine, signalLine) or rsi < oversoldLevel
if (shortExitCondition)
    strategy.close("Short")
```

This Pine Script implements the described MACD and RSI multi-filter intraday trading strategy. It includes the necessary parameters and conditions for entering and exiting trades based on the crossover and crossunder of MACD lines, the RSI level, and the relationship between the 50-period and 200-period SMAs.