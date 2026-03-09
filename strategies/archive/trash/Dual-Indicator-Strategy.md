``` pinescript
/*backtest
start: 2023-10-02 00:00:00
end: 2023-11-01 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("SMA & MACD Dual Direction Strategy", shorttitle="SMDDS", overlay=true, initial_capital=1000)

// SMA settings
sma7_length = input.int(7, title="7 Candle SMA Length")
sma15_length = input.int(15, title="15 Candle SMA Length")
sma60_length = input.int(60, title="60 Candle SMA Length")

// MACD settings
fast_length = input.int(12, title="Fast Length")
slow_length = input.int(26, title="Slow Length")
signal_length = input.int(9, title="Signal Length")

// Calculate SMAs
sma7 = ta.sma(close, sma7_length)
sma15 = ta.sma(close, sma15_length)
sma60 = ta.sma(close, sma60_length)

// MACD calculation
[macd_line, signal_line, _] = ta.macd(close, fast_length, slow_length, signal_length)

// Bullish and Bearish Signal Conditions
bullish_signal = (ta.crossover(sma7, sma15) and ta.crossover(sma15, sma60)) or (macd_line > signal_line)
bearish_signal = (ta.crossunder(sma7, sma15) and ta.crossunder(sma15, sma60)) or (macd_line < signal_line)

// Trading Logic
if bullish_signal
    strategy.entry("Buy", strategy.long)
else if bearish_signal
    strategy.entry("Sell", strategy.short)

// Take Profit Conditions
take_profit_9 = 0.09 * strategy.position_avg_price
take_profit_21 = 0.21 * strategy.position_avg_price

if (bullish_signal and ta.crossover(close, sma7 + take_profit_9)) or (bearish_signal and ta.crossunder(close, sma7 - take_profit_21))
    strategy.close("Buy")
    
// Stop Loss Conditions
stop_loss_9 = 0.09 * strategy.position_avg_price
stop_loss_21 = 0.21 * strategy.position_avg_price

if (bullish_signal and ta.crossover(close, sma7 - stop_loss_9)) or (bearish_signal and ta.crossunder(close, sma7 + stop_loss_21))
    strategy.close("Sell")

```

This Pine Script code implements the `SMA & MACD Dual Direction Strategy` as described in the original document. It sets up SMAs with different periods and uses both SMA crossovers and MACD crossover signals to determine trading actions, including entry points, take profit conditions, and stop loss levels.