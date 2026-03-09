> Name

Get-your-trend

> Author

InnovQuant

> Strategy Description

From the popular TradingView community strategy.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|src: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|5|  1-SMA Lenght|
|v_input_3|15|  2-SMA Lenght|
|v_input_4|25|  3-SMA Lenght|
|v_input_5|15|(?Average True Range)  PP period|
|v_input_6|true|  ATR Factor|
|v_input_7|true|  ATR Period|
|v_input_8|0|(?ADX)  Adx Type: CLASSIC|MASANAKAMURA|
|v_input_9|20|  Adx Length|
|v_input_10|15|  Adx Threshold|
|v_input_11|30|(?Cloud)  Cloud Length|
|v_input_12|1.8|(?Volume)  Volume Multiplier|
|v_input_13|30|  Volume Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2020-01-28 00:00:00
end: 2022-04-27 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Bitfinex","currency":"BTC_USD"}]
*/

//@version=4

src = input(close)

strategy("Get your trend", overlay = true)


// Inputs -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Length1 =                               input(5,                                title="  1-SMA Lenght", minval=1)
Length2 =                               input(15,                               title="  2-SMA Lenght", minval=1)
Length3 =                               input(25,                               title="  3-SMA Lenght", minval=1)
prd                     =               input(15,                               title="  PP period",                                                                                                                        group="Average True Range")
Factor                  =               input(1,                                title="  ATR Factor",                                                                                                                       group="Average True Range")
Pd                      =               input(1,                                title="  ATR Period",                                                                                                                       group="Average True Range")
ADX_options         =                   input("CLASSIC",                        title="  Adx Type",                                          options = ["CLASSIC", "MASANAKAMURA"],                                          group = "ADX")
ADX_len             =                   input(20,                               title="  Adx Length",                                        type = input.integer, minval = 1,                                               group = "ADX")
th                  =                   input(15,                               title="  Adx Threshold",                                      type = input.float, minval = 0, step = 0.5,                                     group = "ADX")
len                 =                   input(30,                               title="  Cloud Length",                                                                                                                       group="Cloud")
volume_f            =                   input(1.8,                              title="  Volume Multiplier",                                  minval = 0, step = 0.1,                                                         group="Volume")
sma_length          =                   input(30,                               title="  Volume Length",                                      minval = 1,                                                                     group="Volume")

// Indicators -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

calcADX(_len) =>
    up              =                                                                                                                       change(high)
	down            =                                                                                                                      -change(low)
	plusDM          =                                                                                                                       na(up)   ? na : (up > down and up > 0   ? up   : 0)
    minusDM         =                                                                                                                       na(down) ? na : (down > up and down > 0 ? down : 0)
	truerange       =                                                                                                                       rma(tr, _len)
	_plus           =                                                                                                                       fixnan(100 * rma(plusDM, _len)  / truerange)
	_minus          =                                                                                                                       fixnan(100 * rma(minusDM, _len) / truerange)
	sum             =                                                                                                                       _plus + _minus
	_adx            =                                                                                                                       100 * rma(abs(_plus - _minus) / (sum == 0 ? 1 : sum), _len)
    [_plus,_minus,_adx]
calcADX_Masanakamura(_len) =>
    SmoothedTrueRange                   =                                                                                                   0.0
    SmoothedDirectionalMovementPlus     =  
```