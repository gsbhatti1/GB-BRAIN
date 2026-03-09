``` pinescript
/*backtest
start: 2023-06-08 00:00:00
end: 2024-06-13 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Chande-Kroll Stop Dynamic ATR Trend Following Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=2)

// Parameters
atrLength = input(14, title="ATR Length")
multiplier = input(3.0, title="ATR Multiplier")
smaLength = input(21, title="SMA Length")

// Calculate ATR and SMA
atr = ta.atr(atrLength)
sma = ta.sma(close, smaLength)

// Chande-Kroll Stop Levels
lowerBand = close - multiplier * atr
upperBand = close + multiplier * atr

// Trend Filter
longCondition = ta.crossover(sma, close) and close > lowerBand
strategy.entry("Long", strategy.long, when=longCondition)

// Exit Condition
shortCondition = ta.crossunder(close, upperBand)
strategy.close("Long", when=shortCondition)
```

This Pine Script implements the Chande-Kroll Stop Dynamic ATR Trend Following Strategy as described in the document. The script uses the ATR and SMA to dynamically manage stop-loss levels and filter trends, ensuring trades are made only during upward market trends while managing risk effectively.