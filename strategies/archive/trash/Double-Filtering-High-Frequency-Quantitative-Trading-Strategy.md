> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long Trading|
|v_input_2|true|Short Trading|
|v_input_3|true|Enable|

## Overview

The strategy is named "Double Filtering Quant", which adopts multi-timeframe techniques to implement a high-frequency quantitative trading strategy based on double filtering ideas. The strategy uses indicators on different timeframes to make judgments and implement more rigorous trading signal filtering to filter out a large number of false signals, thereby obtaining higher win rates.

## Strategy Principle 

The core principle of the strategy is:

1. Use weekly and daily lines to judge the market trend direction as the strategy direction filter condition. Only trades that meet the trend conditions can be made.
2. Construct the channel at the 4-hour level to determine selling and buying points and issue trading signals.
3. The consistency of directions judged by weekly, daily, and 4-hour timeframes can filter out a lot of false signals and improve the reliability of trading signals.
4. Use Fibonacci retracement points to determine profit-taking and stop-loss positions for rapid profit-taking and stopping losses.

Specifically, the strategy first judges the priority direction of the trend on the weekly and daily lines. The principle of judging the priority direction is: if the closing price of the current K-line is on the side with a larger lag angle on the cycle line, it is determined as the direction of the cycle line. Then, construct the A B C D channel at the 4-hour level, and determine buy and sell points through the channel direction and turning points to issue trading signals. Finally, the priority direction determined by the current cycle line must be consistent with the direction of the trading signal at the 4-hour level. This can filter out many false signals and improve the reliability of trading signals.

## Strategy Advantages

The main advantages of this strategy are:

1. The dual signal filtering mechanism based on multiple timeframes can filter out a lot of noise and obtain highly reliable trading opportunities.
2. The use of channels to construct buying and selling points makes trading signals clear.
3. Fibonacci retracement points are used to set profit-taking and stop-loss positions for fast profit-taking and stopping losses.
4. The strategy has few parameters and is easy to understand and master.
5. Good scalability for easy optimization and improvement.

## Strategy Risks

The main risks of this strategy are:

1. Monitoring too many timeframes increases complexity and prone to errors.
2. Does not consider sudden events of special market conditions, such as drastic market fluctuations caused by major news events.
3. There is a possibility of insufficient profit setting stop-loss and profit-taking points using retracement.
4. Parameter settings不当可能导致过度交易或漏单.

对策:

1. 加强对异常情况和重大新闻事件的监控。
2. 优化止盈止损逻辑，确保盈利达到一定水平。
3. 详细测试与优化参数，减少过度交易和漏单概率。

## Strategy Optimization Directions

The main optimization directions of this strategy are:

1. Increase the possibility of using machine learning models to determine the priority direction of trends, and use more data to improve judgment accuracy.
2. Test other indicators to construct channels and determine buying and selling points.
3. Try more advanced ways of profit-taking and stop-loss, such as moving profit-taking, jumping profit-taking, etc.
4. Derive optimal parameters from backtesting results to make parameter settings more in line with quantitative investment principles.
5. Increase monitoring and response mechanisms for major sudden events.

## Conclusion 

In general, the core idea of ​​this strategy is a high-frequency quantitative trading strategy based on double filtering to reduce noise. It uses multi-timeframe judgment and channel determination of buying and selling points to achieve double reliability filtering of trading signals. At the same time, the strategy has few parameters and is easy to master; scalability is good and easy to optimize and improve. Next, optimization will be carried out from aspects such as judgment accuracy, profit-taking and stop-loss methods, and parameter optimization to make the strategy work better.

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Long Trading|
|v_input_2|true|Short Trading|
|v_input_3|true|Enable