``` pinescript
/*backtest
start: 2024-08-05 00:00:00
end: 2025-02-19 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("Triple Sync Strategy", overlay=false)
 
// Inputs
length    = input.int(14, "Base Period")
dynLen    = input.int(100, "Dynamic Lookback")
 
// DMI/ADX
dmiPlus   = ta.rma(math.max(ta.change(high), 0), length)
dmiMinus  = ta.rma(math.max(-ta.change(low), 0), length)
dx        = (math.abs(dmiPlus - dmiMinus) / (dmiPlus + dmiMinus)) * 100
adx       = ta.rma(dx, length)
 
// Stoch RSI
rsiValue  = ta.rsi(close, length)
stochRsi  = (rsiValue - ta.lowest(rsiValue, length)) / (ta.highest(rsiValue, length) - ta.lowest(rsiValue, length))
 
// CCI
cci       = ta.cci(close, length)
 
// Combined
snakeLine = (adx + stochRsi * 100 + cci) / 3
 
// Dynamic Levels
sh = ta.highest(snakeLine, dynLen)
sl = ta.lowest(snakeLine, dynLen)
 
// Signals
longCondition = crossover(snakeLine, sl)
shortCondition = crossunder(snakeLine, sh)
 
// Plotting
plot(snakeLine, title="Snake Line", color=color.blue)
plotshape(series=longCondition, location=location.belowbar, color=color.green, style=shape.labelup, text="Long")
plotshape(series=shortCondition, location=location.abovebar, color=color.red, style=shape.labeldown, text="Short")
```