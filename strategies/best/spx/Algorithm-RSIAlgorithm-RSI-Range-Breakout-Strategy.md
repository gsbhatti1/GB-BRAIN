``` pinescript
/*backtest
start: 2023-09-16 00:00:00
end: 2023-10-16 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Rawadabdo

// Ramy's Algorithm

//@version=5
strategy("Algorithm-RSI-Range-Breakout-Strategy", overlay=false, initial_capital = 5000)

// User input
length = input(title="Length", defval=14, tooltip="RSI period")
first_buy_level = input(title="Buy Level 1", defval=27, tooltip="Level where 1st buy triggers")
second_buy_level = input(title="Buy Level 2", defval=18, tooltip="Level where 2nd buy triggers")
first_sell_level = input(title="Sell Level 1", defval=68, tooltip="Level where 1st sell triggers")
second_sell_level = input(title="Sell Level 2", defval=80, tooltip="Level where 2nd sell triggers")
takeProfit = input(title="target Pips", defval=2500, tooltip="Fixed pip take profit distance")
stopLoss = input(title="Stop Pips", defval=5000, tooltip="Fixed pip stop loss distance")
lot = input(title="Lot Size", defval=1, tooltip="Trading Lot size")

// Get RSI
vrsi = ta.rsi(close, length)

// Entry Conditions
long1 = (vrsi <= first_buy_level and vrsi > second_buy_level)
long2 = (vrsi <= second_buy_level)

short1 = (vrsi >= first_sell_level and vrsi < second_sell_level)
short2 = (vrsi >= second_sell_level)

// Entry Orders
if (long1 and strategy.position_size == 0)
    strategy.entry("Long", strategy.long, qty=lot, comment="Buy")
    if (long2 and strategy.position_size > 0)
        strategy.modify_order("Long", stop=stopLoss, limit=takeProfit, comment="Add to Long")

if (short1 and strategy.position_size == 0)
    strategy.entry("Short", strategy.short, qty=lot, comment="Sell")
    if (short2 and strategy.position_size > 0)
        strategy.modify_order("Short", stop=stopLoss, limit=takeProfit, comment="Add to Short")

// Exit Conditions
if (vrsi < first_buy_level or vrsi > first_sell_level) and strategy.position_size > 0
    strategy.close("Long")
    
if (vrsi < second_buy_level or vrsi > second_sell_level) and strategy.position_size > 0
    strategy.close("Short")
```

This translation ensures all code blocks, numbers, and formatting remain unchanged while translating the human-readable text as requested.