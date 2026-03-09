```pinescript
/*backtest
start: 2025-01-10 00:00:00
end: 2025-02-08 08:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("AI Bollinger Bands Strategy with SL, TP, and Bars Till Close", overlay=true)

// Input parameters
bb_length           = input.int(14, title="Bollinger Bands Length", minval=1)
bb_stddev           = input.float(1.5, title="Bollinger Bands Standard Deviation", minval=0.1)
use_ema             = input.bool(true, title="Use EMA Filter")
ema_length          = input.int(80, title="EMA Length", minval=1)
use_trailing_stop   = input.bool(true, title="Use Trailing Stop")
use_sl              = input.bool(true, title="Use Stop Loss")
use_tp              = input.bool(false, title="Use Take Profit")
sl_dollars          = input.float(300.0, title="Stop Loss (\$)", minval=0.0)
tp_dollars          = input.float(1000.0, title="Take Profit (\$)", minval=0.0)
use_bars_till_close = input.bool(true, title="Use Bars Till Close")
bars_till_close     = input.int(10, title="Bars Till Close", minval=1)
// New input to toggle indicator plotting
plot_indicators     = input.bool(true, title="Plot Bollinger Bands and EMA on Chart")

// Calculate Bollinger Bands and EMA
basis      = ta.sma(close, bb_length)
upper_band = basis + bb_stddev * ta.stdev(close, bb_length)
lower_band = basis - bb_stddev * ta.stdev(close, bb_length)
ema        = ta.ema(close, ema_length)

// Plot Bollinger Bands and EMA conditionally
plot(plot_indicators  ? basis : na, color=color.blue, linewidth=2, title="Basis (SMA)")
plot(plot_indicators ? upper_band : na, color=color.red, linewidth=2, title="Upper Band")
plot(plot_indicators  ? lower_band : na, color=color.green, linewidth=2, title="Lower Band")
plot(plot_indicators ? ema : na, color=color.orange, linewidth=2, title="EMA")

// Define conditions for entering positions
long_condition = ta.crossover(close, lower_band) and ta.up_cross(ema)
short_condition = ta.crossunder(close, upper_band) and ta.down_cross(ema)

if (use_ema and long_condition and not ta.inupcross(basis, ema))
    strategy.entry("Long", strategy.long)

if (use_ema and short_condition and not ta.indowncross(basis, ema))
    strategy.entry("Short", strategy.short)

// Trailing stop
trail_stop = use_trailing_stop ? true : false

// Stop loss and take profit
if (use_sl)
    strategy.exit("SL", "Long", stop=sl_dollars)
    strategy.exit("SL", "Short", stop=-sl_dollars)

if (use_tp)
    strategy.exit("TP", "Long", profit=tp_dollars)
    strategy.exit("TP", "Short", profit=-tp_dollars)

// Close positions based on bars till close
if (use_bars_till_close and bar_index >= bars_till_close - 1)
    strategy.close("Long")
    strategy.close("Short")

```
```