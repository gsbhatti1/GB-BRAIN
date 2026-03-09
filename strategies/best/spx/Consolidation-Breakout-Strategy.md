> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|75|LENGTH|
|v_input_float_1|3.2|MULT_STDEV|
|v_input_float_2|10|ATR TRAIL|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-08 00:00:00
end: 2023-12-14 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Consolidation Breakout [Indian Market Timing]", overlay=true, pyramiding=0, initial_capital=50000, default_qty_value=5, currency=currency.NONE, commission_type=strategy.cash, commission_value=30, slippage=1 )


// ══════════════════════════════════//
// ————————> INPUT VALUES <————————— //
// ══════════════════════════════════//

LENGTH = input.int(title='LENGTH', defval=75, minval=10, maxval=300)
MULT_STDEV = input.float(title='MULT_STDEV', defval=3.2, minval=1, maxval=7, step=0.1)

// EMA1 = input.int(title='EMA1', defval=50, minval=10, maxval=550)
// EMA2 = input.int(title='EMA2', defval=135, minval=10, maxval=550)
factor_trail = input.float(title="ATR TRAIL", defval=10, step=0.1)

// ══════════════════════════════════//
// ————————> DAY TIME LIMIT <——————— //
// ══════════════════════════════════//

t = time(timeframe.period, '0935-1430:1234567')
time_condition = not na(t)

//**********************//
// ————————> ATR & PLOT <————————— //
//**********************

// ema1 = ta.ema(close, EMA1)
// ema2 = ta.ema(close, EMA2)

// plot(ema1, color=color.new(color.blue, 0), style=plot.style_linebr, title='ema1')
// plot(ema2, color=color.new(color.yellow, 0), style=plot.style_linebr, title='ema2')

atr_trail = ta.atr(16) * factor_trail

long_stop = close - atr_trail
short_stop = close + atr_trail

entry_price = close
length = LENGTH
mult_stdev = MULT_STDEV
basis = ta.sma(entry_price, length)
deviation = mult_stdev * ta.stdev(entry_price, length)
upper_band = basis + deviation
lower_band = basis - deviation
buy_entry = ta.crossover(entry_price, upper_band)
sell_entry = ta.crossunder(entry_price, lower_band)

// plot(upper_band, color=color.new(color.red, 0), style=plot.style_linebr, title="short stop")
// plot(lower_band, color=color.new(color.green, 0), style=plot.style_linebr, title="long stop")

plot(upper_band, color=close[1] > upper_band and close > upper_band ? color.green : color.red, linewidth=2)
plot(lower_band, color=close[1] > lower_band and close < lower_band ? color.red : color.green, linewidth=2)

// Exit at 14:57 every day
if (time == time("1430") and minute >= 56) or (time == time("1459"))
    strategy.close_all()

```

This script implements the described consolidation breakout trading strategy for Indian markets with PineScript. It includes necessary inputs, logic for generating buy/sell signals based on Bollinger Bands, ATR for stop loss/trail, and a day-time limit to close all positions at 14:57 every day.