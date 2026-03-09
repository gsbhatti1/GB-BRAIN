> Name

Directional-Movement-Index-DMI-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

This strategy implements trend trading based on the Directional Movement Index (DMI). DMI consists of three lines: ADX, +DI, and -DI. ADX shows trend strength; values above a given threshold indicate a trend. +DI and -DI represent upward and downward trend strengths respectively. Go long when +DI crosses above -DI, and short when -DI crosses above +DI.

## Strategy Logic

Calculate the ADX, +DI, and -DI lines. Set a reasonable threshold for ADX to determine if a trend is present, such as 25. When ADX is above this level, if +DI is greater than -DI, an upward trend is identified, go long. If -DI is greater than +DI, a downward trend is identified, go short. Hold the position until a reverse signal appears.

## Advantage Analysis

- DMI accurately identifies trend direction with fewer signals.
- ADX filters insignificant breakouts to avoid meaningless trades.
- Trading in trend direction avoids whipsaws.
- Large parameter tuning space—ADX threshold, DI period, etc.

## Risk Analysis

- Trend reversal can lead to losses.
- ADX has lag in determining trend strength.
- Long holding periods increase drawdown risk.

Mitigate by shortening holding period or adding other indicators to determine trend reversal.

## Optimization Directions

- Optimize ADX parameters to balance responsiveness and noise filtering.
- Test impact of different holding period settings.
- Consider adding moving averages etc. to identify trend reversal.
- Test robustness across different products.

## Conclusion

DMI strategy accurately determines trend direction with controlled drawdown. Further improvements possible through parameter optimization. A simple and practical trend following strategy.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_int_1|14|ADX Smoothing|
|v_input_int_2|7|DI Length|
|v_input_int_3|25|Consolidation ADX|
|v_input_1|timestamp(2017-01-01T00:00:00)|(?Trading Settings)Testing Start Date|
|v_input_2|timestamp(2025-01-01T00:00:00)|Testing End Date|
|v_input_color_1|teal|(?Signals Style - Setting)Long Entry|
|v_input_color_2|purple|Long Exit|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-09-10 00:00:00
end: 2023-09-17 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// ©wojak_bogdanoff
// @version=5
// Directional Movement Index (DMI)

strategy(title="Directional Movement Index", shorttitle="DMI", overlay=true, pyramiding=1, calc_on_every_tick=false, calc_on_order_fills=false, initial_capital=100.0, default_qty_type=strategy.percent_of_equity, default_qty_value=100.0, commission_type=strategy.commission.percent, commission_value=0.1, slippage=1)

trade_type = 'Long' // input.string(defval="Long", title="Position Type", options=["Both", "Long", "Short"], group='Trading Settings')
strategy_type = 'DMI' // input.string(defval="ECS", title="Strategy Type", options=['DMI'], group='Trading Settings')

start_date  = input(title='Testing Start Date', defval=timestamp("2017-01-01T00:00:00"), group='Trading Settings')
finish_date = input(title='Testing End Date', defval=timestamp("2025-01-01T00:00:00"), group='Trading Settings')

_testperiod = true
_check = _testperiod

// --- (Start) Directional Movement Index (DMI) ----------------------------- //

dmi_adxSmoothing = input.int(14, title="ADX Smoothing", minval=1, maxval=50)
dmi_len = input.int(7, minval=1, title="DI Length")
dmi_up = ta.change(high)
dmi_down = -ta.change(low)
dmi_plusDM = na(dmi_up) ? na : (dmi_up > dmi_down and dmi_up > 0 ? dmi_up : 0)
dmi_minusDM = na(dmi_down) ? na : (dmi_down > dmi_up and dmi_down > 0 ? dmi_down : 0)
dmi_rma = ta.rma(ta.tr, dmi_len)
dmi_plus = fixnan(100 * ta.rma(dmi_plusDM, dmi_len) / dmi_rma)
dmi_minus = fixnan(100 * ta.rma(dmi_minusDM, dmi_len) / dmi_rma)
dmi_sum = dmi_plus + dmi_minus
dmi_adx = 100 * ta.rma(math.abs(dmi_plus - dmi_minus) / (dmi_sum == 0 ? 1 : dmi_sum), dmi_adxSmoothing)

plot(dmi_adx, color=#F50057, title="ADX")
plot(dmi_plus, color=#2962FF, title="+DI")
plot(dmi_minus, color=#FF6D00, title="-DI")

dmi_consld_limit=input.int(defval=25, title='Consolidation ADX')
dmi_consld=dmi_adx<=dmi_consld_limit
dmi_strong_up=dmi_adx>dmi_consld_limit and dmi_plus>dmi_minus
dmi_strong_down=dmi_adx>dmi_consld_limit and dmi_plus<dmi_minus

barcolor(dmi_consld ? color.new(color.black,0) : na, title='Consolidation region', display=display.none)
barcolor(dmi_strong_up ? color.new(color.green,0) : na, title='Uptrend Region')
barcolor(dmi_strong_down ? color.new(color.red,0) : na, title='Downtrend Region')

dmi_long_e = (not dmi_strong_up[1]) and dmi_strong_up[0]
dmi_long_x = dmi_strong_up[1] and (not dmi_strong_up[0])

dmi_short_e = dmi_strong_up[1] and (not dmi_strong_up[0])
dmi_short_x = (not dmi_strong_up[1]) and dmi_strong_up[0]

// --- (End) Directional Movement Index (DMI) ------------------------------- //

// --- Trade Conditions ----------------------------------------------------- //

var is_long_open=false, var is_short_open=false

long_e = strategy_type == "DMI" ? dmi_long_e : na
long_x = strategy_type == "DMI"
```