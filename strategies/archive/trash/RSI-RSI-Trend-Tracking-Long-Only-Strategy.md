---
> Name

RSI-Based Bull Trend Tracking Strategy RSI-Trend-Tracking-Long-Only-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1483945845b7d65d5e7.png)
[trans]

## Overview

This strategy implements a trend tracking approach that is long-only and does not enter short positions. When the RSI indicator reaches an oversold level, it enters a long position with fixed take profit and stop loss levels. The strategy is straightforward and suitable for bull markets.

## Strategy Logic

The strategy uses the RSI indicator to determine entry points. It goes long when the RSI drops below the oversold level of 25. After entering, fixed take profit and stop loss levels are set based on the entry price. Specifically, the take profit level is set at 7% above the entry price, while the stop loss level is set at 3.5% below the entry price.

This strategy only goes long and does not go short. It is a trend tracking strategy aimed at capturing upward trends after prices bounce back from oversold RSI levels. When RSI is oversold, it suggests that the price may have been in a short-term oversold condition, allowing for potential rebounds by going long.

## Advantage Analysis

The advantages of this strategy include:

1. Clear and simple logic, making it easy to understand and implement.
2. Distinctive long-only approach, avoiding risks associated with regularity FD003.
3. Long signals are derived from the RSI indicator, effectively identifying oversold rebound opportunities.
4. Fixed take profit/stop loss ratios help control single trade losses.

## Risk Analysis

This strategy also has some drawbacks:

1. It performs well in bull markets but cannot generate profits during bear markets.
2. It misses opportunities to enter on new high breakouts.
3. The fixed stop loss ratio does not adapt to changes in market volatility.
4. Improper RSI parameter settings may result in overtrading or insufficient signals.

## Optimization Directions

The strategy can be improved by:

1. Adding a short side strategy to profit from bear markets.
2. Incorporating new entry conditions such as breakouts of new highs or pattern signals to enhance accuracy.
3. Optimizing RSI parameters through training to reduce errors.
4. Making the stop loss mechanism more intelligent, integrating ATR indicators for adjusting based on volatility.

## Summary

Overall, this strategy uses the RSI indicator to identify oversold opportunities and track bull trends. Its strengths lie in simplicity and reliability, but it is limited to bull markets with significant room for improvement. It can serve as a foundational long-side trend tracking strategy, potentially enhanced by introducing additional conditions and technical indicators to form a reliable positive swing system.

||

## Overview  

This strategy implements a long-only trend tracking approach based on the RSI indicator. It enters long positions when the RSI reaches an oversold level and employs fixed take profit and stop loss ratios. The strategy is simple and straightforward, suitable for bull markets.   

## Strategy Logic

The strategy uses the RSI indicator to determine entry signals. It goes long when the RSI drops below the oversold level of 25. After entering, fixed take profit and stop loss levels are set based on the entry price. Specifically, the take profit level is 7% above the entry price, and the stop loss level is 3.5% below the entry price.

The strategy only goes long and does not go short. It is a trend tracking strategy aimed at capturing upward trends after prices rebound from oversold RSI levels. When RSI is oversold, it suggests that the price may have been in a short-term oversold condition, allowing for potential rebounds by going long.

## Advantage Analysis

The advantages of this strategy include:

1. Clear and simple logic, making it easy to understand and implement.
2. Distinctive long-only approach, avoiding risks associated with regularity FD003.
3. Long signals are derived from the RSI indicator, effectively identifying oversold rebound opportunities.
4. Fixed take profit/stop loss ratios help control single trade losses.

## Risk Analysis

This strategy also has some drawbacks:

1. It performs well in bull markets but cannot generate profits during bear markets.
2. It misses opportunities to enter on new high breakouts.
3. The fixed stop loss ratio does not adapt to changes in market volatility.
4. Improper RSI parameter settings may result in overtrading or insufficient signals.

## Optimization Directions

The strategy can be improved by:

1. Adding a short side strategy to profit from bear markets.
2. Incorporating new entry conditions such as breakouts of new highs or pattern signals to enhance accuracy.
3. Optimizing RSI parameters through training to reduce errors.
4. Making the stop loss mechanism more intelligent, integrating ATR indicators for adjusting based on volatility.

## Conclusion

In summary, this strategy uses clear logic to enter long positions during oversold RSI levels and track bull trends. Its strengths lie in simplicity and reliability, but it is limited to bull markets with significant room for improvement. It can serve as a foundational long-side trend tracking strategy, potentially enhanced by introducing additional conditions and technical indicators to form a reliable positive swing system.

---

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|RSI Length|
|v_input_2|25|Overbought Level|
|v_input_3|0.07|Long Take Profit %|
|v_input_4|0.035|Long Stop Loss %|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-12-28 00:00:00
end: 2024-01-03 00:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("RSI BENI strategy (Long Only)", overlay=true, shorttitle="RSI BENI Long")

length = input(14, title="RSI Length")
overSold = input(25, title="Overbought Level")
price = close
vrsi = ta.rsi(price, length)

// Plot Einstiege und Levels im Chart für überverkaufte Zonen
plotshape(series=strategy.position_avg_price > 0 and vrsi[1] <= overSold and vrsi > overSold,
         title="Long Entry",
         color=color.green,
         style=shape.triangleup,
         size=size.small,
         location=location.belowbar)

long_tp_inp = input(0.07, title='Long Take Profit %')
long_sl_inp = input(0.035, title='Long Stop Loss %')

long_take_level = strategy.position_avg_price * (1 + long_tp_inp)
long_stop_level = strategy.position_avg_price * (1 - long_sl_inp)

plot(long_take_level, color=color.green, title="Long Take Profit Level", linewidth=2)
plot(long_stop_level, color=color.red, title="Long Stop Loss Level", linewidth=2)

if (not na(vrsi))
    if vrsi < overSold
        // Long Entry
        strategy.entry("Long", strategy.long, comment="enter long")

        strategy.exit("Take Profit/Stop Loss", "Long", limit=long_take_level, stop=long_stop_level)
```

> Detail

https://www.fmz.com/strategy/437800

> Last Modified

2024-01-05 16:19:57