``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-28 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("OBV Strategy with SMA, RSI, SL and TP (Improved Visualization)", overlay=true)

// Calculate OBV manually
obv = ta.cum(math.sign(close - close[1]) * volume)

// Setup Simple Moving Average for OBV
lengthOBV = input(20, title="OBV SMA Length")
obvSMA = ta.sma(obv, lengthOBV)

// Setup RSI indicator
lengthRSI = input(14, title="RSI Length")
rsi = ta.rsi(close, lengthRSI)

// Setup stop loss and take profit percentages
stopLossPerc = input(2.0, title="Stop Loss %") / 100   // 2% stop loss
takeProfitPerc = input(4.0, title="Take Profit %") / 100   // 4% take profit

// Calculate stop loss and take profit levels
longStopLoss = close * (1 - stopLossPerc)
longTakeProfit = close * (1 + takeProfitPerc)
shortStopLoss = close * (1 + stopLossPerc)
shortTakeProfit = close * (1 - takeProfitPerc)

// Setup buy conditions
longCondition = ta.crossover(obv, obvSMA) and rsi < 70
if (longCondition)
    strategy.entry("Buy", strategy.long)
    strategy.exit("Take Profit/Stop Loss", "Buy", stop=longStopLoss, limit=longTakeProfit)

// Setup sell conditions
shortCondition = ta.crossunder(obv, obvSMA) and rsi > 30
if (shortCondition)
    strategy.entry("Sell", strategy.short)
    strategy.exit("Take Profit/Stop Loss", "Sell", stop=shortStopLoss, limit=shortTakeProfit)
```

``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-28 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("OBV Strategy with SMA, RSI, SL and TP (Improved Visualization)", overlay=true)

// Calculate OBV manually
obv = ta.cum(math.sign(close - close[1]) * volume)

// Setup Simple Moving Average for OBV
lengthOBV = input(20, title="OBV SMA Length")
obvSMA = ta.sma(obv, lengthOBV)

// Setup RSI indicator
lengthRSI = input(14, title="RSI Length")
rsi = ta.rsi(close, lengthRSI)

// Setup stop loss and take profit percentages
stopLossPerc = input(2.0, title="Stop Loss %") / 100   // 2% stop loss
takeProfitPerc = input(4.0, title="Take Profit %") / 100   // 4% take profit

// Calculate stop loss and take profit levels
longStopLoss = close * (1 - stopLossPerc)
longTakeProfit = close * (1 + takeProfitPerc)
shortStopLoss = close * (1 + stopLossPerc)
shortTakeProfit = close * (1 - takeProfitPerc)

// Setup buy conditions
longCondition = ta.crossover(obv, obvSMA) and rsi < 70
if (longCondition)
    strategy.entry("Buy", strategy.long)
    strategy.exit("Take Profit/Stop Loss", "Buy", stop=longStopLoss, limit=longTakeProfit)

// Setup sell conditions
shortCondition = ta.crossunder(obv, obvSMA) and rsi > 30
if (shortCondition)
    strategy.entry("Sell", strategy.short)
    strategy.exit("Take Profit/Stop Loss", "Sell", stop=shortStopLoss, limit=shortTakeProfit)
```