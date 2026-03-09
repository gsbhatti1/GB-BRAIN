``` pinescript
/* backtest
start: 2022-04-07 00:00:00
end: 2022-05-06 23:59:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
indicator(title="MAGIC MACD", shorttitle="MAGIC MACD", timeframe="", timeframe_gaps=true)
// By ChaoZhang

// Strategy Description
Thanks & Credits
To Tradingview Team for allowing me to use their default MACD version and coding it into a MAGIC MACD by adding a few lines of code that makes it more enhanced.

About:
MAGIC MACD (MACD Indicator with Trend Filter and EMA Crossover confirmation and Momentum). This MACD uses Default Trading View MACD from the Technical indicators library and adds a second MACD along with 3 EMAs to detect trend and confirm MACD signal. Eliminates usage of 3 different indicators (Default MACD, MACD-2, EMA5, EMA20, EMA50).

Basic IDEA.
Idea is to filter Histogram when price is above or below 50EMA. Similar to QQE -mod oscillator but has an EMA Filter
1. Take DEFAULT MACD crossover signals with lower period
2. Check with a Higher MACD Histogram.
3. Enter upon EMA crossover signal and Histogram confirmation.
Histogram changes to GRAY when price is below EMA 50 or above EMA 50 (Follows Trend)
4. Exit on next Default MACD crossover signal.

Overview:
Moving Average Convergence Divergence Indicator, Popularly Known as MACD, is widely used. MACD usually generates a lot of false signals and noise in Lower Time Frames, making it difficult to enter a trade in sideways market. Divergence is a major issue along with sideways movement and tangling of MACD and Signal Lines. There is no way to confirm a Default MACD signal, except to switch time frames and verify.
Magic MACD can be used to in combination with other signals. This MACD uses two MACD Signals to verify the signal given by Default MACD. The Histogram Plot shown is of a higher period MACD (close,5,50,30) values. When a signal is generated on a lower MACD it is verified by the histogram with higher time period.

Technical Used:
1. Lower MACD-1 values 12,26 and signal-9 (crossover Signals)
2. Higher MACD-2 values 5,50 and signal-30 (Histogram)
3. EMA 50 (Histogram Filter to allow only if price above or below EMA 50)
4. EMA 5 and EMA 20 for crossover confirmation of trend

What's in this Indicator?
1. Histogram-(higher period 5,50 and 30 signal)
2. MACD crossover Signals-(lower period Default MACD setting)
3. Signal Lines-(EMA 5 & 20)

Implemented & Removed in this Indicator
1. Default MACD and Signal Lines are removed completely
2. MACD crossover are taken on lower periods and plotted as signals (Blue Triangle or Red Triangle)
3. Histogram is plotted from a higher Period providing a clear picture with Higher Time period
4. EMA 5 and EMA 20 are used for MACD signal confirmation

How to use?
Up Signal:
1. MACD Default (12,26,30) up signals are shown in Blue
2. Wait till the Histogram changes Blue
3. Look for EMA signals crossover nearby

Down Signal:
1. MACD Default (12,26,30) down signals are shown in Red
2. Wait till the Histogram changes Red
3. Look for EMA signals crossover nearby

Do's
Consider only opposite color as signals
1. Red Triangle on Blue Histogram (likely to move down direction)
2. Blue Triangle on Red Histogram (likely to move up direction)

Don'ts
1. Ignore Blue Signal on Blue Histogram (pull back signals can be used to enter trade if you miss first crossover)
2. Ignore Red Signal on Red Histogram (pull back signals can be used to enter trade if you miss first crossover)
3. Ignore Up and Down signals till Gray or Blacked out area is finished in Histogram

Tips:
1. EMA plot also shows pull back areas along with signals
2. Side by side opposite signals show sideways movement
3. EMA 5,20 is plotted on MACD Histogram for additional benefit

Warning...!
This is purely for Educational purpose only. Not to be used as a stand-alone indicator. Usage is at your own risk. Please get familiar with its working before implementing. It's not Financial Advice or Suggestion. Any losses or gains are at your own risk.

// Getting inputs
enableema = input.bool(true, title='Enable Signal EMA=ON/MACD=OFF', inline="MACD")
fast_length = input(title="Fast Length", defval=5)
slow_length = input(title="Slow Length", defval=50)
src = input(title="Source", defval=ohlc4)
signal_length = input.int(title="Signal Smoothing", minval=1, maxval=50, defval=30)
sma_source = input.string(title="Oscillator MA Type", defval="EMA", options=["SMA", "EMA"])
sma_signal = input.string(title="Signal Line MA Type", defval="EMA", options=["SMA", "EMA"])

// Plot colors
col_macd = input(#2962FF, "MACD Line  ", group="Color Settings", inline="MACD")
col_signal = input(#FF6D00, "Signal Line  ", group="Color Settings", inline="Signal")
col_grow_above = input(#26A69A, "Above   Grow", group="Histogram", inline="Above")
col_fall = input(#B2DFDB, "Fall", group="Histogram", inline="Fall")
col_grow_below = input(#FFCDD2, "Below Grow", group="Histogram", inline="Below")
col_red_fall = input(#ff0062, "Red Fall", group="Histogram", inline="Red Fall")

// MACD Calculation
[MACD, signal, _] = ta.macd(src, fast_length, slow_length, signal_length)
histogram = macd - signal

// EMA Calculation
ema_50 = ta.ema(src, 50)
ema_5 = ta.ema(src, 5)
ema_20 = ta.ema(src, 20)

// Plotting
plotshape(series=crossunder(macd, signal) and ema_5 < ema_20, title="Down Signal", location=location.belowbar, color=color.red, style=shape.triangledown, size=size.small)
plotshape(series=crossover(macd, signal) and ema_5 > ema_20, title="Up Signal", location=location.abovebar, color=color.blue, style=shape.triangleup, size=size.small)

// Histogram
hline(0, "Zero Line")
fill(histogram > 0 ? histogram : na, col_grow_above, title="Above Grow")
fill(histogram < 0 ? histogram : na, col_fall, title="Fall")

```