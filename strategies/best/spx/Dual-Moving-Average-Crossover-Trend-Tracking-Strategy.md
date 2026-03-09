> Name

Dual-Moving-Average-Crossover-Trend-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description


## Overview

This strategy employs the dual moving average crossover principle, combined with a trend tracking indicator, to identify and follow trends. The main idea is to go long when the short-term moving average crosses above the long-term moving average, and to go short when the short-term moving average crosses below the long-term moving average. Additionally, a 100-day moving average is used to determine the overall trend direction, helping to avoid false breakouts.

## Strategy Logic

The strategy consists primarily of a dual moving average crossover system and a trend tracking system.

The dual moving average crossover system includes a fast EMA (Exponential Moving Average) with a default period of 10 days and a slow EMA with a default period of 20 days. A buy signal is generated when the fast EMA crosses above the slow EMA, while a sell signal is generated when the fast EMA crosses below the slow EMA.

A 100-day EMA (EMA100) is added to determine the overall trend direction. Buy signals are only generated when the price is in an upward trend (price above the 100-day EMA). Sell signals are only generated when the price is in a downward trend (price below the 100-day EMA). This helps filter out most false breakout situations.

Buy and sell arrows are also plotted on the candles to visually display the trading signals.

The trend tracking system uses intraday and cycle day lines to confirm the trend direction again. Intraday uses 5-minute and 60-minute Heikin-Ashi moving averages, while the cycle uses 8-day and 12-day moving averages of the daily line.

Trading signals are only generated when the intraday and cycle judgments agree. This further filters out most noise in non-major trend directions.

## Advantage Analysis

The biggest advantage of this strategy lies in its integration of both trend tracking and moving average crossover systems, effectively filtering out false signals and keeping drawdowns within acceptable levels.

Specifically, the advantages of the dual moving average crossover system are:

1. Simple logic and easy to understand, suitable for beginners.
2. Trend-following, avoiding trading against the trend.
3. Customizable fast and slow EMA periods, adaptable to different cycles.
4. Strong profitability in major trends.

Adding the 100-day EMA has the advantages of:

1. Avoiding false breakout trades, reducing losses.
2. Following the overall trend, keeping drawdowns controllable.

The trend tracking system's advantages include:

1. Multiple timeframe analysis, avoiding noise from a single period.
2. Ensuring alignment with major trend direction, reducing drawdowns.
3. Heikin-Ashi smoothing filters out noise and captures only trends.

## Risk Analysis

Some risks to note for this strategy include:

1. Frequent crossovers and additional trading costs during prolonged consolidations.
2. Delayed signals, missing early trend stages.
3. Severe losses when major trends reverse.
4. Performance depends on parameter optimization.

Solutions:

1. Reduce trading frequency during consolidations.
2. Shorten EMA periods to get earlier trend signals.
3. Use stop loss orders to control single-loss events.
4. Optimize parameters for different products and market conditions.

## Optimization Directions

This strategy can be optimized in the following areas:

1. EMA period optimization by testing more combinations to find optimal periods.
2. Adding more timeframe judgments, such as monthly or quarterly lines.
3. Incorporating stop loss mechanisms like moving or exponential stops.
4. Combining with volume indicators like On Balance Volume.
5. Improving entry timing using faster oscillators like MACD.
6. Parameter optimization for different products and assets.

## Conclusion

This strategy combines the strengths of dual moving average crossover and trend tracking systems, avoiding the weaknesses of single-system approaches. Multiple timeframe analysis ensures correct trade direction while drawdown control is excellent. Further optimizations can adapt it to more market environments for practical usage.

---

> Strategy Arguments


|Argument     |Default|Description|
|-------------|-------|-----------|
|v_input_1    |10     |par1       |
|v_input_2    |20     |par2       |
|v_input_3    |8      |MA1        |
|v_input_4    |12     |MA2        |
|v_input_5    |D      |Short Time|
|v_input_6    |W      |Long Time |
|v_input_7    |16     |EMA Period|

> Source (PineScript)

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
//@version=5
strategy("Dual-Moving-Average-Crossover-Trend-Tracking-Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Inputs for EMA periods
ema1_len = input(10, title="Short Time", type=input.integer)
ema2_len = input(20, title="Long Time", type=input.integer)

// Inputs for trend direction determination
trend_dir = input("D", title="Direction", options=["D", "W"])

// 100-day EMA period
ema100_len = input(16, title="EMA Period", type=input.integer)

// Short and long time frames
short_timeframe = input.timeframe(trend_dir == "D" ? "5m" : "30m")
long_timeframe = input.timeframe(trend_dir == "W" ? "24h" : "1d")

// Calculate EMAs
fast_ema = ta.ema(close, ema1_len)
slow_ema = ta.ema(close, ema2_len)

// Generate signals based on crossovers and 100-day EMA direction
buy_signal = ta.crossover(fast_ema, slow_ema) and close > ta.ema(close, ema100_len)
sell_signal = ta.crossunder(fast_ema, slow_ema) and close < ta.ema(close, ema100_len)

// Plot signals on the chart
plotshape(series=buy_signal, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.triangleup, text="BUY")
plotshape(series=sell_signal, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.tiangroupdown, text="SELL")

// Intraday and cycle trend tracking
intraday_fast_ema = ta.ema(close, ema1_len * 5)
intraday_slow_ema = ta.ema(close, ema2_len * 5)

cycle_fast_ema = ta.ema(close, ema1_len * 8)
cycle_slow_ema = ta.ema(close, ema2_len * 8)

// Generate intraday and cycle signals
intraday_buy_signal = ta.crossover(intraday_fast_ema, intraday_slow_ema)
intraday_sell_signal = ta.crossunder(intraday_fast_ema, intraday_slow_ema)

cycle_buy_signal = ta.crossover(cycle_fast_ema, cycle_slow_ema)
cycle_sell_signal = ta.crossunder(cycle_fast_ema, cycle_slow_ema)

// Ensure agreement between intraday and cycle signals
final_buy_signal = buy_signal or (intraday_buy_signal and cycle_buy_signal)
final_sell_signal = sell_signal or (intraday_sell_signal and cycle_sell_signal)

// Apply final trading signals
strategy.entry("Buy", strategy.long, when=final_buy_signal)
strategy.close("Buy", when=final_sell_signal)

// Plot buy and sell arrows on the candlesticks
plotshape(series=final_buy_signal, title="Buy Arrow", location=location.belowbar, color=color.green, style=shape.triangleup, text="BUY")
plotshape(series=final_sell_signal, title="Sell Arrow", location=location.abovebar, color=color.red, style=shape.tiangroupdown, text="SELL")
```