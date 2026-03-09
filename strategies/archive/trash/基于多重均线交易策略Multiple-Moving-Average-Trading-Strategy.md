``` pinescript
/*backtest
start: 2023-02-22 00:00:00
end: 2024-02-28 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Multiple Moving Average Trading Strategy", overlay=true)

// Input Arguments
fast_length = input.int(title = "Fast Length", defval = 12)
slow_length = input.int(title = "Slow Length", defval = 26)
src = input.source(title = "Source", defval = close)
signal_length = input.int(title = "Signal Smoothing", minval = 1, maxval = 50, defval = 9)
sma_source = input.string(title = "Oscillator MA Type", defval = "EMA", options = ["SMA", "EMA"])
sma_signal = input.string(title = "Signal Line MA Type", defval = "EMA", options = ["SMA", "EMA"])

// Calculating
fast_ma = sma_source == "SMA" ? ta.sma(src, fast_length) : ta.ema(src, fast_length)
slow_ma = sma_source == "SMA" ? ta.sma(src, slow_length) : ta.ema(src, slow_length)
macd = fast_ma - slow_ma
signal = sma_signal == "SMA" ? ta.sma(macd, signal_length) : ta.ema(macd, signal_length)
hist = macd - signal

// Plotting and Alerts
alertcondition(hist[1] >= 0 and hist < 0, title = 'Rising to falling', message = 'The MACD histogram switched from a rising to falling state')
alertcondition(hist[1] <= 0 and hist > 0, title = 'Falling to rising', message = 'The MACD histogram switched from a falling to rising state')

hline(0, "Zero Line", color=color.new(#787B86, 50))
plot(hist, title="Histogram", color=hist > 0 ? color.green : color.red)

// MA Signals
ma5 = ta.sma(src, 5)
ma25 = ta.sma(src, 25)
ma45 = ta.sma(src, 45)
ma100 = ta.sma(src, 100)

// ZLSMA Signal
zlsma_length = input.int(title="Length", defval=32)
zlsma = ta.sma(src, zlsma_length)

// Divergence
distance = abs(ma5 - ma25) + abs(ma25 - ma45) + abs(ma45 - ma100)
alertcondition(distance > 0.03, title="Divergence", message="Divergence detected")

// Exit Conditions
long_stop = input.float(title="Long Stop Loss (pips)", defval=0.06)
short_stop = input.float(title="Short Stop Loss (pips)", defval=-0.06)
long_take = input.float(title="Long Take Profit (pips)", defval=0.06)
short_take = input.float(title="Short Take Profit (pips)", defval=-0.06)

// Strategy Execution
if (hist[1] > 0 and hist < 0)
    strategy.entry("Long", strategy.long)
if (hist[1] < 0 and hist > 0)
    strategy.entry("Short", strategy.short)
if (strategy.position_size > 0 and close < (strategy.entry_price("Long") * (1 - long_stop)))
    strategy.close("Long")
if (strategy.position_size < 0 and close > (strategy.entry_price("Short") * (1 + short_stop)))
    strategy.close("Short")

// Plot ZLSMA
plot(zlsma, title="ZLSMA", color=color.blue)

```

This script incorporates the described strategy, including the calculation of MACD, multiple moving averages, and ZLSMA, as well as the stop and take profit conditions.