> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|9|Count of consecutive bars|
|v_input_3|false|useLinearRegression|
|v_input_4|13|Linear Regression length|
|v_input_5|true|Shows Supports and Resistance lines|
|v_input_6|true|Color bars when there is a signal|
|v_input_7|false|Transparency of triangle Up or Downs|
|v_input_8|true|Plot triangle Up or Downs at signal|
|v_input_9|false|Take Profit Points|
|v_input_10|false|Stop Loss Points|
|v_input_11|100|Trailing Stop Loss Points|
|v_input_12|false|Trailing Stop Loss Offset Points|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-10 00:00:00
end: 2023-12-17 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//This strategy is based on TD sequential study from glaz. 
//I made some improvement and modification to comply with pine script version 4.
//Basically, it is a strategy based on proce action, supports and resistance.

strategy("Sequential Up/Down", overlay=true )
source = input(close)
BarsCount = input(9, "Count of consecutive bars")
useLinearRegression = input(false)
LR_length = input(13,"Linear Regression length")
SR = input(true,"Shows Supports and Resistance lines")
Barcolor = input(true,"Color bars when there is a signal")
transp = input(0, "Transparency of triangle Up or Downs")
Numbers = input(true,"Plot triangle Up or Downs at signal")

//Calculation
src=useLinearRegression?linreg(source,LR_length,0):source
UP = 0
DW = 0
UP := src > src[4] ? nz(UP[1]) + 1 : 0
DW := src < src[4] ? nz(DW[1]) + 1 : 0

UPUp = UP - valuewhen(UP < UP[1], UP, 1)
DWDn = DW - valuewhen(DW < DW[1], DW, 1)

plotshape(Numbers ? UPUp == BarsCount ? true : na : na, style=shape.triangledown, text="", color=color.green, location=location.abovebar, transp=transp)
plotshape(Numbers ? DWDn == BarsCount ? true : na : na, style=shape.triangleup, text="", color=color.red, location=location.belowbar, transp=transp)


// S/R Code By johan.gradin
//------------//
// Sell Setup //
//------------//
priceflip = barssince(src < src[4])
sellsetup = src > src[4] and priceflip
sell = sellsetup and barssince(priceflip != BarsCount)
sellovershoot = sellsetup and barssince(priceflip != BarsCount+4)
sellovershoot1 = sellsetup and barssince(priceflip != BarsCount+5)
sellovershoot2 = sellsetup and barssince(priceflip != BarsCount+6)
sellovershoot3 = sellsetup and barssince(priceflip != BarsCount+7)

//----------//
// Buy setup//
//----------//
priceflip1 = barssince(src > src[4])
```