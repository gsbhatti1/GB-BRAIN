``` pinescript
/*backtest
start: 2024-11-04 00:00:00
end: 2024-11-11 00:00:00
period: 10m
basePeriod: 10m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Harmony Signal Flow By Arun", overlay=true)

// RSI settings
rsiLength = 14
rsiSource = close
rsiValue = ta.rsi(rsiSource, rsiLength)

// Define RSI levels
buyLevel = 30
sellLevel = 70

// Buy signal: RSI crosses above 30
buyCondition = ta.crossover(rsiValue, buyLevel)

// Sell signal: RSI crosses below 70
sellCondition = ta.crossunder(rsiValue, sellLevel)

// Ensure only one order at a time
if (strategy.position_size == 0) // No open positions
    if (buyCondition)
        strategy.entry("Buy", strategy.long)
    else if (sellCondition)
        strategy.entry("Sell", strategy.short)

// Stop-loss and target conditions
var float stopLossBuy = na
var float targetBuy = na
var float stopLossSell = na
var float targetSell = na

if (strategy.position_size > 0) // If there's an open buy position
    stopLossBuy := strategy.position_avg_price - 100 // Set stop-loss for buy
    targetBuy := strategy.position_avg_price + 150 // Set target for buy

    if (close <= stopLossBuy)
        strategy.close("Buy", comment="Stoploss Hit")
    else if (close >= targetBuy)
        strategy.close("Buy", comment="Target Hit")

if (strategy.position_size < 0) // If there's an open sell position
    stopLossSell := strategy.position_avg_price + 100 // Set stop-loss for sell
    targetSell := strategy.position_avg_price - 150 // Set target for sell

    if (close >= stopLossSell)
        strategy.close("Sell", comment="Stoploss Hit")
    else if (close <= targetSell)
        strategy.close("Sell", comment="Target Hit")

// Close all positions by 3:25 PM
if (hour(timenow) == 15 and minute(timenow) == 25)
    strategy.close_all(comment="Close at 15:25")
```

This Pine Script code defines a trading strategy based on RSI levels with multi-level risk management. The script includes conditions for entering trades, setting stop-loss and take-profit levels, and automatically closing positions at 3:25 PM to avoid overnight risks.