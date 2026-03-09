``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © bensonsuntw

strategy("Moving-Average-Channel-Breakout-Trading-Strategy", pyramiding=1, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

backtest_year = input(2019, type=input.integer, title='backtest_year')
backtest_month = input(01, type=input.integer, title='backtest_month', minval=1, maxval=12)
backtest_day = input(01, type=input.integer, title='backtest_day', minval=1, maxval=31)
enable_stop_loss_and_take_profit = input(true, type=input.bool, title='Enable Stop Loss and Take Profit')
enable_trail_stop = input(true, type=input.bool, title='Enable Trail Stop')
buy_stop_loss = input(0.2, type=input.float, title='buy_stop_loss')
sell_stop_loss = input(0.1, type=input.float, title='sell_stop_loss')
buy_tp = input(0.4, type=input.float, title='buy_tp')
sell_tp = input(0.2, type=input.float, title='sell_tp')
trail_stop_long = input(1.1, type=input.float, title='trail_stop_long')
trail_stop_short = input(0.9, type=input.float, title='trail_stop_short')
trail_stop_long_offset = input(0.05, type=input.float, title='trail_stop_long_offset')
trail_stop_short_offset = input(0.05, type=input.float, title='trail_stop_short_offset')

var float buy_price = na
var float sell_price = na
var float buy_stop = na
var float sell_stop = na
var int buy_trail_stop = na
var int sell_trail_stop = na

// Calculate moving averages
sma_7 = sma(close, 7)
sma_14 = sma(close, 14)

// Buy condition
if (sma_7 > sma_14 and na(buy_price) and not na(sell_price))
    strategy.entry("Long", strategy.long)
    buy_price := close
    buy_stop := close * (1 - buy_stop_loss)
    buy_trail_stop := 1

// Sell condition
if (sma_7 < sma_14 and na(sell_price) and not na(buy_price))
    strategy.entry("Short", strategy.short)
    sell_price := close
    sell_stop := close * (1 + sell_stop_loss)
    sell_trail_stop := 1

// Trailing stop
if (buy_trail_stop == 1 and close > buy_stop)
    buy_stop := close * (1 - trail_stop_long_offset)
if (sell_trail_stop == 1 and close < sell_stop)
    sell_stop := close * (1 + trail_stop_short_offset)

// Stop Loss and Take Profit
if (enable_stop_loss_and_take_profit)
    if (strategy.position_size > 0 and close < buy_stop)
        strategy.close("Long")
    if (strategy.position_size < 0 and close > sell_stop)
        strategy.close("Short")

// Trail Stop
if (enable_trail_stop)
    if (strategy.position_size > 0)
        if (close > buy_stop and close > buy_stop * trail_stop_long)
            strategy.close("Long")
    if (strategy.position_size < 0)
        if (close < sell_stop and close < sell_stop * trail_stop_short)
            strategy.close("Short")
```

This script implements the Moving-Average-Channel-Breakout-Trading-Strategy based on the provided description and arguments. The strategy uses 7-day and 14-day simple moving averages to generate buy and sell signals, with additional features for stop loss, take profit, and trailing stop.