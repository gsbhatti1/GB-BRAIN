``` pinescript
/*backtest
start: 2025-02-16 00:00:00
end: 2025-02-23 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © bommytarton

//@version=6
strategy("Midline Rejection Entry with TP/SL at Supply/Demand", overlay=true)

// User inputs for Swing Length and Length for Supply/Demand Zones
length = input.int(50, title="Swing Length", minval=1)
midlineLength = input.int(20, title="Midline Length for Trend", minval=1)  // Moving average length for trend

// Identify swing highs (Supply Zone) and swing lows (Demand Zone)
supplyZone = ta.highest(high, length) // Supply Zone (resistance)
demandZone = ta.lowest(low, length) // Demand Zone (support)

// Calculate the midpoint between supply and demand zones
midpoint = (supplyZone + demandZone) / 2

// Trend Detection: Use a simple moving average (SMA) for trend direction
smaTrend = ta.sma(close, midlineLength)

// Variables to store Supply/Demand Zones at the time of entry
var float entrySupplyZone = na
var float entryDemandZone = na

// Entry Conditions
if (close > smaTrend and close < midpoint)  // Long entry condition: Price above SMA and below Midpoint
    entryPrice = close
    takeProfit = supplyZone
    stopLoss = demandZone
    strategy.entry("Long", strategy.long, when=close > smaTrend and close < midpoint)
    
if (close < smaTrend and close > midpoint)  // Short entry condition: Price below SMA and above Midpoint
    entryPrice = close
    takeProfit = demandZone
    stopLoss = supplyZone
    strategy.entry("Short", strategy.short, when=close < smaTrend and close > midpoint)

// Set Take-Profit and Stop-Loss
if (strategy.position_size > 0)  // For long positions
    strategy.exit("Take Profit/Stop Loss", "Long", profit_target=takeProfit, stop_loss=stopLoss)
    
if (strategy.position_size < 0)  // For short positions
    strategy.exit("Take Profit/Stop Loss", "Short", profit_target=takeProfit, stop_loss=stopLoss)

// Plotting supply and demand zones and midpoint on the chart
plot(supplyZone, color=color.red, title="Supply Zone")
plot(demandZone, color=color.green, title="Demand Zone")
plot(midpoint, color=color.blue, title="Midline")

```