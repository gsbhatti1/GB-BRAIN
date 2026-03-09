> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|20|Swing Lookback|
|v_input_float_1|5|Stop Target Percentage|
|v_input_bool_1|true|Begin Backtest at Start Date|
|v_input_1|timestamp(1 Jan 2020)|Start Date|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-09-29 00:00:00
end: 2023-10-29 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © deperp

//@version=5
strategy("Scalable Breakout Trading Strategy", overlay=true, initial_capital=100000, default_qty_type=strategy.percent_of_equity, default_qty_value=10, commission_type=strategy.commission.percent, commission_value=0.07, pyramiding=0)

// Backtest Time Period

useDateFilter = input.bool(true, title="Begin Backtest at Start Date",
     group="Backtest Time Period")
backtestStartDate = input(timestamp("1 Jan 2020"), 
     title="Start Date", group="Backtest Time Period")

// Strategy Parameters
swingLookback = input.int(20, title="Swing Lookback")
stopTargetPercent = input.float(5.0, title="Stop Target Percentage")
useDateFilter ? backtestStartDate : datetime.max

// Swing Calculation
highSwing = ta.highest(high, swingLookback)
lowSwing = ta.lowest(low, swingLookback)

// Long Entry Condition
longCondition = close >= highSwing

// Short Entry Condition
shortCondition = close <= lowSwing

// Stop Loss Conditions
stopLossLong = (high - (high * stopTargetPercent / 100))
stopLossShort = (low + (low * stopTargetPercent / 100))

// Order Management
if (useDateFilter and backtestStartDate < time)
    strategy.entry("Long", strategy.long, when=longCondition)
    strategy.exit("Stop Loss Long", "Long", stop=stopLossLong)
    
if (useDateFilter and backtestStartDate < time) 
    strategy.entry("Short", strategy.short, when=shortCondition)
    strategy.exit("Stop Loss Short", "Short", stop=stopLossShort)

// Plotting
plotshape(series=longCondition, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labeldown, text="BUY")
plotshape(series=shortCondition, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labelup, text="SELL")
```

This script implements the scalable breakout trading strategy as described in the document. It includes backtesting parameters and order management logic with stop loss conditions based on the specified `stopTargetPercent`. The code also plots buy and sell signals for visualization.