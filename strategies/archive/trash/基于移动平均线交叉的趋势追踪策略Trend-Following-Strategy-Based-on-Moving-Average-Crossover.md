> Name

Trend-Following-Strategy-Based-on-Moving-Average-Crossover

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1027409f8e007535a66.png)
[trans]
## Overview

This strategy determines the price trend direction by calculating two moving averages with different parameter settings and comparing their crossover situations, so as to implement trend following trading. When the fast moving average breaks through the slow moving average from below, it is judged as a bullish signal. When the fast moving average breaks through the slow moving average from above, it is judged as a bearish signal. This strategy can achieve judgment of trends of different cycles by adjusting parameters.

## Strategy Principle  

This strategy uses two sets of moving averages with different parameter settings for comparison. The first moving average parameter is set by `len1` and `type1`, and the second moving average parameter is set by `len2` and `type2`. Where `len1` and `len2` represent the cycle length of the two moving averages respectively, and `type1` and `type2` represent the algorithm type of the moving average.

When the fast moving average crosses above the slow moving average to form a golden cross, it is judged as a bullish signal. When the fast moving average crosses below the slow moving average to form a dead cross, it is judged as a bearish signal.

According to the direction of the crossover signal, long or short positions will be executed. When a bullish signal is triggered, if `needlong` parameter is true, a long position will be opened with the quantity `default_qty_value` or percentage of equity. When a bearish signal is triggered, if `needshort` parameter is true, a short position will be opened with the quantity `default_qty_value` or percentage of equity.

## Advantages

1. Support the combination of 7 different types of moving averages to flexibly adapt to market conditions  
2. Customize parameters of two moving averages to judge long-term and medium-short term trends  
3. Simple and clear signal judgment rules, easy to understand and implement  
4. Support long and short positions, can carry out trend tracking transactions

## Risks and Solutions

1. Moving averages have lagging properties and may miss price reversal points  
Solution: Appropriately shorten moving average cycles, or use in combination with other indicators

2. Not suitable for markets with high volatility and frequent reversals  
Solution: Add filtering conditions to avoid trading in oscillating markets  

3. There are certain risks of false signals  
Solution: Add other filtering indicators for combination to improve signal reliability   

## Optimization Directions    

1. Optimize the cycle combination of moving averages, and test the impact of long and short cycle parameters on strategy return  
2. Test the performance of different types of moving averages to find the optimal moving average algorithm  
3. Add trading volume variable or Bollinger Bands for combination to improve signal quality   
4. Optimize position management strategy to improve fixed position percentage_of_equity approach  

## Summary

This strategy judges the price trend by comparing the crossovers of two moving averages, and makes corresponding long and short operations to capture and profit from trends. The advantage is that the signal rules are simple and clear, the parameters are adjustable, the applicability is strong, and it can be optimized and adjusted for various market environments. Pay attention to prevent the lagging risks of moving averages and choppy markets, which can be reduced by adding other indicators for filtering to improve signal quality.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|long|
|v_input_2|true|short|
|v_input_3|15|Fast MA length|
|v_input_4|true|Fast MA Type|
|v_input_5_close|0|Fast MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_6|30|Slow MA length|
|v_input_7|true|Slow MA Type|
|v_input_8_close|0|Slow MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_9|false|Color of bar|
|v_input_10|false|1 SMA, 2 EMA, 3 VWMA, 4 DEMA, 5 TEMA, 6 KAMA, 7 Price Channel|


> Source (PineScript)

```pinescript
//@version=2
strategy(title = "Noro's MAs Cross Tests v1.0", shorttitle = "MAs Cross tests 1.0", overlay=true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100.0, pyramiding = 0)

needlong = input(true, "long")
needshort = input(true, "short")

len2 = input(15, defval = 15, minval = 2, maxval = 1000, title = "Fast MA length")
type2 = input(1, de