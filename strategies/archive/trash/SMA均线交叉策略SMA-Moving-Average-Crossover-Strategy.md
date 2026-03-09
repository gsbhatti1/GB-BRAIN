``` pinescript
/*backtest
start: 2023-03-22 00:00:00
end: 2024-03-27 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © j0secyn

//@version=5
strategy("MA Cross", overlay=true, margin_long=100, margin_short=100, default_qty_value=100, default_qty_type=strategy.percent_of_equity, initial_capital=10000)

// === INPUT BACKTEST RANGE ===
fromDay   = input.int(defval = 1, title = "From Day", minval = 1, maxval = 31)
fromMonth = input.int(defval = 1, title = "From Month", minval = 1, maxval = 12)
fromYear  = input.int(defval = 2018,title = "From Year", minval = 1970)
thruDay   = input.int(defval = 30, title = "Thru Day", minval = 1, maxval = 31)
thruMonth = input.int(defval = 9, title = "Thru Month", minval = 1, maxval = 12)
thruYear  = input.int(defval = 2024,title = "Thru Year", minval = 1970)

// === INPUT MA PERIODS ===
slowMAlength = input.int(title="Slow MA length", defval=100, minval=1)
fastMAlength = input.int(title="Fast MA length", defval=30, minval=1)

// === BACKTEST DATES ===
start_date = timestamp(fromYear, fromMonth, fromDay, 0, 0)
end_date   = timestamp(thruYear, thruMonth, thruDay, 0, 0)

// === STRATEGY LOGIC ===
var float slowMA = na
var float fastMA = na

if time >= start_date and time <= end_date
    slowMA := ta.sma(close, slowMAlength)
    fastMA := ta.sma(close, fastMAlength)

plot(slowMA, color=color.blue, linewidth=2, title="Slow MA")
plot(fastMA, color=color.red, linewidth=2, title="Fast MA")

// === ENTRY/EXIT RULES ===
longCondition = crossover(fastMA, slowMA)
if longCondition
    strategy.entry("Long", strategy.long)

shortCondition = crossunder(fastMA, slowMA)
if shortCondition
    strategy.close("Long")
```

This script completes the Pine Script by adding the missing input for `thruMonth` and `thruYear`. It also includes the logic to calculate and plot the SMAs based on the specified time periods. The entry/exit rules are defined using the crossover/crossunder functions to manage long positions accordingly.