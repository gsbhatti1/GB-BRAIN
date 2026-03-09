``` pinescript
/*backtest
start: 2023-12-18 00:00:00
end: 2023-12-21 03:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © FX_minds

//@version=4
strategy("ETF tradedr", overlay=true, pyramiding=100, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

//------------------------------ get user input
lookback                   = input(title="HH LL lookback", type=input.integer, defval=20)
ATR_periode                = input(title="ATR period", type=input.integer, defval=14)
ATR_SL_multiplier          = input(title="ATR SL multiplier", type=input.float, defval=2)
ATR_TP_multiplier          = input(title="ATR TP multiplier", type=input.float, defval=1)
max_sequel_trades          = input(title="max sequel trades", type=input.integer, defval=3)
trailing_SL_multiplier     = input(title="ATR trailing SL multiplier", type=input.float, defval=3.5)
trailing_SL_lookback       = input(title="trailing SL lookback", type=input.integer, defval=4)
trade_long                 = input(title="trade long?", type=input.bool, defval=true)
trade_short                = input(title="trade short?", type=input.bool, defval=false)

//------------------------------ get indicators
hhll                        = highest(high, lookback)
llhh                        = lowest(low, lookback)
atr                         = atr(ATR_periode)
atr_sl                       = atr * ATR_SL_multiplier
atr_tp                       = atr * ATR_TP_multiplier
trailing_sl                  = atr * trailing_SL_multiplier

//------------------------------ strategy logic
if (trade_long)
    long_condition = close > hhll
    if (long_condition)
        strategy.entry("Long", strategy.long)
        strategy.exit("Take Profit", "Long", stop=hhll + atr_tp, limit=hhll + 2 * atr_tp)
        strategy.exit("Stop Loss", "Long", stop=hhll - atr_sl, limit=hhll - 2 * atr_sl)
        if (trade_short)
            strategy.exit("Reverse", "Long", stop=llhh, limit=llhh + atr_sl)
if (trade_short)
    short_condition = close < llhh
    if (short_condition)
        strategy.entry("Short", strategy.short)
        strategy.exit("Take Profit", "Short", stop=llhh - atr_tp, limit=llhh - 2 * atr_tp)
        strategy.exit("Stop Loss", "Short", stop=llhh + atr_sl, limit=llhh + 2 * atr_sl)
        if (trade_long)
            strategy.exit("Reverse", "Short", stop=hhll, limit=hhll - atr_sl)
```

This completes the Pine Script for the ETF trading strategy based on ATR and breakout with the correct parameter and logic.