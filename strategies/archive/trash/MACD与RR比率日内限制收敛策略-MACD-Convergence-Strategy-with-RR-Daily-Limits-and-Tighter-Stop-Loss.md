> Name

MACD with RR Ratio Daily Limit Convergence Strategy - MACD-Convergence-Strategy-with-RR-Daily-Limits-and-Tighter-Stop-Loss

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/6519b3e7a42df48c24.png)

[trans]
#### Overview
This strategy uses the convergence and divergence of the MACD indicator to generate trading signals. When the MACD line crosses the signal line, and the value of the MACD line is greater than 1.5 or less than -1.5, it generates long and short signals, respectively. The strategy sets fixed take-profit and stop-loss levels and introduces the concept of risk-reward ratio (R:R). Additionally, it employs daily maximum loss and profit limits and a tighter trailing stop-loss to better control risks.

#### Strategy Principle
1. Calculate the MACD line and signal line of the MACD indicator.
2. Determine the crossover situations between the MACD line and signal line, while considering whether the value of the MACD line exceeds certain thresholds (1.5 and -1.5).
3. When a long signal appears, open a long position with a take-profit price of the current highest price + 600 minimum tick units and a stop-loss price of the current lowest price - 100 minimum tick units.
4. When a short signal appears, open a short position with a take-profit price of the current lowest price - 600 minimum tick units and a stop-loss price of the current highest price + 100 minimum tick units.
5. Introduce a trailing stop-loss logic: when the price rises (long position) or falls (short position) more than 300 minimum tick units relative to the entry price, move the stop-loss price to the entry price + (close price - entry price - 300) for long positions or entry price - (entry price - close price - 300) for short positions.
6. Set daily maximum loss and profit limits: when the daily loss reaches 600 minimum tick units or the profit reaches 1800 minimum tick units, close all positions.

#### Advantage Analysis
1. Combining the MACD indicator with price threshold conditions effectively filters out some noise signals.
2. Fixed risk-reward ratio (R:R) makes the risk and reward of each trade controllable.
3. The trailing stop-loss logic protects profits after a trend forms and reduces drawdowns.
4. Daily maximum loss and profit limits help control daily risk exposure and avoid excessive losses or profits followed by drawdowns.

#### Risk Analysis
1. The MACD indicator has a lag effect, which may result in delayed or false signals.
2. Fixed take-profit and stop-loss levels may not adapt to different market conditions and could be frequently triggered in choppy markets.
3. The trailing stop-loss logic may fail to stop losses in time during trend reversals, leading to profit givebacks.
4. Daily maximum loss and profit limits may cause the strategy to close positions prematurely when the daily trend is clear, missing potential profits.

#### Optimization Direction
1. Consider using multi-timeframe MACD indicators to confirm signals and improve signal accuracy.
2. Dynamically adjust take-profit and stop-loss levels based on market volatility to adapt to different market conditions.
3. Optimize the trailing stop-loss logic, such as setting the trailing stop-loss distance based on the ATR indicator for better adaptation to price fluctuations.
4. Optimize the parameters of daily maximum loss and profit limits to find appropriate limit values that control risks while capturing trend movements as much as possible.

#### Summary
This strategy uses the convergence and divergence of the MACD indicator to generate trading signals while introducing risk control measures such as risk-reward ratio, trailing stop-loss, and daily limits. Although the strategy can capture trend movements and control risks to some extent, there is still room for optimization and improvement. In the future, optimization can be considered from aspects such as signal confirmation, take-profit and stop-loss levels, trailing stop-loss, and daily limits to obtain more robust and considerable returns.

||

#### Overview
This strategy uses the convergence and divergence of the MACD indicator to generate trading signals. When the MACD line crosses the signal line, and the value of the MACD line is greater than 1.5 or less than -1.5, it generates long and short signals, respectively. The strategy sets fixed take-profit and stop-loss levels and introduces the concept of risk-reward ratio (R:R). Additionally, it employs daily maximum loss and profit limits and a tighter trailing stop-loss to better control risks.

