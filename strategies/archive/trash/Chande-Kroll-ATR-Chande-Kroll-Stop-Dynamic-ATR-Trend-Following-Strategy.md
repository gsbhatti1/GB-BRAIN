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

atrLength = input.int(14, title="ATR Length")
multiplier = input.float(3.0, title="ATR Multiplier")

smaPeriod = input.int(21, title="SMA Period")

// Calculate ATR
atrValue = ta.atr(atrLength)

// Chande-Kroll Stop Levels
lowerBand = close - multiplier * atrValue
upperBand = close + multiplier * atrValue

// 21-period SMA
sma = ta.sma(close, smaPeriod)

// Strategy Conditions
longCondition = close > lowerBand and close > sma
if (longCondition)
    strategy.entry("Long", strategy.long)

// Exit Condition
exitCondition = close < upperBand
if (exitCondition)
    strategy.close("Long")

// Plot Bands and SMA on the chart
plot(lowerBand, color=color.red, title="Chande-Kroll Lower Band")
plot(upperBand, color=color.green, title="Chande-Kroll Upper Band")
hline(sma, "SMA", color=color.blue)
```