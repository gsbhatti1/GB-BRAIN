``` pinescript
/*backtest
start: 2023-08-24 00:00:00
end: 2023-09-23 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
//based on Range Strat - MACD/RSI 
strategy("MACD/RSI - edited", 
    overlay=true,
    default_qty_type=strategy.percent_of_equity,
    default_qty_value=10, precision=2, initial_capital=100000,
    pyramiding=2,
    commission_value=0.05)

//Backtest date range
StartDate = input(timestamp("13 Jun 2022"), title="Start Date")
EndDate = input(timestamp("13 Jun 2024"), title="End Date")
inDateRange = (time >= StartDate and time <= EndDate)

// RSI Input Settings
rsisrc = input(title="RSI Source", defval=close, group="RSI Settings")
length = input(title="Length", defval=14, group="RSI Settings" )
overSold = input(title="Over Sold Threshold", defval=30, group="RSI Settings" )
overBought = input(title="Over Bought Threshold", defval=70, group="RSI Settings" )
rsi_lookback = input(title="RSI cross lookback period", defval=7, group="RSI Settings")

// Calculating RSI
vrsi = ta.rsi(rsisrc, length)
co = ta.crossover(vrsi, overSold)
cu = ta.crossunder(vrsi, overBought)

// Function looking for a happened condition during lookback period
f_somethingHappened(_cond, _lookback) =>
    bool _crossed = false
    for i = 1 to _lookback
        if _cond[i]
            _crossed := true
    _crossed

coCheck = f_somethingHappened(co, rsi_lookback)
cuCheck = f_somethingHappened(cu, rsi_lookback)

// MACD Input Settings
macdsrc = input(title="MACD Source", defval=close, group="MACD Settings")
fast_length = input(title="Fast Length", defval=12, group="MACD Settings")
slow_length = input(title="Slow Length", defval=26, group="MACD Settings")
signal_length = input.int(title="Signal Smoothing",  minval = 1, maxval = 50, defval = 9, group="MACD Settings")
sma_source = input.string(title="Oscillator MA Type", defval="EMA", options=["EMA", "SMA"], group="MACD Settings")
ema_fast = ta.ema(macdsrc, fast_length)
ema_slow = ta.ema(macdsrc, slow_length)
macd_line = ema_fast - ema_slow
signal_line = ta.sma(macd_line, signal_length)

// MACD Crossovers
buy_signal = ta.crossover(macd_line, signal_line) and coCheck
sell_signal = ta.crossunder(macd_line, signal_line) and cuCheck

// Trading Logic
if (inDateRange)
    if buy_signal
        strategy.entry("Buy", strategy.long)
        
    if sell_signal
        strategy.exit("Sell", "Buy")

// Stop Loss Settings
longStopLossPercent = input(15.0, title="Long Stop Loss (%)", group="Stop Loss Settings")
shortStopLossPercent = input(15.0, title="Short Stop Loss (%)", group="Stop Loss Settings")
stopLossLevel = close * (1 - longStopLossPercent / 100)

// Set Stop Loss on Entry
if (strategy.position_size > 0)
    strategy.exit("Exit Long Position", "Buy", stop=stopLossLevel)

if (strategy.position_size < 0)
    strategy.exit("Exit Short Position", "Sell", stop=stopLossLevel)
```

This code reflects the translation of the provided Chinese text into English, keeping all original code blocks and parameters intact.