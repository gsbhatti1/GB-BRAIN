```pinescript
/*backtest
start: 2023-12-31 00:00:00
end: 2024-01-30 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright (C) 2023 Qwen, Alibaba Cloud.
//  This strategy is for educational purposes only.
//  Please test and use with caution.

study("Dual-Mechanism-Dynamic-Trend-Tracking-Strategy", shorttitle="DMTTS", precision=5)

// Input Parameters
length = input(14, title="Length")
kSmoothing = input(true, title="KSmoothing")
dLength = input(3, title="DLength")
level = input(50, title="Level")
lengthDSP = input(14, title="LengthDSP")
tradeReverse = input(false, title="Trade reverse")

// 123 Reversal Strategy
var float[] bull_points = array.new_float(0)
var float[] bear_points = array.new_float(0)

bull_123 = 0
bear_123 = 0

bull_123 := close[1] < close[2] and close[2] > close[3] and close[3] < close[4] and close[4] > close[5] and close[5] < close[6] and close[6] > close[7] and close[7] < close[8] and close[8] > close[9] and close[9] < close[10] and close[10] > close[11] and close[11] < close[12] and close[12] > close[13] and close[13] < close[14]
bear_123 := close[1] > close[2] and close[2] < close[3] and close[3] > close[4] and close[4] < close[5] and close[5] > close[6] and close[6] < close[7] and close[7] > close[8] and close[8] < close[9] and close[9] > close[10] and close[10] < close[11] and close[11] > close[12] and close[12] < close[13] and close[13] > close[14]

if bull_123
    array.push(bull_points, close)
if bear_123
    array.push(bear_points, close)

bull_123 := array.size(bull_points) > 0 and array.size(bull_points) % 2 == 1
bear_123 := array.size(bear_points) > 0 and array.size(bear_points) % 2 == 1

// D_DSP Index
src = close
len1 = lengthDSP / 4
len2 = lengthDSP / 2
dDsp = sma(src, len1) - sma(src, len2)

// Trade Logic
if bull_123 and dDsp > level and not tradeReverse
    strategy.entry("Buy", strategy.long)
if bear_123 and dDsp < -level and not tradeReverse
    strategy.entry("Sell", strategy.short)
if tradeReverse and bull_123 and dDsp < -level
    strategy.entry("Buy", strategy.long)
if tradeReverse and bear_123 and dDsp > level
    strategy.entry("Sell", strategy.short)

// Stop Loss
if bull_123 and dDsp < -level
    strategy.close("Buy")
if bear_123 and dDsp > level
    strategy.close("Sell")

// Plot
plot(dDsp, title="D_DSP Index", color=color.blue, linewidth=2)
plotshape(series=bull_points, title="Bull Points", location=location.abovebar, color=color.green, style=shape.labelup, text="Bull")
plotshape(series=bear_points, title="Bear Points", location=location.belowbar, color=color.red, style=shape.labeldown, text="Bear")
```

```