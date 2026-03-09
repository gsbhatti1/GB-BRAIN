> Name

Dual-directional ADX Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ad58a4a820714a412d.png)
 [trans]
### Overview

The dual-directional ADX trading strategy is a quantitative strategy that uses the Average Directional Index (ADX) indicator to execute trades in both long and short directions. The strategy generates trading signals by calculating the difference between the ADX indicator and the DIPlus and DIMinus indicators and setting thresholds to determine long and short entries for profit.

### Strategy Logic

1. Calculate the True Range
2. Calculate the Directional Movement Plus and Directional Movement Minus
3. Calculate the Smoothed True Range  
4. Calculate the Smoothed Directional Movement Plus and Smoothed Directional Movement Minus
5. Calculate the DIPlus, DIMinus and ADX indicators  
6. Calculate the difference between DIPlus & ADX and DIMinus & ADX
7. Set thresholds for long and short trade differences
8. Generate trading signals when difference exceeds thresholds
9. Create buy and sell orders  

The core of this strategy is using ADX and directional movement indicators to determine trend direction and strength, combined with difference threshold rules to filter signals and automate trading.  

### Advantage Analysis

1. ADX accurately captures market trend  
2. Difference threshold rules effectively filter false signals
3. Dual-directional trading fully captures long and short opportunities  
4. Fully automated trading without manual intervention  
5. Clear strategy logic, easy to understand and modify  

### Risk Analysis

1. ADX has lag, may miss trend turning points  
2. Increased risk from dual-directional trading, larger losses
3. Improper parameter setting may cause over-trading  
4. Backtest data cannot represent real market, real trading risk exists  

Solutions:  

1. Confirm signals with other indicators  
2. Optimize parameters, control trade frequency  
3. Strict position sizing to manage position size  

### Optimization Directions

1. Optimize ADX parameters to improve sensitivity  
2. Add other indicators to filter signals  
3. Apply machine learning to optimize parameters  
4. Use advanced stop loss strategies to control losses 
5. Combine with model predictions for more accurate signals  

### Conclusion

The dual-direction ADX trading strategy overall is a very practical quantitative strategy. It identifies trends using the ADX indicator and captures trading opportunities in both directions. Meanwhile, it uses difference thresholds to validate signal effectiveness. The strategy has clear and simple logic that is easy to modify and optimize. It is a dual-directional trend following system. Further improvements in stability and profitability can be achieved through parameter optimization, stop loss strategies, and signal filtration.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|20|Threshold|
|v_input_3|10|Long Difference|
|v_input_4|10|Short Difference|
|v_input_bool_1|true|(?Monthly Performance) Show Monthly Performance?|
|v_input_5|0|Location: Bottom Right, Top Right, Top Left, Bottom Left, Middle Right, Bottom Center|
|v_input_6|0|Size: Small, Tiny, Normal, Large|
|v_input_color_1|#07e2f2|Background Color|
|v_input_color_2|#000000|Month/Year Heading Color|
|v_input_color_3|white|Month PnL Data Color|
|v_input_color_4|#000000|Year PnL Data Color|
|v_input_color_5|white|Table Border Color|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © MAURYA_ALGO_TRADER

//@version=5
strategy("Monthly Performance", overlay=true)


len = input(14)
th = input(20)

TrueRange = math.max(math.max(high - low, math.abs(high - nz(close[1]))), math.abs(low - nz(close[1])))
DirectionalMovementPlus = high - nz(high[1]) > nz(low[1]) - low ? math.max(high - nz(high[1]), 0) : 0
DirectionalMovementMinus = nz(low[1]) - low > high - nz(high[1]) ? math.max(nz(low[1]) - low, 0) : 0

SmoothedTrueRange = 0.0
SmoothedTrueRange := nz(SmoothedTrueRange[1]) - nz(SmoothedTrueRange[1]) / len + TrueRange

SmoothedDirectionalMovementPlus = 0.0
SmoothedDirectionalMovementPlus := nz(SmoothedDirectionalMovementPlus[1]) - nz(SmoothedDirectionalMovementPlus[1]) / len + DirectionalMovementPlus

SmoothedDirectionalMovementMinus = 0.0
SmoothedDirectionalMovementMinus := nz(SmoothedDirectionalMovementMinus[1]) - nz(SmoothedDirectionalMovementMinus[1]) / len + DirectionalMovementMinus

DIPlus = SmoothedDirectionalMovementPlus / SmoothedTrueRange * 100
DIMinus = SmoothedDirectionalMovementMinus / SmoothedTrueRange * 100
```