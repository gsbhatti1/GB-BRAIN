> Name

Parabolic-SAR-Momentum-Reversal-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/efc7411f52f0ae1400.png)
[trans]

## Overview

This strategy is a swing trading approach that utilizes the crossover operation between Parabolic SAR values and candlesticks to achieve momentum tracking and stop-loss. It establishes long and short positions during price rises and falls, and closes these positions with stop loss orders when a price reversal occurs.

## Strategy Logic

The core of this strategy relies on the Parabolic SAR indicator to determine whether the current price is in an upward or downward trend. When the Parabolic SAR value is below the candlestick, it indicates that the price is currently rising. In such cases, the strategy checks at the close of each candlestick whether the Parabolic SAR value crosses above the low of the candlestick. If not, it means the upward trend continues and the strategy will establish a long position. If Parabolic SAR crosses above the low, it indicates an upside trend reversal to downside, and the strategy will close the long position to stop loss.

Conversely, when Parabolic SAR is above the candlestick, it signifies that the price is currently falling. The strategy checks at the close of each candlestick whether the Parabolic SAR value crosses below the high of the candlestick. If not, a short position is established. If Parabolic SAR crosses the high, it means the downside trend reverses to upside, and the strategy will close the short position to stop loss.

Through this logic, the strategy can establish positions in line with the price trend and realize stop-loss upon reversal, locking in profits. Meanwhile, as a momentum indicator, Parabolic SAR can more accurately determine whether the trend has reversed, making the stop loss more precise.

## Strategy Advantages

1. Using Parabolic SAR to judge trends and reversals is an advanced and accurate technical indicator, improving judgment accuracy.
2. Adopting momentum tracking and reversal stop-loss operations can fully leverage trending opportunities.
3. Strict stop-loss rules provide strong risk control capabilities.
4. Optimized parameters make this strategy particularly suitable for GBP/JPY with strong trends.

## Risks

1. Like any single-indicator strategy, this one may suffer from incorrect judgments by Parabolic SAR regarding trend and reversals. Invalid signals could lead to unnecessary losses.
2. The strategy fully relies on Parabolic SAR for entries and exits; improper parameter settings or overly lenient stop-loss points can fail to control risks effectively.
3. Any single strategy may gradually deteriorate due to changing market structures and environments, necessitating regular backtests and optimizations.

Methods to enhance robustness include: optimizing stop-loss points to be strict enough; combining other indicators for confirmation; adjusting parameters to adapt to changing market conditions; selecting optimal parameter sets for different products, etc.

## Optimization Directions

1. Test and optimize combinations of Parabolic SAR parameters for better performance.
2. Combine other indicators like MACD, KD, to form a multi-indicator confirmation system, improving signal reliability.
3. Test the effects of different stop-loss methods such as trailing stops, time-based stops, or price stops, etc.
4. Optimize parameters based on product characteristics so that the strategy can achieve good returns across various products.

## Conclusion

In general, this Parabolic SAR swing trading strategy is quite effective for short-term operations. It leverages Parabolic SAR to determine trend direction and momentum changes, together with swing trading methods, to repeatedly establish long and short positions during uptrends and downtrends. The strict stop-loss mechanism also gives this strategy decent risk control capabilities. However, as a single-indicator strategy, the invalidity of Parabolic SAR could significantly impact performance. So, it is a strategy with both strength and potential but also some risks that need to be backtested and optimized continuously for stable excess returns.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|0.05|start|
|v_input_2|0.075|increment|
|v_input_3|true|max|
|v_input_4|true|From Day|
|v_input_5|true|From Month|
|v_input_6|2000|From Year|
|v_input_7|31|To Day|
|v_input_8|12|To Month|
|v_input_9|2020|To Year|


> Source (PineScript)

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
//@version=5
strategy("Parabolic-SAR-Momentum-Reversal-Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Input Parameters
start = input.float(0.05, title="Start")
increment = input.float(0.075, title="Increment")
max = input.bool(true, title="Maximum")
from_day = input.bool(true, title="From Day")
from_month = input.bool(true, title="From Month")
from_year = input.int(2000, minval=1970, title="From Year")
to_day = input.int(31, minval=1, maxval=31, title="To Day")
to_month = input.int(12, minval=1, maxval=12, title="To Month")
to_year = input.int(2020, minval=1970, title="To Year")

// Parabolic SAR Indicator
sar = ta.sar(from_day ? from_year : na, from_month ? from_year : na, from_day ? to_day : na, from_month ? to_month : na, to_year)

// Long Condition
long_condition = sar > close[1] and sar < sar[1]
if (long_condition)
    strategy.entry("Long", strategy.long)

// Short Condition
short_condition = sar < close[1] and sar > sar[1]
if (short_condition)
    strategy.entry("Short", strategy.short)

// Exit Conditions
exit_long_condition = not long_condition or ta.crossover(sar, close)
if (exit_long_condition)
    strategy.close("Long")

exit_short_condition = not short_condition or ta.crossunder(sar, close)
if (exit_short_condition)
    strategy.close("Short")
```
```