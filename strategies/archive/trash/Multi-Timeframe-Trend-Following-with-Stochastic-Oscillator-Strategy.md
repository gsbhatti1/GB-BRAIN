``` pinescript
/*backtest
start: 2024-02-19 00:00:00
end: 2025-02-16 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("15-Min Trend Strategy", overlay=true, default_qty_type=strategy.fixed, default_qty_value=0.02)

// Define EMA for trend confirmation
ema50 = ta.ema(close, 50)
trendLong = close > ema50
trendShort = close < ema50

// Stochastic settings
length = 14
smoothK = 3
smoothD = 3
stochK = ta.stoch(close, high, low, length)[0][0]
stochD = ta.sma(stochK, smoothD)[0][0]

// Entry conditions
longCondition = stochK < 30 and trendLong
shortCondition = stochK > 70 and trendShort

// ATR-based stop-loss calculation
atrValue = ta.atr(14)
stopLossLong = close - (1.5 * atrValue)
stopLossShort = close + (1.5 * atrValue)
takeProfitLong = close + (2 * atrValue)
takeProfitShort = close - (2 * atrValue)

// Execute trades
if longCondition
    strategy.entry("Long", strategy.long, qty=0.02)
    strategy.exit("TP Long 1", from_entry="Long", qty=0.01, stop=stopLossLong, limit=takeProfitLong)
    strategy.exit("TP Long 2", from_entry="Long", qty=0.01, stop=stopLossLong, limit=takeProfitLong * 1.5)

if shortCondition
    strategy.entry("Short", strategy.short, qty=0.02)
    strategy.exit("TP Short 1", from_entry="Short", qty=0.01, stop=stopLossShort, limit=takeProfitShort)
    strategy.exit("TP Short 2", from_entry="Short", qty=0.01, stop=stopLossShort, limit=takeProfitShort * 1.5)

// Move SL to breakeven after 50% move to target
if strategy.position_size > 0
    if strategy.position_avg_price != 0
```