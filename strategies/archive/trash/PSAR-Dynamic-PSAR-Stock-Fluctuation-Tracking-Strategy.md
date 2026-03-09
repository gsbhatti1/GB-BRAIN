> Name

Dynamic PSAR Stock Fluctuation Tracking Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13bf3536176ed9e8720.png)
[trans]

### Overview

This strategy implements a simple and efficient stock fluctuation tracking and automatic take profit/stop loss strategy based on the Parabolic SAR indicator. It can dynamically track the uptrend and downtrend of stock prices and automatically set take profit/stop loss points at the reversal points without manual intervention, achieving fully automated trading.

### Strategy Principle

This strategy uses the Parabolic SAR (PSAR) indicator to determine the trend direction of stock price fluctuations. When the PSAR indicator is below the K-line, it indicates an upward trend; when the PSAR indicator is above the K-line, it indicates a downward trend. The strategy tracks changes in PSAR values ​​in real time to determine changes in trends.

When an upward trend is confirmed, the strategy will set a stop loss point at the PSAR point of the next BAR; when a downward trend is confirmed, the strategy will set a take profit point at the PSAR point of the next BAR. This achieves the automatic take profit/stop loss function when stock prices reverse.

At the same time, the strategy has built-in parameters such as starting value, step value and maximum value to adjust the sensitivity of the PSAR indicator, thereby optimizing the effect of take profit/stop loss.

### Advantage Analysis

The biggest advantage of this strategy is that it realizes full automation of stock fluctuation tracking and automatic take profit/stop loss. Profits can be realized without manual judgment of market trends, which greatly reduces the time and energy costs of manual trading.

Compared with traditional stop loss/take profit strategies, the take profit/stop loss points of this strategy are variable, which can capture price changes and opportunities more quickly. It also reduces the probability of misjudgment and increases profit potential.

After parameter optimization, this strategy can continuously profit in major trends while automatically stopping to protect the principal when reversal comes.

### Risk Analysis

The biggest risk of this strategy is the probability that the PSAR indicator misjudges the trend direction. When stock prices have short-term adjustments and fluctuations, the PSAR indicator may give a wrong signal. At this time, it is necessary to reasonably optimize the parameters of PSAR to improve the accuracy of judgment.

Another risk point is that the take profit/stop loss points are too close to the current price. This may increase the probability that the stop loss point is broken, bringing greater impact to the principal. At this time, appropriately relax the take profit/stop loss range to ensure sufficient buffer space.

### Strategy Optimization

The optimization potential of this strategy mainly focuses on adjusting the parameters of the PSAR indicator itself. By testing different stocks and optimizing the settings of starting value, step value, and maximum value, the PSAR indicator can be more sensitive to price fluctuations while ensuring judgment accuracy. This requires a lot of backtesting and analysis work.

Another optimization direction is setting the range of take profit/stop loss. It is necessary to study the intraday fluctuation range of different stocks and set reasonable profit/loss ratio requirements based on this. This can further reduce the probability of principal loss.

### Summary

This strategy utilizes the Parabolic SAR indicator to realize a fully automated stock tracking and automatic take profit/stop loss trading strategy. Its biggest advantage is that no manual intervention is required, which can reduce time and energy costs. The main risks come from misjudgments of indicators, which can be reduced through parameter optimization. In general, this strategy provides an efficient and reliable solution for quantitative trading of stocks.

||

### Overview

This strategy implements a simple and efficient stock fluctuation tracking and automatic take profit/stop loss strategy based on the Parabolic SAR indicator. It can dynamically track the uptrend and downtrend of stock prices and automatically set take profit/stop loss points at the reversal points without manual intervention, achieving fully automated trading.

### Strategy Principle

This strategy uses the Parabolic SAR (PSAR) indicator to determine the trend direction of stock price fluctuations. When the PSAR indicator is below the K-line, it indicates an upward trend; when the PSAR indicator is above the K-line, it indicates a downward trend. The strategy tracks changes in PSAR values ​​in real time to determine changes in trends.

When an upward trend is confirmed, the strategy will set a stop loss point at the PSAR point of the next BAR; when a downward trend is confirmed, the strategy will set a take profit point at the PSAR point of the next BAR. This achieves the automatic take profit/stop loss function when stock prices reverse.

At the same time, the strategy has built-in parameters such as starting value, step value and maximum value to adjust the sensitivity of the PSAR indicator, thereby optimizing the effect of take profit/stop loss.

### Advantage Analysis

The biggest advantage of this strategy is that it realizes full automation of stock fluctuation tracking and automatic take profit/stop loss. Profits can be realized without manual judgment of market trends, which greatly reduces the time and energy costs of manual trading.

Compared with traditional stop loss/take profit strategies, the take profit/stop loss points of this strategy are variable, which can capture price changes and opportunities more quickly. It also reduces the probability of misjudgment and increases profit potential.

After parameter optimization, this strategy can continuously profit in major trends while automatically stopping to protect the principal when reversal comes.

### Risk Analysis

The biggest risk of this strategy is the probability that the PSAR indicator misjudges the trend direction. When stock prices have short-term adjustments and fluctuations, the PSAR indicator may give a wrong signal. At this time, it is necessary to reasonably optimize the parameters of PSAR to improve the accuracy of judgment.

Another risk point is that the take profit/stop loss points are too close to the current price. This may increase the probability that the stop loss point is broken, bringing greater impact to the principal. At this time, appropriately relax the take profit/stop loss range to ensure sufficient buffer space.

### Strategy Optimization

The optimization potential of this strategy mainly focuses on adjusting the parameters of the PSAR indicator itself. By testing different stocks and optimizing the settings of starting value, step value, and maximum value, the PSAR indicator can be more sensitive to price fluctuations while ensuring judgment accuracy. This requires a lot of backtesting and analysis work.

Another optimization direction is setting the range of take profit/stop loss. It is necessary to study the intraday fluctuation range of different stocks and set reasonable profit/loss ratio requirements based on this. This can further reduce the probability of principal loss.

### Summary

This strategy utilizes the Parabolic SAR indicator to realize a fully automated stock tracking and automatic take profit/stop loss trading strategy. Its biggest advantage is that no manual intervention is required, which can reduce time and energy costs. The main risks come from misjudgments of indicators, which can be reduced through parameter optimization. In general, this strategy provides an efficient and reliable solution for quantitative trading of stocks.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|0.02|start|
|v_input_2|0.02|increment|
|v_input_3|0.2|maximum|

> Source (PineScript)

```pinescript
/*backtest
start: 2024-01-28 00:00:00
end: 2024-02-04 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Swing Parabolic SAR Strategy", overlay=true)
start = input(0.02)
increment = input(0.02)
maximum = input(0.2)
var bool uptrend = na
var float EP = na
var float SAR = na
var float AF = start
var float nextBarSAR = na
if bar_index > 0
	firstTrendBar = false
	SAR := nextBarSAR
	if bar_index == 1
		float prevSAR = na
		float prevEP = na
		lowPrev = low[1]
		highPrev = high[1]
		closeCur = close
		closePrev = close[1]
		if closeCur > closePrev
```