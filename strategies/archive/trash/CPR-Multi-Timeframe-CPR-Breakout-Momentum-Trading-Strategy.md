``` pinescript
//@version=5
strategy("Ahmad Ali Khan CPR Strategy", overlay=true, margin_long=100, margin_short=100)

// ———— Inputs ————
use_daily_cpr = input.bool(true, "Use Daily CPR Levels")
ema_length = input.int(20, "EMA Trend Filter Length")
show_week_open = input.bool(true, "Show Weekly Open Price")
enable_divergence = input.bool(true, "Enable RSI Divergence Check")

// ———— Daily CPR Calculation ————
daily_high = request.security(syminfo.tickerid, "D", high[1], lookahead=barmerge.lookahead_on)
daily_low = request.security(syminfo.tickerid, "D", low[1], lookahead=barmerge.lookahead_on)
daily_close = request.security(syminfo.tickerid, "D", close[1], lookahead=barmerge.lookahead_on)

pivot = (daily_high + daily_low + daily_close) / 3
bc = (daily_high + daily_low) / 2
tc = pivot + (pivot - bc)

// ———— Weekly Open Price ————
weekly_open = request.security(syminfo.tickerid, "W", open, lookahead=barmerge.lookahead_on)

// ———— Trend Analysis ————
ema_trend = ta.ema(close, ema_length)
market_phase = close > ema_trend ? "Bullish" : "Bearish"

// ———— Momentum Confirmation ————
rsi_length = 14
rsi = ta.rsi(close, rsi_length)
bullish_div = ta.valuewhen(ta.crossover(rsi, 30), low, 0) > ta.valuewhen(ta.crossover(rsi, 30), low, 1)
bearish_div = ta.valuewhen(ta.crossunder(rsi, 70), high, 0) < ta.valuewhen(ta.crossunder(rsi, 70), high, 1)

// ———— Plotting ————
// CPR Levels
plot(pivot, "Pivot", color=color.blue, linewidth=2)
plot(bc, "Bottom Central", color=color.green, linewidth=2)
plot(tc, "Top Central", color=color.red, linewidth=2)
plot(weekly_open, "Weekly Open", color=color.orange, linewidth=2)
plot(ema_trend, "EMA", color=color.purple, linewidth=2)

// ———— Trade Conditions ————
long_condition = use_daily_cpr and market_phase == "Bullish" and close > tc and volume > ta.avg(volume[1..20]) and not bullish_div
short_condition = use_daily_cpr and market_phase == "Bearish" and close < bc and volume > ta.avg(volume[1..20]) and not bearish_div

// ———— Trade Execution ————
if (long_condition)
    strategy.entry("Long", strategy.long)
if (short_condition)
    strategy.entry("Short", strategy.short)

// ———— Risk Management ————
stop_loss = use_daily_cpr and market_phase == "Bullish" ? tc - (tc - bc) : bc - (tc - bc)
strategy.exit("Long Exit", from_entry="Long", stop=stop_loss)
strategy.exit("Short Exit", from_entry="Short", stop=stop_loss)

// ———— Additional Filters ————
if (enable_divergence)
    if (market_phase == "Bullish" and bullish_div)
        strategy.entry("Short", strategy.short)
    if (market_phase == "Bearish" and bearish_div)
        strategy.entry("Long", strategy.long)
```

This Pine Script implements the described strategy with the necessary inputs, calculations, and trade logic. The script includes plotting of CPR levels, weekly open price, EMA, and trade entries based on the defined conditions.