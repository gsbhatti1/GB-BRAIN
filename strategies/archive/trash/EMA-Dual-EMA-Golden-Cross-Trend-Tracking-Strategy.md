``` pinescript
/*backtest
start: 2023-10-21 00:00:00
end: 2023-11-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy(title = "Dual-EMA-Golden-Cross-Trend-Tracking-Strategy", overlay=false)


// Create General Strategy Inputs
st_yr_inp = input(defval=2017, title='Backtest Start Year')
st_mn_inp = input(defval=01, title='Backtest Start Month')
st_dy_inp = input(defval=01, title='Backtest Start Day')
en_yr_inp = input(defval=2025, title='Backtest End Year')
en_mn_inp = input(defval=01, title='Backtest End Month')
en_dy_inp = input(defval=01, title='Backtest End Day')

// Default Stop Types
fstp = input(defval=false, title="Fixed Perc stop")
fper = input(defval=0.1, title='Percentage for fixed stop', type=float)
atsp = input(defval=true, title="ATR Based stop")
atrl = input(defval=14, title='ATR Length for stop')
atrmsl = input(defval=1.5, title='ATR Multiplier for stoploss')
atrtpm = input(defval=1, title='ATR Multiplier for profit')

// Sessions
asa_inp = input(defval=true, title="Trade the Asian Session")
eur_inp = input(defval=true, title="Trade the European Session")
usa_inp = input(defval=true, title="Trade the US session")
ses_cls = input(defval=true, title="End of Session Close Out?")

// Session Start / End times (In exchange TZ = UTC-5)    
asa_ses = "1700-0300"
eur_ses = "0200-1200" 
usa_ses = "0800-1700"

in_asa = time(timeframe.period, asa_ses)
in_eur = time(timeframe.period, eur_ses)
in_usa = time(timeframe.period, usa_ses)

// Calculate EMAs
fast_ema = ema(close, 21) 
slow_ema = ema(close, 55)

// Entry Conditions
long_condition = fast_ema > slow_ema and in_asa or in_eur or in_usa  
short_condition = fast_ema < slow_ema and in_asa or in_eur or in_usa

if (long_condition)
    strategy.entry("Long", strategy.long)    

if (short_condition)
    strategy.entry("Short", strategy.short)

// Exit Conditions
exit_long = not long_condition and in_asa or in_eur or in_usa
exit_short = not short_condition and in_asa or in_eur or in_usa

if (exit_long)
    strategy.close("Long")

if (exit_short)
    strategy.close("Short")

// Stop Loss and Take Profit
stop_loss_level = na
take_profit_level = na

if (strategy.opentrades > 0)  
    if (fstp)
        stop_loss_level := fper * strategy.position_avg_price
    else 
        stop_loss_level := atr(atrl, atrmsl)

    take_profit_level := atr(atrl, atrtpm)

stoploss = min(stop_loss_level, strategy.position_avg_price - fper * strategy.position_avg_price)  
takeprofit = max(take_profit_level, strategy.position_avg_price + fper * strategy.position_avg_price) 

if (strategy.opentrades > 0)
    if (exit_long and stoploss >= stop_loss_level or takeprofit <= take_profit_level)
        strategy.close("Long")

    if (exit_short and stoploss >= stop_loss_level or takeprofit <= take_profit_level)
        strategy.close("Short")
```

This script implements the Dual-EMA-Golden-Cross-Trend-Tracking-Strategy as described. The comments in the code provide a clear understanding of each step, including backtesting parameters and session timing.