> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|3|Swing Points|
|v_input_float_1|1.1|Median drop Mult|
|v_input_2|-5|Floating Loss|
|v_input_3|5|Number of all orders|
|v_input_4|20|Length of relative volume|
|v_input_5|2|Volume Multiplier|
|v_input_float_2|true|Take Profit Multiplier|


> Source (PineScript)

```pinescript
/*backtest
start: 2024-04-04 00:00:00
end: 2024-04-11 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © AHMEDABDELAZIZZIZO

//@version=5
strategy("Volume-based Dynamic DCA Strategy", overlay=true)

// Pa
```