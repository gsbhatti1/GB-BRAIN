> Name

Dual-Moving-Average-Trend-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/8a528a6bbc068fb910.png)
[trans]

## Overview

The Dual Moving Average Trend Tracking strategy (Dual-Moving-Average-Trend-Tracking-Strategy) is a quantitative trading strategy that uses both fast and slow moving averages to determine trend direction, with the candlestick body color serving as an entry signal. The strategy possesses characteristics of both trend following and mean reversion.

## Principle

The strategy employs a 20-period slow moving average to identify overall trend direction. An upward crossover indicates an uptrend, while a downward crossover suggests a downtrend. A 5-period fast moving average serves as an entry filter; trades are triggered only when the price breaks above this fast moving average. Additionally, it checks the color of the recent N candlesticks' bodies. Long signals are generated if the body colors turn red in an uptrend, and short signals are issued if the body colors turn green in a downtrend to avoid false breakouts.

The strategy considers three dimensions—overall trend, short-term moving average, and candlestick body—to enhance signal reliability. Signals are only emitted when all three align, effectively filtering out some noise.

## Advantages

1. Combines both trend following and mean reversion characteristics, making it adaptable across different market environments.
2. Multi-dimensional signal validation helps avoid false signals and improves win rate.
3. The strategy offers significant parameter optimization space by adjusting the moving average lengths, number of candlesticks checked for color, etc.
4. The logic is clear and concise, making it easy to understand and suitable for beginners.

## Risks

1. During volatile market conditions, the strategy may experience drawdowns due to false breakouts. Consider adjusting moving average parameters or adding stop-loss mechanisms.
2. In sideways markets, the strategy may generate whipsaws leading to losses. Adjust the number of candlesticks checked for body color or disable mean reversion as needed.
3. Extensive backtesting is essential to ensure proper parameter settings and overall performance.

## Optimization Directions

1. Experiment with different types of moving averages such as Exponential Moving Average (EMA) or Kaufman Adaptive Moving Average (KAMA).
2. Implement position sizing rules, like fixed quantity trading or percentage-of-equity-based adjustment.
3. Integrate stop-loss mechanisms to exit positions if the price closes below the slow moving average.
4. Test across different instruments to assess stability and adaptability.

## Conclusion

The Dual-Moving-Average-Trend-Tracking-Strategy combines trend following with mean reversion to capture both long-term trends and short-term opportunities for additional gains. By optimizing parameters and enhancing mechanisms, it can further expand profitability. Despite its simplicity, this strategy is ideal for beginners to learn about combining trend-following and mean-reversion trading techniques. However, comprehensive validation across different instruments and parameter settings is necessary to ensure stability and profitability.

||

## Overview  

The Dual Moving Average Trend Tracking strategy utilizes both fast and slow moving averages to determine trend direction with candlestick body color as an entry signal. This strategy combines trend following and mean reversion characteristics. 

## Principle  

The strategy uses a 20-period slow moving average to define the overall trend. An upward crossover suggests an uptrend, while a downward crossover indicates a downtrend. A 5-period fast moving average acts as an entry filter; trades are triggered only when the price breaks above this fast moving average. Additionally, it checks the color of the recent N candlesticks' bodies. Long signals are generated if body colors turn red in an uptrend, and short signals are issued if body colors turn green in a downtrend to avoid false breakouts.

The strategy examines three dimensions—overall trend, short-term moving average, and candlestick body—to improve signal reliability. Signals are only emitted when all three align, filtering out some noise.

## Advantages

1. Combines both trend following and mean reversion characteristics, making it adaptable across different market environments.
2. Multi-dimensional signal validation helps avoid false signals and improves win rate.
3. The strategy offers significant parameter optimization space by adjusting moving average lengths, number of candlesticks checked for color, etc.
4. The logic is clear and concise, making it easy to understand and suitable for beginners.

## Risks

