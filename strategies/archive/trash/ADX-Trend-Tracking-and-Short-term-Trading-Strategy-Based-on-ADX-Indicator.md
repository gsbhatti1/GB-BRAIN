``` pinescript
/*backtest
start: 2023-01-15 00:00:00
end: 2024-01-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Trend-Tracking-and-Short-term-Trading-Strategy-Based-on-ADX-Indicator", overlay = true)

///////////////////////////
// SuperTrend + Pivot Point
//////////////////////////

src = input(close, title="EMA Source")
pivot_period = input(2, title="Pivot Point Period")
atr_factor = input(2, title="ATR Factor")
atr_period = input(21, title="ATR Period")
start_date = input(timestamp("20231201"), title="Start Date")
end_date = input(timestamp("20240112"), title="End Date")
rsi_source = input(close, title="Source")
rsi_overSold = input(30, title="OverSold")
rsi_overBought = input(65, title="OverBought")

var float pivot_high = na
var float pivot_low = na
var float pivot_price = na
var float pivot_time = na

// Calculate Pivot Points
pivot_time := ta.bar_index
pivot_price := (ta.highest(high, pivot_period) + ta.lowest(low, pivot_period)) / 2

if (ta.bar_index - pivot_time) % pivot_period == 0
    pivot_high := ta.highest(high, pivot_period)
    pivot_low := ta.lowest(low, pivot_period)
    pivot_price := (pivot_high + pivot_low) / 2
    pivot_time := ta.bar_index

// Calculate ATR
atr = ta.atr(atr_period)

// Calculate SuperTrend
up = (pivot_high - (atr_factor * atr)) < src ? (pivot_high - (atr_factor * atr)) : src
down = (pivot_low + (atr_factor * atr)) > src ? (pivot_low + (atr_factor * atr)) : src
super_trend = up > down ? up : down

// Plot Pivot Points and SuperTrend
plot(pivot_price, color=color.blue, title="Pivot Price")
plot(super_trend, color=color.red, title="SuperTrend")

// Strategy Logic
if (time >= start_date and time <= end_date)
    // Long condition
    long_condition = super_trend < src and ta.crossover(super_trend, src)
    if long_condition
        strategy.entry("Long", strategy.long)

    // Short condition
    short_condition = super_trend > src and ta.crossunder(super_trend, src)
    if short_condition
        strategy.entry("Short", strategy.short)

    // Exit conditions
    if (time > end_date)
        strategy.close("Long")
        strategy.close("Short")
```

This script implements the described trading strategy with the specified parameters and logic. Make sure to test it thoroughly in a backtest environment before using it in a live trading scenario.