``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-11 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © EdgeTools

//@version=5
strategy("123 Reversal Trading Strategy", overlay=true)

// Input for number of days to hold the trade
daysToHold = input(7, title="Days to Hold Trade")

// Input for 20-day moving average
maLength = input(200, title="Moving Average Length")

// Calculate the 20-day moving average
ma20 = ta.sma(close, maLength)

// Define the conditions for the 123 reversal pattern (bullish reversal)
// Condition 1: Today's low is lower than yesterday's low
condition1 = low < low[1]

// Condition 2: Yesterday's low is lower than the low three days ago
condition2 = low[1] < low[3]

// Condition 3: The low two days ago is lower than the low four days ago
condition3 = low[2] < low[4]

// Condition 4: The high two days ago is lower than the high three days ago
condition4 = high[2] < high[3]

// Entry condition: All conditions must be true simultaneously
entryCondition = condition1 and condition2 and condition3 and condition4

// Exit condition: Close position when price touches or exceeds 200-day moving average
exitCondition = ta.crossover(close, ma20) or (bar_index - strategy.opentrades.entry_bar_index(strategy.opentrades-1)) >= daysToHold

// Plot the 20-day moving average on the chart
plot(ma20, color=color.blue)

// Open long position when entry condition is met
if entryCondition
    strategy.entry("Long", strategy.long)

// Close long position based on exit condition
if exitCondition
    strategy.close("Long")

```

This Pine Script code implements a trading strategy based on the 123 point reversal pattern. It includes inputs for holding days and moving average length, calculates the 20-day simple moving average (SMA), defines entry and exit conditions, and plots the SMA on the chart. The script also includes logic to open a long position when the 123 pattern is detected and close it based on either hitting the 200-day SMA or reaching the specified holding period.