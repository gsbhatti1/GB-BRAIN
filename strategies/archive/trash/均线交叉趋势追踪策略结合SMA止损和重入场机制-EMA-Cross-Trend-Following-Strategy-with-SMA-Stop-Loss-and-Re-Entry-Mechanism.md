``` pinescript
/*backtest
start: 2024-02-22 00:00:00
end: 2025-02-19 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=6
strategy("EMA 50 and EMA 150 with SMA150 Stop-loss and Re-Entry #ganges", overlay=true, commission_type=strategy.commission.percent, commission_value=0.1, slippage=3)

// EMA and SMA Calculations
ema50 = ta.ema(close, 50)
ema150 = ta.ema(close, 150)
sma150 = ta.sma(close, 150)

// Conditions for Buy, Sell, and Stop-Loss
ema50CrossAboveEMA150 = ta.crossover(ema50, ema150)  // Buy signal
ema50CrossBelowEMA150 = ta.crossunder(ema50, ema150) // Sell signal
priceCrossAboveEMA150 = ta.crossover(close, ema150) // Price crosses EMA 150 from below
priceCloseBelowSMA150 = close < sma150              // Stop-loss for long positions

// Track stop-loss hit state
var bool stopLossHit = false

// Strategy Logic
// Buy Logic: EMA 50 crosses EMA 150 from below
if ema50CrossAboveEMA150 
    strategy.entry("Buy Signal", strategy.long, qty=1)
    stopLossHit := false // Reset stop-loss state when a new buy position is opened

// Sell Logic: EMA 50 crosses EMA 150 from above
if ema50CrossBelowEMA150 
    strategy.entry("Sell Signal", strategy.short, qty=1)
    stopLossHit := false // Reset stop-loss state when a new sell position is opened

// Stop-Loss for Long Positions: Close if price falls below SMA 150
if strategy.position_size > 0 and priceCloseBelowSMA150
    strategy.close("Buy Signal")
    stopLossHit := true // Mark stop-loss hit

// Re-Entry Logic After Stop-Loss
if stopLossHit and priceCrossAboveEMA150
    strategy.entry("Re-Entry Long", strategy.long, qty=1)
    stopLossHit := false // Reset stop-loss state after re-entry

// Optional: Print signals for debugging
plotshape(series=ema50CrossAboveEMA150, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labeldown, text="Buy")
plotshape(series=ema50CrossBelowEMA150, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labelup, text="Sell")
```

This Pine Script implementation captures the essence of the described strategy, including the use of EMA50 and EMA150 crossovers for entry signals, the SMA150 as a stop-loss line, and a re-entry mechanism after a stop-loss is triggered.