``` pinescript
/*backtest
start: 2022-10-17 00:00:00
end: 2023-01-31 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("SMA-Crossing-RSI Golden Cross Death Cross Trading Strategy", overlay=true)

// SMA Configuration
lengthMA = 200
sma200 = sma(close, lengthMA)

// RSI Configuration
lengthRSI = 14
rsiValue = rsi(close, lengthRSI)
overBought = 70
overSold = 30

// Buy Condition
longCondition = close < sma200 and crossover(rsiValue, overSold)
if (longCondition)
    strategy.entry("Buy", strategy.long)

// Sell Condition
shortCondition = close > sma200 and crossunder(rsiValue, overBought)
if (shortCondition)
    strategy.close("Buy")

// Plot SMA and signals
plot(sma200, title="SMA 200", color=color.blue)
plotshape(series=longCondition, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="Buy")
plotshape(series=shortCondition, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="Sell")
```