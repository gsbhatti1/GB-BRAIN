> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|2020|start year|
|v_input_int_2|true|start month|
|v_input_int_3|true|start day|
|v_input_int_4|2025|end year|
|v_input_int_5|true|end month|
|v_input_int_6|true|end day|
|v_input_1|false|Choose Time Interval|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-02-15 00:00:00
end: 2024-02-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © spacekadet17
// 
//@version=5

strategy(title="Trend Identifier Strategy", shorttitle="Trend Identifier Strategy", format=format.price, precision=4, overlay = false, initial_capital = 1000, pyramiding = 10, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, commission_type = strategy.commission.percent, commission_value = 0.03)

//start-end time
startyear = input.int(2020,"start year")
startmonth = input.int(1,"start month")
startday = input.int(1,"start day")
endyear = input.int(2025,"end year")
endmonth = input.int(1,"end month")
endday = input.int(1,"end day")

timeEnd = time <= timestamp(syminfo.timezone,endyear,endmonth,endday,0,0)
timeStart = time >= timestamp(syminfo.timezone,startyear,startmonth,startday,0,0)
choosetime = input(false,"Choose Time Interval")
condTime = (choosetime ? (timeStart and timeEnd) : true)

// time frame?
tfc = 1
if timeframe.isdaily
```

## Overview  

MyQuant Trend Identifier Strategy is a strategy for daily Bitcoin trading. It identifies market trends by calculating the moving average and its first and second order derivatives of the price, and makes buy and sell decisions accordingly.

## Strategy Principle   

The strategy first calculates the Adaptive Moving Average (ALMA) of the price and its first order and second order derivatives. The first order derivative reflects the rate of change of the price, and the second order derivative reflects the curvature of the price. It then judges the current trend to be upward, downward or fluctuating based on the values of the first and second order derivatives. Combined with stock indicators, it determines whether the buy or sell conditions are met.

Specifically, the strategy calculates the following indicators:  
- ALMA: Adaptive Moving Average of the price, length 140, fast factor 1.1, sigma 6  
- dema: First order derivative of ALMA  
- d2ema: First order derivative of dema, reflecting second order derivative of the price   
- index: Oscillation index of the dema indicator  
- ind: Deviation index of the price from its moving average  

When the buy condition is met, it calculates the number of shares to buy based on the signals from CAUSED Accumulation/Distribution Bands and Caused Exposure Top and Bottom Finder. When the sell condition is met, it sells all current positions.

## Advantages of the Strategy   

By combining trend and indicator judgments, this strategy can effectively identify turning points in market trends. Using the first and second order derivatives of prices to determine trends avoids the impact of price fluctuations and makes signals clearer. Compared to common moving average strategies, it has advantages such as higher accuracy.

## Risk Analysis   

This strategy is very sensitive to the selection of the trading time period and parameter adjustments. If the time period is selected improperly and important price turning points are not covered, the strategy will not be very effective. If the indicator parameters are set improperly, the buy and sell signals will be more affected by noise, thus impacting strategy returns. In addition, the stop loss conditions preset in the strategy also affect final returns.

## Directions for Optimization   

The strategy can be further optimized in the following aspects:  
1) Optimize logic for selecting time periods, through smarter selection of backtest and live trading time periods.   
2) Optimize indicator parameters, such as adjusting length of ALMA and dema etc.  
3) Add stop loss condition judgments to control maximum losses.  
4) Evaluate the effects across different cryptocurrencies and pick the ones that perform the best.

## Conclusion   

By calculating the first and second order derivatives of the adaptive moving average of prices, the MyQuant Trend Identifier Strategy effectively identifies the market trends for Bitcoin and makes corresponding buy and sell decisions. By combining multiple indicators for judgment, it avoids excessive noise interference with the signals. With further optimization of time and parameters, the performance of this strategy can be further improved.

||

## Overview  

MyQuant Trend Identifier Strategy is a strategy for daily Bitcoin trading. It identifies market trends by calculating the moving average and its first and second order derivatives of the price, and makes buy and sell decisions accordingly.

``` pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © spacekadet17

//@version=5
strategy(title="Trend Identifier Strategy", shorttitle="Trend Identifier Strategy", format=format.price, precision=4, overlay = false, initial_capital = 1000, pyramiding = 10, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, commission_type = strategy.commission.percent, commission_value = 0.03)

//start-end time
startyear = input.int(2020,"start year")
startmonth = input.int(1,"start month")
startday = input.int(1,"start day")
endyear = input.int(2025,"end year")
endmonth = input.int(1,"end month")
endday = input.int(1,"end day")

timeEnd = time <= timestamp(syminfo.timezone,endyear,endmonth,endday,0,0)
timeStart = time >= timestamp(syminfo.timezone,startyear,startmonth,startday,0,0)
choosetime = input(false,"Choose Time Interval")
condTime = (choosetime ? (timeStart and timeEnd) : true)

// time frame?
tfc = 1
if timeframe.isdaily
```

The script continues with the remaining code to complete the strategy implementation.