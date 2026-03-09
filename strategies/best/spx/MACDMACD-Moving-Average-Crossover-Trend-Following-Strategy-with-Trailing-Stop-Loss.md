> Name

MACD Moving Average Crossover Trend Following Strategy with Trailing Stop Loss  
MACD-Moving-Average-Crossover-Trend-Following-Strategy-with-Trailing-Stop-Loss

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16eb3d35d99a6630493.png)

[trans]

## Overview

This strategy uses MACD to determine the trend direction, combined with EMA and SMA crossovers as confirmation. The entry signal is when the MACD histogram crosses above the signal line and the trend is up. The stop loss is set at the price level below the floating ATR trailing stop. The strategy also exits partially to take profit, exits more on larger price surges, and holds some positions with a trailing stop until the stop loss is hit.

## Logic

### Entry Signal

When the faster EMA crosses above the slower EMA, it indicates that the short-term trend is better than the long-term trend, signaling a buy. Meanwhile, the faster SMA crossing above the slower SMA also suggests stronger upside momentum in the short term. So the combination of MACD line crossing above the signal and uptrend based on EMA&SMA crossover helps identify stronger entry signals.

### Stop Loss

ATR is used to calculate the stop loss level. ATR can effectively measure the price fluctuation range. When the price breaks below this range, the stop loss is triggered. The ATR period can be adjusted - a smaller period allows for more precise stops but is easier to get stopped out, while a larger period gives a wider stop but makes it less likely to be hit. The stop level also trails the price upside, achieving trend following.

### Exit Signals 

Exit partially on small price surges to take profit. Exit more on large price surges to lock in profits. Hold some positions with trailing stops until the stop loss is triggered. This helps lock in profits while still allowing for a holding period.

## Advantages

- MACD judging trends combined with EMA/SMA crossovers confirms entry timing
- ATR trailing stop allows effective stop loss while following the trend
- Partial exits help take profit, lock in gains, and hold positions for a duration

## Risks & Solutions

- Risk of wrong signals from MACD and trend indicators. Fine-tune parameters or add other indicators.
- Risk of ATR stop loss being hit. Can increase ATR period or stop loss multiplier.
- Risk of trailing position being trapped. Reduce trailing position size and cut losses in time.

## Enhancement Opportunities 

- Optimize MACD parameters for better trend judgment
- Optimize ATR period for a more appropriate stop level
- Optimize exit ratios and position sizing to reduce trapped risk
- Consider adding moving take profit or volatility index to improve stop loss

## Summary

The strategy combines MACD, EMA/SMA, and other indicators to determine trends accurately. The floating ATR stop loss helps lock in profits while following the trend. Exits are staggered to take profits, ensure gains, and hold positions for a duration. Overall, it is stable with decent results but can be further optimized for better returns.

|||

## Overview

This strategy uses MACD to determine the trend direction, combined with EMA and SMA crossovers as confirmation. The entry signal is when the MACD histogram crosses above the signal line and the trend is up. The stop loss is set at the price level below the floating ATR trailing stop. The strategy also exits partially to take profit, exits more on larger price surges, and holds some positions with a trailing stop until the stop loss is hit.

## Logic

### Entry Signal

When the faster EMA crosses above the slower EMA, it indicates that the short-term trend is better than the long-term trend, signaling a buy. Meanwhile, the faster SMA crossing above the slower SMA also suggests stronger upside momentum in the short term. So the combination of MACD line crossing above the signal and uptrend based on EMA&SMA crossover helps identify stronger entry signals.

### Stop Loss

ATR is used to calculate the stop loss level. ATR can effectively measure the price fluctuation range. When the price breaks below this range, the stop loss is triggered. The ATR period can be adjusted - a smaller period allows for more precise stops but is easier to get stopped out, while a larger period gives a wider stop but makes it less likely to be hit. The stop level also trails the price upside, achieving trend following.

### Exit Signals 

Exit partially on small price surges to take profit. Exit more on large price surges to lock in profits. Hold some positions with trailing stops until the stop loss is triggered. This helps lock in profits while still allowing for a holding period.

## Advantages

- MACD judging trends combined with EMA/SMA crossovers confirms entry timing
- ATR trailing stop allows effective stop loss while following the trend
- Partial exits help take profit, lock in gains, and hold positions for a duration

## Risks & Solutions

- Risk of wrong signals from MACD and trend indicators. Fine-tune parameters or add other indicators.
- Risk of ATR stop loss being hit. Can increase ATR period or stop loss multiplier.
- Risk of trailing position being trapped. Reduce trailing position size and cut losses in time.

## Enhancement Opportunities 

- Optimize MACD parameters for better trend judgment
- Optimize ATR period for a more appropriate stop level
- Optimize exit ratios and position sizing to reduce trapped risk
- Consider adding moving take profit or volatility index to improve stop loss

## Summary

The strategy combines MACD, EMA/SMA, and other indicators to determine trends accurately. The floating ATR stop loss helps lock in profits while following the trend. Exits are staggered to take profits, ensure gains, and hold positions for a duration. Overall, it is stable with decent results but can be further optimized for better returns.

|||

## Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|34|Period|
|v_input_2|3|Fast Length|
|v_input_3|5|Slow Length|
|v_input_4_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_5|2|Signal Smoothing|
|v_input_6|false|Simple MA(Oscillator)|
|v_input_7|true|Simple MA(Signal Line)|
|v_input_8|true|Long Take Profit 1 %|
|v_input_9|10|Long Take Profit 1 Qty|
|v_input_10|5|Long Take Profit 2%|
|v_input_11|50|Long Take Profit 2 Qty|
|v_input_12|2.2|SL Mutiplier|
|v_input_13|17|ATR period|
|v_input_14|2018|Backtest Start Year|
|v_input_15|true|Backtest Start Month|
|v_input_16|true|Backtest Start Day|
|v_input_17|2020|Backtest Stop Year|
|v_input_18|12|Backtest Stop Month|
|v_input_19|31|Backtest Stop Day|

## Source (Pine Script)

```pinescript
/*backtest
start: 2022-10-30 00:00:00
end: 2023-11-05 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Deobald

//@version=4
strategy("MACD Strategy", overlay=true)

// FUNCTIONS

Ema(src, p) =>
    ema = 0.
    sf = 2 / (p + 1)
    ema := nz(ema[1] + sf * (src - ema[1]), src)

Sma(src, p) => a = cum(src), (a - a[max(p, 0)]) / max(p, 0)

Atr(p) =>
    atr = 0.
    Tr = max(high - low, max(abs(high - close[1]), abs(low - close[1])))
    atr := nz(atr[1] + (Tr - atr[1]) / p, Tr)

/// TREND
ribbon_period = input(34, "Period", step=1)

leadLine1 = ema(close, ribbon_period)
leadLine2 = sma(close, ribbon_period)

p3 = plot(leadLine1, color=#53b987, title="EMA", transp=50, linewidth=1)
p4 = plot(leadLine2, color=#eb4d5c, title="SMA", transp=50, linewidth=1)
fill(p3, p4, transp=60, color=leadLine1 > leadLine2 ? #53b987 : #eb4d5c)


// MACD
fast_length = input(title="Fast Length", type=input.integer, defval=3)
slow_length = input(title="Slow Length", type=input.integer, defval=5)
```