#### Strategy Principle
1. Calculate the MACD line and signal line of the MACD indicator.
2. Determine the crossover situations between the MACD line and signal line, while considering whether the value of the MACD line exceeds certain thresholds (1.5 and -1.5).
3. When a long signal appears, open a long position with a take-profit price of the current highest price + 600 minimum tick units and a stop-loss price of the current lowest price - 100 minimum tick units.
4. When a short signal appears, open a short position with a take-profit price of the current lowest price - 600 minimum tick units and a stop-loss price of the current highest price + 100 minimum tick units.
5. Introduce a trailing stop-loss logic: when the price rises (long position) or falls (short position) more than 300 minimum tick units relative to the entry price, move the stop-loss price to the entry price + (close price - entry price - 300) for long positions or entry price - (entry price - close price - 300) for short positions.
6. Set daily maximum loss and profit limits: when the daily loss reaches 600 minimum tick units or the profit reaches 1800 minimum tick units, close all positions.

#### Advantage Analysis
1. Combining the MACD indicator with price threshold conditions effectively filters out some noise signals.
2. Fixed risk-reward ratio (R:R) makes the risk and reward of each trade controllable.
3. The trailing stop-loss logic protects profits after a trend forms and reduces drawdowns.
4. Daily maximum loss and profit limits help control daily risk exposure and avoid excessive losses or profits followed by drawdowns.

#### Risk Analysis
1. The MACD indicator has a lag effect, which may result in delayed or false signals.
2. Fixed take-profit and stop-loss levels may not adapt to different market conditions and could be frequently triggered in choppy markets.
3. The trailing stop-loss logic may fail to stop losses in time during trend reversals, leading to profit givebacks.
4. Daily maximum loss and profit limits may cause the strategy to close positions prematurely when the daily trend is clear, missing potential profits.

#### Optimization Direction
1. Consider using multi-timeframe MACD indicators to confirm signals and improve signal accuracy.
2. Dynamically adjust take-profit and stop-loss levels based on market volatility to adapt to different market conditions.
3. Optimize the trailing stop-loss logic, such as setting the trailing stop-loss distance based on the ATR indicator for better adaptation to price fluctuations.
4. Optimize the parameters of daily maximum loss and profit limits to find appropriate limit values that control risks while capturing trend movements as much as possible.

#### Summary
This strategy uses the convergence and divergence of the MACD indicator to generate trading signals while introducing risk control measures such as risk-reward ratio, trailing stop-loss, and daily limits. Although the strategy can capture trend movements and control risks to some extent, there is still room for optimization and improvement. In the future, optimization can be considered from aspects such as signal confirmation, take-profit and stop-loss levels, trailing stop-loss, and daily limits to obtain more robust and considerable returns.

||

> Source (PineScript)

```pinescript
//@version=5
strategy("MACD Convergence Strategy with R:R, Daily Limits, and Tighter Stop Loss", overlay=true, default_qty_type=strategy.fixed, default_qty_value=1)

// MACD settings
fastLength = input.int(12, title="Fast Length", minval=1)
slowLength = input.int(26, title="Slow Length", minval=1)
signalSmoothing = input.int(9, title="Signal Smoothing", minval=1)
source = input(close, title="Source")

// Calculate MACD
[macdLine, signalLine, _] = ta.macd(source, fastLength, slowLength, signalSmoothing)

// Define take-profit and stop-loss levels
longTp = ta.valuewhen(macdLine > 1.5, high, 0) + 600
longSl = ta.valuewhen(macdLine > 1.5, low, 0) - 100
shortTp = ta.valuewhen(macdLine < -1.5, low, 0) - 600
shortSl = ta.valuewhen(macdLine < -1.5, high, 0) + 100

// Set trailing stop-loss
trailTp = ta.valuewhen(macdLine > 1.5, high, 0) + 300
trailSl = ta.valuewhen(macdLine < -1.5, low, 0) - 300

// Enter long position
strategy.entry("Long", strategy.long, when=macdLine > 1.5)
strategy.exit("Long Exit", "Long", limit=longTp, stop=trailTp, loss=trailSl)

// Enter short position
strategy.entry("Short", strategy.short, when=macdLine < -1.5)
strategy.exit("Short Exit", "Short", limit=shortTp, stop=trailSl, loss=trailTp)

// Daily loss and profit limits
dailyLossLimit = 600
dailyProfitLimit = 1800

// Check daily limits and close positions
if (strategy.netprofit < -dailyLossLimit or strategy.netprofit > dailyProfitLimit)
    strategy.close("Long", "Short")
```
[/trans]