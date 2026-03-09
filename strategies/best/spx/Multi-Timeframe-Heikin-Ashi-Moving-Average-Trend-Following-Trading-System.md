``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2025-01-04 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © tradingbauhaus

//@version=5
strategy("Heikin Ashi Candle Time Frame @tradingbauhaus", shorttitle="Heikin Ashi Candle Time Frame @tradingbauhaus", overlay=true)

// Inputs
res = input.timeframe(title="Heikin Ashi Candle Time Frame", defval="60")
hshift = input.int(1, title="Heikin Ashi Candle Time Frame Shift")
res1 = input.timeframe(title="Heikin Ashi EMA Time Frame", defval="180")
mhshift = input.int(0, title="Heikin Ashi EMA Time Frame Shift")
fama = input.int(1, title="Heikin Ashi EMA Period")
test = input.int(1, title="Heikin Ashi EMA Shift")
sloma = input.int(30, title="Slow EMA Period")
slomas = input.int(1, title="Slow EMA Shift")
macdf = input.bool(false, title="With MACD filter")
res2 = input.timeframe(title="MACD Time Frame", defval="15")
macds = input.int(1, title="MACD Shift")

// Heikin Ashi calculation
var float ha_open = na
ha_close = (open + high + low + close) / 4
ha_open := na(ha_open[1]) ? (open + close) / 2 : (ha_open[1] + ha_close[1]) / 2
ha_high = math.max(high, math.max(ha_open, ha_close))
ha_low = math.min(low, math.min(ha_open, ha_close))

// Adjusted Heikin Ashi Close for different timeframes
ha_close_adj = ta.smooth(ha_close, hshift)

// Heikin Ashi EMA calculation
heikin_ashi_ema = ta.ema(ha_close_adj, fama)

// Slow EMA calculation
slow_ema = ta.ema(close, sloma)

// MACD calculation
if (macdf)
    [macd_line, signal_line, _] = ta.macd(ha_close_adj, 12, 26, macds)

// Signal generation
buy_signal = ta.crossover(heikin_ashi_ema, slow_ema)
sell_signal = ta.crossunder(heikin_ashi_ema, slow_ema)

// MACD confirmation
if (macdf)
    buy_signal := buy_signal and ta.crossover(macd_line, signal_line)
    sell_signal := sell_signal and ta.crossunder(macd_line, signal_line)

// Plot signals
plotshape(series=buy_signal, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
plotshape(series=sell_signal, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

// Strategy logic
if (buy_signal)
    strategy.entry("Buy", strategy.long)
if (sell_signal)
    strategy.close("Buy")
```

This code completes the Pine Script for the Heikin Ashi candle-based trend-following strategy with the specified input parameters and logic.