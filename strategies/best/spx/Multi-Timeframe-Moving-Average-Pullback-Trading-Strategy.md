> Name

Multi-Timeframe-Moving-Average-Pullback-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1fae39a31e778b69fef.png)
[trans]

## Overview

This strategy adopts the multi-timeframe moving average approach, using long-term moving averages to determine the major trend direction and short-term moving averages to determine the short-term trend direction. When the long-term trend aligns with the short-term trend, positions are taken accordingly. When the short-term moving average pulls back to the vicinity of the long-term moving average, it indicates a short-term correction presenting trading opportunities for the reverse direction. This strategy works best for trending stocks over medium to long-term timeframes.

## Strategy Logic

The strategy uses the 200-day simple moving average (SMA) to determine the long-term trend direction, and the 10-day SMA for the short-term trend direction. When the price closes above the 200-day SMA and below the 10-day SMA, it signals an upward long-term trend with a short-term pullback, presenting a buying opportunity. When the price closes below the 200-day SMA and above the 10-day SMA, it signals a downward long-term trend with a short-term bounce, presenting a selling opportunity.

Specifically, when the following conditions are met, long entry is triggered: Close > 200-day SMA AND Close < 10-day SMA. When the following conditions are met, short entry is triggered: Close < 200-day SMA AND Close > 10-day SMA.

After entry, a 10% stop loss mechanism is implemented. The position will be stopped out if the retracement from the entry price exceeds 10%. Also, if the `i_lowerClose` option is enabled, it will wait for a lower close before exiting, avoiding excessive sensitivity of the stop loss.

## Advantage Analysis

This strategy combines multi-timeframe moving averages, enabling high probability in capturing the mid-to-long-term trend direction. It provides decent entry timing when the short-term SMA pulls back to the long-term SMA. Compared to single moving average systems, the probability of being caught in short-term corrections is reduced.

The risk involved in this strategy is well defined and capped. A 10% stop loss ratio restricts the maximum loss size. Also, the time range filter avoids trading in specified time periods.

## Risk Analysis

There is still the risk of being caught in this strategy. If the short-term correction lasts too long or the pullback amplitude is too big, the stop loss could be triggered resulting in a forced exit at inopportune times. This introduces the risk of loss.

The adaptiveness of this strategy across trading instruments is limited. For stocks with high volatility and prolonged correction periods, this strategy tends to hit stop loss prematurely, rendering poor performance.

During major market-wide corrections, e.g., financial crisis, this strategy could suffer big losses. Profitability is improbable during such times.

## Optimization Directions

More moving average systems can be introduced to form a multiple filtering mechanism. For example, adding a 50-day SMA, entry positions are considered only when the price is between the 50-day SMA and 200-day SMA. This extra filter out stocks with inferior trend characteristics.

A dynamic stop loss mechanism can be implemented. Specifically, after entry, the stop loss ratio is adjusted based on the observed volatility instead of a fixed 10%. This avoids premature trigger of the hard stop loss.

Other indicators gauging market conditions can also be incorporated. For example, MACD, when MACD shows market divergence, this strategy could be temporarily deactivated to avoid losses. It adds a market timing mechanism to turn the strategy on and off.

## Conclusion

In conclusion, this is a typical multi-timeframe moving average strategy. It capitalizes on the mid-to-long-term trend direction indicated by the long-term moving average, while taking advantage of short-term pullback opportunities revealed by the short-term moving average. The risk factors are defined and well capped. Further enhancements like additional filters, adaptive stop loss, and market timing mechanism could improve its stability.

[/trans]

> Strategy Arguments


| Argument | Default | Description |
| --- | --- | --- |
| v_input_int_1 | 200 | (Strategy Parameters) MA 1 Length |
| v_input_int_2 | 10 | MA 2 Length |
| v_input_float_1 | 0.1 | Stop Loss Percent |
| v_input_bool_1 | false | Exit On Lower Close |
| v_input_1 | timestamp(01 Jan 1995 13:30 +0000) | (Time Filter) Start Filter |
| v_input_2 | timestamp(1 Jan 2099 19:30 +0000) | End Filter |


> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-29 00:00:00
end: 2024-02-28 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance",...
```