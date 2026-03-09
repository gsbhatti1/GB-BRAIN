``` pinescript
/*backtest
start: 2024-02-19 00:00:00
end: 2025-02-16 08:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title='UT Bot Strategy with 100 EMA Filter, Trailing Stop and EMA Cross Exit', overlay=true)

// Inputs
a = input(1, title='Key Value. \'This changes the sensitivity\'')
c = input(10, title='ATR Period')
h = input(false, title='Signals from Heikin Ashi Candles')

// Higher timeframe trend filter (1-hour)
higherTimeframeEMA = request.security(syminfo.tickerid, "60", ta.ema(close, 100)) // 1-hour EMA

xATR = ta.atr(c)

// Adjusting ATR multiplier for Gold on 15-minute timeframe
atrMultiplier = 3
nLoss = atrMultiplier * xATR  // ATR-based loss calculation

src = h ? request.security(ticker.heikinashi(syminfo.tickerid), timeframe.period, close, lookahead=barmerge.lookahead_off) : close

// Trailing Stop Calculation
xATRTrailingStop = 0.0
iff_1 = src > nz(xATRTrailingStop[1], 0) ? src - nLoss : src + nLoss
iff_2 = src < nz(xATRTrailingStop[1], 0) and src[1] < nz(xATRTrailingStop[1], 0) ? math.min(nz(xATRTrailingStop[1]), src + nLoss) : iff_1
xATRTrailingStop := src > nz(xATRTrailingStop[1], 0) and src[1] > nz(xATRTrailingStop[1], 0) ? math.max(nz(xATRTrailingStop[1]), src - nLoss) : iff_2

pos = 0
iff_3 = src[1] > nz(xATRTrailingStop[1], 0) and src < nz(xATRTrailingStop[1], 0) ? -1 : nz(pos[1], 0)
pos := src[1] < nz(xATRTrailingStop[1], 0) and src > nz(xATRTrailingStop[1], 0) ? 1 : iff_3

xcolor = pos == -1 ? color.red : pos == 1 ? color.green : color.blue

// Define 100 EMA
ema100 = ta.ema(src, 100)
plot(ema100, title="100 EMA", color=color.black, linewidth=2)

// Define 15 EMA and 17 EMA for exit conditions
ema15 = ta.ema(src, 15)
ema17 = ta.ema(src, 17)
plot(ema15, title="15 EMA", colo
```