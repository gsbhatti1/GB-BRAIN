``` pinescript
/*backtest
start: 2024-01-06 00:00:00
end: 2024-02-05 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © samuelarbos

//@version=4
strategy("Bollinger Bands and RSI Combination Strategy", overlay=true)

// Define Bollinger Bands parameters
source = input(close, title="Base Price")
length = input(20, minval=1, title="Length")
mult = input(2.0, minval=0.001, maxval=50, title="Standard Deviation")

// Calculate Bollinger Bands
basis = sma(source, length)
dev = mult * stdev(source, length)
upper = basis + dev
lower = basis - dev

// Define RSI parameters and calculate RSI
rsi_source = input(close, title="RSI Source")
rsi_length = input(14, minval=1, title="RSI Length")
rsi_overbought = input(70, minval=0, maxval=100, title="RSI Overbought Level")
rsi_oversold = input(30, minval=0, maxval=100, title="RSI Oversold Level")

// Calculate RSI
rsi = rsi(rsi_source, rsi_length)

// Define trading signals based on Bollinger Bands and RSI
long_condition = close > lower and rsi < rsi_oversold
short_condition = close < upper and rsi > rsi_overbought

// Plot the strategy
plot(upper, color=color.red)
plot(lower, color=color.green)

// Strategy entry and exit logic
if (long_condition)
    strategy.entry("Long", strategy.long)

if (short_condition)
    strategy.exit("Short Exit", from_entry="Long", limit=upper)

```
```