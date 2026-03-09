``` pinescript
/*backtest
start: 2022-12-12 00:00:00
end: 2023-12-18 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("BCE Version of EMA, SMA Mean Reversion", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100)
 
// Inputs
st_yr_inp = input(defval=2017, title='Backtest Start Year')
st_mn_inp = input(defval=01, title='Backtest Start Month')
st_dy_inp = input(defval=01, title='Backtest Start Day')
en_yr_inp = input(defval=2025, title='Backtest End Year')
en_mn_inp = input(defval=01, title='Backtest End Month')
en_dy_inp = input(defval=01, title='Backtest End Day')
sma_lookback = input(defval=100, title="Lookback Period For SMA")
ema_lookback = input(defval=10, title="Lookback Period For EMA")
long_diff_perc = input(defval=6, title="Percentage Deviation From SMA to go Long")/100
short_diff_perc = input(defval=20, title="Percentage Deviation From SMA to go Short")/100
ema_filter_bars = input(defval=4, title="The number of bars the EMA must rise/fall")
lng_allwd = input(defval=true, title="Allow Longs?")
srt_allwd = input(defval=true, title="Allow Shorts?")
use_stop = input(defval=true, title="Use Stoploss?")
stop_perc = input(defval=30, title="Stop Loss Percentage")/100
 
// Dates
start = timestamp(st_yr_inp, st_mn_inp, st_dy_inp,00,00)
end = timestamp(en_yr_inp, en_mn_inp, en_dy_inp,00,00)
can_trade = time >= start and time <= end
// Indicators Setup
sma = sma(close, sma_lookback)
ema = ema(close, ema_lookback)
 
// Strategy Calcuations
close_stdev = stdev(close, sma_lookback)
sd1_upper = close + (close_stdev * 1.0) // Complete the calculation for upper Bollinger Band
sd1_lower = close - (close_stdev * 1.0) // Complete the calculation for lower Bollinger Band

// Long Entry Conditions
long_entry = can_trade and ema > sma and ema[ema_filter_bars] < sma and rank(rank(close)) < long_diff_perc * 100
if (lng_allwd)
    strategy.entry("Long", strategy.long, when=long_entry)

// Short Entry Conditions
short_entry = can_trade and ema < sma and ema[ema_filter_bars] > sma and rank(rank(close)) > (100 - short_diff_perc * 100)
if (srt_allwd) 
    strategy.entry("Short", strategy.short, when=short_entry)

// Stop Loss
if (use_stop)
    stop_price = can_trade ? close : na
    if (lng_allwd and long_entry)
        strategy.exit("Long Exit", "Long", stop=stop_price)
    if (srt_allwd and short_entry) 
        strategy.exit("Short Exit", "Short", stop=stop_price)

```