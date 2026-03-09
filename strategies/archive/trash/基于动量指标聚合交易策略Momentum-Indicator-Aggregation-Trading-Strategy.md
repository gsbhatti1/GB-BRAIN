``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Kesin Etkili Analiz V1 - Artun Sinan", overlay=true)
//indicator("Kesin Etkili Analiz V1 - Artun Sinan", overlay=true)

//BackTest
yearin = input(2019, title="BackTestBaşlangıç Tarihi")

// Define parameters for the indicators
emaShrtPeriod = input.int(title="EMA Kısa Periyodu", defval=50, minval=1)
emaLngPeriod = input.int(title="EMA Uzun Periyodu", defval=100, minval=1)
movingAvgPeriod = input.int(title="Hareketli Ortalama Periyodu", defval=50, minval=1)
macdFastPeriod = input.int(title="MACD Hızlı Periyodu", defval=12, minval=1)
macdSlowPeriod = input.int(title="MACD Yavaş Periyodu", defval=26, minval=1)
macdSigPeriod = input.int(title="MACD Sinyal Periyodu", defval=9, minval=1)
rsiPeriod = input.int(title="RSI Periyodu", defval=14, minval=1)
rsiOverboughtLevel = input.int(title="RSI Aşırı Alım Eşiği", defval=70, minval=1)
rsiOversoldLevel = input.int(title="RSI Aşırı Satım Eşiği", defval=30, minval=1)
bbPeriod = input.int(title="Bollinger Bantları Periyodu", defval=20, minval=1)
bbStdDev = input.float(title="Bollinger Bantları Standart Sapması", defval=2, minval=0.01)

// Calculate moving averages
shortEma = ta.ema(close, emaShrtPeriod)
longEma = ta.ema(close, emaLngPeriod)
movingAvg = ta.sma(close, movingAvgPeriod)

// Calculate MACD
[macdLine, signalLine, _] = ta.macd(close, macdFastPeriod, macdSlowPeriod, macdSigPeriod)

// Calculate RSI
rsiVal = ta.rsi(close, rsiPeriod)

// Calculate Bollinger Bands
[bbUpper, bbLower, _] = ta.bbands(close, length=bbPeriod, stdDev=bbStdDev)

// Buy and Sell signals
buySignal = ta.crossover(shortEma, longEma) and ta.crossover(macdLine, signalLine) and rsiVal < rsiOversoldLevel and close < bbLower
sellSignal = ta.crossunder(shortEma, longEma) and ta.crossunder(macdLine, signalLine) and rsiVal > rsiOverboughtLevel and close > bbUpper

// Plot indicators
plot(shortEma, color=color.blue, title="Short EMA")
plot(longEma, color=color.red, title="Long EMA")
plot(movingAvg, color=color.orange, title="Moving Avg")
hline(rsiOverboughtLevel, "RSI Overbought", color=color.red)
hline(rsiOversoldLevel, "RSI Oversold", color=color.green)
plot(bbUpper, color=color.blue, title="BB Upper")
plot(bbLower, color=color.red, title="BB Lower")

// Strategy logic
if (buySignal)
    strategy.entry("Buy", strategy.long)
if (sellSignal)
    strategy.exit("Sell", "Buy")
```

This code defines the strategy as described, including the necessary parameters and the logic for generating buy and sell signals based on the moving averages, MACD, RSI, and Bollinger Bands.