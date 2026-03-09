> Name

Triple-Indicator-Collision-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1a897bb05ba5579fce9.png)
[trans]
## Overview

The Triple Indicator Collision Strategy (Triple-Indicator-Collision-Strategy) is a very classic quantitative trading strategy. It combines the use of moving averages, MACD indicator, and RSI indicator—three classic technical indicators. When all three indicators simultaneously produce buy or sell signals, corresponding trading actions are taken.

## Strategy Principle

This strategy uses 20-day EMA (Exponential Moving Average), MACD with parameters (12, 26, 9), and a 14-day RSI (Relative Strength Index). The specific trading logic is as follows:

- When the price crosses above the 20-day EMA.
- When the MACD histogram crosses above the signal line.
- And when the RSI crosses above the 20-day EMA of RSI, go long.

- When the price crosses below the 20-day EMA.
- When the MACD histogram crosses below the signal line.
- And when the RSI crosses below the 20-day EMA of RSI, go short.

By requiring all three indicators to produce a trading signal simultaneously, this strategy filters out some false signals and makes it more stable and reliable.

## Advantage Analysis

This multi-indicator collision strategy has several advantages:

1. Filtering noise and reducing false signals. A single indicator is prone to market noise and can generate many false signals. Using three indicators effectively filters out the noise, making the signals more reliable.
2. Capturing trend inflection points. Different indicators respond differently to price fluctuations. When all three agree in the short term, it often signifies a trend reversal, providing an opportunity to capture inflection points.
3. Multi-dimensional market judgment. The three indicators analyze the market from different dimensions and verify each other, allowing for more comprehensive and accurate judgments of market trends.
4. Lowering position risk. Using multiple indicators to filter signals reduces ineffective trade times and unnecessary capital turnover, which helps with risk control.

## Risk Analysis

The strategy also has some risks:

1. Parameter optimization risk. The length of the moving average, MACD parameters, RSI parameters, etc., can all affect strategy performance. An inappropriate parameter combination may lead to poor strategy performance in market trends. Therefore, comprehensive testing and optimization are needed to find the best parameter combination.
2. Missing trading opportunities. The triple indicator strategy is relatively conservative and may miss some trading chances. If it fails to capture major trends, it will impact strategy profitability.
3. Slippage control in live trading. Transaction costs and slippage also affect strategies to some extent in live trading. Trading frequency needs to be controlled to ensure the profit margin is greater than transaction costs.

## Optimization Directions

The strategy can be optimized from the following aspects:

1. Test different parameter combinations to find the optimal parameters by altering the lengths of moving averages, MACD parameters, RSI parameters, etc.
2. Add stop loss mechanisms. Moving stop loss or pending order stop loss can effectively control single trade losses.
3. Combine other indicators to filter signals. Bollinger Bands, KDJ, and other indicators can also be used to verify signals and filter out false signals.
4. Adjust parameters based on different products and timeframes. Parameters can be optimized according to the trading products and timeframes.

## Conclusion

The Triple Indicator Collision Strategy utilizes the signals from moving averages, MACD, and RSI altogether to make long and short decisions. It effectively filters out noise and identifies potential trend inflection points, making trade signals more reliable. By optimizing parameters, setting stop losses, filtering signals, and so on, this strategy can be continuously improved to generate clearer signals and more reliable profits.

||

## Overview  

The Triple Indicator Collision Strategy is a very classic quantitative trading strategy that combines the use of moving averages, MACD indicator, and RSI indicator—three classic technical indicators. It generates trading signals when all three indicators produce buy or sell signals simultaneously.

## Strategy Principle 

This strategy uses 20-day EMA, MACD(12, 26, 9), and a 14-day RSI altogether. The specific logic is:

- When the price crosses above the 20-day EMA.
- When the MACD histogram crosses above the signal line.
- And when the RSI crosses above the 20-day EMA of RSI, go long.

- When the price crosses below the 20-day EMA.
- When the MACD histogram crosses below the signal line.
- And when the RSI crosses below the 20-day EMA of RSI, go short.

With trading signals generated only when all three indicators agree, this filters out some false signals and makes the strategy more solid and reliable.

## Advantage Analysis 

The triple indicator collision strategy has the following advantages:

1. Filtering noise and reducing false signals. A single indicator is prone to market noise and can generate many false signals. Using three indicators effectively filters out the noise, making the signals more reliable.
2. Capturing trend inflection points. Different indicators respond differently to price fluctuations. When all three agree in the short term, it often signifies a trend reversal, providing an opportunity to capture inflection points.
3. Judging market from multiple dimensions. The three indicators analyze market trends from different angles and verify each other, allowing for more comprehensive and accurate judgments of market movements.
4. Lowering position risk. Using multiple indicators to filter signals reduces ineffective trade times and unnecessary capital turnover, which helps with risk control.

## Risk Analysis 

There are also some risks associated with this strategy:

1. Parameter optimization risk. The parameters of the moving average length, MACD parameters, RSI parameters, etc., can all impact strategy performance. An unsuitable parameter combination may lead to poor strategy performance in market trends. Therefore, comprehensive testing and optimization are needed to find the optimal parameter combination.
2. Missing trading opportunities. The triple indicator strategy is relatively conservative and may miss some trading chances. If it fails to capture major trends, it will affect strategy profitability.
3. Slippage control in live trading. Transaction costs and slippage also impact strategies to some extent in live trading. Trading frequency needs to be controlled to ensure the profit margin is greater than transaction costs.

## Optimization Directions 

The strategy can be optimized in the following aspects:

1. Test different parameter combinations to find the optimal parameters by altering the lengths of moving averages, MACD parameters, RSI parameters, etc.
2. Add stop loss mechanisms. Moving stop loss or pending order stop loss can effectively control single trade losses.
3. Combine other indicators to filter signals. Bollinger Bands, KDJ, and other indicators can also be used to verify signals and filter out false signals.
4. Adjust parameters based on different products and timeframes. Parameters can be optimized according to the trading products and timeframes.

## Conclusion 

The Triple Indicator Collision Strategy utilizes the trading signals from moving averages, MACD, and RSI altogether to make long and short decisions. It effectively filters out noise and identifies potential trend inflection points, making trade signals more reliable. By optimizing parameters, setting stop losses, filtering signals, and so on, this strategy can be continuously improved to generate clearer signals and more reliable profits.

[/trans]

> Strategy Arguments

| Argument    | Default  | Description            |
|-------------|----------|------------------------|
| v_input_1   | 20       | EMA length             |
| v_input_2   | 12       | MACD Fast              |
| v_input_3   | 26       | MACD Slow              |
| v_input_4   | 20       | MACD Signal length     |
| v_input_5   | 14       | RSI length             |
| v_input_6   | 20       | RSI signal length      |

> Source (PineScript)

```pinescript
/*backtest
start: 2023-12-29 00:00:00
end: 2024-01-28 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © fangdingjun

//@version=4
strategy("MACD_RSI strategy", overlay=false)

_ema_len = input(20, title="EMA length")
_macd_fast = input(12, title="MACD Fast")
_macd_slow = input(26, title="MACD Slow")
_macd_signal_len = input(20, title="MACD Signal length")
_rsi_len = input(14, title="RSI length")
_rsi_signal_len = input(20, title="RSI signal length")

_ema = ema(close,
```