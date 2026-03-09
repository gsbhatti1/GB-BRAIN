> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|RSI Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|14|RSI Length|
|v_input_3|70|RSI Overbought Level|
|v_input_4|30|RSI Oversold Level|

> Source (PineScript)

```pinescript
/*backtest
start: 2023-01-15 00:00:00
end: 2024-01-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Phil's Pine Scripts - low risk long DCA Trend trade", overlay=true)

////
//// trade on BTCUSDT 4H
```