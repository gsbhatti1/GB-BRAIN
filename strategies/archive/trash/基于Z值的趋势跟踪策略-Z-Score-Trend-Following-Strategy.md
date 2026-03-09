> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_string_1|0|Trading Direction: Both|Short|Long|
|v_input_int_1|100|Standard Deviation Length|
|v_input_int_2|100|Average Length|
|v_input_float_1|true|Threshold|
|v_input_1|true|Bar Color|
|v_input_2_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-04-23 00:00:00
end: 2024-04-28 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © PresentTrading

// This strategy employs a statistical approach by using a Z-score, which measures the deviation of the price from its moving average normalized by the standard deviation.
// Very simple and effective approach

//@version=5
strategy('Price Based Z-Trend - strategy [presentTrading]', shorttitle = 'Price Based Z-Trend - strategy [presentTrading]', over
<|im_start|><|im_start|>user
Continue the PineScript code from the provided snippet.