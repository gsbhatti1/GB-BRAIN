> Name

Long-Term-Quantitative-Strategy-Based-on-Volatility-Bands-Reversal

> Author

ChaoZhang

> Strategy Description


This article explains in detail a long-term quantitative trading strategy that uses volatility bands to identify reversals. The strategy takes long positions when prices break through the lower band, allowing for顺势跟踪操作.

I. Strategy Logic

The core indicator is volatility bands, calculated as:

1. Compute middle, upper, and lower moving average bands.
2. A buy signal is generated when price breaks up through the lower band.
3. A sell signal is generated when price breaks the upper band.
4. Exits can be on sell signals or upper band breaks.
5. Stop loss is set as a fixed percentage.

This allows buying into downward phases, then exiting via profit taking or stops to capitalize on reversals.

II. Advantages of the Strategy

The biggest advantage is using volatility bands to identify reversal points, which is a mature technical analysis method.

Another advantage is the stop loss mechanism that controls risk per trade.

Finally, pyramiding helps in phased profits after reversals.

III. Potential Risks

However, some potential issues exist:

Firstly, moving averages have lag and may cause missed best entry timing.
Secondly, profit taking and stop loss levels require careful optimization.
Lastly, long holding periods mean enduring certain drawdowns.

IV. Summary

In summary, this article has detailed a long-term quantitative trading strategy using volatility bands to capitalize on reversals. It can effectively detect reversal opportunities for long-term holdings but requires prevention of MA lags and optimized exits. Overall, it provides a robust long-term trading approach.

||

This article explains in detail a long-term quantitative trading strategy that uses volatility bands to identify reversals. The strategy takes long positions when prices break through the lower band to ride the upside move.

I. Strategy Logic

The core indicator is volatility bands, calculated as:

1. Compute middle, upper, and lower moving average bands.
2. A buy signal is generated when price breaks up through the lower band.
3. A sell signal is generated when price breaks the upper band.
4. Exits can be on sell signals or upper band breaks.
5. Stop loss is set as a fixed percentage.

This allows buying into downward phases, then exiting via profit taking or stops to capitalize on reversals.

II. Advantages of the Strategy

The biggest advantage is using volatility bands to identify reversal points, which is a mature technical analysis method.

Another advantage is the stop loss mechanism that controls risk per trade.

Finally, pyramiding also helps in phased profits after reversals.

III. Potential Risks

However, some potential issues exist:

Firstly, moving averages have lag and may cause missed best entry timing.
Secondly, profit taking and stop loss levels require careful optimization.
Lastly, long holding periods mean enduring certain drawdowns.

IV. Summary

In summary, this article has explained a long-term quantitative trading strategy using volatility bands to capitalize on reversals. It can effectively detect reversal opportunities for long-term holdings but requires prevention of MA lags and optimized exits. Overall, it provides a robust long-term trading approach.

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|8|Band Average|
|v_input_2|13|Volatility Period|
|v_input_3|3.33|Deviation Factor|
|v_input_4|0.9|Lower Band Adjustment|
|v_input_5|10|Risk % of capital|
|v_input_6|6|Stop Loss|
|v_input_7|0|Exit on: touch_upperband|Sell_Signal|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-09-07 00:00:00
end: 2023-09-12 04:00:00
period: 14m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © ediks123

//strategy logic has been borrowed from ceyhun and tweaked the settings for back testing

//@version=4


//SPY 4 hrs settings 8, 13 , 3.33 , 0.9 on 4 hrs chart
//QQQ above settings is good, but 13, 13 has less number of bars 
//QQQ 4 hrs settings 13, 13 , 3.33 , 0.9 on 4 hrs chart

strategy(title="Volatility Bands Reversal Strategy", shorttitle="VolatilityBandReversal" , overlay=true, pyramiding=2, default_qty_type=strategy.percent_of_equity, default_qty_value=20, initial_capital=10000, currency=currency.USD)  //default_qty_value=10, default_qty_type=strategy.fixed,


av = input(8, title="Band Average")
vp = input(13, title="Volatility Period")
df = input(3.33,title="Deviation Factor",minval=0.1)
lba = input(0.9,title="Lower Band Adjustment",minval=0.1)

riskCapital = input(title="Risk % of capital", defval=10, minval=1)
stopLoss=input(6,title="Stop Loss",minval=1)

exitOn=input(title="Exit on", defval="touch_upperband", options=["Sell_Signal", "touch_upperband"])



src = hlc3
typical = src >= src[1] ? src - low[1] : src[1] - low
deviation = sum( typical , vp )/ vp * df
devHigh = ema(deviation, av)
devLow = lba * devHigh
medianAvg = ema(src, av)

emaMediaAvg=ema(medianAvg, av)

upperBandVal= emaMediaAvg + devHigh
lowerbandVal= emaMediaAvg - devLow
MidLineVal=sma(medianAvg, av)

UpperBand = plot ( upperBandVal, color=#EE82EE, linewidth=2, title="UpperBand")
LowerBand = plot ( lowerbandVal , color=#EE82EE, linewidth=2, title="LowerBand")
MidLine = plot (MidLineVal, color=color.blue, linewidth=2, title="MidLine")
buyLine = plot ( (lowerbandVal + MidLineVal )/2  , color=color.blue, title="BuyLine")

up=ema(medianAvg, av) + devHigh
down=ema(medianAvg, av) - devLow


ema50=ema(hlc3,50)
plot ( ema50, color=color.orange, linewidth=2, title="ema 50")

//outer deviation

//deviation1 = sum( typical , vp )/ vp * 4
//devHigh1 = ema(deviation, av)
//devLow1 = lba * devHigh
//medianAvg1 = ema(src, av)

//UpperBand1 = plot (emaMediaAvg + devHigh1, color=color.red, linewidth=3, title="UpperBand1")
//LowerBand1 = plot (emaMediaAvg - devLow1, color=color.red, linewidth=3, title="LowerBand1")
//


///Entry Rules
//1) First candle close below the Lower Band of the volatility Band
//2) Second candle close above the lower band
//3) Third Candle closes above previous candle
Buy = close[2] < down[2] and close[1]>down[1] and close>close[1]
//plotshape(Buy,color=color.blue,style=shape.arrowup,location=location.belowbar, text="Buy")
//barcolor(close[2] < down[2] and close[1]>down[1] and close>close[1] ? color.blue :na )
//bgcolor(close[2] < down[2] and close[1]>down[1] and close>close[1] ? color.green :na )

///Exit Rules
//1) One can have a static stops initially followed by an trailing stop based on the risk the people are willing to take
//2) One can exit with human based decisions or predefined target exits. Choice of deciding the stop loss and profit targets are left to the readers.
Sell = close[2] > up[2] and close[1]<up[1]
```