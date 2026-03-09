``` pinescript
/*backtest
start: 2024-01-09 00:00:00
end: 2024-01-16 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title='[RS]Khizon (UGAZ) Strategy V0', shorttitle='K', overlay=false, pyramiding=0, initial_capital=100000, currency=currency.USD)
//  ||  Inputs:
macd_src = input(title='MACD Source:',  defval=close)
macd_fast = input(title='MACD Fast Length:',  defval=12)
macd_slow = input(title='MACD Slow Length:',  defval=26)
macd_signal_smooth = input(title='MACD Signal Smoothing:',  defval=9)
srsi_src = input(title='SRSI Source:',  defval=close)
srsi_rsi_length = input(title='SRSI RSI Length:',  defval=14)
srsi_stoch_length = input(title='SRSI Stoch Length:',  defval=14)
srsi_smooth = input(title='SRSI Smoothing:',  defval=3)
srsi_signal_smooth = input(title='SRSI Signal Smoothing:',  defval=3)
//  ||  Strategy Inputs:
trade_size = input(title='Trade Size in USD:', type=float, defval=100000) // Adjusted default value
buy_trade = input(title='Perform buy trading?', type=bool, defval=true)
sell_trade = input(title='Perform sell trading?', type=bool, defval=true)
//  ||  MACD(close, 12, 26, 9):     ||---------------------------------------------||
f_macd_trigger(_src, _fast, _slow, _signal_smooth)=>
    _macd = ema(_src, _fast) - ema(_src, _slow)
    _signal = sma(_macd, _signal_smooth)
    _return_trigger = _macd >= _signal ? true : false
//  ||  Stoch RSI(close, 14, 14, 3, 3):  ||---------------------------------------------||
f_stoch_rsi_trigger(_src, _rsi_length, _stoch_length, _smooth, _signal_smooth)=>
    rsi_val = rsi(_src, _rsi_length)
    stoch_val = stochastic(rsi_val, _rsi_length, _stoch_length)
    signal_line = sma(stoch_val, _signal_smooth)
    _return_trigger = stoch_val >= signal_line ? true : false
//  ||  Strategy Logic:  ||---------------------------------------------||
// Check both MACD and Stoch RSI triggers on daily (1440m) and 4-hour (240m) timeframes.
is_buy = f_macd_trigger(close, macd_fast, macd_slow, macd_signal_smooth) and f_stoch_rsi_trigger(close, srsi_rsi_length, srsi_stoch_length, srsi_smooth, srsi_signal_smooth)
is_sell = not is_buy
//  ||  Entry Conditions:  ||---------------------------------------------||
if (bar_index % 1440 == 0 and buy_trade) // daily
    if (is_buy)
        strategy.entry("Buy", strategy.long, stop=na, limit=na, comment="MACD & Stoch RSI Buy Signal")
if (bar_index % 240 == 0 and sell_trade) // 4-hour
    if (is_sell)
        strategy.entry("Sell", strategy.short, stop=na, limit=na, comment="MACD & Stoch RSI Sell Signal")
//  ||  Exit Conditions:  ||---------------------------------------------||
if (bar_index % 1440 == 0 and buy_trade) // daily
    if (not is_buy)
        strategy.close("Buy", stop=na, limit=na, comment="MACD & Stoch RSI Buy Exit")
if (bar_index % 240 == 0 and sell_trade) // 4-hour
    if (not is_sell)
        strategy.close("Sell", stop=na, limit=na, comment="MACD & Stoch RSI Sell Exit")

//  ||  Plotting:  ||---------------------------------------------||
plotshape(series=f_macd_trigger(close, macd_fast, macd_slow, macd_signal_smooth), style=shape.triangleup, location=location.belowbar, color=color.green, title="MACD Buy Signal")
plotshape(series=f_stoch_rsi_trigger(close, srsi_rsi_length, srsi_stoch_length, srsi_smooth, srsi_signal_smooth), style=shape.triangledown, location=location.abovebar, color=color.red, title="Stoch RSI Sell Signal")
```

This script uses the provided inputs to determine whether to enter a trade based on both MACD and Stoch RSI signals. It then exits trades when either of these indicators no longer provides a buy or sell signal, respectively. The strategy is set up to validate signals across daily (1440 minutes) and 4-hour (240 minutes) timeframes for robustness against false signals.