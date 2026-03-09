> Name

Triple Supertrend Breakout Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ca653fb4b4cefec13d.png)

[trans]

## Overview

The triple supertrend breakout strategy is a commonly used trading strategy that utilizes multiple supertrend lines with different parameter settings and an EMA to define the major trend for identifying trend direction and trade. The main idea of this strategy is to establish long positions when at least two supertrend lines are showing an uptrend above the trend-defining EMA line, and establish short positions when at least two supertrend lines are showing a downtrend below the trend-defining EMA line.

## Strategy Principle

This strategy uses three supertrend lines with different parameters and an EMA to determine entries and exits:

1. Set up three supertrend lines - `supertrend1`, `supertrend2`, `supertrend3`, with green color indicating an uptrend and red color indicating a downtrend.

2. Set up an EMA line `ematrend` to define the major trend. When all three supertrend lines are above this EMA, the market is defined as being in an uptrend, and vice versa for downtrends.

3. When at least two supertrend lines show an uptrend (green) simultaneously under the condition of a major uptrend market, that is, the direction value is less than 0, it is judged as a long signal; when at least two supertrend lines show a downtrend (red) simultaneously under the condition of a major downtrend market, that is, the direction value is greater than 0, it is judged as a short signal.

4. Subsequently, open long/short positions when signals are triggered.

5. Set stop loss and take profit conditions. Fixed take profit is set at a risk/reward ratio of 3; trailing stop loss is set at a drop of one ATR.

6. Close positions when stop loss or take profit conditions are triggered.

## Advantage Analysis

The advantages of this strategy include:

1. Using three supertrend lines combined with a trend-judging EMA can effectively identify trend signals.
2. The long and short conditions are clear and easy to understand and implement.
3. Setting a trailing stop loss and fixed take profit effectively manages risks.
4. Hyperparameters can be adjusted as needed to optimize the strategy.

## Risk Analysis

There are also some risks to this strategy:

1. Improper parameter settings may lead to missing good trading opportunities. Different periods, multiples for ATR, and periods for EMA can be tested.
2. There is some probability of failed breakouts. This can be reduced by adjusting parameters.
3. Stop loss or take profit set too wide may increase loss probability. Stop loss range should be tightened properly.
4. Backtest data can easily lead to overfitting problems. Multi-market, multi-timeframe testing should be noted.

## Optimization Directions

Some ways this strategy can be optimized:

1. Test the optimal parameter combinations. Different combinations of ATR periods, multiples, and EMA periods can be tested to find the best.
2. Increase trading varieties. Can add stocks, cryptocurrencies etc to test effectiveness across markets.
3. Combine with other indicators for signal filtering. For example, RSI, MACD etc can be added to avoid misreading trend signals.
4. Optimize the stop loss and take profit mechanism. Trailing stop loss, or stop loss based on changes in ATR/volatility can be tested.

## Conclusion

In summary, the triple supertrend breakout strategy is a relatively simple and practical trend following strategy. It combines multiple supertrend lines and a trend-judging EMA to discover opportunities and manages risk effectively. Through parameter and logic optimization, better results can be achieved. This strategy is easy to understand and worth learning from.

[/trans]

> Strategy Arguments


| Argument | Default | Description |
| -------- | ------- | ----------- |
| v_input_1 | 10      | ATR Length 1 |
| v_input_float_1 | true    | ATR Factor 1 |
| v_input_2 | 11      | ATR Length 2 |
| v_input_float_2 | 2       | ATR Factor 2 |
| v_input_3 | 12      | ATR Length 3 |
| v_input_float_3 | 3       | ATR Factor 3 |
| v_input_int_1 | 233     | Trend-EMA Length |
| v_input_4_close | 0       | Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4 |
| v_input_int_2 | false   | Offset |
| v_input_5 | timestamp(01 Apr 2016 13:30 +0000) | Backtest Start Time |
| v_input_6 | false   | Define the ending period for backtests (If false, will test up to most recent candle) |
| v_input_7 | timestamp(19 Mar 2021 19:30 +0000) | Backtest End Time |
| v_input_8 | false   | Exit when Risk:Reward met |
| v_input_9 | 3       | Risk:[Reward] (i.e. 3) for exit |
| v_input_10 | true    | Use trailing stop loss |
| v_input_11 | 2       | ATR multiplier for stop loss |

