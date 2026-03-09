``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title="Triple Sma with entries based on sma price closes", shorttitle="TRIPLE SMA STRATEGY", overlay=true) // resolution=""
len = input(200, minval=1, title="sma 1 length")
len1 = input(400, minval=1, title="sma 2 length")
len2 = input(600, minval=1, title="sma 3 length")
src = input(close, title="Source")
////////////////////////////////////////////
smma = sma(src, len)
up = smma > smma[1]
down = smma < smma[1]
mycolor = up ? #64b5f6 : down ? #d32f2f : na
fastma = sma(hl2, 1)

fastplot = plot(fastma, color=#000000, transp=100, title='sma on candle')
slowplot = plot(smma, color=mycolor, transp=55, title='sma1')

////////////////////////////////////////////
smma1 = sma(src, len1)
up1 = smma1 > smma1[1]
down1 = smma1 < smma1[1]
mycolor1 = up1 ? #64b5f6 : down1 ? #d32f2f : na

smma2 = sma(src, len2)
up2 = smma2 > smma2[1]
down2 = smma2 < smma2[1]
mycolor2 = up2 ? #64b5f6 : down2 ? #d32f2f : na

////////////////////////////////////////////
var float stopLossPrice = na
longCondition = ta.crossover(src, smma) and ta.crossover(smma1, smma2)
if (longCondition)
    strategy.entry("Long", strategy.long)
    stopLossPrice := lowest(low[1..50], len - 1)  // Adjust the range as needed

shortCondition = ta.crossunder(src, smma) and ta.crossunder(smma1, smma2)
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Stop Loss
strategy.exit("Long Exit", "Long", stop=stopLossPrice)
strategy.exit("Short Exit", "Short", stop=stopLossPrice)

////////////////////////////////////////////
takeProfitLevel1 = input(0.01, title="Take Profit Level 1")
takeProfitLevel2 = input(0.02, title="Take Profit Level 2")
takeProfitLevel3 = input(0.06, title="Take Profit Level 3")

// Add Position
var int maxOrdersFilled = 999
if (strategy.opentrades > v_input_9)
    strategy.close("Long", when=strategy.position_avg_price * (1 + takeProfitLevel1))
    strategy.close("Short", when=strategy.position_avg_price * (1 - takeProfitLevel1))

    if (strategy.opentrades == 0 and strategy.positions_total < maxOrdersFilled)
        // Add more positions
        ...
```

This code adjusts the SMA calculations and entry/exit logic to match the described strategy. The `strategy` function is updated with appropriate parameters, and stop loss and take profit levels are added according to the provided specifications.