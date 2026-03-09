``` pinescript
/*backtest
start: 2024-09-15 00:00:00
end: 2024-12-10 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("RSI Cross Under Strategy", overlay=true, initial_capital=1500, default_qty_type=strategy.percent_of_equity, default_qty_value=6.6)

// Input parameters
rsiLength = input(14, "RSI Length")
rsiOversold = input(28.5, "RSI Oversold Level")
profitTarget = input(900, "Profit Target (%)")
maxPyramiding = input(15, "Max Pyramiding")

// Calculate RSI
rsi = ta.rsi(close, rsiLength)

// Detect RSI crossunder
rsiCrossunder = ta.crossunder(rsi, rsiOversold)

// Calculate the profit target price
entryPrice = strategy.position_avg_price
targetPrice = entryPrice * (1 + profitTarget / 100)

// Buy condition
if (rsiCrossunder and strategy.position_size <= maxPyramiding * strategy.equity * 0.066)
    strategy.entry("Buy", strategy.long)

// Take profit condition
if (strategy.position_size > 0 and high >= targetPrice)
    strategy.close("Buy", qty_percent = 50)

// Plot buy signals
plotshape(rsiCrossunder, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)

// Plot sell signals
plotshape(not rsiCrossunder and strategy.position_size > 0, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)
```