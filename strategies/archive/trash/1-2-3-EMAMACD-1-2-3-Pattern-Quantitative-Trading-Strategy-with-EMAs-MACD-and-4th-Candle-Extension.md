``` pinescript
/*backtest
start: 2024-02-01 00:00:00
end: 2024-02-29 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("1-2-3 Pattern Strategy with EMAs, MACD, and 4th Candle Extension", overlay=true)

// Define conditions for the 1-2-3 pattern for buy orders
buy_candle1_above_open = close[3] > open[3]
buy_candle2_below_open = close[2] < open[2]
buy_candle3_above_candle1_close = close[1] > close[3]
buy_candle4_above_candle3_close = close >= close[3]

// Define conditions for the 1-2-3 pattern for sell orders
sell_candle1_below_open = close[3] < open[3]
sell_candle2_above_open = close[2] > open[2]
sell_candle3_below_candle1_close = close[1] < close[3]
sell_candle4_below_candle3_close = close <= close[3]

// EMA and MACD conditions
ema_9 = ta.ema(close, 9)
ema_20 = ta.ema(close, 20)
macd_line = ta.macd(close)[1] // The first element of the macd() function returns the MACD line itself.
signal_line = ta.macd_signal(close) // This is the signal line for the MACD

// Buy and Sell signals
buy_condition = buy_candle1_above_open and buy_candle2_below_open and buy_candle3_above_candle1_close and buy_candle4_above_candle3_close and close > ema_9 and close > ema_20 and macd_line > signal_line
if (buy_condition)
    strategy.entry("Long", strategy.long)

sell_condition = sell_candle1_below_open and sell_candle2_above_open and sell_candle3_below_candle1_close and sell_candle4_below_candle3_close and close < ema_9 and close < ema_20 and macd_line < signal_line
if (sell_condition)
    strategy.entry("Short", strategy.short)

// Close positions when opposite signals occur or current candle closes in the opposite direction of the position
if (buy_condition and not na(close[1]))
    if (close <= open)
        strategy.close("Long")
        
if (sell_condition and not na(close[1]))
    if (close >= open)
        strategy.close("Short")

// Plot EMAs and MACD on the chart
plot(ema_9, color=color.blue, title="EMA 9")
plot(ema_20, color=color.red, title="EMA 20")
hline(macd_line, "MACD Line", color=color.green)
```

This code block defines the conditions for the 1-2-3 pattern and incorporates EMA and MACD indicators to confirm trends. It also includes logic to open positions based on these conditions and close them when appropriate.