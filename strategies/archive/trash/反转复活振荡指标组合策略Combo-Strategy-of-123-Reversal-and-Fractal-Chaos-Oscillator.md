> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_1|15|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|true|Pattern|
|v_input_6|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-02 00:00:00
end: 2023-10-26 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 07/10/2020
// This is a combo strategy to get a cumulative signal.
//
// First strategy
// This system was created from the book "How I Tripled My Money in the Futures Market" by Ulf Jensen, page 183. It is a reversal type strategy.
// The strategy buys at market if the close price is higher than the previous close for 2 consecutive days, and the 9-day slow Stoch oscillator is below 50.
// The strategy sells at market if the close price is lower than the previous close for 2 consecutive days, and the 9-day fast Stoch oscillator is above 50.
//
// Second strategy
// The Fractal Chaos Oscillator calculates the difference between the most subtle movements in the market. Its value fluctuates between -1.000 and 1.000.
// The higher the value, the stronger the trend, whether an uptrend or a downtrend.
//
// When the FCO reaches a high value, initiate a "buy" operation. Conversely, when the FCO reaches a low value, initiate a "sell" operation.
// This indicator is excellent for intraday trading.
//
// WARNING:
// - For educational purposes only
// - This script to
```