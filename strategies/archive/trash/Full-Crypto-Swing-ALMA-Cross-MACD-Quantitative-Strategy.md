> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_1|true|From Day|
|v_input_2|true|From Month|
|v_input_3|2010|From Year|
|v_input_4|31|To Day|
|v_input_5|12|To Month|
|v_input_6|2031|To Year|
|v_input_7|false|Use Heikin Ashi Candles in Algo Calculations|
|v_input_8|20|Length Size Fast|
|v_input_9|40|Length Size Slow|
|v_input_10|0.9|Offset|
|v_input_11|5|Sigma|
|v_input_12|6|Fast Length|
|v_input_13|25|Slow Length|
|v_input_14|9|Signal Smoothing|
|v_input_15|2|takeProfit_long|
|v_input_16|0.2|stopLoss_long|
|v_input_17|0.05|takeProfit_short|
|v_input_18|true|stopLoss_short|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-04 00:00:00
end: 2023-12-04 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © exlux99

//@version=4
strategy(title = "Full Crypto Swing Strategy ALMA Cross", overlay = true, pyramiding=1, initial_capital = 1, default_qty_type=strategy.percent_of_equity, default_qty_value = 100, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.03)

// Time condition
fromDay = input(defval = 1, title = "From Day", minval = 1, maxval = 31)
fromMonth = input(defval = 1, title = "From Month", minval = 1, maxval = 12)
fromYear = input(defval = 2010, title = "From Year", minval = 1970)

// To Date Inputs
toDay = input(defval = 31, title = "To Day", minval = 1, maxval = 31)
toMonth = input(defval = 12, title = "To Month", minval = 1, maxval = 12)
toYear = input(defval = 2031, title = "To Year", minval = 1970)

// Heikin Ashi Candles
useHeikinAshi = input(false, title="Use Heikin Ashi Candles in Algo Calculations")

// ALMA Settings
fastLength = input(20, title="Fast Length")
slowLength = input(40, title="Slow Length")
offset = input(0.9, title="Offset", minval=0)
sigma = input(5, title="Sigma", minval=1)

// MACD Settings
shortEMA = input(6, title="Fast Length (MACD)")
longEMA = input(25, title="Slow Length (MACD)")
signalSmoothing = input(9, title="Signal Smoothing")

// Take Profit and Stop Loss
takeProfit_long = input(2.0, title="Take Profit for Long Positions")
stopLoss_long = input(0.2, title="Stop Loss for Long Positions", minval=0)
takeProfit_short = input(0.05, title="Take Profit for Short Positions", minval=0)
stopLoss_short = input(true, title="Stop Loss for Short Positions")

// ALMA Calculation
almaFast = alma(close, fastLength, offset, sigma)
almaSlow = alma(close, slowLength, offset, sigma)

// MACD Calculation
[macdLine, signalLine, _] = macd(close, shortEMA, longEMA, signalSmoothing)

// Generate Signals
longSignal = crossover(almaFast, almaSlow) and macdLine > 0
shortSignal = crossunder(almaFast, almaSlow) and macdLine < 0

// Plot ALMA Lines and MACD
plot(almaFast, title="ALMA Fast", color=color.blue)
plot(almaSlow, title="ALMA Slow", color=color.red)

hline(0, "MACD Zero Line")

plot(macdLine, title="MACD Line", color=color.green)
plot(signalLine, title="Signal Line", color=color.orange)

// Entry Conditions
if (longSignal and useHeikinAshi == true)
    strategy.entry("Long", strategy.long, when=heikinashi(close))
else if (longSignal and useHeikinAshi == false) 
    strategy.entry("Long", strategy.long)

if (shortSignal and useHeikinAshi == true)
    strategy.entry("Short", strategy.short, when=heikinashi(close))
else if (shortSignal and useHeikinAshi == false)
    strategy.entry("Short", strategy.short)

// Exit Conditions
longExit = ta.atr(14) * stopLoss_long
shortExit = ta.atr(14) * -stopLoss_short

if (strategy.position_size > 0 and close < strategy.opentrades[-1].entry_price - longExit)
    strategy.exit("Long Take Profit", "Long")
else if (strategy.position_size < 0 and close > strategy.opentrades[-1].entry_price + shortExit)
    strategy.exit("Short Take Profit", "Short")

```

This completes the translation of your trading strategy document into English. The PineScript code has been fully translated while preserving the original formatting and structure.