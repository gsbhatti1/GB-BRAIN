> Name

Solid-and-Steady-SMA-Position-Holding-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11576d054afd0402f77.png)
 [trans]

## Overview

This strategy is a simple position holding strategy based on SMA lines. It goes long when the short-term SMA line crosses over the long-term SMA line, and closes the position when the short-term SMA line crosses below the long-term SMA line.

## Strategy Principle

The strategy uses two SMA lines, one short-term 20-day line and one long-term 50-day line. The short-term line can catch price trend changes faster, while the long-term line filters out short-term noise. When the short-term line rises quickly above the long-term line, it indicates the trend may have started a long-term upturn, so we go long here. When the short-term line drops below the long-term line, it suggests the uptrend may have ended, so we close the position here.

In summary, this strategy utilizes the curve features of SMA lines to determine price movement trends on two time dimensions, and makes stable profits with relatively steady position holding.

## Advantage Analysis

The advantages of this strategy include:

1. Simple to operate, easy to understand, low barrier to use
2. Relatively stable by leveraging the strengths of SMA lines
3. Long holding periods, less impacted by short-term market noise
4. Few configurable parameters, easy to find optimal parameter combinations

## Risk Analysis

The risks of this strategy include:

1. More stop losses possible when the market is in a long-term range-bound condition
2. SMA lines have a lagging effect, cannot catch immediate price changes
3. Unable to capitalize on short-term spike pullback patterns
4. Unable to control the size of single trade losses

## Optimization Directions

This strategy can be further optimized in the following aspects:

1. Add the MACD indicator to identify bottom rebound timing to reduce losses during range-bound markets
2. Test different SMA line parameter combinations to find the optimal parameters
3. Incorporate domestic indicators to spot trend divergence, improving entry accuracy
4. Add profit-taking and stop-loss mechanisms to control single trade profit/loss

## Summary

In summary, this SMA position holding strategy is stable, simple, and easy to operate, suitable for beginner live trading. As algorithmic trading continues to evolve, this strategy can incorporate more indicators and techniques for better performance.

---

|Argument|Default|Description|
|---|---|---|
|v_input_1|14|Length|
|v_input_2|true|Highlight Movements?|
|v_input_3_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_float_1|true|Long Take Profit 1 %|
|v_input_int_1|10|Long Take Profit 1 Qty|
|v_input_float_2|5|Long Take Profit 2%|
|v_input_int_2|50|Long Take Profit 2 Qty|
|v_input_float_3|2.2|SL Multiplier|
|v_input_int_3|17|ATR period|
|v_input_4|2022|Backtest Start Year|
|v_input_5|true|Backtest Start Month|
|v_input_6|true|Backtest Start Day|
|v_input_7|9999|Backtest Stop Year|
|v_input_8|12|Backtest Stop Month|
|v_input_9|31|Backtest Stop Day|

---

```pinescript
/*backtest
start: 2022-12-11 00:00:00
end: 2023-12-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy('Solid-and-Steady-SMA-Position-Holding-Strategy', overlay=true )

// FUNCTIONS

Atr(p) =>
    atr = 0.
    Tr = math.max(high - low, math.max(math.abs(high - close[1]), math.abs(low - close[1])))
    atr := nz(atr[1] + (Tr - atr[1]) / p, Tr)
    atr

// SMA
length = input(title='Length', defval=14)
highlightMovements = input(title='Highlight Movements ?', defval=true)
src = input(title='Source', defval=close)

lag = math.floor((length - 1) / 2)

sma = ta.sma(src, length)

smaColor = highlightMovements ? sma > sma[1] ? color.green : color.red : color.blue
plot(sma, title='SMA', linewidth=2, color=smaColor, transp=0)

// TAKE PROFIT AND STOP LOSS
long_tp1_inp = input.float(1, title='Long Take Profit 1 %', step=0.1) / 100
long_tp1_qty = input.int(10, title='Long Take Profit 1 Qty', step=1)

long_tp2_inp = input.float(5, title='Long Take Profit 2%', step=0.1) / 100
long_tp2_qty = input.int(50, title='Long Take Profit 2 Qty', step=1)

long_take_level_1 = strategy.position_avg_price * (1 + long_tp1_inp)
long_take_level_2 = strategy.position_avg_price * (1 + long_tp2_inp)

// Stop Loss
multiplier = input.float(2.2, 'SL Multiplier', minval=1, step=0.1)
ATR_period = input.int(17, 'ATR period', minval=1, step=1)

// Strategy
entry_long = sma > sma[1]
entry_price_long = ta.valuewhen(entry_long, close, 0)
SL_floating_long = entry_price_long - multiplier * Atr(ATR_period)
exit_long = sma < sma[1]

// BACKTEST PERIOD
testStartYear = input(2022, 'Backtest Start Year')
testStartMonth = input(1, 'Backtest Start Month')
testStartDay = input(1, 'Backtest Start Day')
testPeriodStart = timestamp(testStartYear, testStartMonth, testStartDay, 0, 0)

testStopYear = input(9999, 'Backtest Stop Year')
testStopMonth = input(12, 'Backtest Stop Month')
testStopDay = input(31, 'Backtest Stop Day')
testPeriodStop = timestamp(testStopYear, testStopMonth, testStopDay, 0, 0)
```