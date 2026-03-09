``` pinescript
/*backtest
start: 2022-12-11 00:00:00
end: 2023-12-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy(shorttitle = "GBPUSD MACD", title = "GBPUSD MACD")
fastMA = input(title="Fast moving average",  defval = 12, minval = 7)
slowMA = input(title="Slow moving average",  defval = 26, minval = 7)
lastColor = yellow
[currMacd,_,_] = macd(close[0], fastMA, slowMA, 9)
[prevMacd,_,_] = macd(close[1], fastMA, slowMA, 9)
plotColor = currMacd > 0 ? currMacd > prevMacd ? lime : green : currMacd < prevmacd ? maroon : red
plot(currMacd, style = histogram, color = plotColor, linewidth = 3)
plot(0, title = "Zero line", linewidth = 1, color = gray)

// MACD
// Getting inputs
fast_length = input(title="Fast Length",  defval=12)
slow_length = input(title="Slow Length",  defval=26)
src = input(title="Source", defval=close)
signal_length = input(title="Signal Smoothing",  minval = 1, maxval = 50, defval =9)
sma_source = input(title="Simple MA(Oscillator)", type=bool, defval=false)
sma_signal = input(title="Simple MA(Signal Line)", type=bool, defval=false)

// Plot colors
col_grow_above = #26A69A
col_grow_below = #FFCDD2
col_fall_above = #B2DFDB
col_fall_below = #EF5350
col_macd = #0094ff
col_signal = #ff6a00

// Calculating
fast_ma = sma_source ? sma(src, fast_length) : ema(src, fastMA)
slow_ma = sma(slow_length) ? sma(src, slow_length) : ema(src, slowMA)
macd_line = fast_ma - slow_ma
signal_line = sma(macd_line, signal_length)

// Buy and Sell Conditions
longEntry = crossover(macd_line, signal_line) and macd_line > v_input_9
if (longEntry)
    strategy.entry("Long", strategy.long)
    
shortExit = crossunder(macd_line, signal_line) and macd_line < v_input_10
if (shortExit)
    strategy.close("Long")

// Trailing Stop Loss
stopLossPercent = v_input_9 / close * 100
strategy.exit("Trailing Stop", "Long", stop = stopLossPercent)

// Plotting
plot(macd_line, title="MACD Line", color=col_macd)
plot(signal_line, title="Signal Line", color=col_signal)
```

This Pine Script translates the provided strategy description and code into English while preserving all original code blocks, numbers, and formatting.