> Name

STARC Channel Backtest Strategy

> Author

ChaoZhang

> Strategy Description



|Argument|Default|Description|
|----|----|----|
|v_input_1|5|LengthMA|
|v_input_2|15|LengthATR|
|v_input_3|1.33|K|
|v_input_4|false|Trade reverse|

> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-04 00:00:00
end: 2023-12-04 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 23/04/2018
// A type of technical indicator that is created by plotting two bands around 
// a short-term simple moving average (SMA) of an underlying asset's price. 
// The upper band is created by adding a value of the average true range 
// (ATR) - a popular indicator used by technical traders - to the moving average. 
// The lower band is created by subtracting a value of the ATR from the SMA.
// STARC is an acronym for Stoller Average Range Channels. The indicator is 
// named after its creator, Manning Stoller.
//
// You can change long to short in the Input Settings
// WARNING:
//  - For purpose educate only
//  -
```