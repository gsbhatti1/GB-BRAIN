> Name

The-Order-Block-Momentum-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/b071ca974b27d8b117.png)
[trans]

## Overview

This strategy identifies order blocks in price action to locate momentum bursts and enters the market when buy/sell signals emerge. Order blocks represent institutional participation and significant market forces. Thus, order block signals have a higher probability of leading to trending price action.

## Strategy Logic

### Identifying Order Blocks

There are two types of order blocks - bullish and bearish. A bullish order block is defined as the last red candle followed by consecutive green candles. A bearish order block is the last green candle followed by consecutive red candles.

To identify an order block, the following criteria must be met simultaneously:

1. Candle color change - The candle color changes from the previous candle to the current one (e.g., from red to green or green to red). This suggests institutions may be ending the previous trend and initiating a new potential trend.
2. Consistent direction afterwards - The subsequent candles maintain the same color direction for the number of periods specified in the parameters (e.g., all green candles after a potential bullish block). This confirms the new trend.
3. Breakout exceeds threshold - The percentage price change from the open of the order block candle to the close of the final confirmation candle exceeds the threshold parameter (default 0). This ensures strong enough momentum.

When all three criteria are true, an order block signal is identified.

### Generating Trading Signals

A buy signal is generated when detecting a bullish order block. A sell signal emerges when a bearish order block is identified.

Considering the uncertainty of order flow signals, the strategy does not immediately enter the market. It alerts the trader and allows price limit orders to be placed near the order block levels instead. This provides controlled entries and risk management.

## Advantages

### Captures hidden momentum 

Order blocks represent institutional money flow and substantial volume. They indicate shifts in market forces and provide early clues into potential breakout direction. This facilitates trend following with good timing.

### Customizable parameters

The parameters controlling candle count, breakout percentage, etc., can be adjusted to optimize for changing market conditions and trading style. This enhances adaptability.

### Controlled risk

By not auto-entering on signals and using limit orders instead, traders can define entry levels and control risk. Failed signals simply lead to unfilled limit orders. Risks are contained.

## Risks

### High retest probability

As order blocks signify zones, prices revisiting the level is common. Signals should not be viewed as direct entries. Further timing judgment is needed.

### Parameter misfit causes bad signals

If parameters are not set properly, fake signals can emerge in range-bound markets. Traders need to exercise discretion in applying signals. Blind optimization should be avoided.

### Manual review is necessary

With each signal requiring further validation, significant manual effort is involved. Inconsistencies in human discretion on signal quality may lead to performance divergence.

## Enhancement Opportunities 

### Signal filtering with other indicators

Incorporate additional indicators like MACD and RSI when signals appear to gauge market conditions. This filters bad signals from poor parameter settings.

### Parameter optimization

The parameters can be tested and tuned to suit different markets and instruments for better fit. Adaptive settings can also be implemented to auto-adjust based on volatility and risk tolerance.

### Automated entry/exit

Currently, the strategy only serves as signal alerts. Logics can be added to automate limit order entries on signals and implement stops for exits. This increases automation and reduces reliance on human judgment.

## Conclusion

By detecting order flow convergence, this strategy aims to identify momentum bursts in price action with high probability of trending behavior. Compared to simple trend-following methods, the order block approach has a certain ability to recognize potential trends early. When combined with parameter optimization and risk management techniques, it can become an effective trend-following strategy. However, traders should be wary of false signals and manually assess each signal's quality. Further development is needed to automate the process more effectively, reducing human bias.