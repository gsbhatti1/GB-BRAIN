``` pinescript
/*backtest
start: 2023-09-19 00:00:00
end: 2023-09-26 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © tweakerID

// This is a strategy that uses the 7 Period RSI to buy when the indicator is shown as oversold (OS) and sells when 
// the index marks overbought (OB). It also uses the ADX to determine whether the trend is ranging or trending
// and filters out the trending trades. Seems to work better for automated trading when the logic is inversed (buying OB 
// and selling the OS) without stop loss.

//@version=4
strategy("ADX + RSI Strat", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital=100, commission_value=0.04, calc_on_every_tick=false)

direction = input(0, title="Strategy Direction", type=input.integer, minval=-1, maxval=1)
strategy.risk.allow_entry_in(direction == 0 ? strategy.direction.all : (direction < 0 ? strategy.direction.short : strategy.direction.long))


//SL & TP Inputs
i_SL=input(false, title="Use Swing Lo/Hi Stop Loss & Take Profit")
i_SwingLookback=input(20, title="Swing Lo/Hi Lookback")
i_SLExpander=input(defval=0, step=.2, title="SL Expander")
i_TPExpander=input(defval=0, step=.2, title="TP Expander")
i_reverse=input(true, title="Reverse Trades")

//SL & TP Calculations
SwingLow=lowest(i_SwingLookback)
SwingHigh=highest(i_SwingLookback)
bought=strategy.position_size != strategy.position_size[1]
LSL=valuewhen(bought, SwingLow, 0)-((valuewhen(bought, atr(14), 0))*i_SLExpander)
SSL=valuewhen(bought, SwingHigh, 0)+((valuewhen(bought, atr(14), 0))*i_SLExpander)
lTP=strategy.position_avg_price + (strategy.position_avg_price-(valuewhen(bought, SwingLow, 0))+((valuewhen(bought, atr(14), 0))*i_TPExpander))
sTP=strategy.position_avg_price - (valuewhen(bought, SwingHigh, 0)-strategy.position_avg_price)-((valuewhen(bought, atr(14), 0))*i_TPExpander)
islong=strategy.position_size > 0
isshort=strategy.position_size < 0
SL= islong ? LSL : isshort ? SSL : na
TP= islong ? lTP : isshort ? sTP : na

//RSI Calculations
RSI=rsi(close, 7)
OS=input(30, step=5)
OB=input(80, step=5)
overbought = RSI > OB
oversold = RSI < OS

// Entry Rules
longCondition = oversold and ADX > 30
shortCondition = overbought and ADX > 30

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

// Exit Rules
if (islong and close < SL or islong and close > TP)
    strategy.exit("Close Long", "Long")

if (isshort and close > SSL or isshort and close < LSL)
    strategy.exit("Close Short", "Short")
```

This translation maintains the original code structure, numbers, and formatting while translating the human-readable text from Chinese to English.