``` pinescript
/*backtest
start: 2023-11-10 00:00:00
end: 2023-12-01 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("ADXRSI Momentum Indicators Strategy", overlay=true)

// Input Parameters
adxlen = input(14, title="ADX Smoothing")
dilen = input(14, title="DI Length")
threshold = input(20, title="Threshold")
rsiLength = input(7, title="Periodo RSI")
oversoldLevel = input(30, title="Livello Ipervenduto")
overboughtLevel = input(70, title="Livello Ipercomprato")
bbLength = input(50, title="Periodo BB")
bbDeviation = input(2, title="Dev BB")

// Calculate ADX
adx = ta.adx(dilen, adxlen)

// Calculate RSI
rsi = ta.rsi(close, rsiLength)

// Calculate Bollinger Bands
src = close
basis = sma(src, bbLength)
dev = bbDeviation * ta.stdev(src, bbLength)
upperBB = basis + dev
lowerBB = basis - dev

// Buy Condition
buyCondition1 = adx > 32
buyCondition2 = rsi < oversoldLevel
buyCondition3 = close < lowerBB
buy = buyCondition1 and buyCondition2 and buyCondition3

// Sell Condition
sellCondition1 = adx > 32
sellCondition2 = rsi > overboughtLevel
sellCondition3 = close > upperBB
sell = sellCondition1 and sellCondition2 and sellCondition3

// Plot Indicators
plot(adx, title="ADX", color=color.blue)
hline(oversoldLevel, "OverSold Level")
hline(overboughtLevel, "OverBought Level")
plotshape(series=buy, location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=sell, location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Entry and Exit
strategy.entry("Buy", strategy.long, when=buy)
strategy.close("Buy", when=sell)
```

This Pine Script translates the provided Chinese document to English while maintaining the original code format and structure.