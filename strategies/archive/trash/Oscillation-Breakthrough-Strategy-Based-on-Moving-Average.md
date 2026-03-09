```pinescript
/*backtest
start: 2023-01-16 00:00:00
end: 2024-01-22 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("Oscillation Breakthrough Strategy Based on Moving Average", overlay=true)

// Input Arguments
use_session = input(true, title="Use Trading Session?")
session_time = input(title="Trade Session:", defval="0800-1600")
fast_line = input(9, title="Fast (Conversion) Line")
slow_line = input(26, title="Slow (Base) Line")
ema_freq = input(2, title="Ema on price frequency")

// Define Trading Session
var session = na
if use_session
    session := session_strict(time("D", "0800-1600"), time("D", session_time))

// Calculate EMA Lines
short_ema = ema(close, fast_line)
long_ema = ema(close, slow_line)

plot(short_ema, color=color.blue, title="Short EMA")
plot(long_ema, color=color.red, title="Long EMA")

// Strategy Logic
if session and not na(short_ema) and not na(long_ema)
    if short_ema > long_ema
        strategy.entry("Buy", strategy.long)
    else if short_ema < long_ema
        strategy.close("Buy")
        strategy.entry("Sell", strategy.short)

// Plot Buy and Sell Signals
plotshape(series=strategy.opentrades[1].entry_price, location=location.belowbar, color=color.green, style=shape.labelup, title="Long Entry Signal")
plotshape(series=strategy.closedtrades[1].exit_price, location=location.abovebar, color=color.red, style=shape.labeldown, title="Short Exit Signal")

```
```