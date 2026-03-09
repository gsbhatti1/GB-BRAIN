> Name

Reversal Momentum Breakout Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/18dc78eaeb51dedc39e.png)
[trans]
## Overview

The Reversal Momentum Breakout Strategy is a quantitative trading strategy that generates trading signals using price reversal and momentum indicators. Based on the theory of "momentum leads price," this strategy tracks the highest and lowest prices over a certain period to determine whether the market is at a key reversal point, to capture reversal opportunities.

## Strategy Principle

The core logic of this strategy is to identify market reversal points by calculating the highest and lowest prices over a specified lookback window (e.g., 20 days). The specific logic is as follows:

1. Calculate the highest price (window_high) and lowest price (window_low) over the past 20 days.
2. If today's high is higher than the maximum of the past 20 days (a new 20-day high), enter the high reversal monitoring period and set the counter to 5 days.
3. If no new high occurs, deduct the counter by 1 each day. When the counter reaches 0, the high reversal monitoring period ends.
4. The judgment logic for the lowest price is similar. If a new low occurs, enter the low reversal monitoring period.
5. Long and short positions are taken within the reversal monitoring periods. Reversal signals near the key reversal points allow capturing larger moves.

This strategy also sets the start trading time to avoid generating signals on historical data.

## Advantage Analysis

The Reversal Momentum Breakout Strategy has the following main advantages:

1. Captures reversal opportunities, suitable for reversal trends. Markets often show some degree of reversal after a sustained uptrend or downtrend. This strategy aims to capture these turning points.
2. Momentum leads, relatively sensitive. Tracking the highest and lowest prices over a window can sensitively identify price reversal trends and timing.
3. Reversal monitoring periods avoid false signals. Signals are generated only around key reversal points, filtering out some noise.
4. Allows long and short positions. Alternates between long and short following market direction.
5. Relatively simple logic, easy to implement. Mainly relies on price and simple momentum indicators, easy to code.

## Risk Analysis

The main risks of this strategy include:

1. Inaccurate reversal prediction. The strategy can incur losses if the market trends directionally.
2. Overall market trends not considered. Individual stock reversals do not necessarily represent market reversals. Market analysis should be combined.
3. Potentially large drawdowns. Drawdown may expand without actual reversals.
4. Data fitting bias. Performance may significantly differ from backtests.
5. Parameter sensitivity. Window period and counter parameters affect stability.

Corresponding risk control methods include optimizing stop loss, incorporating market factors, adjusting parameter combinations, and verifying stability.

## Optimization Directions

The main optimization directions include:

1. Incorporate market indicators. Assess market strength to avoid unfavorable big picture environments.
2. Multi-factor stock selection. Select stocks with sound fundamentals and overvaluation.
3. Parameter optimization. Adjust window period and counter parameters to find optimal parameter combinations.
4. Add stop loss strategies, such as trailing stops, volatility stops, to control maximum drawdown.
5. Increase machine learning predictive accuracy of price reversals.

## Conclusion

The Reversal Momentum Breakout Strategy identifies reversal opportunities by tracking price and momentum. It reacts sensitively and identifies reversal trends and timing. But it has risks that require proper optimizations and risk control. Overall, when thoroughly understood and optimized, it can form an effective component of a quantitative trading system.

||

## Overview

The Reversal Momentum Breakout Strategy is a quantitative trading strategy that generates trading signals using price reversal and momentum indicators. Based on the theory of "momentum leads price," this strategy tracks the highest and lowest prices over a certain period to determine whether the market is at a key reversal point, to capture reversal opportunities.

## Strategy Principle

The core logic of this strategy is to identify market reversal points by calculating the highest and lowest prices over a specified lookback window (e.g., 20 days). The specific logic is as follows:

