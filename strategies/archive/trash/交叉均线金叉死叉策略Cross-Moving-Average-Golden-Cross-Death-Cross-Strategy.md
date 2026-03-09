```pinescript
/*backtest
start: 2022-11-28 00:00:00
end: 2023-12-04 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © mdeous

//@version=4
strategy(
     title="Ichimoku Kinko Hyo Strategy", 
     shorttitle="Ichimoku Strategy", 
     overlay=true,
     pyramiding=0,
     defaul
```pinescript
    default = false
)

// Input arguments
var int tenkan_len = input(9, title="Tenkan-Sen Length")
var int kijun_len = input(26, title="Kijun-Sen Length")
var int senkou_b_len = input(52, title="Senkou Span B Length")
var int chikou_offset = input(26, title="Offset For Chikou Span / Kumo")
var bool use_imperfect_chikou = input(false, title="Use Imperfect Chikou Position Detection")

// Moving averages
src = close
tenkan_sen = sma(src, tenkan_len)
kijun_sen = sma(src, kijun_len)
senkou_a = (tenkan_sen + kijun_sen) / 2
senkou_b = sma(src, senkou_b_len)

// Chikou Span
chikou_span = plot(close[1], title="Chikou Span", style=line, color=color.red, linewidth=1)
chikou_condition = crossover(tenkan_sen, kijun_sen) or crossunder(tenkan_sen, kijun_sen)

// Signal generation
var float buy_price = na
var bool long_position = false

if (chikou_condition and not use_imperfect_chikou or chikou_span[1] < close)
    if (not long_position and barstate.islast)
        strategy.entry("Buy", strategy.long, when=chikou_condition)
        buy_price := close
        long_position := true
    else if (long_position and barstate.islast)
        strategy.exit("Close Long Position", from_entry="Buy")
        long_position := false

// Plotting Kumo bands
plot(senkou_a, title="Senkou Span A", style=area, color=color.blue, transp=100)
plot(senkou_b, title="Senkou Span B", style=area, color=color.blue, transp=50)

// Stop loss and cooldown period
if (long_position)
    strategy.exit("Stop Loss", from_entry="Buy", stop=buy_price * 0.95) // 5% stop loss

// Order cooldown mechanism
var int order_cooldown = input(5, title="Orders Cooldown Period")
var bool can_trade = true

if barstate.islast and order_cooldown > 0
    if not use_imperfect_chikou or chikou_span[1] < close
        can_trade := false
    else
        order_cooldown := order_cooldown - 1
        can_trade := order_cooldown <= 0

if (can_trade)
    strategy.close("Close Long Position")

plotshape(series=chikou_condition, location=location.belowbar, color=color.red, style=shape.triangleup, title="Buy Signal", size=size.small)

```