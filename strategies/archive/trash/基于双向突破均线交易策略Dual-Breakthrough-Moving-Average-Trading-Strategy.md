> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|200|MA Length|
|v_input_2|12|Fast EMA Length|
|v_input_3|26|Slow EMA Length|
|v_input_4|7|RSI Length|
|v_input_5|50|RSI Threshold|
|v_input_6|true|Long Trades|
|v_input_7|false|Short Trades|
|v_input_8|false|Quick Exits|


> Source (PineScript)

```pinescript
//@version=4
// Original Indicator by @Shizaru - simply mad

strategy("Dual-Breakthrough-Moving-Average-Trading-Strategy", overlay=true)

// Inputs
ma_length = input(200, title="MA Length")
fast_ema_length = input(12, title="Fast EMA Length")
slow_ema_length = input(26, title="Slow EMA Length")
rsi_length = input(7, title="RSI Length")
rsi_threshold = input(50, title="RSI Threshold")
long_trades = input(true, title="Long Trades", type=bool)
short_trades = input(false, title="Short Trades", type=bool)
quick_exits = input(false, title="Quick Exits", type=bool)

// Calculate indicators
ema_fast = ta.ema(close, fast_ema_length)
ema_slow = ta.ema(close, slow_ema_length)
sma = ta.sma(close, ma_length)
rsi = ta.rsi(close, rsi_length)

// Parabolic SAR
sar = ta.sar(high, low, 0.02, 0.2)

// Buy/Sell conditions
buy_condition = close > sar and close > sma and ta.macd(close, 12, 26, 9)[0] > 0 and rsi > rsi_threshold
sell_condition = close < sar and close < sma and ta.macd(close, 12, 26, 9)[0] < 0 and rsi < rsi_threshold

// Long trades
if (long_trades and buy_condition)
    strategy.entry("Buy", strategy.long)

// Short trades
if (short_trades and sell_condition)
    strategy.entry("Sell", strategy.short)

// Quick exits
if (quick_exits)
    strategy.exit("Quick Exit", "Buy")
    strategy.exit("Quick Exit", "Sell")

// Plotting
plot(sar, color=color.red, title="Parabolic SAR")
plot(sma, color=color.blue, title="SMA")
plot(rsi, color=color.orange, title="RSI")
```