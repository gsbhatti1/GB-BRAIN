## Overview

This strategy utilizes two technical indicators, Bollinger Bands and Relative Strength Index (RSI), for bullish swing trading in uptrends. The strategy logic is simple yet effective: open a long position when the price breaks below the lower Bollinger Band and RSI is below 35, and close the position when RSI crosses above 69. Take profit and stop loss levels are also set.

## Strategy Principles

1. Calculate RSI: Use Relative Moving Average (RMA) to calculate the average magnitude of price increases and decreases separately, then divide the magnitude of increases by the total magnitude to obtain RSI. RSI reflects the strength of price movements over a period of time.

2. Calculate Bollinger Bands: Use Simple Moving Average (SMA) to calculate the price midline, then add and subtract standard deviations to get the upper and lower bands. Bollinger Bands can dynamically reflect the range of price fluctuations.

3. Open long: When the price breaks below the lower Bollinger Band and RSI is less than 35, it is considered oversold, and a long position is opened. These two conditions can capture the timing of an upward reversal.

4. Close long: When RSI crosses above 69, it is considered overbought, and the long position is closed to lock in profits.

5. Take profit and stop loss: After opening a position, the take profit and stop loss prices are calculated based on user-defined percentages. The position is closed when either the take profit or stop loss price is reached. This helps control the risk and return of each trade.

## Advantage Analysis

1. Bollinger Bands can objectively reflect the range of price movements and adjust in sync with price trends without being limited by fixed thresholds.

2. RSI can intuitively reflect the balance between bullish and bearish forces and is also relatively objective. It is often used to determine overbought and oversold conditions.

3. When used in uptrends, it is more suitable for swing trading. By capturing price rebounds with the lower Bollinger Band and low RSI, and timely closing positions with high RSI, it can effectively capture short-term market movements.

4. The setting of take profit and stop loss makes the strategy's risk controllable. Investors can flexibly set parameters according to their risk preferences.

5. The strategy logic and code are relatively simple, easy to understand and implement, and the backtest results are relatively stable.

## Risk Analysis

1. In choppy markets, Bollinger Bands and RSI may generate too many trading signals, leading to high trading frequency and increased transaction costs.

2. A single indicator like RSI is easily affected by short-term price fluctuations and may produce misleading signals. Therefore, RSI signals are best analyzed in conjunction with price trends.

3. The selection of Bollinger Band and RSI parameters has a significant impact on strategy performance, and different markets and instruments may require different parameters. Users need to make appropriate adjustments based on specific situations.

4. In the event of unexpected events or abnormal market conditions, Bollinger Bands and RSI may become ineffective. If there are no other risk control measures in place, it may bring significant drawdowns to the strategy.

## Optimization Directions

1. Consider introducing other technical indicators such as moving averages for filtering. For example, only open positions when the moving averages are in a bullish alignment to improve the reliability of signals.

2. Optimize the upper and lower thresholds of RSI, the parameters of Bollinger Bands, etc., to find the best performing parameter combinations for each instrument and time frame.

3. Based on backtesting, conduct forward testing and proper simulated trading to fully validate the effectiveness and stability of the strategy before live trading.

4. Further control strategy drawdowns and improve risk-adjusted returns through position sizing, dynamic take profit and stop loss, and other methods.

5. Incorporate the strategy into an investment portfolio and use it in conjunction with other strategies for hedging, rather than using it in isolation, to improve portfolio stability.

## Conclusion

This article introduces a bullish swing trading strategy based on two technical indicators, Bollinger Bands and RSI. The strategy is suitable for capturing short-term market movements in uptrends and has simple logic and implementation. By opening long positions when the price breaks below the lower Bollinger Band and RSI is low, and closing positions when RSI is high, the strategy sets take profit and stop loss levels to control risk. The strategy's advantages include its objective reflection of price movements and balance between bullish and bearish forces, as well as manageable risk. However, in practical use, it is important to control trading frequency, use additional indicators for signal filtering, optimize parameters, and manage positions. Furthermore, the strategy may become ineffective in unexpected market conditions, and other risk control measures should be considered. By incorporating additional filtering indicators, dynamic take profit and stop loss, position management, and portfolio configuration, the stability and profitability of the strategy can be further enhanced. In summary, this strategy can be a valuable supplement for trend investors, but its use should be carefully considered based on individual characteristics.