``` pinescript
/*backtest
start: 2024-09-18 00:00:00
end: 2024-09-25 00:00:00
period: 15m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Enhanced Trend Following with ML", overlay=true)

// User Inputs
shortLength = input.int(20, minval=1, title="Short Moving Average Length")
longLength = input.int(50, minval=1, title="Long Moving Average Length")
atrPeriod = input.int(14, title="ATR Period")
stopLossMultiplier = input.fl
```