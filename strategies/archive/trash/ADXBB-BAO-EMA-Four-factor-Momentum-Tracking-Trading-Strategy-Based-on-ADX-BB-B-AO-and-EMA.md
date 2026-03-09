``` pinescript
/*backtest
start: 2022-12-04 00:00:00
end: 2023-12-10 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4

//ADX + BB %B + AO + EMA

strategy("Four-factor Momentum Tracking Strategy", overlay=true, initial_capital=10000)
take_profit_perc = input(title="Take Profit %", type=input.integer, defval=10, minval=1, maxval=100)
stop_loss_perc = input(title="Stop Loss %", type=input.integer, defval=5, minval=1, maxval=100)
bb_overbought = input(title="BB %B Overbought", type=input.float, defval=75)
bb_oversold = input(title="BB %B Oversold", type=input.float, defval=25)
ao_value = input(title="Awesome Oscillator", type=input.integer, defval=2)
adx_value = input(title="ADX", type=input.integer, defval=15)
start_date = input(title="Start Date", type=input.string, defval="true")
start_month = input(title="Start Month", type=input.string, defval="true")
start_year = input(title="Start Year", type=input.float, defval=2018)
length = input(title="Length", type=input.integer, defval=20)
close_source = input(title="Close Source", type=input.source, defval=0)
std_dev = input(title="StdDev", type=input.integer, defval=2)
adx_smoothing = input(title="ADX Smoothing", type=input.integer, defval=14)
di_length = input(title="DI Length", type=input.integer, defval=14)

// Calculate ADX
[adx, adx_pos, adx_neg] = adx(close_source, length, adx_smoothing)

// Calculate BB %B and Bollinger Bands
bbands = ta.bbands(close_source, length, std_dev)
bb_percent_b = (close_source - bbands[2]) / (bbands[1] - bbands[2])

// Calculate Awesome Oscillator
ao = ao_value

// Long Entry Condition
long_entry_condition = ta.crossover(adx_pos, adx_neg) and 
                       ta.crossover(close_source, ema(close_source, 50)) and 
                       ta.crossover(close_source, ema(close_source, 200)) and 
                       bb_percent_b > bb_overbought and 
                       ao > 0 and 
                       adx >= adx_value

// Short Entry Condition
short_entry_condition = ta.crossunder(adx_neg, adx_pos) and 
                        ta.crossunder(close_source, ema(close_source, 50)) and 
                        ta.crossunder(close_source, ema(close_source, 200)) and 
                        bb_percent_b < bb_oversold and 
                        ao < 0 and 
                       adx >= adx_value

// Set Take Profit and Stop Loss
take_profit = close * (1 + take_profit_perc / 100)
stop_loss = close * (1 - stop_loss_perc / 100)

// Place Orders
if (long_entry_condition)
    strategy.entry("Long", strategy.long, when=bar_index > ta.time(start_year, start_month, start_date))
    
if (short_entry_condition) 
    strategy.entry("Short", strategy.short, when=bar_index > ta.time(start_year, start_month, start_date))

// Manage Stop Loss and Take Profit
strategy.exit("Take Profit Long", "Long", limit=take_profit)
strategy.exit("Stop Loss Long", "Long", stop=stop_loss)

strategy.exit("Take Profit Short", "Short", limit=ta.lowest(low, length))
strategy.exit("Stop Loss Short", "Short", stop=ta.highest(high, length))

```

This script implements the described four-factor momentum tracking strategy using Pine Script. It includes the necessary indicators and logic to determine entry and exit conditions based on ADX, BB %B, Awesome Oscillator (AO), and Exponential Moving Averages (EMA). The take profit and stop loss percentages are set as inputs for flexibility.