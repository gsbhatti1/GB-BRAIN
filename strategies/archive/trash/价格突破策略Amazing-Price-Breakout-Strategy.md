> Name

Amazing-Price-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/13d90740841c52b4a85.png)
[trans]
Overview: This strategy utilizes Bollinger Bands, KDJ indicator and trend following for price breakout operations. It can make long and short entries at breakout points and set stop loss to control risks.

Strategy Logic:

1. Calculate 15-day and 30-day simple moving averages to determine the price trend.
2. Calculate Bollinger Bands upper and lower rail, and combine candlestick breakout of BB rails to determine entries and exits.
3. Use RSI indicator to judge overbought and oversold conditions. RSI greater than 50 indicates overbought signal and RSI less than 50 indicates oversold signal.
4. When price breaks above the BB upper rail with RSI greater than 50, a buy signal is generated. When price falls below the BB lower rail with RSI less than 50, a sell signal is generated.
5. Set ATR stop loss to control risks.

Advantage Analysis:

1. This strategy combines multiple indicators like Bollinger Bands and RSI to determine trading signals, which can effectively avoid errors caused by single indicator.
2. With trend filtering, it prevents wrong signals during consolidation and reversal.
3. Setting ATR stop loss controls the risk of each order.
4. The strategy operation is clear and simple, easy to understand and implement.

Risks and Improvements:

1. As an envelope indicator, the Bollinger Band's upper and lower rails are not absolute support and resistance levels. After the price breaks through the upper and lower rails, the stop loss may be broken down. You can set a looser stop loss point or use other stop loss strategies such as time stop loss.
2. The RSI indicator may fail in certain markets. You can consider combining other indicators like KDJ, MACD, etc., to achieve more reliable overbought and oversold judgments.
3. In reversal and consolidation markets, it is easy to generate wrong signals. You can consider adding trend filtering and only participate in operations when the trend is obvious.

Optimization Suggestions:

1. Test and optimize the period number and standard deviation parameters of Bollinger Bands to make them more consistent with the characteristics of different varieties.
2. Test and optimize the period parameters of RSI.
3. Test other stop loss strategies, such as trailing stop loss, time stop loss, etc.
4. Combine more trend judgment indicators and signal indicators to build a multi-factor model.

Summary:

This strategy comprehensively uses multiple indicators like Bollinger Bands and RSI to determine the timing of buying and selling. While ensuring the accuracy of certain trading signals, it also sets stop losses to control risks. However, parameter optimization still needs to be carried out for specific varieties to make the signal more accurate and reliable. Additionally, you can consider adding more factors to build a multi-factor model. Overall, this strategy provides a relatively simple and practical idea for price breakthrough operations, which is worthy of further research and optimization.

||

Overview: This strategy utilizes Bollinger Bands, KDJ indicator and trend following for price breakout operations. It can make long and short entries at breakout points and set stop loss to control risks.

Strategy Logic:

1. Calculate 15-day and 30-day simple moving averages to determine the price trend.
2. Calculate Bollinger Bands upper and lower rail, and combine candlestick breakout of BB rails to determine entries and exits.
3. Use RSI indicator to judge overbought and oversold conditions. RSI greater than 50 indicates overbought signal and RSI less than 50 indicates oversold signal.
4. When price breaks above the BB upper rail with RSI greater than 50, a buy signal is generated. When price falls below the BB lower rail with RSI less than 50, a sell signal is generated.
5. Set ATR stop loss to control risks.

Advantages:

1. The strategy combines multiple indicators like Bollinger Bands and RSI to determine trading signals, which can effectively avoid errors caused by single indicator.
2. With trend filtering, it prevents wrong signals during consolidation and reversal.
3. Setting ATR stop loss controls the risk of each trade.
4. The strategy logic is simple and easy to understand.

Risks & Improvements:

1. As an envelope indicator, the Bollinger Band's upper and lower rails are not absolute support and resistance levels. Prices may break the rails and hit stop loss. Can set wider stop loss or use other stop loss methods like time exit.
2. RSI may fail in some markets. Can consider combining other indicators like KDJ and MACD for more reliable overbought/oversold judgment.
3. Wrong signals may occur during reversals and consolidations. Can add trend filter to only trade along the major trend.

Enhancement Suggestions:

1. Test and optimize BB period and standard deviation for different products.
2. Test and optimize RSI period parameter.
3. Test other stop loss methods like trailing stop loss and time exit.
4. Add more trend indicators and signal indicators to build multifactor models.

Conclusion:

The strategy combines Bollinger Bands, RSI and other indicators for entry and exit signals. It controls risks while ensuring signal accuracy. More optimization can be done on parameters and enhancements like multifactor models. Overall it provides a simple and practical idea on price breakout strategies.

[/trans]

> Source (PineScript)

```pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
Period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Custom Strategy", overlay=true)

length = 14
mult