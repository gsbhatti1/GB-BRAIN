``` pinescript
/*backtest
start: 2024-01-09 00:00:00
end: 2024-01-16 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Santanu Strategy", overlay=true)

atrPeriod = input(3, "ATR Length")
factor = input.float(1, "Factor", step = 0.01)

[supertrend, direction] = ta.supertrend(factor, atrPeriod)

buystop = ta.crossover(close, ta.sma(close, 14))
sellstop = ta.crossunder(close, ta.sma(close, 14))

if (supertrend > 0 and buystop)
    strategy.entry("Buy", strategy.long)

if (supertrend < 0 and sellstop)
    strategy.entry("Sell", strategy.short)

// 设置跟踪止损
stopLoss = strategy.position_size * 0.01
if (direction > 0)
    strategy.exit("Stop Loss", "Buy", stop=stopLoss)
else
    strategy.exit("Stop Loss", "Sell", stop=stopLoss)
```

This PineScript code implements the strategy described in the text. It uses the Supertrend indicator to determine entry points and sets up a tracking stop loss mechanism. The strategy enters a long position when the closing price crosses above the 14-period simple moving average, and a short position when it crosses below. The stop loss is set at 1% of the position size.