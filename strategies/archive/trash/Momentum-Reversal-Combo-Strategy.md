> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|5|Length1|
|v_input_6|10|Length2|
|v_input_7|20|Length3|
|v_input_8|70|TopBand|
|v_input_9|-70|LowBand|
|v_input_10|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 19/09/2019
// This is combo strategies for get a cumulative signal.
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close 
// during 2 days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market, if close price is lower than the previous close price 
// during 2 days and the meaning of 9-days Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
//    This strategy uses the CMO indicator to determine price momentum over different timeframes. It calculates the CMO values for 5, 10, and 20 periods, takes their average, and generates buy or sell signals based on whether the average is above or below certain thresholds.
//
// Combo Strategy
//    The combo strategy performs an AND operation over the signals of the two strategies. This means that it only triggers actual trading signals when both strategies give buy or sell signals simultaneously.

```