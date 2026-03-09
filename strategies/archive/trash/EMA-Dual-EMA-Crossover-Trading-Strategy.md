> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|Fast EMA|
|v_input_2|21|Slow EMA|
|v_input_3|5|Exit EMA|
|v_input_4|true|FastConf EMA|
|v_input_5|4|SlowConf EMA|
|v_input_6|0|What trades should be taken : : BOTH|SHORT|LONG|NONE|
|v_input_7|true|Stop Loss (ATR)|
|v_input_8|6|Take Profit 1 (ATR)|
|v_input_9|timestamp(01 Sep 2002 13:30 +0000)|Backtesting Start Time|
|v_input_10|timestamp(30 Sep 2099 19:30 +0000)|Backtesting End Time|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-10-09 00:00:00
end: 2023-04-13 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// @author ADHDCRYPT0

//@version=4
strategy(title = "EMA double crossover", shorttitle = "(TEST) double cross over", overlay = true, default_qty_value = 100, initial_capital = 1000, default_qty_type=strategy.percent_of_equity, pyramiding=0, process_orders_on_close=true)


// Variables
ema_len1 = input(9, title="Fast EMA")
ema_len2 = input(21, title="Slow EMA")
ema_len3 = input(5, title="Exit EMA")
ema_len4 = input(1, title="FastConf EMA")
ema_len5 = input(4, title="SlowConf EMA")

fastEMA = ema(open, ema_len1)
slowEMA = ema(open, ema_len2)
exitEMA = ema(open, ema_len3)
conf1EMA = ema(open, ema_len4)
conf2EMA = ema(open, ema_len5)
plot(fastEMA, title='fastEMA', transp=0, color=color.green)
plot(slowEMA, title='slowEMA', transp=0, color=color.red)
plot(exitEMA, title='exitEMA', transp=0, color=color.orange)
plot(conf1EMA, title='conf1EMA', transp=0, color=color.blue)
plot(conf2EMA, title='conf2EMA', transp=0, color=color.black)

vol = volume
volma = sma(volume, 7)
vol_cond = vol > volma

atr = atr(5)


// Entry Conditions and vol_cond
long = crossover(fastEMA, slowEMA) and (conf1EMA > conf2EMA) and (fastEMA < exitEMA)
short = crossunder(fastEMA, slowEMA) and (conf1EMA < conf2EMA) and (fastEMA > exitEMA)

tradeType = input("BOTH", title="What trades should be taken : ", options=["LONG", "SHORT", "BOTH", "NONE"])

pos = 0.0

if tradeType == "BOTH"
    pos := long ? 1 : short ? -1 : pos[1]
if tradeType == "LONG"
    pos := long ? 1 : pos[1]
if tradeType == "SHORT"
    pos := short ? -1 : pos[1]

longCond = long and (pos[1] != 1 or na(pos[1]))
shortCond = short and (pos[1] != -1 or na(pos[1]))

// EXIT FUNCTIONS //
sl = input(1, title="Stop Loss (ATR)", minval=0)
tp = input(6, title="Take Profit 1 (ATR)", minval=0)

// Simple Stop Loss + 2 Take Profit
if longCond
    strategy.exit("Long Exit", "buy", stop=atr * sl, limit=atr * tp)
if shortCond
    strategy.exit("Short Exit", "sell", stop=atr * sl, limit=atr * tp)
```