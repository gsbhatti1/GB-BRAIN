> Name

PPO Bull/Bear Divergence Trading Strategy

> Author

ChaoZhang

> Strategy Description


## Overview 

This strategy uses PPO divergence patterns for trend trading, and price high/low points for stop loss exits.

## How it Works

1. Calculate the PPO indicator.
2. Identify PPO bull/bear divergences.
3. Enter trades when price diverges from PPO.
4. Stop loss exits at recent price highs/lows.

## Advantages

- Captures PPO indicator's trendiness
- Strong divergence signals
- Clear stop loss points
- Identifies medium/long term trends

## Risks

- Moderate divergence recognition accuracy
- Unable to effectively control loss size
- Some lag, may misjudge trends
- Higher fees and slippage costs

## Optimization Directions

- Optimize PPO parameters for sensitivity
- Add filters with other indicators 
- Incorporate trailing stops for loss control
- Consider additional profit taking mechanisms
- Improve divergence pattern recognition logic

## Conclusion 

The strategy capitalizes on PPO's trending characteristics. Further improving parameters, logic and risk controls can enhance performance. But inherent risks need addressing. Overall a practical trend trading approach based on PPO divergences.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Use long term Divergences?|
|v_input_2|55|Lookback Period|
|v_input_3|12|fastLength|
|v_input_4|26|slowLength|
|v_input_5|9|signalLength|
|v_input_6|2|smoother|


> Source (PineScript)


```pinescript
/* backtest
start: 2022-09-14 00:00:00
end: 2023-03-11 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
// Credit to https://www.tradingview.com/script/p3oqCa56-Pekipek-s-PPO-Divergence-BETA/ (I just changed the visuals a bit)
// A simple strategy that uses the divergences to open trades and the highs/lows to close them. Would love to see any variations! - @scarf
// FYI: I have alerts set up for the purple and orange circles on daily forex charts and I get a lot of excellent trade entries.
strategy("PPO Bull/Bear Divergence to High/Low Trader", overlay=false)

source = open
long_term_div = input(true, title="Use long term Divergences?")
div_lookback_period = input(55, minval=1, title="Lookback Period")
fastLength = input(12, minval=1), slowLength=input(26,minval=1)
signalLength=input(9,minval=1)
smoother = input(2,minval=1)
fastMA = ema(source, fastLength)
slowMA = ema(source, slowLength)
macd = fastMA - slowMA
macd2=(macd/slowMA)*100
d = sma(macd2, smoother) // smoothing PPO

bullishPrice = low 

priceMins = bullishPrice > bullishPrice[1] and bullishPrice[1] < bullishPrice[2] or low[1] == low[2] and low[1] < low and low[1] < low[3] or low[1] == low[2] and low[1] == low[3] and low[1] < low and low[1] < low[4] or low[1] == low[2] and low[1] == low[3] and low[1] and low[1] == low[4] and low[1] < low and low[1] < low[5] // this line identifies bottoms and plateaus in the price
oscMins= d > d[1] and d[1] < d[2] // this line identifies bottoms in the PPO

BottomPointsInPPO = oscMins

bearishPrice = high
priceMax = bearishPrice < bearishPrice[1] and bearishPrice[1] > bearishPrice[2] or high[1] == high[2] and high[1] > high and high[1] > high[3] or high[1] == high[2] and high[1] == high[3] and high[1] > high and high[1] > high[4] or high[1] == high[2] and high[1] == high[3] and high[1] and high[1] == high[4] and high[1] > high and high[1] > high[5]  // this line identifies tops in the price
oscMax = d < d[1] and d[1] > d[2]   // this line identifies tops in the PPO

TopPointsInPPO = oscMax

currenttrough4=valuewhen (oscMins, d[1], 0) // identifies the value of PPO at the most recent BOTTOM in the PPO
lasttrough4=valuewhen (oscMins, d[1], 1) // NOT USED identifies the value of PPO at the second most recent BOTTOM in the PPO
currenttrough5=valuewhen (oscMax, d[1], 0) // identifies the value of PPO at the most recent TOP in the PPO
lasttrough5=valuewhen (oscMax, d[1], 1) // NOT USED identifies the value of PPO at the second most recent TOP in the PPO

currenttrough6=valuewhen (priceMins, low[1], 0) // this line identifies the low (price) at the most recent bottom in the Price
lasttrough6=valuewhen (priceMins, low[1], 1) // NOT USED this line identifies the low (price) at the second most recent bottom in the Price
currenttrough7=valuewhen (priceMax, high[1], 0) // this line identifies the high (price) at the most recent top in the Price
lasttrough7=valuewhen (priceMax, high[1], 1) // NOT USED this line identifies the high (price) at the second most recent top in the Price

delayedlow = priceMins and barssince(oscMins) < 3 ? low[1] : na
delayedhigh = priceMax and barssince(oscMax) < 3 ? high[1] : na

// only take tops/bottoms in price when tops/bottoms are less than 5 bars away
filter = barssince(priceMins) < 5 ? lowest(currenttrough6, 4) : na
filter2 = barssince(priceMax) < 5 ? highest(currenttrough7, 4) : na

//delayed bottom/top when oscillator bottom/top is earlier than price bottom/top
y11 = valuewhen(oscMins, delayedlow, 0)
y12 = valuewhen(oscMax, delayedhigh, 0)

// only take tops/bottoms in price when tops/bottoms are less than 5 bars away, since 2nd most recent top/bottom in osc
y2=valuewhen(oscMax, filter2, 1) // identifies the highest high in the tops of price with 5 bar lookback period SINCE the SECOND most recent top in PPO
y6=valuewhen(oscMins, filter, 1) // iden