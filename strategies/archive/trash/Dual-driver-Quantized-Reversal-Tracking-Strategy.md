> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_1|false|Trade reverse|
|v_input_2|14|Length|
|v_input_3|true|KSmoothing|
|v_input_4|3|DLength|
|v_input_5|50|Level|
|v_input_6|21|LengthKAMA|
|v_input_7|false|Trade reverse|


> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-18 00:00:00
end: 2024-02-17 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 08/12/2020
// This is combo strategies for getting a cumulative signal.
//
// First strategy
// This system was created from the book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is a reverse type of strategy.
// The strategy buys at market if the close price is higher than the previous close 
// during the last 2 days and the meaning of the 9-day Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market if the close price is lower than the previous close 
// during the last 2 days and the meaning of the 9-day Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
// Everyone wants a short-term, fast trading trend that works without large
```