``` pinescript
/*backtest
start: 2023-01-10 00:00:00
end: 2024-01-16 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("RSI Strategy", overlay=true)
length = input(14, title="Length")
overSold = input(30, title="OverSold")
overBought = input(70, title="OverBought")
sl_inp = input(10.0, title="Stop Loss %", type=float)
tp_inp = input(true, title="Take Profit %")

plot(title="RSI", series=rsi(close, length), color=color.blue, linewidth=2)

// Buy signal
when rsi(close, length) > overSold and prev(rsi(close, length)) <= overSold
    strategy.entry("Buy", strategy.long)

// Sell signal
when rsi(close, length) < overBought and prev(rsi(close, length)) >= overBought
    strategy.close("Buy")

// Stop Loss
sl = sl_inp * point_size
strategy.exit("SL", from_entry="Buy", stop=low - sl)

// Take Profit (optional)
if tp_inp
    tp = tp_inp * point_size
    strategy.exit("TP", from_entry="Buy", limit=high + tp)
```

This Pine Script implements the RSI-based short-term trading strategy with inputs for length, overSold, and overBought levels, as well as stop loss and take profit percentages. The script includes entry and exit conditions based on the RSI values crossing the predefined thresholds.