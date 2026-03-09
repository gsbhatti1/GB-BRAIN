> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_bool_1|true|Use Volatility Filter|
|v_input_int_1|14|ATR Periods|
|v_input_float_1|1.5|ATR Multiplier|
|v_input_bool_2|true|Use Trailing Stop|
|v_input_float_2|15|Trailing Stop Percentage|
|v_input_bool_3|true|Use Short EMA Crosses Mid EMA to Exit Long|
|v_input_int_2|200|Long-term EMA Period|
|v_input_int_3|5|Short-term EMA Period|
|v_input_int_4|10|Mid-term EMA Period|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Long Strategy with Advanced Exit Options and Custom EMA Periods", overlay=true)

// General Input Parameters
useVolatilityFilter = input.bool(true, title="Use Volatility Filter")
atrPeriods = input.int(14, title="ATR Periods", minval=1)
atrMultiplier = input.float(1.5, title="ATR Multiplier", step=0.1)
useTrailingStop = input.bool(true, title="Use Trailing Stop")
trailingStopPercent = input.float(15.0, title="Trailing Stop Percentage", minval=0.1, step=0.1) / 100.0
useEMAExit = input.bool(true, title="Use Short EMA Crosses Mid EMA to Exit Long")

// Customizable EMA Periods Input Parameters
emaLongTermPeriod = input.int(200, title="Long-term EMA Period", minval=1)
emaShortTermPeriod = input.int(5, title="Short-term EMA Period", minval=1)
emaMidTermPeriod = input.int(10, title="Mid-term EMA Period", minval=1)

// Calculation of custom EMA
longTermEMA = ta.ema(close, emaLongTermPeriod)
shortTermEMA = ta.ema(close, emaShortTermPeriod)
midTermEMA = ta.ema(close, emaMidTermPeriod)

// ATR and Volatility Threshold Calculation
atr = ta.atr(atrPeriods)
atrThreshold = ta.sma(atr, atrPeriods) * atrMultiplier

// Entry Condition
enterLongCondition = close > longTermEMA and shortTermEMA > midTermEMA
enterLong = useVolatilityFilter ? (enterLongCondition and atr > atrThreshold) : enterLongCondition

if (enterLong)
    strategy.entry("Enter Long", strategy.long)

// Track the entry price and highest price reached for trailing stop
var float entryPrice = na
var float maxPriceSinceEntry = na
if (strategy.position_size > 0)
    maxPriceSinceEntry := math.max(na(maxPriceSinceEntry) ? high : maxPriceSinceEntry, high)
    entryPrice := na(entryPrice) ? strategy.position_avg_price : entryPrice
else
    maxPriceSinceEntry := na
    entryPrice := na

// Calculation of trailing stop value
trailStopPrice = maxPriceSinceEntry * (1 - trailingStopPercent)

// Exit Conditions Implementation
exitCrossUnder = close < longTermEMA
emaCross = ta.crossunder(shortTermEMA, midTermEMA)

if (useEMAExit and emaCross)
    strategy.close("Enter Long", comment="EMA Cross Exit")

if (useTrailingStop)
    strategy.exit("Trailing Stop", from_entry="Enter Long", stop=trailStopPrice)

// Visualizations
plot(longTermEMA, color=color.yellow, title="Long-term EMA")
plot(shortTermEMA, color=color.blue, title="Short-term EMA")
plot(midTermEMA, color=color.green, title="Mid-term EMA")
```