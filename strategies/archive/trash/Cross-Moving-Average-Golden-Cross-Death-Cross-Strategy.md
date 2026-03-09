> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Tenkan-Sen Length|
|v_input_2|26|Kijun-Sen Length|
|v_input_3|52|Senkou Span B Length|
|v_input_4|26|Offset For Chikou Span / Kumo|
|v_input_5|5|Orders Cooldown Period|
|v_input_6|false|Use Imperfect Chikou Position Detection|


> Source (PineScript)

``` pinescript
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
     defaultlong=false,
     calc_on_every bar_close=true
)

// Input parameters
tenkan_length = input(9, title="Tenkan-Sen Length")
kijun_length = input(26, title="Kijun-Sen Length")
senkou_b_length = input(52, title="Senkou Span B Length")
chikou_offset = input(26, title="Offset For Chikou Span / Kumo")
cooldown_period = input(5, title="Orders Cooldown Period")
use_imperfect_chikou = input(false, title="Use Imperfect Chikou Position Detection")

// Calculate Tenkan-Sen (9-period EMA)
tenkan_sen = sma(close, tenkan_length)

// Calculate Kijun-Sen (26-period EMA)
kijun_sen = sma(close, kijun_length)

// Calculate Senkou Span A (52-period EMA)
senkou_a = sma(close, senkou_b_length)

// Calculate Senkou Span B
senkou_b = (tenkan_sen + kijun_sen) / 2

// Plot Senkou Spans as Cloud Bands
plot(senkou_a, color=color.blue, title="Senkou A")
plot(senkou_b, color=color.red, title="Senkou B")

// Calculate Chikou Span (26-period price shift)
chikou_span = na(chikou_offset) ? close[1] : close

// Plot Chikou Span
plot(chikou_span, color=color.orange, style=plot.style_square, title="Chikou Span")

// Generate Buy Signal: Tenkan-Sen crosses above Kijun-Sen with cooldown period
buy_signal = crossover(tenkan_sen, kijun_sen) and not crossover(tenkan_sen, kijun_sen)[cooldown_period]
if (buy_signal)
    strategy.entry("Buy", strategy.long)

// Generate Sell Signal: Tenkan-Sen crosses below Kijun-Sen with cooldown period
sell_signal = crossunder(tenkan_sen, kijun_sen) and not crossunder(tenkan_sen, kijun_sen)[cooldown_period]
if (sell_signal)
    strategy.close("Buy")

// Optional: Use imperfect Chikou position detection
if (use_imperfect_chikou)
    // Code for handling imperfect Chikou position could go here

// Optional: Stop loss mechanism can be added here
```