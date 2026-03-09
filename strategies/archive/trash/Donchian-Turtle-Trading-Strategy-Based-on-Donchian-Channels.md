``` pinescript
/*backtest
start: 2023-11-24 00:00:00
end: 2023-12-24 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
// Coded by Vladkos
strategy("Donchian strategy with filter", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=4, pyramiding=5)

fromyear = input(2017, defval=2018, minval=1800, maxval=2100, title="From Year")
toyear = input(2100, defval=2100, minval=1800, maxval=2100, title="To Year")
frommonth = input(1, defval=12, minval=1, maxval=12, title="From Month")
tomonth = input(12, defval=12, minval=1, maxval=12, title="To Month")
fromday = input(1, defval=21, minval=1, maxval=31, title="From day")
today = input(31, defval=31, minval=1, maxval=31, title="To day")
atr = input(20, defval=20, title="ATR")
long = input(true, defval=true, title="Long")
short = input(true, defval=true, title="Short")
stop_loss = input(true, defval=true, title="Stop LOSS")
donchian_slow = input(20, defval=20, title="Donchian slow")
donchian_fast = input(10, defval=10, title="Donchian fast")
slow_ema = input(125, defval=125, title="Slow EMA")
fast_ema = input(50, defval=50, title="Fast EMA")

// Function to get the date range
from_date = time >= timestamp(fromyear, frommonth, fromday, 0, 0, 0)
to_date = time <= timestamp(toyear, tomonth, today, 23, 59, 59)

// Donchian Channels
high_20 = highest(high, donchian_fast)
low_20 = lowest(low, donchian_fast)
high_20_20 = highest(high, donchian_slow)
low_20_20 = lowest(low, donchian_slow)

// Moving Averages
ema250 = ema(close, slow_ema)
ema50 = ema(close, fast_ema)

// Conditions for long and short positions
long_condition = close > high_20 and close > ema50 and ema250 > ema50
short_condition = close < low_20 and close < ema50 and ema250 < ema50

// Trade only within the date range
if (from_date and to_date)
    if (long and long_condition)
        strategy.entry("Long", strategy.long)
    if (short and short_condition)
        strategy.entry("Short", strategy.short)

// Stop Loss
if (stop_loss)
    stop_loss_value = atr * atr
    if (long and long_condition)
        strategy.exit("Long Exit", "Long", stop=stop_loss_value)
    if (short and short_condition)
        strategy.exit("Short Exit", "Short", stop=stop_loss_value)
```

Note: The Pine Script code has been updated to include the additional input parameters and conditions as described in the original strategy document.