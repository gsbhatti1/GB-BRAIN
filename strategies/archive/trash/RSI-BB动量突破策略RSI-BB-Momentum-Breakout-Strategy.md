> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|50|length|
|v_input_2|0.2|Mult Factor|
|v_input_3|0.1|alertLevel|
|v_input_4|0.75|impulseLevel|
|v_input_5|false|showRange|
|v_input_6|250|TP|
|v_input_7|20|SL|
|v_input_8|false|TS|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-03 00:00:00
end: 2023-11-02 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//Based on Larry Connors RSI-2 Strategy - Lower RSI
strategy(title="RSI-BB Momentum Breakout Strategy", shorttitle="RSIBB_MomentumBreakout")

length = input(50, title="Length")
multFactor = input(0.2, title="Mult Factor")
alertLevel = input(0.1, title="Alert Level")
impulseLevel = input(0.75, title="Impulse Level")
showRange = input(false, title="Show Range", type=input.bool)
takeProfit = input(250, title="Take Profit")
stopLoss = input(20, title="Stop Loss")
trailingStop = input(false, title="Trailing Stop")

basis = sma(close, length)
dev = multFactor * stdev(close, length) 
upper = basis + dev
lower = basis - dev

bbr = close > upper ? 1 : close < lower ? -1 : 0
bbi = bbr - bbr[1]

rsiUp = rma(max(change(close), 0), 30)
rsiDown = rma(-min(change(close), 0), 30) 
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

longCondition = rsi > 52 and rsi < 65 and bbi > alertLevel and bbi < impulseLevel
shortCondition = rsi < 48 and rsi > 35 and bbi < -alertLevel and bbi > -impulseLevel

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

if (showRange)
    plot(basis, color=color.blue, title="Bollinger Basis")
    plot(upper, color=color.red, title="Upper Band")
    plot(lower, color=color.green, title="Lower Band")

trailStop = not trailingStop ? 0 : max(strategy.highest(strategy.close, takeProfit), strategy.position_avg_price) - stopLoss
strategy.exit("Trail Stop", "Long", trail = true, price = trailStop)
strategy.exit("Trail Stop", "Short", trail = true, price = strategy.position_avg_price + stopLoss)

```

This PineScript code implements the RSI-BB Momentum Breakout Strategy based on the provided description. It includes the necessary calculations and trading logic as described in the original document.