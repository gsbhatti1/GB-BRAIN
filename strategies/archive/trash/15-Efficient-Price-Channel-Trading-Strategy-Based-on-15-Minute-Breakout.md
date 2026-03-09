``` pinescript
/*backtest
start: 2024-01-17 00:00:00
end: 2024-07-25 00:00:00
period: 15m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT","balance":49999}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © OLYANGO
//@version=5
strategy("15 Min Breakout Strategy by https://x.com/iamgod43 (Yallappa)", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// Define the start of backtest period
startDate = timestamp(2023, 1, 1, 0, 0)

// Ensure the script is run on a 15-minute chart
// if (timeframe.period != "15")
//     alert("Switch to a 15-minute chart for this strategy.", alert.freq_once_per_bar_close)

// Variables to store the first 15-minute candle's high and low
var float firstCandleHigh = na
var float firstCandleLow = na
var bool isFirstCandleCaptured = false

// Detect the first candle of the session
isFirstCandle = (hour == 9 and minute == 15)

// Reset first candle values for the new session
if isFirstCandle
    firstCandleHigh := high
    firstCandleLow := low
    isFirstCandleCaptured := true

// Check for breakout conditions
longCondition = isFirstCandleCaptured and close > firstCandleHigh
shortCondition = isFirstCandleCaptured and close < firstCandleLow

// Entry signals
if longCondition
    strategy.entry("Buy Signal", strategy.long)

if shortCondition
    strategy.entry("Sell Signal", strategy.short)
```