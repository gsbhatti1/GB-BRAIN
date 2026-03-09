> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_float_1|2|Standard Deviation (Top)|
|v_input_float_2|2|Standard Deviation (Bottom)|
|v_input_1|timestamp(01 Jan 2019 06:00 +0000)|(?backtest window)Backtest Start Date|
|v_input_2|timestamp(01 Jan 2100 00:00 +0000)|Backtest End Date|
|v_input_int_1|20|(?Bollinger Band Settings)Bollinger Band Length|
|v_input_bool_1|false|(?order entry)Use Fixed Percentage for Initial Stop?|
|v_input_int_2|8|Stop|
|v_input_string_1|0|Execute Trades On...: Wick|Close|
|v_input_bool_2|false|(?moving average filtering)Use Moving Average for Filtering (Current Timeframe)?|
|v_input_string_2|0|MA Type For Filtering: SMA|EMA|
|v_input_int_3|50|Moving Average:    Length|
|v_input_color_1|green| Color|
|v_input_bool_3|false|Use Moving Average for Filtering (High Timeframe)?|
|v_input_timeframe_1|D|Timeframe of Moving Average|
|v_input_string_3|0|MA Type For Filtering: SMA|EMA|
|v_input_int_4|50|Moving Average:    Length|
|v_input_color_2|white| Color|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-11-06 00:00:00
end: 2023-11-12 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5

// Revision:        1
// Author:          @millerrh
// Strategy:  
//      Entry: Buy when price breaks out of upper Bollinger Band
//      Exit: Tr
```