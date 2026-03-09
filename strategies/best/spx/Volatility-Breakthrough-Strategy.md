> Name

Price Volatility Breakthrough Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ee9d0469967007f329.png)
[trans]

## Overview

The Volatility Breakthrough Strategy is a trading strategy that takes advantage of price volatility patterns, executing trades when prices break through key support or resistance levels. This strategy combines multiple technical indicators to identify critical trading opportunities.

## Strategy Principle

This strategy primarily relies on the combination of Bollinger Middle Band, 48-day Simple Moving Average (SMA), MACD, and ADX four technical indicators. The specific logic is:

1. Consider trading opportunities when closing price crosses above or below the 48-day SMA;
2. When closing price breaks through the Bollinger Middle Band, it serves as an entry signal;
3. MACD greater than or less than zero helps determine trend direction;
4. ADX greater than 25 filters out non-trending markets.

When all four conditions are met, a long or short position is taken.

## Advantages of the Strategy

This strategy combines both trend and volatility indicators. Its main advantages include:

1. The 48-day SMA helps filter out excessive trading and focuses on medium-to-long-term trends;
2. Breakouts from the Bollinger Middle Band capture key support/resistance break points with strong stop loss functionality;
3. MACD aids in determining major trend directions, avoiding trades against the prevailing trend;
4. ADX filters non-trending markets to improve the overall win rate of the strategy.

In summary, this strategy optimizes trading frequency, captures critical points, determines trend direction, and filters out invalid moves, leading to a higher win rate.

## Risks of the Strategy

The primary risks associated with this strategy are:

1. In volatile markets, frequent triggers from the Bollinger Middle Band may lead to excessive trading;
2. The ADX indicator can have errors in determining trends or non-trending periods;
3. Significant drawdown risk; suitable for investors who can tolerate a certain level of risk.

## Optimization Directions

This strategy can be further optimized in the following areas:

1. Add ATR indicators to set stop loss points and reduce single trade losses;
2. Optimize Bollinger Band parameters to decrease middle band trigger frequency;
3. Incorporate trading volume or trend strength indicators to assess the strength of trends, avoiding weak reversals.

## Summary

In summary, this Volatility Breakthrough Strategy is relatively mature, effectively capturing key trading points during volatile periods. It combines trend and volatility indicators while balancing risk and return. With further optimization, it can generate more stable excess returns.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|12|fastLength|
|v_input_3|26|slowlength|
|v_input_4|9|MACDLength|
|v_input_5|20|length|
|v_input_6|2|mult|
|v_input_7|25|ADX Threshold|
|v_input_8|14|ADX Smoothing|
|v_input_9|14|DI Length|
|v_input_10|false|Take Profit Points|
|v_input_11|false|Stop Loss Points|
|v_input_12|false|Trailing Stop Loss Points|
|v_input_13|false|Trailing Stop Loss Offset Points|
|v_input_14|false|Custom Backtesting Dates|
|v_input_15|2020|Backtest Start Year|
|v_input_16|true|Backtest Start Month|
|v_input_17|true|Backtest Start Day|
|v_input_18|false|Backtest Start Hour|
|v_input_19|2020|Backtest Stop Year|
|v_input_20|12|Backtest Stop Month|
|v_input_21|31|Backtest Stop Day|
|v_input_22|23|Backtest Stop Hour|

> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-11 00:00:00
end: 2023-12-12 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © 03.freeman
// Volatility Traders Minds Strategy (VTM Strategy)
// I found this strategy on internet, with a video explaining how it works.
// Conditions for entry:
// 1 - Candles must be above or below the 48 MA (Yellow line)
// 2 - Candles must break the middle of Bollinger Bands
// 3 - MACD must be above or below zero level;
// 4 - ADX must be above 25 level
//@version=4
strategy("Volatility Traders Minds Strategy (VTM Strategy)", shorttitle="VTM", overlay=true)
source = input(close)
// MA
ma48 = sma(source, 48)
// MACD
fastLength = input(12)
slowlength = input(26)
MACDLength = input(9)

MACD = ema(source, fastLength) - ema(source, slowlength)
aMACD = ema(MACD, MACDLength)
delta = MACD - aMACD

// BB
length = input(20, minval=1)
mult = input(2.0, minval=0.001, maxval=50)

basis = sma(source, length)
dev = mult * stdev(source, length)

upper = basis + dev
lower = basis - dev

// ADX
adxThreshold = input(title="ADX Threshold", type=input.integer, defval=25, minval=1)
adxlen = input(14, title="ADX Smoothing")
dilen = input(14, title="DI Length")

dirmov(len) =>
	up = change(high)
	down = -change(low)
	plusDM = na(up) ? na : (up > down and up > 0 ? up : 0)
	minusDM = na(down) ? na :
```