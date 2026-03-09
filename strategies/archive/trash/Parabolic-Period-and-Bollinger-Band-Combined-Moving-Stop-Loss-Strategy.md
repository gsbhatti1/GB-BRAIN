> Name

Parabolic-Period-and-Bollinger-Band-Combined-Moving-Stop-Loss-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/20aebdfdb4a0d59f3f7.png)
[trans]
### Overview

This article will introduce a quantitative trading strategy that combines the parabolic period indicator and the Bollinger band indicator to set a moving stop loss strategy. By calculating the parabolic period line to judge the market trend direction, and then using the upper and lower rails of the Bollinger bands to dynamically set the stop loss position, the strategy realizes moving stop loss to lock in profits.

### Strategy Principle

Firstly, this strategy uses the parabolic indicator to judge the current market trend. When today's closing price crosses above yesterday's parabolic period line, it is considered that the market has reversed to bullish and can go long; when today's closing price crosses below the period line, the market outlook is bearish and can go short.

Secondly, this strategy combines the Bollinger Band indicator to set a dynamic stop loss position. The upper rail of the Bollinger Band can be seen as an overbought zone, and the lower rail is an oversold zone. After going long, if the price falls back below the lower rail of the Bollinger Band, stop loss to close position; after going short, if the price rises above the upper rail again, stop loss to exit. Thus, the upper and lower rails of Bollinger Bands become moving stop loss lines.

Through the above principles, this strategy realizes judging the market direction while setting a dynamic stop loss mechanism to track profits. This allows it to capture some ups and downs in major trends, while also being able to lock in profits through stop losses to avoid risks.

### Advantages of the Strategy

Compared with traditional stop loss strategies that only set one fixed stop loss position, this strategy uses the Bollinger band indicator as the stop loss line, so that the stop loss line can move with price fluctuations. This allows it to lock in more profits in relatively large moves. In addition, compared to using the parabolic period line alone, this strategy adds the Bollinger band indicator to determine overbought and oversold areas, which can be more accurate.

### Risks and Solutions

The main risk of this strategy is that the trending of the parabolic indicator is not strong. In oscillating markets, prices may cross parabolic period lines several times, causing frequent but small profitable trades for the strategy. At this point, transaction fees and slippage costs may account for a large proportion and reduce the profitability of the strategy.

To cope with the above risks, parameters can be adjusted to increase the degree of change in the parabolic period line to reduce misjudgment probability; or consider combining other indicators to filter entry timing. For example, volatility indicators can be added to determine if the market is trending or oscillating in order to reduce unnecessary trades.

### Strategy Optimization

This strategy can be optimized in the following aspects:

1. Optimize parabolic indicator parameters to adjust indicator change rate to reduce misjudgment probability
2. Increase other technical indicators filtering, such as adding MACD, KD to determine market type, avoid arbitrage in oscillating market
3. Optimize Bollinger Band parameters to adjust bandwidth parameters to make Bollinger Bands stick closer to price changes
4. Increase volume indicators, such as trading volume, positions to assist in judging to avoid false breakouts
5. Combine fundamentals of stocks to avoid problems with earnings of stocks strategy holding

### Summary

This strategy combines judging market trend direction and strength with the parabolic indicator, and then uses the upper and lower rails of Bollinger Bands as the moving stop loss position to set a stop loss strategy, achieving a combination of trend tracking and risk control. Compared with traditional fixed stop loss strategies, this strategy can achieve higher returns in larger moves. By optimizing parameters and adding other auxiliary judgment indicators, the stability of the strategy can be further enhanced and unnecessary trades reduced.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_bool_1|true|(?Backtest Time Period)Filter Date Range of Backtest|
|v_input_1|timestamp(5 June 2022)|Start Date|
|v_input_2|timestamp(5 July 2022)|End Date|
|v_input_int_1|10|(?number of past candles)Swing High|
|v_input_int_2|10|Swing Low|
|v_input_int_3|200|(?EMA)Ema Period|
|v_input_int_4|14|(?RSI)RSI Period|
|v_input_3|0.02|(?Parabolic SAR)start|
|v_input_4|0.02|increment|
|v_input_5|0.2|Max Value|


> Source (PineScript)