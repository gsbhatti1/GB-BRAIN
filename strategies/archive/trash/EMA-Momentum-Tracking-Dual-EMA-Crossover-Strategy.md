``` pinescript
/*backtest
start: 2023-02-19 00:00:00
end: 2024-02-25 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © RealTraderAkeme

//@version=5
strategy("AKEME_EMA_CROSS_V6", overlay=true)

////////////////////////////////////////////////////////////PARAMETERS/////////////////////////////////////////////////////////////////
emaFast_op = input(title="Fast_EMA", defval=6)
emaSlow_op = input(title="Slow_EMA", defval=26)
emaExit_op = input(title="Sell_EMA_Exit",defval=10)
emabuyExit_op = input(title="Buy_EMA_Exit",defval=20)
orderValue_op = input(title="Order_Value in Pounds", defval=1000)
tradeDirection_op = input(title="Trade Direction", defval="Both")

////////////////////////////////////////////////////////////INDICATORS/////////////////////////////////////////////////////////////////////
emaFast = ta.ema(close, emaFast_op)
emaSlow = ta.ema(close, emaSlow_op)
emaExit = ta.ema(close, emaExit_op)
emaBuyExit = ta.ema(close, emabuyExit_op)

////////////////////////////////////////////////////////////TRADE SIGNALS/////////////////////////////////////////////////////////////////////
buySignal = ta.crossover(emaFast, emaSlow)
sellSignal = ta.crossunder(emaFast, emaSlow)

////////////////////////////////////////////////////////////EXIT STRATEGIES/////////////////////////////////////////////////////////////////////
exitBuySignal = ta.crossover(emaFast, emaExit)
exitSellSignal = ta.crossover(emaExit, emaSlow)

////////////////////////////////////////////////////////////TRADE ENTRY AND EXIT/////////////////////////////////////////////////////////////////////
if (buySignal)
    strategy.entry("Buy", strategy.long, when=buySignal, comment="Buy Signal")
    strategy.exit("Buy Exit", "Buy", profit_offset=emaBuyExit, stop_offset=-orderValue_op * 0.06, when=exitBuySignal)
if (sellSignal)
    strategy.entry("Sell", strategy.short, when=sellSignal, comment="Sell Signal")
    strategy.exit("Sell Exit", "Sell", profit_offset=emaExit_op, stop_offset=-orderValue_op * 0.03, when=exitSellSignal)

////////////////////////////////////////////////////////////PLOTTING/////////////////////////////////////////////////////////////////////
plot(emaFast, color=color.blue, title="Fast EMA")
plot(emaSlow, color=color.red, title="Slow EMA")
plot(emaExit, color=color.green, title="Sell EMA Exit")
plot(emaBuyExit, color=color.orange, title="Buy EMA Exit")

////////////////////////////////////////////////////////////NOTES/////////////////////////////////////////////////////////////////////
// This strategy is designed to track trends using EMA crossovers and exits. It uses multiple EMA lines to lock in profits and sets stop loss points to control risk.
// The strategy is optimized for both long and short trades, and includes mechanisms for profit taking and risk management.
```