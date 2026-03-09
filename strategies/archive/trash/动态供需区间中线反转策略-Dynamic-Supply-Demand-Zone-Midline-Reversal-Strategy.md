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

// Determine entry conditions based on current price position relative to SMA and Midpoint
if (close > smaTrend and close < midpoint)
    strategy.entry("Long", strategy.long, when=close < supplyZone) // Long entry if price is below supply zone

if (close < smaTrend and close > midpoint)
    strategy.entry("Short", strategy.short, when=close > demandZone) // Short entry if price is above demand zone

// Take-Profit and Stop-Loss Setup
takeProfitLevel = max(supplyZone, demandZone) + 10 * syminfo.mintick // Adjust take-profit level based on supply/demand zones
stopLossLevel = min(supplyZone, demandZone) - 5 * syminfo.mintick    // Adjust stop-loss level based on supply/demand zones

// Set take-profits and stop-losses for long trades
strategy.exit("TakeProfit", from_entry="Long", limit=takeProfitLevel)
strategy.exit("StopLoss", from_entry="Long", stop=stopLossLevel)

// Set take-profits and stop-losses for short trades
strategy.exit("TakeProfit", from_entry="Short", limit=stopLossLevel)
strategy.exit("StopLoss", from_entry="Short", stop=takeProfitLevel)
```