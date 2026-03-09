> Name

OCC-Strategy-R51

> Author

ChaoZhang

> Strategy Description

Strategy R5.1 fix is a modified version of Open Close Cross Strategy R5.1 revised by JustUncleL. It helps you determine the time of entry and exit for deals.

**backtest**

![IMG](https://www.fmz.com/upload/asset/f2bbc09f841459100f.jpg)

> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_1|true|Use Alternate Resolution?|
|v_input_2|3|Multiplier for Alernate Resolution|
|v_input_string_1|0|MA Type: : SMMA|EMA|DEMA|TEMA|WMA|VWMA|SMA|HullMA|LSMA|ALMA|SSMA|TMA|
|v_input_int_1|8|MA Period|
|v_input_int_2|6|Offset for LSMA / Sigma for ALMA|
|v_input_float_1|0.85|Offset for ALMA|
|v_input_3|false|Show coloured Bars to indicate Trend?|
|v_input_int_3|false|Delay Open/Close MA (Forces Non-Repainting)|
|v_input_string_2|0|What trades should be taken : : BOTH|SHORT|LONG|NONE|
|v_input_int_4|false|Initial Stop Loss Points (zero to disable)|
|v_input_int_5|false|Initial Target Profit Points (zero for disable)|
|v_input_int_6|10000|Number of Bars for Back Testing|
|v_input_4|false|- SET to ZERO for Daily or Longer Timeframes|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-04-15 00:00:00
end: 2022-05-14 23:59:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//

indicator(title='Strategy R5.1 fix', shorttitle='OCC Strategy R5.1', overlay=true)


// === INPUTS ===
useRes = input(defval=true, title='Use Alternate Resolution?')
intRes = input(defval=3, title='Multiplier for Alernate Resolution')
stratRes = timeframe.ismonthly ? str.tostring(timeframe.multiplier * intRes, '###M') : timeframe.isweekly ? str.tostring(timeframe.multiplier * intRes, '###W') : timeframe.isdaily ? str.tostring(timeframe.multiplier * intRes, '###D') : timeframe.isintraday ? str.tostring(timeframe.multiplier * intRes, '####') : '60'
basisType = input.string(defval='SMMA', title='MA Type: ', options=['SMA', 'EMA', 'DEMA', 'TEMA', 'WMA', 'VWMA', 'SMMA', 'HullMA', 'LSMA', 'ALMA', 'SSMA', 'TMA'])
basisLen = input.int(defval=8, title='MA Period', minval=1)
offsetSigma = input.int(defval=6, title='Offset for LSMA / Sigma for ALMA', minval=0)
offsetALMA = input.float(defval=0.85, title='Offset for ALMA', minval=0, step=0.01)
scolor = input(false, title='Show coloured Bars to indicate Trend?')
delayOffset = input.int(defval=0, title='Delay Open/Close MA (Forces Non-Repainting)', minval=0, step=1)
tradeType = input.string('BOTH', title='What trades should be taken : ', options=['LONG', 'SHORT', 'BOTH', 'NONE'])
// === /INPUTS ===

// Constants colours that include fully non-transparent option.
green100 = #008000FF
lime100 = #00FF00FF
red100 = #FF0000FF
blue100 = #0000FFFF
aqua100 = #00FFFFFF
darkred100 = #8B0000FF
gray100 = #808080FF

// === BASE FUNCTIONS ===
// Returns MA input selection variant, default to SMA if blank or typo.
variant(type, src, len, offSig, offALMA) =>
    v1 = ta.sma(src, len)  // Simple
    v2 = ta.ema(src, len)  // Exponential
    v3 = 2 * v2 - ta.ema(v2, len)  // Double Exponential
    v4 = 3 * (v2 - ta.ema(v2, len)) + ta.ema(ta.ema(v2, len), len)  // Triple Exponential
    v5 = ta.wma(src, len)  // Weighted
    v6 = ta.vwma(src, len)  // Volume Weighted
    v7 = 0.0
    sma_1 = ta.sma(src, len)  // Smoothed
    v7 := na(v7[1]) ? sma_1 : (v7[1] * (len - 1) + src) / len
    v8 = ta.wma(2 * ta.wma(src, len / 2) - ta.wma(src, len), math.round(math.sqrt(len)))  // Hull
    v9 = ta.linreg(src, len, offSig)  // Least Squares
    v10 = ta.alma(src, len, offALMA, offSig)  // Arnaud Legoux
    v11 = ta.sma(v1, len)  // Triangular (extreme smooth)
    // SuperSmoother filter
    // © 2013  John F. Ehlers
    a1 = math.exp(-1.414 * 3.14159 / len)
    b1 = 2 * a1 * math.cos(1.414 * 3.14159 / len)
    c2 = b1
    c3 = -a1 * a1
    c1 = 1 - c2 - c3
    v12 = 0.0
    v12 := c1 * (src + nz(src[1])) / 2 + c2 * nz(v12[1]) + c3 * nz(v12[2])
    type == 'EMA' ? v2 : type == 'DEMA' ? v3 : type == 'TEMA' ? v4 : type == 'WMA' ? v5 : type == 'VWMA' ? v6 : type == 'SMMA' ? v7 : type == 'HullMA' ? v8 : type == 'LSMA' ? v9 : type == 'ALMA' ? v10 : type == 'TMA' ? v11 : type == 'SSMA' ? v12 : v1

// security wrapper for repeat calls
reso(exp, use, res) =>
    security_1 = request.security(syminfo.tickerid, res, exp, gaps=barmerge.gaps_off, lookahead=barmerge.lookahead_on)
    use ? security_1 : exp

// === /BASE FUNCTIONS ===

// === SERIES SETUP ===
closeSeries = variant(basisType, close[delayOffset], basisLen, offsetSigma, offsetALMA)
openSeries = variant(basisType, open[delayOffset], basisLen, offsetSigma, offsetALMA)
// === /SERIES ===

// === PLOTTING ===

// Get Alternate resolution Series if selected.
closeSeriesAlt = reso(closeSeries, useRes, stratRes)
openSeriesAlt = reso(openSeries, useRes, stratRes)
//
trendColour = closeSeriesAlt > openSeriesAlt ? color.green : color.red
bcolour = closeSeries > openSeriesAlt ? lime100 : red100
//barcolor(scolor ? bcolour : na, title='Bar Colours')
closeP = plot(closeSeriesAlt, title='Close Series', color=trendColour, linewidth=2, style=plot.style_line, transp=20)
openP = plot(openSeriesAlt, title='Open Series', color=trendColour, linewidth=2, style=plot.style_line, transp=20)
fill(closeP, openP, color=trendColour, transp=80)

// === /PLOTTING ===
//

//
// === ALERT conditions
xlong = ta.crossover(closeSeriesAlt, openSeriesAlt)
xshort = ta.crossunder(closeSeriesAlt, openSeriesAlt)
// === /ALERT conditions.

// === STRATEGY ===
// stop loss
slPoints = input.int(defval=0, title='Initial Stop Loss Points (zero to disable)', minval=0)
tpPoints = input.int(defval=0, title='Initial Target Profit Points (zero for disable)', minval=0)
// Include bar limiting algorithm
ebar = input.int(defval=10000)  
``` 

This script should now be fully translated and readable in English. If you need any further adjustments or additional information, feel free to ask!