> Name

Moving-Average-Directionality-Trend-Strategy

> Author

ChaoZhang

> Strategy Description


<!-- AUTO-TRANSLATE FAILED: the JSON object must be str, bytes or bytearray, not NoneType -->


## Strategy Logic

This strategy determines the long-term trend direction by analyzing the directionality of multiple moving averages. It goes long or short according to the trend.

The logic is:

1. Compute moving averages of differing periods, e.g., 5-day, 20-day, 50-day, etc.
2. Compare the directional tendency of the MAs to determine consistent alignment
3. When all MAs are uniformly trending up, a long-term bullish view is held. When uniformly down, a long-term bearish view is held.
4. In bullish conditions, breakouts above the downside stop loss trigger long entries
5. In bearish conditions, breakouts below the upside stop loss trigger short entries
6. Trailing stops are used to control risk

The strategy emphasizes confirming the long-term trend before trading to reduce non-systematic risk.

## Advantages

- Multiple MAs combine to judge long-term trend directionality
- Breakout entries follow the trend 
- Trailing stop strategy controls risk

## Risks

- MAs themselves lag prices
- Incorrect trend judgement can lead to sustained losses
- LONG or SHORT only misses opportunities

## Summary 

This strategy stresses determining the secular trend via MA directionality to minimize non-systematic risks. But judgment accuracy and stop tuning are critical.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|0|Moving Average Type: sma|ema|hma|rma|vwma|wma|
|v_input_2|5|LookbackPeriod|
|v_input_3|10|shortHighLowPeriod|
|v_input_4|20|longHighLowPeriod|
|v_input_5|22|atrlength|
|v_input_6|6|stopMultiplyer|
|v_input_7|3|reentryStopMultiplyer|
|v_input_8|false|exitOnSignal|
|v_input_9|0|Trade Direction: strategy.direction.long|strategy.direction.all|strategy.direction.short|
|v_input_10|10|backtestYears|

> Source (PineScript)

```pinescript
/*backtest
start: 2022-09-07 00:00:00
end: 2023-06-24 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © HeWhoMustNotBeNamed

//@version=4
strategy("TrendMaAlignmentStrategy", overlay=true, initial_capital = 2000, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, commission_type = strategy.commission.cash_per_order, pyramiding = 1, commission_value = 2)

MAType = input(title="Moving Average Type", defval="sma", options=["ema", "sma", "hma", "rma", "vwma", "wma"])
LookbackPeriod = input(5, step=10)
shortHighLowPeriod = input(10, step=10)
longHighLowPeriod = input(20, step=10)

atrlength=input(22)
stopMultiplyer = input(6, minval=1, maxval=10, step=0.5)
reentryStopMultiplyer = input(3, minval=1, maxval=10, step=0.5)
exitOnSignal = input(false)
tradeDirection = input(title="Trade Direction", defval=strategy.direction.long, options=[strategy.direction.all, strategy.direction.long, strategy.direction.short])

backtestYears = input(10, minval=1, step=1)
inDateRange = true

allowReduceCompound=true
includePartiallyAligned = true
considerYearlyHighLow = true
considerNewLongTermHighLows = true

//////////////////////////////////// Get Moving average ///////////////////////////////////
f_getMovingAverage(source, MAType, length)=>
    ma = sma(source, length)
    if(MAType == "ema")
        ma := ema(source,length)
    if(MAType == "hma")
        ma := hma(source,length)
    if(MAType == "rma")
        ma := rma(source,length)
    if(MAType == "vwma")
        ma := vwma(source,length)
    if(MAType == "wma")
        ma := wma(source,length)
    ma
    
f_getMaAlignment(MAType, includePartiallyAligned)=>
    ma5 = f_getMovingAverage(close,MAType,5)
    ma10 = f_getMovingAverage(close,MAType,10)
    ma20 = f_getMovingAverage(close,MAType,20)
    ma30 = f_getMovingAverage(close,MAType,30)
    ma50 = f_getMovingAverage(close,MAType,50)
    ma100 = f_getMovingAverage(close,MAType,100)
    ma200 = f_getMovingAverage(close,MAType,200)

    upwardScore = 0
    upwardScore := close > ma5 ? upwardScore+1 : upwardScore
    upwardScore := ma5 > ma10 ? upwardScore+1 : upwardScore
    upwardScore := ma10 > ma20 ? upwardScore+1 : upwardScore
    upwardScore := ma20 > ma30 ? upwardScore+1 : upwardScore
    upwardScore := ma30 > ma50 ? upwardScore+1 : upwardScore
    upwardScore := ma50 > ma100 ? upwardScore+1 : upwardScore
    upwardScore := ma100 > ma200 ? upwardScore+1 : upwardScore
    
    upwards = close > ma5 and ma5 > ma10 and ma10 > ma20 and ma20 > ma30 and ma30 > ma50 and ma50 > ma100 and ma100 > ma200
    downwards = close < ma5 and ma5 < ma10 and ma10 < ma20 and ma20 < ma30 and ma30 < ma50 and ma50 < ma100 and ma100 < ma200
    upwards ? 1 : downwards ? -1 : includePartiallyAligned ? (upwardScore > 5 ? 0.5 : upwardScore < 2 ? -0.5 : upwardScore > 3 ? 0.25 : -0.25) : 0

f_getMaAlignmentHighLow(MAType, includePartiallyAligned, LookbackPeriod)=>
    maAlignment = f_getMaAlignment(MAType,includePartiallyAligned)
    [highest(maAlignment, LookbackPeriod), lowest(maAlignment, LookbackPeriod)]

//////////////////////////////////// Calculate new high low condition //////////////////////////////////////////////////
f_calculateNewHighLows(shortHighLowPeriod, longHighLowPeriod, considerNewLongTermHighLows)=>
    newHigh = highest(shortHighLowPeriod) == highest(longHighLowPeriod) or not considerNewLongTermHighLows
    newLow = lowest(shortHighLowPeriod) == l
```