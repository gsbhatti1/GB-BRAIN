> Name

Dual-Donchian-Channel-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/10d8acc7a960c28685b.png)
[trans]
## Overview
The Dual-Donchian Channel Breakout Strategy (Dual Donchian Channel Breakout Strategy) is a trading strategy based on Donchian Channels. It uses fast and slow Donchian Channels to generate long and short trading signals. When the price breaks through the slow channel, open a long or short position. When the price breaks back through the fast channel, close the position. The strategy also sets take profit and stop loss conditions.

## Strategy Principle

The Dual-Donchian Channel Breakout Strategy is based on two parameters: **Slow Donchian Channel Period** and **Fast Donchian Channel Period**. The strategy first calculates the upper and lower bands of the two Donchian Channels.

- The default slow Donchian channel period is 50 bars, reflecting longer term trends.
- The default fast Donchian channel period is 30 bars, reflecting shorter term trend changes.

The long entry signal is a **breakout above the upper band** with **volatility greater than the threshold**. The short entry signal is a **breakdown below the lower band** with **volatility greater than the threshold**.

The long stop loss exit signal is a **breakdown below the lower band**. The short stop loss exit signal is a **breakout above the upper band**.

The strategy also sets **take profit** exit conditions. The default take profit ratio is 2%, that is, take profit half the position when the price movement reaches 2%.

## Advantage Analysis

The Dual-Donchian Channel Breakout Strategy has the following advantages:

1. The dual channel design can capture trend signals from both longer and shorter timeframes, allowing more accurate entries.
2. The volatility condition avoids frequent trading in range-bound markets.
3. Comprehensive take profit and stop loss settings lock in partial profits and reduce losses.
4. Simple and clear strategy logic, easy to understand and implement.
5. Customizable parameters suit different products and trading preferences.

## Risk Analysis

The Dual-Donchian Channel Breakout Strategy also has some risks:

1. The dual channel design is sensitive and can generate false signals. Wider channels or adjusted volatility parameters may reduce false signals.
2. In volatile markets, stop loss may trigger too frequently. Consider setting a limit on the number of trades or widening the stop loss range.
3. Fixed percentage take profit fails to maximize profits. Consider dynamic or manual intervention for optimal take profit pricing.
4. Real trading performance may differ from backtest expectations. Requires thorough validation and parameter adjustments if needed.

## Optimization Directions

The Dual-Donchian Channel Breakout Strategy can be optimized in several aspects:

1. Test more period combinations to find optimal parameters.
2. Try different volatility measures like ATR to find the most stable metric.
3. Set a limit on the number of entries to avoid losses at the end of trends.
4. Try dynamic take profit for higher single trade profit.
5. Incorporate other indicators to filter entries and improve accuracy, e.g., volume.
6. Optimize money management models like fixed fractional position sizing for better risk control.

## Conclusion

In conclusion, the Dual-Donchian Channel Breakout Strategy is an excellent trend following strategy. It combines both trend identification and reversal protection capabilities. With parameter optimization and rule refinement, it can be profitable across most products and market conditions. The strategy is simple and practical, worth learning and applying for quantitative traders.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|50|(?Conditions)Slow Donchian|
|v_input_int_2|30|Fast Donchian|
|v_input_int_3|3|Volatility (%)|
|v_input_bool_1|true|(?Strategy)Long Position On/Off|
|v_input_float_1|2|Long TP1 (%)|
|v_input_bool_2|true|Short Position On/Off|
|v_input_float_2|2|Short TP1 (%)|
|v_input_int_4|50|TP1 Position Amount (%)|


> Source (PineScript)

```pinescript
//@version=5
strategy(title="Dual Donchian Channel Breakout Strategy", overlay=true, initial_capital=1000, commission_value=0.05, default_qty_type=strategy.percent_of_equity)

// Donchian Channels
slowLen = input.int(50, minval=1, title="Slow Donchian")
fastLen = input.int(30, minval=1, title="Fast Donchian")
volThresh = input.int(3, minval=1, title="Volatility (%)")
longPos = input.bool(true, title="Long Position On/Off")
longTp1Pct = input.float(2, minval=0, maxval=100, title="Long TP1 (%)")
shortPos = input.bool(true, title="Short Position On/Off")
shortTp1Pct = input.float(2, minval=0, maxval=100, title="Short TP1 (%)")
tp1PosAmount = input.int(50, minval=1, title="TP1 Position Amount (%)")

// Calculate Donchian Channels
slowHigh = ta.highest(high, slowLen)
slowLow = ta.lowest(low, slowLen)
fastHigh = ta.highest(high, fastLen)
fastLow = ta.lowest(low, fastLen)

// Long Entry
longEntry = ta.crossover(close, slowHigh) and ta.volatility > volThresh
if (longEntry and longPos)
    strategy.entry("Long", strategy.long)

// Long Stop Loss
longExit = ta.crossunder(close, slowLow)
if (longExit)
    strategy.close("Long")

// Long Take Profit
longTp1 = strategy.position_avg_price * (1 + longTp1Pct / 100)
if (strategy.position_size > 0 and close > longTp1)
    strategy.exit("Long TP1", "Long", profit=longTp1Pct / 100)

// Short Entry
shortEntry = ta.crossunder(close, fastLow) and ta.volatility > volThresh
if (shortEntry and shortPos)
    strategy.entry("Short", strategy.short)

// Short Stop Loss
shortExit = ta.crossover(close, fastHigh)
if (shortExit)
    strategy.close("Short")

// Short Take Profit
shortTp1 = strategy.position_avg_price * (1 - shortTp1Pct / 100)
if (strategy.position_size < 0 and close < shortTp1)
    strategy.exit("Short TP1", "Short", loss=shortTp1Pct / 100)
```