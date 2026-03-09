``` pinescript
/*backtest
start: 2024-11-12 00:00:00
end: 2024-12-11 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © MounirTrades007

// @version=6
strategy("Bollinger Bands", overlay=true, initial_capital=100000, default_qty_type=strategy.percent_of_equity, default_qty_value=200)

// Get user input
var g_bb        = "Bollinger Band Settings"
upperBandSD     = input.float(title="Upper Band Std Dev", defval=3.0, tooltip="Upper band's standard deviation multiplier", group=g_bb)
lowerBandSD     = input.float(title="Lower Band Std Dev", defval=1.0, tooltip="Lower band's standard deviation multiplier", group=g_bb)
maPeriod        = input.int(title="Middle Band MA Length", defval=100, tooltip="Middle band's SMA period length", group=g_bb)
var g_tester    = "Backtester Settings"
drawTester      = input.bool(title="Draw Backtester", defval=true, group=g_tester, tooltip="Turn on/off inbuilt backtester display")

// Get Bollinger Bands
[bbIgnore1, bbHigh, bbIgnore2] = ta.bb(close, maPeriod, upperBandSD)
[bbMid, bbIgnore3, bbLow]      = ta.bb(close, maPeriod, lowerBandSD)

// Plot the bands and middle line
plot(bbHigh, title="Upper Band", color=color.blue, linewidth=1)
plot(bbMid, title="Middle Band", color=color.orange, linewidth=1)
plot(bbLow, title="Lower Band", color=color.red, linewidth=1)

// Generate buy/sell signals
longCondition = ta.crossover(close, bbHigh)
shortCondition = ta.crossunder(close, bbLow)

if (drawTester) 
    if (longCondition) 
        strategy.entry("Long", strategy.long)
    if (shortCondition) 
        strategy.close("Long")
```

This Pine Script code sets up a trading strategy based on Bollinger Bands with specific settings for the upper and lower bands. It also includes basic backtesting functionality to monitor performance.