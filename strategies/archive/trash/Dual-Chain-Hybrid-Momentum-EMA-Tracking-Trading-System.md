``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-28 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title='Dual Chain Strategy', shorttitle='DualChain', overlay=true)

// User inputs for enabling/disabling chains
enableChain1 = input.bool(true, title='Enable Chain 1')
enableChain2 = input.bool(true, title='Enable Chain 2')

// User inputs for the first chain
len1 = input.int(10, minval=1, title='Length Chain 1 EMA', group="Chain 1")
src1 = input(close, title='Source Chain 1', group="Chain 1")
tf1_entry = input.timeframe("W", title='Chain 1 Entry Timeframe', group="Chain 1")
tf1_exit = input.timeframe("D", title='Chain 1 Exit Timeframe', group="Chain 1")

// Weekly timeframe EMA for Chain 1
entryEMA1 = request.security(syminfo.tickerid, tf1_entry, ta.ema(src1, len1))

// Daily timeframe EMA for Chain 1
exitEMA1 = request.security(syminfo.tickerid, tf1_exit, ta.ema(src1, len1))

// User inputs for the second chain
len2 = input.int(9, minval=1, title='Length Chain 2 EMA', group="Chain 2")
src2 = input(close, title='Source Chain 2', group="Chain 2")
tf2_entry = input.timeframe("720", title='Chain 2 Entry Timeframe (12H)', group="Chain 2")  // 12 hours
tf2_exit = input.timeframe("540", title='Chain 2 Exit Timeframe (9H)', group="Chain 2")    // 9 hours

// Entry timeframe EMA for Chain 2
entryEMA2 = request.security(syminfo.tickerid, tf2_entry, ta.ema(src2, len2))

// Exit timeframe EMA for Chain 2
exitEMA2 = request.security(syminfo.tickerid, tf2_exit, ta.ema(src2, len2))

// Entry and exit conditions for Chain 1
if (enableChain1)
    strategy.entry("Entry Chain 1", side=side.long, when=cross(close, entryEMA1))
    strategy.exit("Exit Chain 1", from_entry="Entry Chain 1", when=cross(close, exitEMA1))

// Entry and exit conditions for Chain 2
if (enableChain2)
    strategy.entry("Entry Chain 2", side=side.long, when=cross(higher_close, entryEMA2))
    strategy.exit("Exit Chain 2", from_entry="Entry Chain 2", when=cross(lower_close, exitEMA2))

// Helper function to get the higher close price
higher_close = ta.highestbars(close, len1)
lower_close = ta.lowestbars(close, len1)

plot(series=entryEMA1, color=color.blue, title='Chain 1 EMA Entry')
plot(series=exitEMA1, color=color.red, title='Chain 1 EMA Exit')
plot(series=entryEMA2, color=color.green, title='Chain 2 EMA Entry')
plot(series=exitEMA2, color=color.orange, title='Chain 2 EMA Exit')

```
```