1. Calculate the highest price (window_high) and lowest price (window_low) over the past 20 days.
2. If today's high is higher than the maximum of the past 20 days (a new 20-day high), enter the high reversal monitoring period and set the counter to 5 days.
3. If no new high occurs, deduct the counter by 1 each day. When the counter reaches 0, the high reversal monitoring period ends.
4. The judgment logic for the lowest price is similar. If a new low occurs, enter the low reversal monitoring period.
5. Long and short positions are taken within the reversal monitoring periods. Reversal signals near the key reversal points allow capturing larger moves.

The strategy also sets the start trading time to avoid generating signals on historical data.

## Advantage Analysis

The Reversal Momentum Breakout Strategy has the following main advantages:

1. Captures reversal opportunities, suitable for reversal trends. Markets often show some degree of reversal after a sustained uptrend or downtrend. This strategy aims to capture these turning points.
2. Momentum leads, relatively sensitive. Tracking the highest and lowest prices over a window can sensitively identify price reversal trends and timing.
3. Reversal monitoring periods avoid false signals. Signals are generated only around key reversal points, filtering out some noise.
4. Allows long and short positions. Alternates between long and short following market direction.
5. Relatively simple logic, easy to implement. Mainly relies on price and simple momentum indicators, easy to code.

## Risk Analysis

The main risks of this strategy include:

1. Inaccurate reversal prediction. The strategy can incur losses if the market trends directionally.
2. Overall market trends not considered. Individual stock reversals do not necessarily represent market reversals. Market analysis should be combined.
3. Potentially large drawdowns. Drawdown may expand without actual reversals.
4. Data fitting bias. Performance may significantly differ from backtests.
5. Parameter sensitivity. Window period and counter parameters affect stability.

Corresponding risk control methods include optimizing stop loss, incorporating market factors, adjusting parameter combinations, and verifying stability.

## Optimization Directions

The main optimization directions include:

1. Incorporate market indicators. Assess market strength to avoid unfavorable big picture environments.
2. Multi-factor stock selection. Select stocks with sound fundamentals and overvaluation.
3. Parameter optimization. Adjust window period and counter parameters to find optimal parameter combinations.
4. Add stop loss strategies, such as trailing stops, volatility stops, to control maximum drawdown.
5. Increase machine learning predictive accuracy of price reversals.

## Conclusion

The Reversal Momentum Breakout Strategy identifies reversal opportunities by tracking price and momentum. It reacts sensitively and identifies reversal trends and timing. But it has risks that require proper optimizations and risk control. Overall, when thoroughly understood and optimized, it can form an effective component of a quantitative trading system.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_int_1|20|New Highs and Lows Window|
|v_input_int_2|5|Decay|
|v_input_1|timestamp(1 Jan 2023)|Start Date|
|v_input_bool_1|false|Allow shorting|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-02-16 00:00:00
end: 2024-02-22 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Reversal Momentum Breakout Strategy", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100)

window = input.int(20, title="New Highs and Lows Window", minval=1)
decay = input.int(5, title="Decay", minval=1)
start_date = input.timestamp(1676073600, title="Start Date", defval=timestamp("2023-01-01"))

allow_shorting = input.bool(false, title="Allow shorting")

h = ta.highest(high, window)
l = ta.lowest(low, window)

var float hi = na
var int hi_count = 0
hi := na(hi) ? h : hi
hi_count := na(hi) ? 0 : hi_count

var float lo = na
var int lo_count = 0
lo := na(lo) ? l : lo
lo_count := na(lo) ? 0 : lo_count

if bar_index >= start_date
    if high >= hi
        hi := high
        hi_count := 5
    else if hi_count > 0
        hi_count := hi_count - 1

    if low <= lo
        lo := low
        lo_count := 5
    else if lo_count > 0
        lo_count := lo_count - 1

if hi_count == 0
    strategy.entry("Buy", strategy.long)

if lo_count == 0
    strategy.entry("Sell", strategy.short)

if allow_shorting
    strategy.close("Sell", when=low <= lo)
else
    strategy.close("Buy", when=high >= hi)
```

Note: The `start_date` is set to the timestamp of 1 January 2023, which is `1676073600`.