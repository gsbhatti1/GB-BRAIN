``` pinescript
/*backtest
start: 2022-04-11 00:00:00
end: 2022-05-10 23:59:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// Source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/ - © José Manuel Gassin Pérez-Traverso
// Credit for each indicator belongs to its author.

//@version=5
indicator(title="HALFTREND + HEMA + SMA (FALSE SIGNAL)", shorttitle="HALFTREND + HEMA + SMA (FALSE SIGNAL)", overlay=true)


//== Constants
c_black               = color.rgb(0, 0, 0, 0)
c_green_radioactive   = color.rgb(0, 255, 0, 0)
c_green               = color.rgb(0, 128, 0, 0)
c_dark_green          = color.rgb(0, 80, 0, 0)
c_red_radioactive     = color.rgb(255, 0, 0, 0)
c_red                 = color.rgb(128, 0, 0, 0)
c_dark_red            = color.rgb(80, 0, 0, 0)
c_red_t               = color.new(color.red, 90)
c_yellow              = color.rgb(255, 255, 0, 0)
none_color            = color.new(color.white, 100)


//== Strategy
strategy_group = "Strategy"
ema_filter = input.bool(title="Full candle must be outside the EMA / Wicks can touch the EMA but body must be out", defval=false, group=strategy_group)

//== Simple Moving Average (SMA)
sma_group = "Simple Moving Average (SMA)"
sma_length = input.int(150, minval=1, title="Length", group=sma_group)
sma_source = input(close, title="Source", group=sma_group)
sma_offset = input.int(title="Offset", defval=6, minval=-500, maxval=500, group=sma_group)
sma = ta.sma(sma_source, sma_length)


//== Hull Moving Average (HEMA) - Source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/ - © alexgrover
hma_group = "Hull Moving Average (HEMA)"
hma_length = input.int(title="Length", defval=50, minval=1, group=hma_group)
hma = 3 * ta.wma(close, hma_length / 2) - 2 * ta.ema(close, hma_length / 2)


//== HALFTREND - Copyright (c) 2021-present, Alex Orekhov (everget)
ht_group = "Halftrend"
amplitude = input(title='Amplitude', defval=1, group=ht_group)
channel_deviation = input(title='Channel Deviation', defval=2, group=ht_group)
show_arrows = input(title='Show Arrows', defval=true, group=ht_group)
show_channels = input(title='Show Channels', defval=false, group=ht_group)

var int trend_state = 0
var int next_trend_state = 0
var float max_low_price = na
var float min_high_price = na

var float upper_band = 0.0
var float lower_band = 0.0
float atr_high = 0.0
float atr_low = 0.0
float arrow_up = na
float arrow_down = na

atr2 = ta.atr(100) / 2
deviation = channel_deviation * atr2

high_price = high[max(0, abs(ta.highestbars(amplitude))) - 1]
low_price = low[max(0, abs(ta.lowestbars(amplitude))) - 1]
high_ma = ta.sma(high, amplitude)
low_ma = ta.sma(low, amplitude)

if next_trend_state == 1
    max_low_price := math.max(low_price, max_low_price)

    if high_ma < max_low_price and close < low[1]
        trend_state := 1
        next_trend_state := 0
        min_high_price := high_price
else
    min_high_price := math.min(high_price, min_high_price)

    if low_ma > min_high_price and close > high[1]
        trend_state := 0
        next_trend_state := 1
        max_low_price := low_price

if trend_state == 0
    if not na(trend_state[1]) and trend_state[1] != 0
        lower_band := na(lower_band[1]) ? lower_band : lower_band[1]
        arrow_down := lower_band - atr2
        arrow_down
    else
        lower_band := na(lower_band[1]) ? max_low_price : math.max(max_low_price, lower_band[1])
        lower_band
    atr_low := lower_band + deviation
else
    if not na(trend_state[1]) and
```