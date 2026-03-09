> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|8|EMA1 Length|
|v_input_2|14|EMA2 Length|
|v_input_3|50|EMA3 Length|
|v_input_4|3|K|
|v_input_5|3|D|
|v_input_6|14|RSI Length|
|v_input_7|14|Stochastic Length|
|v_input_8_close|0|RSI Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_9|14|ATR Period|
|v_input_10|2|Take-profit Multiplier|
|v_input_11|3|Stop-loss Multiplier|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-10-15 00:00:00
end: 2023-11-14 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © FreddieChopin

//@version=4
strategy("3 x EMA + Stochastic RSI + ATR", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100)

// 3x EMA
ema1Length = input(8, "EMA1 Length", minval = 1)
ema2Length = input(14, "EMA2 Length", minval = 1)
ema3Length = input(50, "EMA3 Length", minval = 1)
ema1 = ema(close, ema1Length)
ema2 = ema(close, ema2Length)
ema3 = ema(close, ema3Length)

plot(ema1, color = color.green)
plot(ema2, color = color.orange)
plot(ema3, color = color.red)

// Stochastic RSI
smoothK = input(3, "K", minval=1)
smoothD = input(3, "D", minval=1)
lengthRSI = input(14, "RSI Length", minval=1)
lengthStoch = input(14, "Stochastic Length", minval=1)
src = input(close, title="RSI Source")
rsi1 = rsi(src, lengthRSI)
k = sma(stoch(rsi1, rsi1, rsi1, lengthStoch), smoothK)
d = sma(k, smoothD)

// ATR
atrPeriod = input(14, "ATR Period")
takeProfitMultiplier= input(2.0, "Take-profit Multiplier")
stopLossMultiplier= input(3.0, "Stop-loss Multiplier")
atrSeries = atr(atrPeriod)[1]

longCondition = ema1 > ema2 and ema2 > ema3 and crossover(k, d)
strategy.entry("long", strategy.long, when = longCondition)

float stopLoss = na
float takeProfit = na

if (strategy.position_size > 0)
    if (na(stopLoss[1]))
        stopLoss := strategy.position_avg_price - atrSeries * stopLossMultiplier
    else
        stopLoss := stopLoss[1]
    if (na(takeProfit[1]))
        takeProfit := strategy.position_avg_price + atrSeries * takeProfitMultiplier
    else
        takeProfit := takeProfit[1]

    strategy.exit("take profit / stop loss", limit = takeProfit, stop = stopLoss)

plot(stopLoss, color = color.red, linewidth = 2, style = plot.style_linebr)
plot(takeProfit, color = color.green, linewidth = 2, style = plot.style_linebr)
```

> Detail

https://www.fmz.com/strategy/376852