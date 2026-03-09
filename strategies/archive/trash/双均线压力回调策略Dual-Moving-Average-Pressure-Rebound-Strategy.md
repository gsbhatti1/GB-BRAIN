> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|200|(?Parameter) Period of long-term SMA (200)|
|v_input_int_2|10|Period of short-term SMA (10)|
|v_input_int_3|5|Stop loss percentage (%)|
|v_input_int_4|20|Take profit percentage (%)|
|v_input_1|timestamp(01 Jan 2000 13:30 +0000)|Start trade day for backtest|
|v_input_2|timestamp(1 Jan 2099 19:30 +0000)|Finish date for backtest|


> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-22 00:00:00
end: 2024-02-21 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is s
