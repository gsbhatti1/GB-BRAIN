> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|main strat profit|
|v_input_2|true|Shorts on/off|
|v_input_3|false|Flipping on/off -> Go directly from long -> short or short -> long without closing |
|v_input_4|false|Stoploss on/off|
|v_input_5|30|Stoploss %|
|v_input_6|true|Trailing on/off|
|v_input_7|true|Trailing use ATR on/off|
|v_input_8|true|Multiplier for ATR|
|v_input_9|10|Trailing %|
|v_input_10|false|backtest date on/off|
|v_input_11|2018|Backtest Start Year|
|v_input_12|true|Backtest Start Month|
|v_input_13|true|Backtest Start Day|
|v_input_14|2019|Backtest Stop Year|
|v_input_15|true|Backtest Stop Month|
|v_input_16|true|Backtest Stop Day|
|v_input_17|true|Color Background?|
|v_input_18|20|ATR Length|
|v_input_19|false|1 for added ATR when selling|
|v_input_20|20|OC2 Length|
|v_input_21|false|1 for added OC2 when selling|
|v_input_22|true|OC2 Multiplier|
|v_input_23|10|DI Length|
|v_input_24|10|ADX Smoothing|
|v_input_25|3|smoothKRSI|
|v_input_26|3|smoothDRSI|
|v_input_27|14|lengthRSI|
|v_input_28|14|lengthStochRSI|
|v_input_29_close|0|RSI Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_30|30|RSI Buy Value|
|v_input_31|70|RSI Sell Value|
|v_input_32|20|lengthbb|
|v_input_33_close|0|Sourcebb: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_34|2|multbb|
|v_input_35|0.5|BB Buy Value|
|v_input_36|0.5|BB Sell Value|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
// THIS SCRIPT IS MEANT TO ACCOMPANY COMMAND EXECUTION BOTS
// THE INCLUDED STRATEGY IS NOT MEANT FOR LIVE TRADING
// THIS STRATEGY IS PURELY AN EXAMLE TO START EXPERIMENTATING WITH YOUR OWN IDEAS
/////////////////////////////////////////////////////////////////////////////////

// comment out the next line to use
```