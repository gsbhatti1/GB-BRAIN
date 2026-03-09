``` pinescript
/*backtest
start: 2024-03-01 00:00:00
end: 2024-03-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Triple EMA Crossover Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Input for EMA periods
fastLength = input(10, title="Fast EMA Length")
mediumLength = input(25, title="Medium EMA Length")
slowLength = input(50, title="Slow EMA Length")
riskMultiplier = input(3.0, title="Risk Multiplier for Stop Loss and Take Profit")

// Calculating EMAs
fastEMA = ta.ema(close, fastLength)
mediumEMA = ta.ema(close, mediumLength)
slowEMA = ta.ema(close, slowLength)

// Plot EMAs
plot(fastEMA, color=color.blue, title="Fast EMA")
plot(mediumEMA, color=color.green, title="Medium EMA")
plot(slowEMA, color=color.red, title="Slow EMA")

// Calculate ATR for stop-loss and take-profit levels
atrLength = input(14, title="ATR Length", minval=1)
atrValue = ta.atr(atrLength)

// Generate buy signal when fast EMA crosses above slow EMA and medium EMA is above slow EMA
buySignal = ta.crossover(fastEMA, slowEMA) and ta.gt(mediumEMA, slowEMA)
if (buySignal)
    strategy.entry("Buy", strategy.long)
    strategy.exit("Take Profit", "Buy", stop=slowEMA + riskMultiplier * atrValue)

// Generate sell signal when fast EMA crosses below slow EMA and medium EMA is below slow EMA
sellSignal = ta.crossunder(fastEMA, slowEMA) and ta.lt(mediumEMA, slowEMA)
if (sellSignal)
    strategy.entry("Sell", strategy.short)
    strategy.exit("Stop Loss", "Sell", stop=slowEMA - riskMultiplier * atrValue)
```

This Pine Script code implements the described Triple EMA Crossover Strategy. It includes the setup of EMAs, plotting them on the chart, and setting up entry and exit conditions based on the specified parameters.