> Source (PineScript)

```pinescript
//@version=5
strategy("Triple Supertrend Breakout Strategy", overlay=true, margin_long=100, margin_short=100)
atr_length1 = input.int(10, "ATR Length 1")
atr_factor1 = input.float(1.3, "ATR Factor 1", step=0.1)
atr_length2 = input.int(11, "ATR Length 2")
atr_factor2 = input.float(2.0, "ATR Factor 2", step=0.1)
atr_length3 = input.int(12, "ATR Length 3")
atr_factor3 = input.float(3.0, "ATR Factor 3", step=0.1)
trend_ema_length = input.int(233, "Trend-EMA Length")

// Source and offset
source = input(close, title="Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4")
offset = input.int(0, title="Offset", minval=-50000, maxval=50000)

// Backtest settings
backtest_start_time = input.time(timestamp("2016-04-01 13:30 +0000"), title="Backtest Start Time")
backtest_end_time = input.time(timestamp("2021-03-19 19:30 +0000"), title="Backtest End Time", confirm=true)
exit_on_risk_reward_ratio = input.bool(false, "Exit when Risk:Reward met", title="Exit on risk/reward ratio")
risk_reward_ratio = input.float(3.0, title="Risk:[Reward] (i.e. 3) for exit", minval=1.0)

// Use trailing stop loss
use_trailing_stop_loss = input.bool(true, "Use trailing stop loss")
stop_loss_multiplier = input.int(2, title="ATR multiplier for stop loss")

// Supertrend calculations
[supertrend1, direction1] = supertrend(source, atr_length1, atr_factor1)
[supertrend2, direction2] = supertrend(source, atr_length2, atr_factor2)
[supertrend3, direction3] = supertrend(source, atr_length3, atr_factor3)

// EMA for defining the major trend
ema = ta.ema(source, trend_ema_length)

// Conditions for entering long and short positions
long_condition = (direction1 < 0) and (direction2 < 0) and (direction3 < 0) and (supertrend1 > ema) and (supertrend2 > ema) and (supertrend3 > ema)
short_condition = (direction1 > 0) and (direction2 > 0) and (direction3 > 0) and (supertrend1 < ema) and (supertrend2 < ema) and (supertrend3 < ema)

// Plot Supertrends
plotshape(series=long_condition, title="Long Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=short_condition, title="Short Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Plot EMA
plot(ema, title="Trend-EMA", color=color.blue)

// Trailing stop loss logic
trail_stop = na
if (long_condition)
    trail_stop := ta.valuewhen(long_condition, ema - atr_length1 * atr_factor1, 0)
if (short_condition)
    trail_stop := ta.valuewhen(short_condition, ema + atr_length1 * atr_factor1, 0)

// Exit logic based on risk/reward
risk_reward = na
if (long_condition and not na(trail_stop))
    risk_reward := (ta.highest(high, atr_length1) - close) / (close - trail_stop)
if (short_condition and not na(trail_stop))
    risk_reward := (low - ta.lowest(low, atr_length1)) / (trail_stop - close)

// Exit on risk/reward
exit_position = false
if (risk_reward >= risk_reward_ratio)
    exit_position := true

// Trade execution logic
if long_condition and not exit_position
    strategy.entry("Long", strategy.long)
if short_condition and not exit_position
    strategy.entry("Short", strategy.short)

// Plot stop loss levels
plot(trail_stop, title="Stop Loss", color=color.red, style=plot.style_linebr, linewidth=2)
``` ```pinescript
//@version=5
strategy("Triple Supertrend Breakout Strategy", overlay=true, margin_long=100, margin_short=100)

// Input parameters for ATR settings
atr_length1 = input.int(10, "ATR Length 1")
atr_factor1 = input.float(1.3, "ATR Factor 1", step=0.1)
atr_length2 = input.int(11, "ATR Length 2")
atr_factor2 = input.float(2.0, "ATR Factor 2", step=0.1)
atr_length3 = input.int(12, "ATR Length 3")
atr_factor3 = input.float(3.0, "ATR Factor 3", step=0.1)

// Input parameter for EMA length
trend_ema_length = input.int(233, "Trend-EMA Length")

// Source and offset
source = input(close, title="Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4")
offset = input.int(0, title="Offset", minval=-50000, maxval=50000)

// Backtest settings
backtest_start_time = input.time(timestamp("2016-04-01 13:30 +0000"), title="Backtest Start Time")
backtest_end_time = input.time(timestamp("2021-03-19 19:30 +0000"), title="Backtest End Time", confirm=true)
exit_on_risk_reward_ratio = input.bool(false, "Exit when Risk:Reward met", title="Exit on risk/reward ratio")
risk_reward_ratio = input.float(3.0, title="Risk:[Reward] (i.e. 3) for exit", minval=1.0)

// Use trailing stop loss
use_trailing_stop_loss = input.bool(true, "Use trailing stop loss")
stop_loss_multiplier = input.int(2, title="ATR multiplier for stop loss")

// Supertrend calculations
[supertrend1, direction1] = supertrend(source, atr_length1, atr_factor1)
[supertrend2, direction2] = supertrend(source, atr_length2, atr_factor2)
[supertrend3, direction3] = supertrend(source, atr_length3, atr_factor3)

// EMA for defining the major trend
ema = ta.ema(source, trend_ema_length)

// Conditions for entering long and short positions
long_condition = (direction1 < 0) and (direction2 < 0) and (direction3 < 0) and (supertrend1 > ema) and (supertrend2 > ema) and (supertrend3 > ema)
short_condition = (direction1 > 0) and (direction2 > 0) and (direction3 > 0) and (supertrend1 < ema) and (supertrend2 < ema) and (supertrend3 < ema)

// Plot Supertrends
plotshape(series=long_condition, title="Long Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=short_condition, title="Short Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Plot EMA
plot(ema, title="Trend-EMA", color=color.blue)

// Trailing stop loss logic
trail_stop = na
if (long_condition)
    trail_stop := ta.valuewhen(long_condition, ema - atr_length1 * atr_factor1, 0)
if (short_condition)
    trail_stop := ta.valuewhen(short_condition, ema + atr_length1 * atr_factor1, 0)

// Exit logic based on risk/reward
risk_reward = na
if (long_condition and not na(trail_stop))
    risk_reward := (ta.highest(high, atr_length1) - close) / (close - trail_stop)
if (short_condition and not na(trail_stop))
    risk_reward := (low - ta.lowest(low, atr_length1)) / (trail_stop - close)

// Exit on risk/reward
exit_position = false
if (risk_reward >= risk_reward_ratio)
    exit_position := true

// Trade execution logic
if long_condition and not exit_position
    strategy.entry("Long", strategy.long)
if short_condition and not exit_position
    strategy.entry("Short", strategy.short)

// Plot stop loss levels
plot(trail_stop, title="Stop Loss", color=color.red, style=plot.style_linebr, linewidth=2)
``` ```pinescript
//@version=5
strategy("Triple Supertrend Breakout Strategy", overlay=true, margin_long=100, margin_short=100)

// Input parameters for ATR settings
atr_length1 = input.int(10, "ATR Length 1")
atr_factor1 = input.float(1.3, "ATR Factor 1", step=0.1)
atr_length2 = input.int(11, "ATR Length 2")
atr_factor2 = input.float(2.0, "ATR Factor 2", step=0.1)
atr_length3 = input.int(12, "ATR Length 3")
atr_factor3 = input.float(3.0, "ATR Factor 3", step=0.1)

// Input parameter for EMA length
trend_ema_length = input.int(233, "Trend-EMA Length")

// Source and offset
source = input(close, title="Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4")
offset = input.int(0, title="Offset", minval=-50000, maxval=50000)

// Backtest settings
backtest_start_time = input.time(timestamp("2016-04-01 13:30 +0000"), title="Backtest Start Time")
backtest_end_time = input.time(timestamp("2021-03-19 19:30 +0000"), title="Backtest End Time", confirm=true)
exit_on_risk_reward_ratio = input.bool(false, "Exit when Risk:Reward met", title="Exit on risk/reward ratio")
risk_reward_ratio = input.float(3.0, title="Risk:[Reward] (i.e. 3) for exit", minval=1.0)

// Use trailing stop loss
use_trailing_stop_loss = input.bool(true, "Use trailing stop loss")
stop_loss_multiplier = input.int(2, title="ATR multiplier for stop loss")

// Supertrend calculations
[supertrend1, direction1] = supertrend(source, atr_length1, atr_factor1)
[supertrend2, direction2] = supertrend(source, atr_length2, atr_factor2)
[supertrend3, direction3] = supertrend(source, atr_length3, atr_factor3)

// EMA for defining the major trend
ema = ta.ema(source, trend_ema_length)

// Conditions for entering long and short positions
long_condition = (direction1 < 0) and (direction2 < 0) and (direction3 < 0) and (supertrend1 > ema) and (supertrend2 > ema) and (supertrend3 > ema)
short_condition = (direction1 > 0) and (direction2 > 0) and (direction3 > 0) and (supertrend1 < ema) and (supertrend2 < ema) and (supertrend3 < ema)

// Plot Supertrends
plotshape(series=long_condition, title="Long Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=short_condition, title="Short Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Plot EMA
plot(ema, title="Trend-EMA", color=color.blue)

// Trailing stop loss logic
trail_stop = na
if (long_condition)
    trail_stop := ta.valuewhen(long_condition, ema - atr_length1 * atr_factor1, 0)
if (short_condition)
    trail_stop := ta.valuewhen(short_condition, ema + atr_length1 * atr_factor1, 0)

// Exit logic based on risk/reward
risk_reward = na
if (long_condition and not na(trail_stop))
    risk_reward := (ta.highest(high, atr_length1) - close) / (close - trail_stop)
if (short_condition and not na(trail_stop))
    risk_reward := (low - ta.lowest(low, atr_length1)) / (trail_stop - close)

// Exit on risk/reward
exit_position = false
if (risk_reward >= risk_reward_ratio)
    exit_position := true

// Trade execution logic
if long_condition and not exit_position
    strategy.entry("Long", strategy.long)
if short_condition and not exit_position
    strategy.entry("Short", strategy.short)

// Plot stop loss levels
plot(trail_stop, title="Stop Loss", color=color.red, style=plot.style_linebr, linewidth=2)
``` ```plaintext
The provided Pine Script for a "Triple Supertrend Breakout Strategy" is well-structured and includes the necessary components to identify trading signals based on the supertrend indicators and EMA crossover. Here’s an explanation of each part:

1. **Inputs**:
   - `atr_length1`, `atr_factor1` (for first ATR setting)
   - `atr_length2`, `atr_factor2` (for second ATR setting)
   - `atr_length3`, `atr_factor3` (for third ATR setting)
   - `trend_ema_length` (length of the EMA used to define trend direction)
   - `source` (default is close price, but can be modified if needed)
   - `offset` (offset for plotting shapes and lines)
   - `backtest_start_time`, `backtest_end_time` (for backtesting purposes)
   - `exit_on_risk_reward_ratio` (logical input to decide when to exit based on risk/reward ratio)
   - `risk_reward_ratio` (minimum required risk-reward ratio for exiting a trade)

2. **Supertrend Calculation**:
   Each supertrend is calculated using the `supertrend` function with specified lengths and factors.

3. **Condition Logic**:
   - `long_condition`: A long position will be triggered when all three Supertrends indicate downward momentum (`direction < 0`) and are above the EMA.
   - `short_condition`: A short position will be triggered when all three Supertrends indicate upward momentum (`direction > 0`) and are below the EMA.

4. **Plotting**:
   - Long signals and short signals are plotted using `plotshape`.
   - The trend-EMA is also plotted.
   - Stop loss levels (calculated based on the highest high or lowest low within a certain ATR) are plotted as horizontal lines.

5. **Trade Execution**:
   - Entries are made when conditions for long or short positions are met, and if no exit condition has been triggered yet (`exit_position` is `false`).

6. **Risk Management**:
   - Risk/reward ratio is used to decide whether to exit the trade based on the current position.
   
This script should be tested in the TradingView Pine Editor before deploying it for live trading, as backtesting and thorough testing are crucial steps to ensure that the strategy performs well under various market conditions. Adjust the parameters and logic according to your specific requirements or risk tolerance.

If you need further customization or optimization, please specify your exact needs.
```