> Name

Volatility Breakthrough Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ee9d0469967007f329.png)
[trans]

## Overview

The Volatility Breakthrough Strategy is a trading strategy that takes advantage of price volatility patterns by entering trades when prices break through key support or resistance levels. This strategy combines various technical indicators to identify critical trading opportunities.

## Strategy Principle  

This strategy primarily relies on Bollinger Middle Band, 48-day Simple Moving Average (SMA), MACD, and ADX four technical indicators. The specific logic is:

1. Consider trading opportunities when the closing price crosses above or below the 48-day SMA;

2. When the closing price breaks through the Bollinger Middle Band, it serves as an entry signal;

3. The MACD must be greater than or less than zero to determine trend direction;

4. ADX must be greater than 25 to filter out non-trending markets.

When all four conditions are met, a long or short position is taken.

## Advantages of the Strategy

This is a strategy that combines trend and volatility indicators. Its main advantages include:

1. The 48-day SMA filters out excessive trading frequency, locking in medium-to-long-term trends;

2. Bollinger Middle Band breakout captures critical support/resistance breakouts with strong stop loss functionality;

3. MACD judges the direction of major trends to avoid trading against the trend;

4. ADX filters non-trending markets, improving the strategy's win rate.

In summary, this strategy optimizes multiple aspects such as controlling trade frequency, capturing key points, determining trend direction, and filtering out invalid moves, resulting in a relatively high win rate.

## Risks of the Strategy  

The main risks associated with this strategy are:

1. In volatile markets, frequent Bollinger Middle Band triggers may lead to excessive trading;

2. ADX indicators have some errors when determining trends and non-trending periods;

3. Significant drawdown risk, suitable for investors who can bear certain levels of risk.

## Optimization Directions  

This strategy can be further optimized in the following areas:

1. Add ATR indicator to set stop loss points and reduce single trade losses;

2. Optimize Bollinger parameters to decrease middle line trigger frequency;

3. Include trading volume or trend strength indicators to determine trend strength, avoiding weak reversals.

## Summary  

In summary, this Volatility Breakthrough Strategy is relatively mature and effectively captures key trading points during volatile periods. By combining trend and volatility indicators, it balances risk and return. With further optimization, it is expected to generate more stable excess returns.

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
// I found this strategy on the internet, with a video explaining how it works.
// Conditions for entry:
// 1 - Candles must be above or below the 48 MA (Yellow line)
// 2 - Candles must break the middle of Bollinger bands
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

// Bollinger Bands
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