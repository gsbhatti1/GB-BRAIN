``` pinescript
/*backtest
start: 2023-12-26 00:00:00
end: 2024-01-02 00:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
// Copyright (c) 2020-present, JMOZ (1337.ltd)
// Copyright (c) 2018-present, Alex Orekhov (everget)
// Stiffness Indicator script may be freely distributed under the MIT license.
strategy("Stiffness Breakthrough Strategy", overlay=true)

// Input arguments
length = input(100, title="Moving Average Length")
stiff_length = input(60, title="Stiffness Length")
smooth_length = input(3, title="Stiffness Smoothing Length")
threshold = input(90, title="Threshold")
highlight_crossovers = input(false, title="Highlight Threshold Crossovers?", type=bool)

// Calculate moving average and standard deviation
sma_price = sma(close, length)
std_dev = ta.stdev(close, length) * 0.2

// Calculate stiffness indicator
stiffness = na
for i = 1 to stiff_length
    if close[i] > sma_price[0]
        sum = 1 + (sum == na ? 0 : sum)
    else
        sum = 0
    stiffness := sum / stiff_length

// Smooth the stiffness indicator
stiffness_smoothed = ta.ema(stiffness, smooth_length)

// Plot stiffness and threshold
plot(stiffness_smoothed, title="Stiffness", color=color.blue, linewidth=2)
hline(threshold, "Threshold", color=color.red)

// Generate buy/sell signals based on threshold crossovers
if crossover(stiffness_smoothed, threshold) and not highlight_crossovers
    strategy.entry("Buy", strategy.long)

if crossunder(stiffness_smoothed, threshold) and not highlight_crossovers
    strategy.close("Buy")

// Highlight crossovers if requested
plotshape(series=crossover(stiffness_smoothed, threshold), title="Crossover Buy Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=crossunder(stiffness_smoothed, threshold), title="Crossover Sell Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// Add stop loss
stop_loss_level = input(90, title="Stop Loss Level")
strategy.exit("Stop Loss", from_entry="Buy", stop=stop_loss_level)
```

This script defines the `Stiffness Breakthrough Strategy` as described in the document. It calculates the stiffness indicator based on the number of days the closing price exceeds a moving average and smoothes it over a specified period. Buy and sell signals are generated when the smoothed stiffness value crosses above or below the threshold, respectively. The script also includes an optional stop loss mechanism.