1. Whipsaws during volatile markets can lead to losses/drawdowns. Consider adjusting moving average parameters or adding stop-loss mechanisms.
2. In sideways market conditions, the strategy may generate whipsaws leading to losses. Try tweaking the number of candlesticks checked for body color or disable mean reversion.
3. Extensive backtesting is essential to ensure proper parameter settings and overall performance.

## Enhancement

1. Experiment with different types of moving averages such as Exponential Moving Average (EMA) or Kaufman Adaptive Moving Average (KAMA).
2. Implement position sizing rules, like fixed quantity trading or percentage-of-equity-based adjustment.
3. Integrate stop-loss mechanisms to exit positions if the price closes below the slow moving average.
4. Test across different instruments to verify stability and adaptability.

## Conclusion

The Dual-Moving-Average-Trend-Tracking-Strategy combines trend following with mean reversion to capture both long-term trends and short-term opportunities for additional gains. By optimizing parameters and enhancing mechanisms, it can further expand profitability. Despite its simplicity, this strategy is ideal for beginners to learn about combining trend-following and mean-reversion trading techniques. However, comprehensive validation across different instruments and parameter settings is necessary to ensure stability and profitability.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|long|
|v_input_2|true|short|
|v_input_3|7|Type of Slow MA|
|v_input_4_close|0|Source of Slow MA: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_5|true|Use fast MA Filter|
|v_input_6|5|fast MA Period|
|v_input_7|20|slow MA Period|
|v_input_8|2|Bars Q|

> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-04 00:00:00
end: 2024-02-03 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy(title = "Noro's Trend MAs 1.5", shorttitle = "Trend MAs 1.5", overlay=true, default_qty_type = strategy.percent_of_equity, default_qty_value=100.0, pyramiding=0)

//Settings
needlong = input(true, "long")
needshort = input(true, "short")
type = input(7, defval = 7, minval = 1, maxval = 7, title = "Type of Slow MA")
src = input(close, defval = close, title = "Source of Slow MA")
usefastsma = input(true, "Use fast MA Filter")
fastlen = input(5, defval = 5, minval = 1, maxval = 50, title = "fast MA Period")
len = input(20, defval = 20, minval = 2, maxval = 200, title = "slow MA Period")
bars = input(2, defval = 2, minval = 0, maxval = 3, title = "Bars Q")

fastsma = ema(src, fastlen)

//DEMA
dema = 2 * ema(src, len) - ema(ema(close, len), len)

//TEMA
xPrice = close
xEMA1 = ema(src, len)
xEMA2 = ema(xEMA1, len)
xEMA3 = ema(xEMA2, len)
tema = 3 * xEMA1 - 3 * xEMA2 + xEMA3

//KAMA
xvnoise = abs(src - src[1])
nfastend = 0.20
nslowend = 0.05
nsignal = abs(src - src[len])
nnoise = sum(xvnoise, len)
nefratio = iff(nnoise != 0, nsignal / nnoise, 0)
nsmooth = pow(nefratio * (nfastend - nslowend) + nslowend, 2) 
kama = nz(kama[1]) + nsmooth * (src - nz(kama[1]))

//PriceChannel
lasthigh = highest(src, len)
lastlow = lowest(src, len)
center = (lasthigh + lastlow) / 2

//Trend
ma = type == 1 ? sma(src, len) : type == 2 ? ema(src, len) : type == 3 ? dema : type == 4 ? hlc3 : type == 5 ? hlcc4 : type == 6 ? ohlc4 : kama
trend = ma > ma[1] ? 1 : ma < ma[1] ? -1 : 0

// Entry Conditions
longCondition = needlong and trend == 1 and fastsma > src and bars == 2 and (bar_index % 3) == 0
shortCondition = needshort and trend == -1 and fastsma < src and bars == 2 and (bar_index % 3) == 0

// Place Orders
if longCondition
    strategy.entry("Long", strategy.long)

if shortCondition
    strategy.entry("Short", strategy.short)
```