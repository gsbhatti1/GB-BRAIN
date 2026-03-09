#### Overview

This strategy is a trading system based on the Relative Strength Index (RSI), specifically designed for certain markets. It utilizes the oversold and overbought zones of the RSI indicator to determine entry and exit points, while incorporating a dynamic stop-loss mechanism to control risk. The core idea of this strategy is to enter long positions when the market is oversold and exit when the RSI rises to the overbought zone or reaches a preset maximum loss percentage.

#### Strategy Principles

1. **Entry Condition**: The strategy opens a long position when the RSI value falls below the set entry threshold (default 24). It uses the daily low price to calculate RSI, rather than the commonly used closing price, which may make the strategy more sensitive to market lows.

2. **Exit Conditions**: The strategy has two exit conditions:
   - a) When the RSI value exceeds the set exit threshold (default 72), indicating potential market overbought, the position is closed.
   - b) When the loss percentage exceeds the preset maximum loss tolerance (default 20%), it triggers a stop-loss closure.

3. **Position Management**: The strategy defaults to using 10% of the account's total value as the fund amount for each trade.

4. **RSI Calculation**: RSI is calculated using a 14-day period, but based on the low price rather than the traditional closing price.

#### Strategy Advantages

1. **Dynamic Entry**: By using RSI lows as entry signals, the strategy can capture potential rebound opportunities when the market is oversold.
2. **Risk Control**: Combines both technical indicator (RSI) and percentage stop-loss exit mechanisms, allowing for timely profit-taking when the market turns and controlling losses when the trend is unfavorable.
3. **Flexibility**: The strategy allows users to customize the RSI calculation period, entry and exit thresholds, and maximum loss percentage, which can be adjusted according to different market characteristics.
4. **Using Low Price for RSI Calculation**: This non-traditional RSI calculation method may be more likely to capture extreme market lows, favoring entry at lower price positions.
5. **Simplicity and Clarity**: The strategy logic is relatively simple, easy to understand and implement, while also being convenient for subsequent optimization and expansion.

#### Strategy Risks

1. **False Breakout Risk**: In highly volatile markets, RSI may frequently trigger entry signals, leading to multiple trades being initiated and quickly stopped out.
2. **Insufficient Trend Following**: The strategy mainly relies on RSI reversal signals, which may lead to premature closing of positions in strong trend markets, missing out on larger profit opportunities.
3. **Fixed Percentage Stop-Loss**: Although a stop-loss mechanism is set, a fixed percentage stop-loss may not be suitable for all market conditions, potentially being too loose or too tight in certain situations.
4. **Single Indicator Dependence**: The strategy relies solely on the RSI indicator, lacking verification from other technical indicators or fundamental factors, which may increase the risk of misjudgment.
5. **Specific Market Limitations**: The strategy is designed for specific markets and may not be applicable to other types of financial products or markets.

#### Strategy Optimization Directions

1. **Multi-Indicator Combination**: Consider introducing other technical indicators such as moving averages, Bollinger Bands, etc., to be used in conjunction with RSI to improve signal reliability.
2. **Adaptive Parameters**: Develop a mechanism to automatically adjust the RSI calculation period and entry/exit thresholds based on market volatility, making the strategy more adaptive.
3. **Dynamic Stop-Loss**: Change the fixed percentage stop-loss to a trailing stop-loss or ATR (Average True Range) stop-loss, which may better adapt to different market volatility situations.
4. **Position Management Optimization**: Consider dynamically adjusting the fund ratio for each trade based on RSI strength or market volatility, rather than using a fixed 10% of account value.
5. **Trend Filtering**: Introduce trend determination mechanisms such as long-term moving averages to avoid premature closure in strong uptrends.
6. **Time Window Filtering**: Add transaction time window restrictions to avoid trading during times of low market volatility or poor liquidity.
7. **Backtesting and Optimization**: Conduct extensive parameter optimization and backtesting to find the best parameters for different market conditions.

#### Summary

This RSI-based dynamic low-price entry and stop-loss strategy provides a concise and effective trading method by leveraging RSI oversold and overbought signals, combined with dynamic stop-loss mechanisms, to capture market lows while controlling risk. Its uniqueness lies in using the daily low price to calculate RSI, which may make it more sensitive to market bottoms.

However, the strategy also has some limitations, such as excessive reliance on a single indicator and potential premature exits. To enhance its robustness and adaptability, incorporating multi-indicator validation, adaptive parameters, dynamic stop-loss mechanisms, and trend filtering can be considered. Additionally, thorough backtesting and parameter optimization tailored to different market conditions are necessary.

Overall, this strategy offers traders a solid starting point that can be customized and improved based on individual trading styles and market characteristics. In practical application, it is recommended for traders to carefully assess the strategy's performance across various market environments and combine other analytical tools and risk management techniques to enhance its overall effectiveness.