``` pinescript
/*backtest
start: 2023-05-11 00:00:00
end: 2024-05-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy('Laguerre RSI with Buy/Sell Signals and ADX Filter', shorttitle='LaRSI_ADX Signals', overlay=false)

// User Inputs
src = input(title='Source', defval=close)
alpha = input.float(title='Alpha', minval=0, maxval=1, step=0.1, defval=0.2)
buyLevel = input(20, title='Buy Level')
sellLevel = input(80, title='Sell Level')
adxPeriod = input.int(title='ADX Period', minval=14, defval=14)
adxThreshold = input.float(title='ADX Threshold', minval=25, step=1, defval=30)

// Laguerre RSI Calculation
lrsi = ta.rsi(src, 7) * (1 - alpha) + src * alpha

// ADX Calculation
[adx, adxDir] = ta.adx(high, low, close, adxPeriod)

longCondition = lrsi > buyLevel and adx > adxThreshold
shortCondition = lrsi < sellLevel and adx > adxThreshold

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

// No exit conditions in this example, you can add them as needed.
```

This code completes the Pine Script for the given trading strategy, ensuring that all user inputs and logic are maintained while translating the provided Chinese text into English.