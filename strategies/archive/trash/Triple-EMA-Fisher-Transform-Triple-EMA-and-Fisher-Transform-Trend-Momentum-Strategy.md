``` pinescript
/*backtest
start: 2024-02-21 00:00:00
end: 2025-02-19 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("Triple EMA (TEMA) + Fisher Transform Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// ==== Triple EMA (TEMA) Settings ====
temaLength = input.int(21, title="TEMA Length", minval=1)

// Implementing Triple EMA (TEMA)
// TEMA = 3 * EMA(close, length) - 3 * EMA(EMA(close, length), length) + EMA(EMA(EMA(close, length), length), length)
ema1 = ta.ema(close, temaLength)
ema2 = ta.ema(ema1, temaLength)
ema3 = ta.ema(ema2, temaLength)
tema = 3 * ema1 - 3 * ema2 + ema3
plot(tema, color=color.blue, title="TEMA")

// ==== Fisher Transform Settings ====
fisherLength = input.int(10, title="Fisher Length", minval=1)
fisherSmooth = input.int(1, title="Fisher Smoothing", minval=1)  // Usually set to 1 or 2

// Calculation of Fisher Transform
// Step 1: Price normalization
price = (high + low) / 2
maxPrice = ta.highest(price, fisherLength)
minPrice = ta.lowest(price, fisherLength)
value = 0.5 * (2 * ((price - minPrice) / (maxPrice - minPrice)) - 1)
value := math.min(math.max(value, -0.9
```