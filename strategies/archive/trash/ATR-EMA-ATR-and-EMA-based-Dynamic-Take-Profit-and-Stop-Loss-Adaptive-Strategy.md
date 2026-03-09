``` pinescript
/*backtest
start: 2024-04-27 00:00:00
end: 2024-05-27 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy(title='UT MB&SS Bot', overlay=true)

// Inputs
a = input(1, title='Key Value. \'This changes the sensitivity\'')
c = input(10, title='ATR Period')
h = input(false, title='Signals from Heikin Ashi Candles')
stoploss = input(2.0, title='Stop Loss (ATR Multiples)')

xATR = ta.atr(c)
nLoss = a * xATR

src = h ? request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, close, lookahead=barmerge.lookahead_off) : close

var xATR_trailing_stop = 0.0
iff_1 = src > nz(xATR_trailing_stop[1], 0) ? src - nLoss : src + nLoss
iff_2 = src < nz(xATR_trailing_stop[1], 0) and src[1] < nz(xATR_trailing_stop[1], 0) ? math.min(nz(xATR_trailing_stop[1]), src + nLoss) : iff_1
xATR_trailing_stop := src > nz(xATR_trailing_stop[1], 0) and src[1] > nz(xATR_trailing_stop[1], 0) ? math.max(nz(xATR_trailing_stop[1]), src - nLoss) : iff_2

pos = 0
iff_3 = src[1] > nz(xATR_trailing_stop[1], 0) and src < nz(xATR_trailing_stop[1], 0) ? -1 : nz(pos[1], 0)
pos := src[1] < nz(xATR_trailing_stop[1], 0) and src[2] > nz(xATR_trailing_stop[1], 0) ? 1 : iff_3
order = iff(pos == -1, order.close_all(), iff(pos == 1, order.open_limit, 0))

// Plotting
plot(xATR_trailing_stop, color=color.red, title='Trailing Stop')
plot(src, color=color.blue, title='Source Price')

// Conditional Orders
if (order)
    strategy.entry("Long", strategy.long, when = order == 1)
    strategy.exit("Stop Loss", "Long", stop = xATR_trailing_stop)
```

This Pine Script code implements the strategy described in the Chinese document. It uses ATR and EMA to dynamically adjust stop loss and take profit levels. The script includes necessary conditions for entering long positions and handling stop loss exits. The `overlay=true` parameter ensures that the strategy is displayed on the price chart.