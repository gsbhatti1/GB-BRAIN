> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Bars Until Close|
|v_input_2|true|Backtest on Twice alert?|
|v_input_3|2017|Backtest Start Year|
|v_input_4|true|Backtest Start Month|
|v_input_5|2|Backtest Start Day|
|v_input_6|2019|Backtest Stop Year|
|v_input_7|7|Backtest Stop Month|
|v_input_8|30|Backtest Stop Day|
|v_input_9|true|Color Background?|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-30 00:00:00
end: 2023-11-06 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("No Shadow Candles", overlay=true)

//set inputs
bars_until_close_trade = input(1, "Bars Until Close", minval=1)
backtest_option = input(true, "Backtest on Twice alert?", type=bool)

//set conditions
up = close > close[1] and low >= open and high <= close
down = close < close[1] and low >= close and high <= open

up2 = (close > close[1] and low >= open and high <= close) and (close[1] > close[2] and low[1] >= open[1] and high[1] <= close[1])
down2 = (close < close[1] and low >= close and high <= open) and (close[1] < close[2] and low[1] >= close[1] and high[1] <= open[1])

close_trade = barssince(up or down) == bars_until_close_trade
close_trade2 = barssince(up2 or down2) == bars_until_close_trade

//plot indicators
plotshape(up, "Up Marker", shape.triangleup, location.belowbar, color=olive, size=size.tiny, transp=50)
plotshape(down, "Down Marker", shape.triangledown, location.abovebar, color=orange, size=size.tiny, transp=50)
plotshape(up2, "Up Twice Marker", shape.triangleup, location.belowbar, color=white, size=size.small)
plotshape(down2, "Down Twice Marker", shape.triangledown, location.abovebar, color=white, size=size.small)
plotshape(close_trade, "Close Trigger", shape.circle, location.belowbar, color=fuchsia, size=size.tiny, transp=50)
plotshape(close_trade2, "Close Trigger2 (After Twice Alert)", shape.circle, location.belowbar, color=red, size=size.small)

//Strategy Testing

// Component Code Start
// Example usage:
// if testPeriod()
//   strategy.entry("LE", strategy.long)
testStartYear = input(2017, "Backtest Start Year")
testStartMonth = input(1, "Backtest Start Month")
testStartDay = input(2, "Backtest Start Day")
testStopYear = input(2019, "Backtest Stop Year")
testStopMonth = input(7, "Backtest Stop Month")
testStopDay = input(30, "Backtest Stop Day")

// Component Code End
```