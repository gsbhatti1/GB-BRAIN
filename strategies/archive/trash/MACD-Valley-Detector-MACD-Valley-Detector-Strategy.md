> Strategy Arguments



|Argument|Default|Description|
|--------|-------|-----------|
|v_input_1|12|fastLength|
|v_input_2|26|slowlength|
|v_input_3|9|MACDLength|


> Source (PineScript)

```pinescript
/*backtest
start: 2024-03-12 00:00:00
end: 2024-04-11 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0

//@version=5
indicator("MACD Valley Detector Strategy", overlay=false)

fastLength = input(12, title="Fast Length")
slowLength = input(26, title="Slow Length")
macdLength = input(9, title="MACD Length")

[fastSMA, slowSMA, macdLine] = ta.macd(close, fastLength, slowLength, macdLength)

// Detecting MACD valley
var int lastValleyIdx = na
lastValleyDiff = 0.0

for i = 1 to bar_index - 1
    if (macdLine[i + 1] < macdLine[i] and macdLine[i - 1] > macdLine[i])
        if ((macdLine[i] <= -0.4) and (macdLine[i] - ta.signal_line(macdLine, signal_length=9)[i]) < 0)
            lastValleyIdx := i
            lastValleyDiff := macdLine[i]

// Generate buy signal
if not na(lastValleyIdx) and bar_index == lastValleyIdx + 1
    plotshape(series=lastValleyIdx, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")

// Take profit price
takeProfitValue = input(50, title="Take Profit Value")
plot(takeProfitValue + close, title="Take Profit Price", color=color.red)

//@version=4
// Strategy definition in Pine Script v4 (not used here)
```