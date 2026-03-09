> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_hl2|0|Source: hl2|high|low|open|close|hlc3|hlcc4|ohlc4|
|v_input_2|0.07|Alpha|
|v_input_3|9|Lag|
|v_input_4|true|oppositeTrade|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-19 00:00:00
end: 2024-02-18 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Ehlers Cyber Cycle Strategy", overlay=false, default_qty_type = strategy.percent_of_equity, default_qty_value = 100.0, pyramiding = 1, commission_type = strategy.commission.percent, commission_value = 0.1)
src = input(hl2, title = "Source") 
alpha = input(0.07, title = "Alpha")
lag = input(9, title = "Lag")
smooth = (src + 2 * src[1] + 2 * src[2] + src[3]) / 6

cycle = na
if na(cycle[7])
    cycle := (src - 2 * src[1] + src[2]) / 4
else
    cycle := (1 - 0.5 * alpha) * (1 - 0.5 * alpha) * (smooth - 2 * smooth[1] + smooth[2]) + 2 * (1 - alpha) * cycle[1] - (1 - alpha) * (1 - alpha) * cycle[2]

alpha2 = 1 / (lag + 1)
signal = na
signal := alpha2 * cycle + (1 - alpha2) * nz(signal[1])
oppositeTrade = input(true)
barsSinceEntry = 0
barsSinceEntry := nz(barsSinceEntry[1]) + 1
if strategy.position_size == 0
    barsSinceEntry := 0
if
```

This PineScript code defines the strategy with the specified parameters and calculations. The `strategy` function initializes the strategy with the given name, overlay settings, and default quantity type. The `src` variable is set to the high-low average (hl2), and the `alpha` and `lag` parameters are defined. The `smooth` variable calculates the smoothed source data, and the `cycle` variable computes the cyclic indicator. The `signal` variable is then derived from the `cycle` using exponential smoothing. The `oppositeTrade` input determines whether to take opposite trades based on the previous entry. The `barsSinceEntry` variable tracks the number of bars since the last entry.