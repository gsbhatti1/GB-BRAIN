``` pinescript
/*backtest
start: 2022-12-04 00:00:00
end: 2023-12-10 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA and SuperTrend Combined Trend Following Strategy", overlay=true)

// Input Parameters for SuperTrend
length = input.int(10, title="SuperTrend Length")
multiplier = input.float(2.0, title="Multiplier")

// Input Parameters for EMA
ema_length_up = input.int(34, title="EMA UpTrend")
ema_length_down = input.int(34, title="EMA DownTrend")
show_ema_trend_based_on = input.bool(true, title="Show EMA Trend is Based On?")

// SuperTrend Calculation
[supertrend_directional, supertrend] = superTrend(length, multiplier)

// EMA Calculation
ema_up = ta.ema(close, ema_length_up)
ema_down = ta.ema(close, ema_length_down)

// Buy Signal: Price above Supertrend and above EMA
long_condition = close > supertrend and close > ema_up

// Sell Signal: Price below Supertrend and below EMA
short_condition = close < supertrend and close < ema_down

// Close Long Position: Price below Supertrend or below EMA
close_long = close < supertrend or close < ema_up

// Close Short Position: Price above Supertrend or above EMA
close_short = close > supertrend or close > ema_down

// Plotting
plot(supertrend, title="SuperTrend", color=color.blue)
plot(ema_up, title="EMA UpTrend", color=color.green)
plot(ema_down, title="EMA DownTrend", color=color.red)

if (long_condition)
    strategy.entry("Long", strategy.long)

if (short_condition)
    strategy.entry("Short", strategy.short)

if (close_long or close_short)
    strategy.close("Long")
    strategy.close("Short")

// Show EMA Trend
if (show_ema_trend_based_on)
    plotshape(series=long_condition, title="Buy Signal", location=location.belowbar, color=color.green, style=shape.labelup, text="BUY")
    plotshape(series=short_condition, title="Sell Signal", location=location.abovebar, color=color.red, style=shape.labeldown, text="SELL")

```

```