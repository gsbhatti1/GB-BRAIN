> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|3|MACD fast moving average|
|v_input_2|9|MACD slow moving average|
|v_input_3|5|MACD signal line moving average|
|v_input_4|true|length|
|v_input_5|true|From Month|
|v_input_6|true|From Day|
|v_input_7|2002|From Year|
|v_input_8|3|To Month|
|v_input_9|true|To Day|
|v_input_10|2029|To Year|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-03-23 00:00:00
end: 2024-03-28 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("MACD trendfollow", shorttitle="MACD TF", overlay=true)
```