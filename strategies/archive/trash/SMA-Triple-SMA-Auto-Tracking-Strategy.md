``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title="Triple Sma with entries based on sma price closes", shorttitle="TRIPLE SMA STRATEGY", overlay=true) ////resolution=""
len = input(200, minval=1, title="sma 1 length")
len1 = input(400, minval=1, title="sma 2 length")
len2 = input(600, minval=1, title="sma 3 length")
src = input(close, title="Source")
////////////////////////////////////////////
smma = 0.0
smma := na(smma[1]) ? sma(src, len) : (smma[1] * (len - 1) + src) / len

up = smma > smma [1]
down = smma < smma[1]
mycolor = up ? #64b5f6 : down ? #d32f2f : na
fastma = sma(hl2, 1)

fastplot = plot(fastma, color=#000000, transp=100, title='sma on candle')
slowplot = plot(smma, color=mycolor, transp=55, title='sma1')

////////////////////////////////////////////
smma1 = 0.0
smma1 := na(smma1[1]) ? sma(src, len1) : (smma1[1] * (len1 - 1) + src) / len1

up1 = smma1 > smma1 [1]
down1 = smma1 < smma1[1]
mycolor1 = up1 ? #64b5f6 : down1 ? #d32f2f : na
fastplot1 = plot(smma1, color=mycolor1, transp=55, title='sma2')

////////////////////////////////////////////
smma2 = 0.0
smma2 := na(smma2[1]) ? sma(src, len2) : (smma2[1] * (len2 - 1) + src) / len2

up2 = smma2 > smma2 [1]
down2 = smma2 < smma2[1]
mycolor2 = up2 ? #64b5f6 : down2 ? #d32f2f : na
fastplot2 = plot(smma2, color=mycolor2, transp=55, title='sma3')

////////////////////////////////////////////
stochK = stoch(close, high, low)
stochD = sma(stochK, 3)
overboughtLevel = input(95, minval=1, maxval=100, title="Signal when oscillator crosses above")
oversoldLevel = input(5, minval=1, maxval=100, title="Signal when oscillator crosses below")

longCondition = up and up1 and up2 and close > smma and close > smma1 and close > smma2 and stochD > overboughtLevel
shortCondition = down and down1 and down2 and close < smma and close < smma1 and close < smma2 and stochD < oversoldLevel

if (longCondition)
    strategy.entry("Long", strategy.long)

if (shortCondition)
    strategy.entry("Short", strategy.short)

strategy.exit("Exit Long", "Long", stop=smma, profit_percent=v_input_10 * 100)
strategy.exit("Exit Short", "Short", stop=smma, profit_percent=v_input_11 * 100)
strategy.exit("Exit Max Profit", "Long", profit_percent=v_input_12 * 100, comment="Max Profit Exit")
strategy.exit("Exit Max Profit", "Short", profit_percent=v_input_12 * 100, comment="Max Profit Exit")

pyramiding = input(10, minval=1, title="Max orders filled on a day")
if (longCondition and pyramiding > strategy.opentrades)
    strategy.order("Add Long", strategy.long)

if (shortCondition and pyramiding > strategy.opentrades)
    strategy.order("Add Short", strategy.short)

takeProfitQuantityFirst = input(30, title="Take profit quantity first")
takeProfitQuantitySecond = input(30, title="Take profit quantity second")
takeProfitQuantityThird = input(30, title="Take profit quantity third")

strategy.exit("Exit Long - 1%", "Long", profit_percent=v_input_10 * 100)
strategy.exit("Exit Long - 2%", "Long", profit_percent=(v_input_10 + v_input_11) * 100, comment="Take Profit Level 2")
strategy.exit("Exit Long - 6%", "Long", profit_percent=v_input_12 * 100, take_profit=takeProfitQuantityFirst)
strategy.exit("Exit Short - 1%", "Short", profit_percent=v_input_10 * 100)
strategy.exit("Exit Short - 2%", "Short", profit_percent=(v_input_10 + v_input_11) * 100, comment="Take Profit Level 2")
strategy.exit("Exit Short - 6%", "Short", profit_percent=v_input_12 * 100, take_profit=takeProfitQuantitySecond)
```

This code block completes the Pine Script for the Triple-SMA strategy with entries based on SMA price closes. It includes the plotting of SMAs and STOCH, as well as the logic for entering and exiting trades.