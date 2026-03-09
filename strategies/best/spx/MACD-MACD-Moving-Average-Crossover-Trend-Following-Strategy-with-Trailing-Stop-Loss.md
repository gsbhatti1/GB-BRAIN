> Name

MACD Moving Average Crossover Trend Following Strategy with Trailing Stop Loss  
MACD-Moving-Average-Crossover-Trend-Following-Strategy-with-Trailing-Stop-Loss

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16eb3d35d99a6630493.png)

[trans]

## Overview

This strategy uses MACD to determine the trend direction, combined with EMA and SMA crossovers as confirmation. The entry signal is when the MACD histogram crosses above the signal line and the trend is upward. The stop loss is set at the price level below a floating ATR trailing stop. The strategy also exits partially to take profit, exits more on larger price surge, and holds some position with trailing stop until the stop loss is hit.

## Logic

### Entry Signal

When the faster EMA crosses above the slower EMA, it indicates that the short-term trend is better than the long-term trend, signaling a buy. Meanwhile, a faster SMA crossing above a slower SMA also suggests stronger upside momentum in the short term. So, the combination of MACD line crossing above the signal and an uptrend based on EMA & SMA crossovers helps identify stronger entry signals.

### Stop Loss

ATR is used to calculate the stop loss level. ATR can effectively measure the price fluctuation range. When the price breaks below this range, the stop loss is triggered. The ATR period can be adjusted - a smaller period allows for more precise stops but makes it easier to get stopped out; while a larger period gives a wider stop but is more robust. The stop level also trails the price upside, achieving trend following.

### Exit Signals

Exit partially on small price surge to take profit. Exit more on large price spike to lock in profit. Keep some position with trailing stop until the stop loss is hit. This helps lock in profits while still holding the position for a period.

## Advantages

- MACD judging trends combined with EMA/SMA crossovers confirms entry timing accurately.
- ATR trailing stop allows effective stop loss while following the trend.
- Partial exits help take profit, lock in gains, and hold positions for duration.

## Risks & Solutions

- Risk of incorrect signals from MACD and trend indicators. Fine-tune parameters or add other indicators as aids.
- Risk of ATR stop loss being hit. Increase ATR period or add a stop-loss multiplier.
- Risk of trailing position being trapped in losses. Reduce the size of trailing positions and cut losses promptly.

## Enhancement Opportunities

- Optimize MACD parameters for better trend judgment.
- Optimize ATR period for a better stop loss level.
- Optimize exit ratios and position sizing to reduce the risk of getting trapped.
- Consider adding moving take profit or volatility index improvements for the stop loss.

## Summary

The strategy combines MACD, EMA/SMA, and other indicators to determine trend direction accurately. The floating ATR trailing stop helps lock in profits while following the trend. Exits are staggered to take profits, secure gains, and hold positions for a duration. Overall, it is stable with decent results; however, further optimization of parameters and exits can lead to better returns.

|||


## Overview

This strategy uses MACD to determine the trend direction, combined with EMA and SMA crossovers as confirmation. The entry signal is when the MACD histogram crosses above the signal line and the trend is upward. The stop loss is set at the price level below a floating ATR trailing stop. The strategy also exits partially to take profit, exits more on larger price surge, and holds some position with trailing stop until the stop loss is hit.

## Logic

### Entry Signal

When the faster EMA crosses above the slower EMA, it indicates that the short-term trend is better than the long-term trend, signaling a buy. Meanwhile, a faster SMA crossing above a slower SMA also suggests stronger upside momentum in the short term. So, the combination of MACD line crossing above the signal and an uptrend based on EMA & SMA crossovers helps identify stronger entry signals.

### Stop Loss

ATR is used to calculate the stop loss level. ATR can effectively measure the price fluctuation range. When the price breaks below this range, the stop loss is triggered. The ATR period can be adjusted - a smaller period allows for more precise stops but makes it easier to get stopped out; while a larger period gives a wider stop but is more robust. The stop level also trails the price upside, achieving trend following.

### Exit Signals 

Exit partially on small price surge to take profit. Exit more on large price spike to lock in profit. Keep some position with trailing stop until the stop loss is hit. This helps lock in profits while still being able to hold the position for a period.

## Advantages

- MACD judging trends combined with EMA/SMA crossovers confirms entry timing accurately.
- ATR trailing stop allows effective stop loss while following the trend.
- Partial exits help take profit, lock in gains, and hold positions for duration.

## Risks & Solutions

- Risk of incorrect signals from MACD and trend indicators. Fine-tune parameters or add other indicators as aids.
- Risk of ATR stop loss being hit. Increase ATR period or add a stop-loss multiplier.
- Risk of trailing position being trapped in losses. Reduce the size of trailing positions and cut losses promptly.

## Enhancement Opportunities

- Optimize MACD parameters for better trend judgment.
- Optimize ATR period for a better stop loss level.
- Optimize exit ratios and position sizing to reduce the risk of getting trapped.
- Consider adding moving take profit or volatility index improvements for the stop loss.

## Summary

The strategy combines MACD, EMA/SMA, and other indicators to determine trend direction accurately. The floating ATR trailing stop helps lock in profits while following the trend. Exits are staggered to take profits, secure gains, and hold positions for a duration. Overall, it is stable with decent results; however, further optimization of parameters and exits can lead to better returns.

|||

```pinescript
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