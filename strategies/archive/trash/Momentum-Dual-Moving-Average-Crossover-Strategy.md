``` pinescript
/*backtest
start: 2023-09-19 00:00:00
end: 2023-10-19 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Cryptoluc1d

//@version=4
strategy("Equal-Length EMA/SMA Crossover Strategy", initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=25, commission_type=strategy.commission.percent, commission_value=0.2, overlay=true)

// Create inputs

mom_length = input(title="Momentum Length (EMA=SMA)", defval=50)
bias_length_fast  = input(title="Golden Cross Length (Fast)", defval=50)
bias_length_slow  = input(title="Golden Cross Length (Slow)", defval=100)

// Define MAs

ema = ema(close, mom_length) // EMA/SMA crossover of the same period for detecting trend acceleration/deceleration
sma = sma(close, mom_length)
bias_fast = sma(close, bias_length_fast) // golden/death cross for overall trend bias
bias_slow = sma(close, bias_length_slow)

// Define signal conditions

buy_trend = crossover(ema, sma) and bias_fast >= bias_slow // buy when EMA crosses above SMA. if this happens during a bullish golden cross, buying is in confluence with the overall trend (bias).
buy_risky = crossover(ema, sma) and bias_fast < bias_slow // buy when EMA crosses above SMA. if this happens during a bearish death cross, buying is early, more risky, and not in confluence with the overall trend (bias).
buy_late = crossover(sma, bias_slow) and ema > sma // the SMA crossing the Slow_SMA gives further confirmation of bullish trend, but signal comes later.
sell = crossunder(ema, sma) // sell when EMA crosses under SMA.

// Enable option to hide signals, then plot signals

show_signal = input(title="Show Signals", defval=true)

plotshape(show_signal ? buy_trend : na, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(show_signal ? sell : na, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)

// Enable option to hide MAs

show_mas = input(title="Show MAs", defval=false)

if (show_mas)
    plot(ema, title="EMA", color=color.blue)
    plot(sma, title="SMA", color=color.orange)
```

This completes the translation and formatting of your strategy document to English.