``` pinescript
/*backtest
start: 2022-04-12 00:00:00
end: 2022-05-11 23:59:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5


// Original Script > @DonovanWall

// Previous Version > @guikroth
// Ultimate Oscillator > @PineCoders

// Updated by > @jwelmac


//////////////////////////////////////////////////////////////////////////
// Range Filter x 2, EMA and UO
//////////////////////////////////////////////////////////////////////////


indicator(title='FTL - Range Filter X2 + EMA + UO', overlay=true)

// Groups

string groupLeadingRange = "Leading Range Filter"
string groupTriggerRange = "Trigger Range Filter"
string groupEMA = "EMA"
string groupUO = "Ultimate Oscillator (UO)"
string GROUP_BUY_OPTIONS = "Buy Options"
string GROUP_SELL_OPTIONS = "Sell Options"


//-------  *********  --------  *********  ---------
// Range Filter (Leader) {

// Source
src = input(defval=hl2, title='Source', group=groupLeadingRange)

// Sampling Period
per = input.int(defval=30, minval=1, title='Sampling Period', group=groupLeadingRange)

// Range Multiplier
mult = input.float(defval=2.6, minval=0.1, title='Range Multiplier', group=groupLeadingRange)

// Smooth Average Range {
smoothrng(x, t, m) =>
    wper = t * 2 - 1
    avrng = ta.ema(math.abs(x - x[1]), t)
    _smoothrng = ta.ema(avrng, wper) * m
    _smoothrng
// }
smrng = smoothrng(src, per, mult)

// Range Filter{
rngfilter(x, r) =>
    rngfilt = x
    rngfilt := x > nz(rngfilt[1]) ? x - r < nz(rngfilt[1]) ? nz(rngfilt[1]) : x - r : x + r > nz(rngfilt[1]) ? nz(rngfilt[1]) : x + r
    rngfilt
//}
filt = rngfilter(src, smrng)

// Filter Direction

upward = 0.0
upward := filt > filt[1] ? nz(upward[1]) + 1 : filt < filt[1] ? 0 : nz(upward[1])

downward = 0.0
downward := filt < filt[1] ? nz(downward[1]) + 1 : filt > filt[1] ? 0 : nz(downward[1])


// Colors

filtcolor = upward > 0 ? color.lime : downward > 0 ? color.red : color.orange

filtplot = plot(filt, color=filtcolor, linewidth=1, title='Range Filter (Leader)')

// }
//-------  *********  --------  *********  ---------

//-------  *********  --------  *********  ---------
// Range Filter (Trigger){
// Source
src2 = input(defval=ohlc4, title='Source', group=groupTriggerRange)

// Sampling Period
// Settings for 1min chart, US 100.

per2 = input.int(defval=48, minval=1, title='Sampling Period', group=groupTriggerRange)

// Range Multiplier

mult2 = input.float(defval=3.4, minval=0.1, title='Range Multiplier', group=groupTriggerRange)

// Smooth Average Range

smrng2 = smoothrng(src2, per2, mult2)

// Range Filter

rngfilt2(x, r) =>
    rngfilt = x
    rngfilt := x > nz(rngfilt[1]) ? x - r < nz(rngfilt[1]) ? nz(rngfilt[1]) : x - r : x + r > nz(rngfilt[1]) ? nz(rngfilt[1]) : x + r
    rngfilt
filt2 = rngfilt2(src2, smrng2)

// Filter Direction

upward2 = 0.0
upward2 := filt2 > filt2[1] ? nz(upward2[1]) + 1 : filt2 < filt2[1] ? 0 : nz(upward2[1])
downward2 = 0.0
downward2 := filt2 < filt2[1] ? nz(downward2[1]) + 1 : filt2 > filt2[1] ? 0 : nz(downward2[1])

// Colors

filtcolor2 = upward2 > 0 ? color.lime : downward2 > 0 ? color.red : color.orange

filtplot2 = plot(filt2, color=filtcolor2, linewidth=3, title='Range Filter (trigger)')

barcolor = src2 > filt2 and upward2 > 0
   ? color.green 
   : src2 < filt2 and downward > 0 
     ? color.red 
     : color.rgb(120, 123, 134)
// Bar Color
//barcolor(barcolor)

// }
//-------  *********  --------  *********  ---------


//-------  *********  --------  *********  ---------
// Default EMA 144 {
len4 = input.int(144, minval=1, title='Length', group=groupEMA)
src4 = input(close, title='Source')
ema4 = ta.ema(src4, len4)

// }
```

> Strategy Arguments

``` pinescript
|Argument|Default|Description|
|----|----|----|
|v_input_3_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_1_hl2|0|(?Leading Range Filter)Source: hl2|high|low|open|close|hlc3|hlcc4|ohlc4|
|v_input_int_1|30|Sampling Period|
|v_input_float_1|2.6|Range Multiplier|
|v_input_2_ohlc4|0|(?Trigger Range Filter)Source: ohlc4|high|low|open|hl2|hlc3|hlcc4|close|
|v_input_int_2|48|Sampling Period|
|v_input_float_2|3.4|Range Multiplier|
|v_input_int_3|144|(?EMA)Length|
|v_input_bool_1|false|Show crossover only in uptrend|
|v_input_bool_2|false|Show crossunder only in downtrend|
|v_input_int_4|7|(?Ultimate Oscillator UO)Fast Length|
|v_input_int_5|14|Middle Length|
|v_input_int_6|28|Slow Length|
|v_input_float_3|60|(?Buy Options)UO Overbought value|
|v_input_bool_3|true|Show BUY only when not overbought (UO)|
|v_input_bool_4|true|Show BUY only above the EMA|
|v_input_float_4|40|(?Sell Options)UO Oversold value|
|v_input_bool_5|true|Show SELL only when not oversold (UO)|
|v_input_bool_6|true|Show SELL only below the EMA|
```