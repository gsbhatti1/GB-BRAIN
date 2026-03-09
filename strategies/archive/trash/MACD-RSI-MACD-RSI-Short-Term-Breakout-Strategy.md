``` pinescript
/*backtest
start: 2023-09-06 00:00:00
end: 2023-10-06 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © pluckyCraft54926

//@version=5
strategy("MACD-RSI-Short-Term-Breakout-Strategy", overlay=true, margin_long=100, margin_short=100)

fast_length = input.int(title="Fast Length", defval=12)
slow_length = input.int(title="Slow Length", defval=26)
src = input.source(title="Source", defval=close)
signal_smooth = input.int(title="Signal Smoothing", minval=1, maxval=50, defval=9)
sma_source = input.string(title="Oscillator MA Type", options=['EMA', 'SMA'], defval='EMA')
sma_length_signal = input.int(title="Signal Line MA Length", minval=1, defval=9)
length_bb_long = input.int(title="LengthBB Long", minval=5, defval=94)
length_bb_short = input.int(title="LengthBB Short", minval=5, defval=83)
std_dev = input.float(title="StdDev", defval=2.0)
offset = input.int(title="Offset", defval=0, minval=-1000, maxval=1000)
length_rsi_long = input.int(title="Rsi Length Long", minval=5, defval=11)
length_rsi_short = input.int(title="Rsi Length Short", minval=5, defval=29)
take_profit_percent = input.float(title="% Take Profit", defval=0.5)
stop_loss_percent = input.float(title="% Stop Loss", defval=0.3)
macd_tick_low = input.int(title="MacdTick Low", defval=-10)
macd_tick_high = input.int(title="MacdTick High", defval=35)

// MACD
[macd_line, signal_line, _] = macd(src, fast_length, slow_length, signal_smooth)
hline(macd_tick_low, "MACDTick Low")
hline(macd_tick_high, "MACDTick High")

// RSI
rsi_long = rsi(src, length_rsi_long)
rsi_short = rsi(src, length_rsi_short)

// Bollinger Bands
length_bb = input.int(title="Bollinger Length", defval=20, minval=5)
basis = sma(src, length_bb)
dev = std_dev * ta.stdev(src, length_bb)
upper_band = basis + dev
lower_band = basis - dev

// Strategy Conditions
long_condition = macd_line < lower_band and rsi_long > 51
short_condition = macd_line > upper_band and rsi_short < 49

// Plotting
plot(macd_line, color=color.new(#26A69A, 0), title="MACD Line")
plot(signal_line, color=color.new(#FF6D00, 0), title="Signal Line")
fill(area(hline(macd_tick_low) and macd_line < lower_band, hline(macd_tick_high) and macd_line > upper_band), color=color.green, transp=90)
fill(area(macd_line < lower_band, macd_line > upper_band), color=color.red, transp=50)

// Trading Logic
if (long_condition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Take Profit/Stop Loss", "Long", profit:=take_profit_percent * 100 / 100, loss:=stop_loss_percent * 100 / 100)

if (short_condition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Take Profit/Stop Loss", "Short", profit:=take_profit_percent * 100 / 100, loss:=stop_loss_percent * 100 / 100)
```