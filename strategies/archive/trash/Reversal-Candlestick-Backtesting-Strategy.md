---

> Name

Reversal-Candlestick-Backtesting-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/7f07f6bbf203fc7150.png)
 [trans]
## Overview 

This strategy identifies candlestick patterns to track trading signals and incorporates take profit and stop loss logic for automated trading. It goes long or short when reversal patterns are identified and closes positions when take profit or stop loss is triggered.

## Strategy Logic

1. Identify candlestick patterns: When the candle body size is smaller than a threshold, and the open equals the close, it is identified as a tracking signal.

2. Long/short: When a reversal candlestick pattern is identified, go long if the previous close is higher than two days ago; go short if the previous close is lower than two days ago.

3. Take profit/Stop loss: When the price reaches the entry price plus take profit points when going long, take profit; when the price reaches the entry price minus take profit points when going short, take profit; when the price triggers a stop loss point after being long or short, stop loss.

## Advantages

1. Using candlestick reversal patterns can effectively capture turning points of prices, enhancing the validity of trading signals.

2. Combining take profit and stop loss mechanisms can effectively control risks, lock in profits, and avoid expanding losses.

3. Automated trading without manual intervention reduces trading costs and improves efficiency.

## Risks 

1. Subjectivity in candlestick pattern identification may lead to misjudgments.

2. Improper take profit/stop loss point settings may miss larger trends or stop out prematurely.

3. Strategy parameters need constant testing and optimization, otherwise leading to overfitting.

## Optimization Directions

1. Optimize the conditions for identifying candlesticks by incorporating more indicators to improve accuracy.

2. Test on different trading instruments, adjust take profit/stop loss points, optimize parameters.

3. Enrich strategy logic by adding algorithms to identify more trading signals.

4. Add a position sizing module to dynamically adjust positions based on reference indicators.

## Conclusion

This strategy identifies reversal signals through candlestick patterns and sets take profit and stop loss rules for automated trading. The strategy is simple and practical to a certain extent, but there is room for improvement in terms of identification accuracy and parameter optimization. Further testing and optimization are recommended before applying it in live trading.

||

## Overview

This strategy identifies candlestick patterns to track trading signals and incorporates take profit and stop loss logic for automated trading. It goes long or short when reversal patterns are identified and closes positions when take profit or stop loss is triggered.

## Strategy Logic

1. Identify candlestick patterns: When the candle body size is smaller than a threshold, and the open equals the close, it is identified as a tracking signal.

2. Long/short: When a reversal candlestick pattern is identified, go long if the previous close is higher than two days ago; go short if the previous close is lower than two days ago.

3. Take profit/Stop loss: When the price reaches the entry price plus take profit points when going long, take profit; when the price reaches the entry price minus take profit points when going short, take profit; when the price triggers a stop loss point after being long or short, stop loss.

## Advantages

1. Candlestick reversal patterns effectively capture turning points of prices, enhancing the validity of trading signals.

2. Combining take profit and stop loss mechanisms can effectively control risks, lock in profits, and avoid expanding losses.

3. Automated trading without manual intervention reduces trading costs and improves efficiency.

## Risks 

1. Subjectivity in candlestick pattern identification may lead to misjudgments.

2. Improper take profit/stop loss point settings may miss larger trends or stop out prematurely.

3. Strategy parameters need constant testing and optimization, otherwise leading to overfitting.

## Optimization Directions

1. Optimize the conditions for identifying candlesticks by incorporating more indicators to improve accuracy.

2. Test on different trading instruments, adjust take profit/stop loss points, optimize parameters.

3. Enrich strategy logic by adding algorithms to identify more trading signals.

4. Add a position sizing module to dynamically adjust positions based on reference indicators.

## Conclusion

This strategy identifies reversal signals through candlestick patterns and sets take profit and stop loss rules for automated trading. The strategy is simple and practical to a certain extent, but there is room for improvement in terms of identification accuracy and parameter optimization. Further testing and optimization are recommended before applying it in live trading.

---

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|10|Take Profit pip|
|v_input_2|10|Stop Loss pip|
|v_input_3|0.5|Min. Size Body pip|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-12-26 00:00:00
end: 2024-01-25 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 30/01/2019
//   This is a candlestick where the open and close are the same. 
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
////////////////////////////////////////////////////////////
strategy(title = "Doji Backtest", overlay = true)
input_takeprofit = input(10, title="Take Profit pip", step=0.01)
input_stoploss = input(10, title="Stop Loss pip", step=0.01)
input_minsizebody = input(0.5, title="Min. Size Body pip", step=0.01)
barcolor(abs(close - open) <= input_minsizebody ? open == close ? yellow : na : na)
possell = 0.0
posbuy = 0.0
pospricebuy = 0.0
pospricesell = 0.0
barcolornow = blue
pospricesell := close< close[2] ? abs(close - open) <= input_minsizebody ? open == close ? close : nz(pospricesell[1], 0) : nz(pospricesell[1], 0) : nz(pospricesell[1], 0) 
possell := iff(pospricesell > 0 , -1, 0)
barcolornow := possell == -1 ? red: posbuy == 1 ? green : blue 
pospricesell := iff(low <= pospricesell - input_takeprofit and pospricesell > 0, 0 ,  nz(pospricesell, 0))
pospricesell := iff(high >= pospricesell + input_stoploss and pospricesell > 0, 0 ,  nz(pospricesell, 0))
pospricebuy := close > close[2] ? abs(close - open) <= input_minsizebody ? open == close ? close : nz(pospricebuy[1], 0) : nz(pospricebuy[1], 0) : nz(pospricebuy[1], 0) 
posbuy := iff(pospricebuy > 0 , 1, 0)
barcolornow := posbuy == 1 ? green: barcolornow
pospricebuy := iff(high >= pospricebuy + input_takeprofit and pospricebuy > 0, 0 ,  nz(pospricebuy, 0))
pospricebuy := iff(low <= pospricebuy - input_stoploss and pospricebuy > 0, 0 ,  nz(pospricebuy, 0))
barcolor(barcolornow)
if (posbuy == 0 and possell == 0) 
    strategy.close_all()
if (posbuy == 1)
    strategy.entry("Long", strategy.long)
if (possell == -1)
    strategy.entry("Short", strategy.short)	   	    
pospricebuy := iff(high <= pospricebuy + input_takeprofit and pospricebuy > 0, 0 ,  nz(pospricebuy, 0))
pospricebuy := iff(low >= pospricebuy - input_stoploss and pospricebuy > 0, 0 ,  nz(pospricebuy, 0))
pospricesell := iff(low <= pospricesell - input_takeprofit and pospricesell > 0, 0 ,  nz(pospricesell, 0))
pospricesell := iff(high >= pospricesell + input_stoploss and pospricesell > 0, 0 ,  nz(pospricesell, 0))

```

> Detail

https://www.fmz.com/strategy/440100

> Last Modified

2024-01-26 16:04