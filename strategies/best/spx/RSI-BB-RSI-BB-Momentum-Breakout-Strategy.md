> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|50|length|
|v_input_2|0.2|Mult Factor|
|v_input_3|0.1|alertLevel|
|v_input_4|0.75|impulseLevel|
|v_input_5|false|showRange|
|v_input_6|250|TP|
|v_input_7|20|SL|
|v_input_8|false|TS|


> Source (PineScript)

```pinescript
//@version=4
// Based on Larry Connors RSI-2 Strategy - Lower RSI
strategy(title="RSI-BB Momentum Breakout Strategy", shorttitle="RSIBBMBS")

length = input(50, title="length")
mult_factor = input(0.2, title="Mult Factor")
alert_level = input(0.1, title="alertLevel")
impulse_level = input(0.75, title="impulseLevel")
show_range = input(false, title="showRange")
take_profit = input(250, title="TP")
stop_loss = input(20, title="SL")
trade_stop = input(false, title="TS")

// RSI Calculation
up = rma(max(change(close), 0), length)
down = rma(-min(change(close), 0), length)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Bollinger Bands Calculation
basis = sma(close, length)
dev = mult_factor * stdev(close, length) 
upper = basis + dev
lower = basis - dev

bbr = close > upper ? 1 : close < lower ? -1 : 0
bbi = bbr - bbr[1]

// Strategy Logic
long_condition = rsi > 52 and rsi < 65 and bbi > alert_level and bbi < impulse_level
short_condition = rsi < 48 and rsi > 35 and bbi < -alert_level and bbi > -impulse_level

if (long_condition)
    strategy.entry("Long", strategy.long)

if (short_condition)
    strategy.entry("Short", strategy.short)

// Optional: Show RSI and BBI
if (show_range)
    plot(rsi, color=color.blue, title="RSI")
    plot(bbi, color=color.red, title="BBI")
```

This Pine Script defines the `RSI-BB Momentum Breakout Strategy` with customizable parameters for RSI length, mult_factor, alertLevel, impulseLevel, and optional range visualization.