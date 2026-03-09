> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Display SMA 9|
|v_input_2|true|Display EMA 20|
|v_input_3|true|Display SMA 180|
|v_input_4|false|Color-code 180 trend direction|
|v_input_5|true|Display VWAP|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-20 00:00:00
end: 2023-12-26 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © bradvaughn

//@version=4
strategy("JBravo Quantitative Trend Strategy", overlay = false)

var buy_in_progress = false


//Moving Averages
smaInput1 = input(title="Display SMA 9", type=input.bool, defval=true)
smaInput2 = input(title="Display EMA 20", type=input.bool, defval=true)
smaInput4 = input(title="Display SMA 180", type=input.bool, defval=true)
c
```