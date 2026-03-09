``` pinescript
/*backtest
start: 2023-02-23 00:00:00
end: 2024-02-29 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © maizirul959

//@version=4
strategy("MACD, RSI & EMA Strategy with MA+PSAR by ChaoZhang", overlay=true)

// Input Data
ema1_len = input(5, title="EMA1 length")
ema2_len = input(20, title="EMA2 length")

macd_fast = input(12, title="MACD Fast")
macd_slow = input(26, title="MACD Slow")
macd_signal_len = input(20, title="MACD Signal length")

// Add SMA
sma1_len = input(5, title="SMA1 Length")
sma2_len = input(10, title="SMA2 Length")
sma3_len = input(50, title="SMA3 Length")
sma4_len = input(200, title="SMA4 Length")

line_width = input(1, minval=1, title="Line width")

src = input(close, title="Source")

// Calculate SMAs
sma1 = if sma1_len != 0
    sma(src, sma1_len)
sma2 = if sma2_len != 0
    sma(src, sma2_len)
sma3 = if sma3_len != 0
    sma(src, sma3_len)
sma4 = if sma4_len != 0
    sma(src, sma4_len)

// Plot SMAs
plot(sma1, color=color.red, title="SMA1", linewidth=line_width)
plot(sma2, color=color.green, title="SMA2", linewidth=line_width)
plot(sma3, color=color.blue, title="SMA3", linewidth=line_width)
plot(sma4, color=color.gray, title="SMA4", linewidth=line_width)

// RSI
rsi_len = input(14, title="RSI length")
rsi_signal_len = input(20, title="RSI signal length")

// Calculate and plot RSI
rsi = rsi(src, rsi_len)
plot(rsi, color=color.orange, title="RSI", linewidth=line_width)

// PSAR
psar_start = input(0.02, title="PSAR start")
psar_increment = input(0.02, title="PSAR increment")
psar_maximum = input(0.2, title="PSAR maximum")

psar = sar(psar_start, psar_increment, psar_maximum)
plot(psar, "Parabolic SAR", color=color.red)

// MACD
macd = ema(src, macd_fast) - ema(src, macd_slow)
macd_signal = ema(macd, macd_signal_len)
plot(macd, color=color.blue, title="MACD", linewidth=line_width)
plot(macd_signal, color=color.green, title="Signal Line", linewidth=line_width)

// Trading logic
short_condition = crossover(sma1_len, sma4_len) and rsi > 100
long_condition = crossunder(sma2_len, sma3_len) and rsi < -100

if short_condition
    strategy.entry("Short", strategy.short)
if long_condition
    strategy.entry("Long", strategy.long)

// Stop loss based on ATR
atr_length = input(14, title="ATR length")
atr_value = atr(atr_length)

stop_loss_long = sma4 + atr_value * -2
stop_loss_short = sma1 - atr_value * 2

if long_condition
    strategy.exit("Long Exit", "Long", stop=stop_loss_long)
if short_condition
    strategy.exit("Short Exit", "Short", stop=stop_loss_short)
```

This Pine Script implements the described MACD, RSI & EMA Strategy with MA+PSAR by ChaoZhang. It includes the necessary inputs and logic to plot SMAs, RSI, PSAR, and manage trading entries and exits based on specified conditions.