> Name

Dual Linear Reversal Moving Average Oscillator Combination Strategy 123 - Reversal-Moving-Average-Convergence-Divergence-Combination-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1cdb9644720db0541ec.png)

[trans]

## Overview
This strategy combines the 123 reversal trading strategy proposed by Ulf Jensen in his book with Martin Pring's Weighted Moving Average Convergence Divergence Oscillator (KST) to build a quantitative strategy that generates trading signals by utilizing reversal patterns and trend oscillation indicators.

## Strategy Principle
### 123 Reversal Formation Mechanism
The core logic of this part of the strategy is to monitor whether the closing price of the stock has reversed in the past 2 days, specifically:

If the closing prices in the past 2 days are in a downward trend, that is, the previous day's closing price is higher than the one before; and today's closing price rebounds upward from the previous day, which is higher than the previous day's closing price, it can be judged as a bottom reversal and a buy signal is generated.

On the contrary, if the closing prices in the past 2 days are in an upward trend, that is, the previous day's closing price is lower than the one before; and today's closing price falls from the previous day, which is lower than the previous day's closing price, it can be judged as a top reversal and a sell signal is generated.

This part of the strategy also combines the Stochastic indicator to determine whether it is overbought or oversold to filter out non-reversal trading signals.

### KST Indicator Principle 
KST indicator's ROC represents the rate of change in price. The ROCs of 6 days, 10 days, 15 days, and 20 days are calculated, and after different parameter moving average smoothing, they are weighted summed to construct the KST indicator.

When the fast line crosses above the slow line, it is judged as bullish; when the fast line crosses below the slow line, it is judged as bearish. Here, the fast line is the original KST value, and the slow line is the moving average of KST.

This strategy uses KST>0 to judge bullish and KST<0 to judge bearish.

### Signal Merge
The Judgment signals of the 123 reversal strategy and the KST indicator are combined:
- If both signals are the same, a trading signal is generated in that direction.
- If the two signals are different, no trading occurs.

It can be seen that this strategy comprehensively uses two different types of technical indicators, the reversal pattern and indicator judgment, and combines their signal strengths to design a more advanced quantitative trading strategy.

## Advantages of the Strategy
- The reversal part can effectively identify turning points, and the indicator part can track trends, complementing each other.
- Filtering with dual indicators can improve signal quality and reduce false signals.
- Flexible adjustment of KST parameters for optimization for stocks of different cycles.
- Can adapt to high volatility stocks, can also be used for relatively stable stocks.

## Risks of the Strategy
- Risk of reversal failure, reversal signal may also be false breakout.
- Some opportunities may be missed after signal merge.
- Improper KST parameters may greatly interfere with results.
- When stock price fluctuates sharply, KST lags, inconsistent signals may appear.

Methods like parameter adjustment, optimization of reversal logic, introduction of stop loss mechanism can be used to control risks.

## Optimization Direction
- Optimize Stochastic Parameters.
- Optimize length parameters of KST line.
- Add trading volume or volatility index filter.
- Add trend judgment to avoid trading against trend.
- Introduce stop loss mechanism.

## Conclusion
This strategy integrates multiple different types of technical indicators. Through dual confirmation and combination optimization, it scientifically designs a relatively strong quantitative trading strategy, and it is a model of strategy combination. Its performance in live trading is yet to be further verified, but from the theoretical conceptualization perspective, it comprehensively considers multiple scenarios, solves the limitations of single indicators, and is worth further research and application.

||


## Overview
This strategy combines the 123 reversal trading strategy proposed by Ulf Jensen in his book with Martin Pring's Weighted Moving Average Convergence Divergence Oscillator (KST) to build a quantitative strategy that generates trading signals by utilizing reversal patterns and trend oscillation indicators.

## Strategy Principle
### 123 Reversal Formation Mechanism
The core logic of this part of the strategy is to monitor whether the closing price of the stock has reversed in the past 2 days, specifically:

If the closing prices in the past 2 days are in a downward trend, that is, the previous day's closing price is higher than the one before; and today's closing price rebounds upward from the previous day, which is higher than the previous day's closing price, it can be judged as a bottom reversal and a buy signal is generated.

On the contrary, if the closing prices in the past 2 days are in an upward trend, that is, the previous day's closing price is lower than the one before; and today's closing price falls from the previous day, which is lower than the previous day's closing price, it can be judged as a top reversal and a sell signal is generated.

This part of the strategy also combines the Stochastic indicator to determine whether it is overbought or oversold to filter out non-reversal trading signals.

### KST Indicator Principle 
KST indicator's ROC represents the rate of change in price. The ROCs of 6 days, 10 days, 15 days, and 20 days are calculated, and after different parameter moving average smoothing, they are weighted summed to construct the KST indicator.

When the fast line crosses above the slow line, it is judged as bullish; when the fast line crosses below the slow line, it is judged as bearish. Here, the fast line is the original KST value, and the slow line is the moving average of KST.

This strategy uses KST>0 to judge bullish and KST<0 to judge bearish.

### Signal Merge
The Judgment signals of the 123 reversal strategy and the KST indicator are combined:
- If both signals are the same, a trading signal is generated in that direction.
- If the two signals are different, no trading occurs.

It can be seen that this strategy comprehensively uses two different types of technical indicators, the reversal pattern and indicator judgment, and combines their signal strengths to design a more advanced quantitative trading strategy.

## Advantages of the Strategy
- The reversal part can effectively identify turning points, and the indicator part can track trends, complementing each other.
- Filtering with dual indicators can improve signal quality and reduce false signals.
- Flexible adjustment of KST parameters for optimization for stocks of different cycles.
- Can adapt to high volatility stocks, can also be used for relatively stable stocks.

## Risks of the Strategy
- Risk of reversal failure, reversal signal may also be false breakout.
- Some opportunities may be missed after signal merge.
- Improper KST parameters may greatly interfere with results.
- When stock price fluctuates sharply, KST lags, inconsistent signals may appear.

Methods like parameter adjustment, optimization of reversal logic, introduction of stop loss mechanism can be used to control risks.

## Optimization Direction
- Optimize Stochastic Parameters.
- Optimize length parameters of KST line.
- Add trading volume or volatility index filter.
- Add trend judgment to avoid trading against trend.
- Introduce stop loss mechanism.

## Conclusion
This strategy integrates multiple different types of technical indicators. Through dual confirmation and combination optimization, it scientifically designs a relatively strong quantitative trading strategy, and it is a model of strategy combination. Its performance in live trading is yet to be further verified, but from the theoretical conceptualization perspective, it comprehensively considers multiple scenarios, solves the limitations of single indicators, and is worth further research and application.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|true|---- 123 Reversal ----|
|v_input_2|14|Length|
|v_input_3|true|KSmoothing|
|v_input_4|3|DLength|
|v_input_5|50|Level|
|v_input_6|false|Trade reverse|


> Source (PineScript)

``` pinescript
//@version=4
///////////////////
```