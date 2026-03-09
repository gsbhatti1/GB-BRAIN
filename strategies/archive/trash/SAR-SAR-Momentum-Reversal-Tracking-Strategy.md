> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|0.02|initial|
|v_input_2|0.02|step|
|v_input_3|0.2|cap|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-27 00:00:00
end: 2024-02-03 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Positional Parabolic SAR Strategy", overlay=true)
initial = input(0.02)
step = input(0.02)
cap = input(0.2)
var bool isUptrend = na
var float Extremum = na
var float SARValue = na
var float Accelerator = initial
var float futureSAR = na

if bar_index > 0
    isNewTrendBar = false
    SARValue := futureSAR
    if bar_index == 1
        float pastSAR = na
        float pastExtremum = na
        previousLow = low[1]
        previousHigh = high[1]
        currentClose = close
        pastClose = close[1]
        if currentClose > pastClose
            isUptrend := true
            Extremum := high
            pastSAR := previousLow
            pastExtremum := high
        else
            isUptrend := false
            Extremum := low
            pastSAR := previousHigh
            pastExtremum := low
        isNewTrendBar := true
        SARValue := pastSAR + initial * (pastExtremum - pastSAR)
    if isUptrend
        if SARValue > low
            isNewTrendBar := true
            isUptrend := false
            SARValue := math.max(Extremum, high)
            Extremum := low
            Accelerator := initial
    else
        if SARValue < high
            isNewTrendBar := true
            isUptrend := true
            SARValue := math.min(Extremum, low)
            Extremum := high
            Accelerator := initial
    if not isNewTrendBar
        if isUptrend
            if high > Extremum
                Extremum := high
                Accelerator := math.min(Accelerator + step, cap)
        else
            if low < Extremum
                Extremum := low
                Accelerator := math.min(Accelerator + step, cap)
    if isUptrend
        SARValue := math.min(SARValue, low[1])
        if bar_index > 1
            SARValue := math.min(SARValue, low[2])
    else
        SARValue := math.max(SARValue, high[1])
        if bar_index > 1
            SARValue := math.max(SARValue, high[2])
    futureSAR := SARValue
```

Note: The `futureSAR := SARValue` line at the end of the script was added to complete the code snippet as per your instructions.