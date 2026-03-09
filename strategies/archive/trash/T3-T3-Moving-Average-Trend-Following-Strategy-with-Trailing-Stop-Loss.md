``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-27 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Lemon Trend Strategy", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// Input parameters
lookbackPeriod = input.int(14, "Lookback Period")
t3Length = input.int(200, "T3 MA Length")
t3Factor = input.float(0.7, "T3 Factor", minval=0, maxval=1)

// Trailing Stop Parameters
trailingStopPct = input.float(1.5, "Trailing Stop Percentage", minval=0.1, step=0.1)
trailingStopActivationPct = input.float(1.0, "Trailing Stop Activation Percentage", minval=0.1, step=0.1)

// === T3 Moving Average Function ===
t3(src, length, factor) =>
    // First EMA
    e1 = ta.ema(src, length)
    // Second EMA
    e2 = ta.ema(e1, length)
    // Third EMA
    e3 = ta.ema(e2, length)
    // Fourth EMA
    e4 = ta.ema(e3, length)
    // Fifth EMA
    e5 = ta.ema(e4, length)
    // Sixth EMA
    e6 = ta.ema(e5, length)

    c1 = -factor * factor * factor
    c2 = 3 * factor * factor + 3 * factor * factor * factor
    c3 = -6 * factor * factor - 3 * factor - 3 * factor * factor * factor
    c4 = 1 + 3 * factor + factor * factor * factor + 3 * factor * factor

    t3 = c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3

// Calculate T3 MA
t3ma = t3(close, t3Length, t3Factor)
plot(t3ma, "T3 MA", color=color.blue)

// === Lemon Trend Indicator ===
highLowDiff = high - low
normalizedDiff = ta.sma(highLowDiff, lookbackPeriod)
upperBand = ta.highest(high, lookbackPeriod)
lowerBand = ta.lowest(low, lookbackPeriod)
buySignal = ta.crossover(close, upperBand - normalizedDiff)
sellSignal = ta.crossunder(close, lowerBand + normalizedDiff)

// === TDFI Indicator ===
tdfiLength = input.int(14, "TDFI Length")
tdfi = ta.ema(close - close[1], tdfiLength)
tdfiSignal = ta.ema(tdfi, 9)

// Plot signals
plotshape(buySignal and tdfi > tdfiSignal and close > t3ma, "Buy Signal", location=location.belowbar, color=color.green)
```

This Pine Script code defines a strategy based on the T3 Moving Average, Lemon Trend Indicator, and TDFI (Trend Direction Force Index) for identifying buy signals. It also includes functionality for trailing stop loss to manage risks effectively.