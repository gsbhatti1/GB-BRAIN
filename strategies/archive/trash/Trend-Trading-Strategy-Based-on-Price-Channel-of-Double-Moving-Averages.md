> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|From Day|
|v_input_2|6|From Month|
|v_input_3|2020|From Year|
|v_input_4|true|To Day|
|v_input_5|12|To Month|
|v_input_6|2020|To Year|
|v_input_7|34|High Low PAC channel Length|
|v_input_8|89|fastEMAlength|
|v_input_9|200|mediumEMAlength|
|v_input_10|600|slowEMAlength|
|v_input_11|false|ShowFastEMA|
|v_input_12|false|ShowMediumEMA|
|v_input_13|false|ShowSlowEMA|
|v_input_14|false|ShowHHLL|
|v_input_15|false|ShowFractals|
|v_input_16|false|Show Ideal Fractals Only|
|v_input_17|true|Show coloured Bars around PAC|
|v_input_18|false|Show Buy/Sell Alert Arrows|
|v_input_19|3|Pullback Lookback for PAC Cross Check|
|v_input_20|false|Show Alert Arrows Only on Closed Candles|
|v_input_21|true|ShowTrendBGcolor|
|v_input_22|false|Use Heikin Ashi Candles in Algo Calculations|
|v_input_23|0.1|Trail Long Loss (%)|
|v_input_24|0.1|Trail Short Loss (%)|
|v_input_25|14|ATR Range|
|v_input_26|2|* ATR Buy SL|
|v_input_27|true|* ATR Sell SL|
|v_input_28|true|* ATR TP1|
|v_input_29|0.5| move to entry in % towards target|
|v_input_30|true|Show Move to Entry points|
|v_input_31|0.0032|tp|
|v_input_32|0.001|sl|


> Source (PineScript)

```pinescript
//@version=5
strategy("Trend-Trading-Strategy-Based-on-Price-Channel-of-Double-Moving-Averages", overlay=true)

from_day = input(true, title="From Day")
from_month = input(6, title="From Month")
from_year = input(2020, title="From Year")
to_day = input(true, title="To Day")
to_month = input(12, title="To Month")
to_year = input(2020, title="To Year")
pchannel_length = input(34, title="High Low PAC channel Length")
fast_ema_length = input(89, title="fastEMAlength")
medium_ema_length = input(200, title="mediumEMAlength")
slow_ema_length = input(600, title="slowEMAlength")
show_fast_ema = input(false, title="ShowFastEMA")
show_medium_ema = input(false, title="ShowMediumEMA")
show_slow_ema = input(false, title="ShowSlowEMA")
show_hhll = input(false, title="ShowHHLL")
show_fractals = input(false, title="ShowFractals")
show_ideal_fractals_only = input(false, title="Show Ideal Fractals Only")
show_pac_colored_bars = input(true, title="Show coloured Bars around PAC")
show_buy_sell_alert_arrows = input(false, title="Show Buy/Sell Alert Arrows")
pullback_lookback = input(3, title="Pullback Lookback for PAC Cross Check")
show_alert_arrows_only_on_closed_candles = input(false, title="Show Alert Arrows Only on Closed Candles")
show_trend_bgcolor = input(true, title="ShowTrendBGcolor")
use_heikin_ashi_candles = input(false, title="Use Heikin Ashi Candles in Algo Calculations")
trail_long_loss = input(0.1, title="Trail Long Loss (%)")
trail_short_loss = input(0.1, title="Trail Short Loss (%)")
atr_range = input(14, title="ATR Range")
atr_buy_sl = input(2, title="* ATR Buy SL")
atr_sell_sl = input(true, title="* ATR Sell SL")
atr_tp1 = input(true, title="* ATR TP1")
move_to_entry_percentage = input(0.5, title="move to entry in % towards target")
show_move_to_entry_points = input(true, title="Show Move to Entry points")
tp = input(0.0032, title="tp")
sl = input(0.001, title="sl")

// Calculate EMA
fast_ema = ta.ema(close, fast_ema_length)
medium_ema = ta.ema(close, medium_ema_length)
slow_ema = ta.ema(close, slow_ema_length)

// Calculate ATR
atr_value = ta.atr(atr_range)

// Define upper and lower rail
upper_rail = ta.ema(high, pchannel_length)
lower_rail = ta.ema(low, pchannel_length)

// Determine trend direction
trend_direction = ta.crossover(fast_ema, medium_ema) and close < lower_rail ? 1 : na
trend_direction := ta.crossunder(fast_ema, medium_ema) and close > upper_rail ? -1 : trend_direction

// Trail stop loss
long_stop_loss = na
short_stop_loss = na
if (trend_direction == 1)
    long_stop_loss := ta.valuewhen(trend_direction == 1 and close > (fast_ema + (fast_ema * trail_long_loss / 100)), fast_ema, 1)
if (trend_direction == -1)
    short_stop_loss := ta.valuewhen(trend_direction == -1 and close < (fast_ema - (fast_ema * trail_short_loss / 100)), fast_ema, 1)

// Enter trades
if (trend_direction == 1)
    strategy.entry("Long", strategy.long, when=trend_direction == 1, comment="Long entry")
    strategy.exit("Long Exit", "Long", stop=long_stop_loss, limit=long_stop_loss + (fast_ema * atr_buy_sl / 100), when=trend_direction != 1)
if (trend_direction == -1)
    strategy.entry("Short", strategy.short, when=trend_direction == -1, comment="Short entry")
    strategy.exit("Short Exit", "Short", stop=short_stop_loss, limit=short_stop_loss - (fast_ema * atr_sell_sl / 100), when=trend_direction != -1)

// Plot indicators
plot(trend_direction == 1 ? fast_ema : na, title="Fast EMA", color=color.green, linewidth=2)
plot(trend_direction == -1 ? fast_ema : na, title="Fast EMA", color=color.red, linewidth=2)
plot(medium_ema, title="Medium EMA", color=color.blue, linewidth=1)
plot(slow_ema, title="Slow EMA", color=color.orange, linewidth=1)
plot(upper_rail, title="Upper Rail", color=color.red, linewidth=2)
plot(lower_rail, title="Lower Rail", color=color.green, linewidth=2)
plot(tp, title="Take Profit", color=color.blue, linewidth=1)
plot(sl, title="Stop Loss", color=color.red, linewidth=1)
```