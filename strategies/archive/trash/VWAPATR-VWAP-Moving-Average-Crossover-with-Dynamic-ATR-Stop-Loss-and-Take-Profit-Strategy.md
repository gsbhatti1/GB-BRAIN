```pinescript
/*backtest
start: 2023-03-26 00:00:00
end: 2024-03-31 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Hannah Strategy Stop Loss and Take Profit", overlay=true)

// Inputs
cumulativePeriod = input(40, "VWAP Period")
atrPeriod = input(14, "ATR Period")
multiplier = input(1.5, "ATR Multiplier for Stop Loss")
targetMultiplier = input(3, "ATR Multiplier for Take Profit")

// Calculations for VWAP
typicalPrice = (high + low + close) / 3
typicalPriceVolume = typicalPrice * volume
cumulativeTypicalPriceVolume = sum(typicalPriceVolume, cumulativePeriod)
cumulativeVolume = sum(volume, cumulativePeriod)
vwapValue = cumulativeTypicalPriceVolume / cumulativeVolume

// Plot VWAP on the chart
plot(vwapValue, color=color.blue, title="VWAP")

// Entry Conditions based on price crossing over/under VWAP
longCondition = crossover(close, vwapValue)
shortCondition = crossunder(close, vwapValue)

// ATR Calculation for setting dynamic stop loss and take profit
atr = atr(atrPeriod)

// Execute Trades with Dynamic Stop Loss and Take Profit based on ATR
if (longCondition)
    strategy.entry("Long", strategy.long)
    stopLossLevel = vwapValue - multiplier * atr
    takeProfitLevel = vwapValue + targetMultiplier * atr
    
    // Set stop loss and take profit levels
    strategy.exit("Stop Loss", from_entry="Long", stop=stopLossLevel)
    strategy.exit("Take Profit", from_entry="Long", limit=takeProfitLevel)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    stopLossLevel = vwapValue + multiplier * atr
    takeProfitLevel = vwapValue - targetMultiplier * atr
    
    // Set stop loss and take profit levels
    strategy.exit("Stop Loss", from_entry="Short", stop=stopLossLevel)
    strategy.exit("Take Profit", from_entry="Short", limit=takeProfitLevel)

// Plot Stop Loss and Take Profit Levels on the chart (optional)
plot(stopLossLevel, color=color.red, title="Stop Loss")
plot(takeProfitLevel, color=color.green, title="Take Profit")

```

This Pine Script code implements the described strategy with dynamic stop loss and take profit levels based on ATR. The script defines inputs for VWAP period, ATR period, stop loss multiplier, and target multiplier, and then uses these to calculate entry and exit points based on price crossovers with VWAP. Stop loss and take profit levels are dynamically set using the calculated ATR values.