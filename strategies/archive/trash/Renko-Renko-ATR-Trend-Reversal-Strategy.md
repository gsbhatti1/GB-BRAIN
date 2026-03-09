``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title='[tradinghook] - Renko Trend Reversal Strategy', shorttitle='[tradinghook] - Renko TRS', overlay=true ,initial_capital = 100, commission_value = 0.05, default_qty_value = 5)

// INPUTS
renkoATRLength = input.int(10, minval=1, title='ATR Length')
stopLossPct = input.float(3, title='Stop Loss Percentage', step=0.1)
takeProfitPct = input.float(20, title='Take Profit Percentage', step=0.1)
startDate = input(timestamp("01 July 2023 00:00"), title="Start Date", type=input.timeframe)
endDate = input.timestamp("31 Dec 2025 23:59"), title="End Date")
enableShorts = input.bool(true, title="Enable Shorts")

// ATR Calculation
atrLength = renkoATRLength
atrValue = ta.atr(atrLength)

// Renko Brick Generation
renkoBricks = security(syminfo.tickerid, "15", ta.rangema(ta.highest(high, atrLength), ta.lowest(low, atrLength)))

// Buy and Sell Conditions
buyCondition = renkoBricks[1] < renkoBricks[0]  // Renko open crosses below close
sellCondition = renkoBricks[1] > renkoBricks[0] // Renko open crosses above close

// Entry Logic
var float entryPrice = na
if (buyCondition and not na(entryPrice))
    strategy.entry("Buy", strategy.long)
    entryPrice := renkoBricks[0]
else if (sellCondition and not na(entryPrice))
    strategy.entry("Sell", strategy.short)
    entryPrice := renkoBricks[0]

// Exit Logic
if (not na(entryPrice)) {
    takeProfitLevel = entryPrice * (1 + takeProfitPct / 100)
    stopLossLevel = entryPrice * (1 - stopLossPct / 100)

    if (enableShorts) {
        strategy.exit("Buy TP/SL", from_entry="Buy", limit=takeProfitLevel, stop=stopLossLevel)
        strategy.exit("Sell TP/SL", from_entry="Sell", limit=takeProfitLevel, stop=stopLossLevel)
    } else {
        strategy.exit("TP/SL", "Buy", limit=takeProfitLevel, stop=stopLossLevel)
        if (na(entryPrice))
            strategy.close("Sell")
    }
}
```