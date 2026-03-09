> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|10|Fast MA|
|v_input_2|30|Slow MA|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-07 00:00:00
end: 2023-12-07 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © HosseinDaftary

//@version=4
strategy("Binomial Moving Average Trend Strategy","BMA", overlay=true, margin_long=100, margin_short=100 ,max_bars_back=96)
// Binomial Moving Average (BMA): A unique type of moving average that I developed and did not see anywhere before. It uses half of the binomial coefficients to
// calculate the average price. For example, if the period is 5, it calculates the 10th degree binomial coefficients (yielding 11 coefficients) and uses half of them.
// We use 126/256 as the weights.

```