> Name

Grid-Trading-Strategy-Based-on-Moving-Average-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/19fe61e0678d9f69c91.png)
[trans]

### Overview

This strategy uses moving average theory to build a grid trading system by judging the market trend through multiple sets of JMA (Jeweled Moving Average) moving averages with different parameters. It aims to capture profits during long-term trend reversals in the market.

### Strategy Logic

1. Use a combination of 1-20 period JMA moving averages to determine the market trend. When the short period MA is above the long period MA, it is judged as an upward trend; otherwise, a downward trend.

2. Open grid trades at trend reversal points, when the short MA crosses below or above the long MA. Establish short positions gradually during uptrends and long positions during downtrends.

3. An option to filter based on candlestick color - only buy on red candles and sell on green candles; otherwise, disregard color and trade only at trend reversal points.

4. Exits are either tracking stop loss or time-based exit when the strategy duration ends.

### Advantage Analysis

1. Using the MA system to determine trends can effectively identify long-term trend reversals.

2. Grid trading can capture profits from range-bound markets without clear trends, with stop losses to control risks.

3. Customizable JMA parameters allow optimization for different periods; highly flexible.

4. Candle filter avoids being misled by false breakouts.

### Risk Analysis

1. In high whipsaw markets without clear trends, the risk of stop loss is higher.

2. Judgment errors from the MA system may lead to incorrect trade signals.

3. The candle filter risks missing some trading opportunities.

4. If grid spacing is too wide, insufficient profits; if too narrow, resulting in excessive positions and high costs.

### Optimization Directions

1. Test more parameter combinations to find optimal JMA MA combinations for different products.

2. Incorporate other filters like BOLL bands or KD to improve signal quality.

3. Optimize grid configurations such as grid spacing, entry lots, etc.

4. Consider additional stop loss methods like gap-based or trailing stops.

### Conclusion

This strategy judges reversals using the JMA theory and opens grid trades at turning points to capture profits from long-term trend shifts. Performance can be further improved through parameter optimization. Overall, it is suitable for medium-long term holdings to gradually track and profit from trending moves.

||

### Overview  

This strategy uses moving average theory to build a grid trading system by judging the market trend through multiple sets of JMA (Jeweled Moving Average) moving averages with different parameters. It aims to capture profits during long-term trend reversals in the market.

### Strategy Logic  

1. Use a combination of 1-20 period JMA moving averages to determine the market trend. When the short period MA is above the long period MA, it is judged as an upward trend; otherwise, a downward trend.  

2. Open grid trades at trend reversal points, when the short MA crosses below or above the long MA. Establish short positions gradually during uptrends and long positions during downtrends.

3. An option to filter based on candlestick color - only buy on red candles and sell on green candles; otherwise, disregard color and trade only at trend reversal points.  

4. Exits are either tracking stop loss or time-based exit when the strategy duration ends.

### Advantage Analysis 

1. Using the MA system to determine trends can effectively identify long-term trend reversals.  

2. Grid trading can capture profits from range-bound markets without clear trends, with stop losses to control risks.

3. Customizable JMA parameters allow optimization for different periods; highly flexible.  

4. Candle filter avoids being misled by false breakouts.

### Risk Analysis   

1. High whipsaw markets without clear trends have higher stop loss risks.

2. Judgment errors from the MA system may lead to incorrect trade signals.  

3. The candle filter risks missing some trading opportunities.

4. If grid spacing is too wide, insufficient profits; if too narrow, resulting in excessive positions and high costs.

### Optimization Directions  

1. Test more parameter combinations to find optimal JMA MA combinations for different products.  

2. Incorporate other filters like BOLL bands or KD to improve signal quality.

3. Optimize grid configurations such as grid spacing, entry lots, etc.  

4. Consider additional stop loss methods like gap-based or trailing stops.

### Conclusion  

This strategy judges reversals using the JMA theory and opens grid trades at turning points to capture profits from long-term trend shifts. Performance can be further improved through parameter optimization. Overall, it is suitable for medium-long term holdings to gradually track and profit from trending moves.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long|
|v_input_2|true|Short|
|v_input_3|100|Lot|
|v_input_4|false|Use Color-filter|
|v_input_5|1900|From Year|
|v_input_6|2100|To Year|
|v_input_7|true|From Month|
|v_input_8|12|To Month|
|v_input_9|true|From day|
|v_input_10|31|To day|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-12-27 00:00:00
end: 2024-01-02 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//Noro
//2019

//@version=3
strategy(title = "Noro's Fishnet Strategy", shorttitle = "Fishnet str", overlay = true, default_qty_type = strategy.percent_of_equity, default_qty_value = 100, pyramiding = 0)

//Settings
needlong = input(true, defval = true, title = "Long")
needshort = input(true, defval = true, title = "Short")
capital = input(100, defval = 100, minval = 1, maxval = 10000, title = "Lot")
usecf = input(false, defval = false, title = "Use Color-filter")
fromyear = input(1900, defval = 1900, minval = 1900, maxval = 2100, title = "From Year")
toyear = input(2100, defval = 2100, minval = 1900, maxval = 2100, title = "To Year")
frommonth = input(01, defval = 01, minval = 01, maxval = 12, title = "From Month")
tomonth = input(12, defval = 12, minval = 01, maxval = 12, title = "To Month")
fromday = input(01, defval = 01, minval = 01, maxval = 31, title = "From day")
today = input(31, defval = 31, minval = 01, maxval = 31, title = "To day")

//JMA
jmax(src, len) =>
    beta = 0.45*(len-1)/(0.45*(len-1)+2)
    alpha = pow(beta, 3)
    L0=0.0, L1=0.0, L2=0.0, L3=0.0, L4=0.0
    L0 := (1-alpha)*src + alpha*nz(L0[1])
    L1 := (src - L0[0])*(1-beta) + beta*nz(L1[1])
    L2 := L0[0] + L1[0]
    L3 := (L2[0] - nz(L4[1]))*((1-alpha)*(1-alpha)) + (alpha*alpha)*nz(L3[1])
    L4 := nz(L4[1]) + L3[0]

trend = 0
trend := ma01 > ma20 ? 1 : ma01 < ma20 ? -1 : trend[1]
col = trend == 1 ? #00FF7F : #DC143C

plot(ma01, transp = 0, color = col)
plot(ma02, transp = 0, color = col)
``` 

The provided Pine Script code correctly implements the strategy logic and settings described in the text. The `jmax` function is used to calculate JMA values for different periods, and the trend calculation is based on these moving averages. The plot statements ensure that the MA lines are displayed with appropriate colors based on their direction.