> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Start Date|
|v_input_2|true|Start Month|
|v_input_3|2014|Start Year|
|v_input_4|14|K|
|v_input_5|3|D|
|v_input_6|3|Smooth|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1d
basePeriod: 1h
exchanges: [{"eid":"FuturesExchangeId","currency":"BTCUSDT"}]
*/

//@version=5
strategy("Stochastic Overlap with RSI Index Quant Trading Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=50)

// Input Parameters
startDate = input.int(v_input_1, title="Start Date")
startMonth = input.int(v_input_2, title="Start Month")
startYear = input.int(v_input_3, title="Start Year")
kPeriod = input.int(v_input_4, title="K", minval=1, maxval=200)
dPeriod = input.int(v_input_5, title="D", minval=1, maxval=200)
smooth = input.int(v_input_6, title="Smooth", minval=1, maxval=200)

// Calculate Stochastic
stochK = ta.stoch(high, low, close, kPeriod, dPeriod)
stochD = ta.sma(stochK, smooth)

// Calculate RSI
rsi = ta.rsi(close, 14)

// Overbought and Oversold Conditions
overbought = stochD > 80
oversold = stochD < 20
rsiOverbought = rsi > 70
rsiOversold = rsi < 30

// Long and Short Conditions
longCondition = overbought and rsiOversold
shortCondition = oversold and rsiOverbought

// Plot Indicators
plot(stochD, color=color.blue, title="Stochastic %D")
plot(rsi, color=color.red, title="RSI")

// Strategy Logic
if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Exit Logic
if (ta.crossover(stochD, 80))
    strategy.close("Long")
if (ta.crossunder(stochD, 20))
    strategy.close("Short")
if (ta.crossover(rsi, 70))
    strategy.close("Long")
if (ta.crossunder(rsi, 30))
    strategy.close("Short")
```

This PineScript code implements the "Stochastic Overlap with RSI Index Quant Trading Strategy" as described. It includes the calculation of the Stochastic and RSI indicators, their overbought and oversold conditions, and the entry and exit logic for both long and short positions.