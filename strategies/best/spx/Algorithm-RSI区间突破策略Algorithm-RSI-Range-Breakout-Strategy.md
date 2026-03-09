> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|27|Buy Level 1|
|v_input_3|18|Buy Level 2|
|v_input_4|68|Sell Level 1|
|v_input_5|80|Sell Level 2|
|v_input_6|2500|Target Pips|
|v_input_7|5000|Stop Pips|
|v_input_8|1|Lot Size|


> Source (PineScript)

```pinescript
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
strategy("BTC/USD - RSI", overlay=false, initial_capital=5000)

// User input
length = input(title="Length", defval=14, tooltip="RSI period")

first_buy_level = input(title="Buy Level 1", defval=27, tooltip="Level where 1st buy triggers")
second_buy_level = input(title="Buy Level 2", defval=18, tooltip="Level where 2nd buy triggers")

first_sell_level = input(title="Sell Level 1", defval=68, tooltip="Level where 1st sell triggers")
second_sell_level = input(title="Sell Level 2", defval=80, tooltip="Level where 2nd sell triggers")

takeProfit = input(title="Target Pips", defval=2500, tooltip="Fixed pip take profit distance")
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
// Buy Orders
if (long1 and strategy.position_size == 0)
    strategy.entry("Long", strategy.long, qty=lot, comment="Buy")
    if (long2 and strategy.position_size > 0)
        strategy.entry("Long2", strategy.long, qty=lot, comment="Additional Buy")

// Sell Orders
if (short1 and strategy.position_size == 0)
    strategy.entry("Short", strategy.short, qty=lot, comment="Sell")
    if (short2 and strategy.position_size > 0)
        strategy.entry("Short2", strategy.short, qty=lot, comment="Additional Sell")

// Exit Conditions
// Exit Long
if (vrsi >= first_sell_level and strategy.position_size > 0)
    strategy.exit("Exit Long", from_entry="Long", limit=vrsi + takeProfit, stop=vrsi - stopLoss)

if (vrsi >= second_sell_level and strategy.position_size > 0)
    strategy.exit("Exit Long2", from_entry="Long2", limit=vrsi + takeProfit, stop=vrsi - stopLoss)

// Exit Short
if (vrsi <= first_buy_level and strategy.position_size < 0)
    strategy.exit("Exit Short", from_entry="Short", limit=vrsi - takeProfit, stop=vrsi + stopLoss)

if (vrsi <= second_buy_level and strategy.position_size < 0)
    strategy.exit("Exit Short2", from_entry="Short2", limit=vrsi - takeProfit, stop=vrsi + stopLoss)
```

This Pine Script implements the RSI interval breakout strategy as described. Adjust the parameters as needed for testing and backtesting.