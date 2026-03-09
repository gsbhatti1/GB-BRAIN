> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|40|VWAP Period|
|v_input_2|14|ATR Period|
|v_input_3|1.5|ATR Multiplier for Stop Loss|
|v_input_4|3|ATR Multiplier for Take Profit|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-03-26 00:00:00
end: 2024-03-31 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("VWAP Moving Average Crossover with Dynamic ATR Stop Loss and Take Profit Strategy", overlay=true)

// Inputs
v_input_1 = input(40, "VWAP Period")
v_input_2 = input(14, "ATR Period")
v_input_3 = input(1.5, "ATR Multiplier for Stop Loss")
v_input_4 = input(3, "ATR Multiplier for Take Profit")

// Calculations for VWAP
typicalPrice = (high + low + close) / 3
typicalPriceVolume = typicalPrice * volume
cumulativeTypicalPriceVolume = ta.csum(typicalPriceVolume, v_input_1)
cumulativeVolume = ta.csum(volume, v_input_1)
vwapValue = cumulativeTypicalPriceVolume / cumulativeVolume

// Plot VWAP on the chart
plot(vwapValue, color=color.blue, title="VWAP")

// Entry Conditions based on price crossing over/under VWAP
longCondition = ta.crossover(close, vwapValue)
shortCondition = ta.crossunder(close, vwapValue)

// ATR Calculation for setting dynamic stop loss and take profit
atrValue = ta.atr(v_input_2)

// Execute Trades with Dynamic Stop Loss and Take Profit based on ATR
if (longCondition)
    strategy.entry("Long", strategy.long)
    stopLossLevel = vwapValue - v_input_3 * atrValue
    takeProfitLevel = vwapValue + v_input_4 * atrValue
    strategy.exit("Take Profit Long", "Long", stop=stopLossLevel, limit=takeProfitLevel)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    stopLossLevel = vwapValue + v_input_3 * atrValue
    takeProfitLevel = vwapValue - v_input_4 * atrValue
    strategy.exit("Take Profit Short", "Short", stop=stopLossLevel, limit=takeProfitLevel)

// Plot Stop Loss and Take Profit Levels on the chart (optional)
plot(stopLossLevel, color=color.red, title="Stop Loss Level")
plot(takeProfitLevel, color=color.green, title="Take Profit Level")

```

This PineScript code implements the described VWAP Moving Average Crossover with Dynamic ATR Stop Loss and Take Profit Strategy. It includes all necessary components as per the provided description and arguments.