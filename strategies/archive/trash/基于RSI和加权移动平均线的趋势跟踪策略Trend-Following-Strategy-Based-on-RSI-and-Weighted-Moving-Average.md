> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|20|(?RSI Settings)RSI Length|
|v_input_string_1|0|(?MA Settings)MA Type: RWMA|SMA|
|v_input_int_2|20|MA Length|
|v_input_int_3|60|(?Strategy parameters)RSI Long Signal|
|v_input_int_4|40|RSI Short Signal|
|v_input_float_1|-1|ROC MA Long Signal|
|v_input_float_2|true|ROC MA Short Signal|
|v_input_float_3|5|TP activation in multiple of ATR|
|v_input_float_4|3|Trailing TP in percentage|
|v_input_int_5|400|(?Money Management)Fixed Ratio Value ($)|
|v_input_int_6|200|Increasing Order Amount ($)|
|v_input_1|timestamp(1 Jan 2018 00:00:00)|(?Backtesting Period)Start Date|
|v_input_2|timestamp(1 July 2024 00:00:00)|End Date|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-12-24 00:00:00
end: 2023-12-06 05:20:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © gsanson66

// This code is based on RSI and a backed weighted MA
//@version=5
strategy("RSI + MA BACKTESTING", overlay=true, initial_capital=1000, default
```