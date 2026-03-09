> Name

Backtesting-Indicator

> Author

ChaoZhang

> Strategy Description

For anyone interested, here is an example of how to integrate backtesting results into an Indicator. This calculates the same values as you find in the Summary Screen of the built-in Strategy backtester. The result size will be the same as the standard backtester; for instance, a 5-minute chart will grab roughly one month of data, and a 1-minute chart will grab about one week of data. I tried to keep this as self-contained as possible by placing most of the code for the results at the bottom of the Indicator. The results stop at the last completed trade signal; that is, a Buy has a corresponding Sell. This is the same indicator I posted earlier with the PCT Trailing StopLoss so you will see that code in here as well. As mentioned in my previous post, this indicator performs a simple EMA crossover to have something to do, and it is not recommended to use this indicator on its own but rather copy the code into your own indicator if you find it useful. I also left the code in so that you can switch back to a Strategy if you want to verify the results.

Additional Notes:
- The results are within an acceptable margin of error due to the fact that the Indicator calculates based on when Buy and Sell signals occur, rather than actual trades like in the Strategy Backtester.
- I was trying to find a way to set the number of Buy Signals to use; for example, showing results from the past 100 trades but couldn't figure out the logic. I am open to suggestions. Also keep in mind that I am not a professional coder, so if you have any ideas on that front, please explain it to me as though I am a five-year-old child and provide code examples if possible.
- I included the Strategy results in the screenshots so that you can see where the results line up.

Additional Additional Note:
This is not financial advice. Use at your own risk.

**backtest**

![IMG](https://www.fmz.com/upload/asset/eb4b87871c37c0b178.png)

> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_float_1|3000|(?Back Test) Opening Balance:|
|v_input_float_2|0.9|Allocated % (90% = .9):|
|v_input_float_3|0.075|Commission%|
|v_input_float_4|0.035|(?Sell Settings) Stop Loss Loss: 1% = .01|
|v_input_float_5|0.0065|Trailing Stop Arm: 1%=.01|
|v_input_float_6|0.003|Trailing Stop Trigger: 1%=.01 |
|v_input_int_1|14|(?Trend Line Settings) ema 1 Length|
|v_input_1_close|0|ema 1 Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_2|22| ema 2 Length|
|v_input_2_close|0|ema 2 Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_3|200| ema 3 Length|
|v_input_3_close|0|ema 2 Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-02-16 00:00:00
end: 2022-05-16 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Thumpyr
//@version=5

/////////////////////////////////////////////////////////////////////////////////////////////
// Comment out Strategy Line and remove // from Indicator line to turn into Indicator  //////
// Do same for alertConidction at bottom                                               //////
/////////////////////////////////////////////////////////////////////////////////////////////
//strategy("Backtesting-Strategy", shorttitle="Backtesting- Strategy", overlay=true, margin_long=100, margin_short=100, default_qty_type=strategy.percent_of_equity,default_qty_value=90, commission_type=strategy.commission.percent, commission_value=.075)
indicator(title="Backtesting- Indicator", shorttitle="Backtesting - Indicator", overlay=true)//


openBalance  =input.float(3000, minval=0, title="Opening Balance:", group="Back Test")
pctAllocated =input.float(.9, minval=0, title="Allocated % (90% = .9):", group="Back Test")
commission   =input.float(.075, minval=0, title="Commission%", group="Back Test")


sellLow=input.float(.035, minval=0, title="Stop Loss Loss: 1% = .01", group="Sell Settings")
trailStopArm=input.float(.0065, minval=0, title="Trailing Stop Arm: 1%=.01", group="Sell Settings")
trailStopPct=input.float(.003, minval=0, title="Trailing Stop Trigger: 1%=.01 ", group="Sell Settings")

/////////////////////////////////////////////////
//               Indicators                    //
/////////////////////////////////////////////////
ema1Len = input.int(14, minval=1, title=" ema 1 Length", group="Trend Line Settings")
ema1Src = input(close, title="ema 1 Source", group="Trend Line Settings")
ema1 = ta.ema(ema1Src, ema1Len)
plot(ema1, title="EMA", color=color.blue)

ema2Len = input.int(22, minval=1, title=" ema 2 Length", group="Trend Line Settings")
ema2Src = input(close, title="ema 2 Source", group="Trend Line Settings")
ema2 = ta.ema(ema2Src, ema2Len)
plot(ema2, title="EMA", color=color.orange)

ema3Len = input.int(200, minval=1, title=" ema 3 Length", group="Trend Line Settings")
ema3Src = input(close, title="ema 2 Source", group="Trend Line Settings")
ema3 = ta.ema(ema3Src, ema3Len)
plot(ema3, title="EMA", color=color.gray)


/////////////////////////////
////   Buy Conditions    ////
/////////////////////////////

alertBuy = ta.crossover(ema1,ema2) and close>ema3

////////////////////////////////////////////////////////////////////
////   Filter redundant Buy Signals if Sell has not happened    ////
////////////////////////////////////////////////////////////////////
var lastsignal = 0
showAlertBuy   = 0
if(alertBuy and lastsignal != 1)
    showAlertBuy           := 1
    lastsignal             := 1
buyAlert= showAlertBuy     > 0

var buyActive = 0
if  buyAlert
    buyActive :=1

//////////////////////////////////////////////////////////////////
////          Track Conditions at buy Signal                  ////
//////////////////////////////////////////////////////////////////

alertBuyValue = ta.valuewhen(buyAlert, close,0)
```