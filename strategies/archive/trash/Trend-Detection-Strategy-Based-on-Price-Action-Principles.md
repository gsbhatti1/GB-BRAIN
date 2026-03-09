### Overview

The core idea of this strategy is to determine the current trend direction based on the relationship between the high point and closing price of K-line bars, and smooth the results using moving average lines. When there are more high closing bars, it is determined as an upward trend. When there are more low closing bars, it is determined as a downward trend. This strategy is suitable for any digital asset with certain liquidity, and better results can be obtained through parameter optimization.

### Strategy Logic

This strategy uses M-minute bars. According to the position relationship between the closing price and the high and low points, it is determined whether the M-minute K-line bar belongs to a high closing type (closing price close to high point), low closing type (closing price close to low point) or normal type (closing price close to middle).

Specifically, first calculate delt = high - close, which is the difference between the high point and the closing price, and height = high - low, which is the difference between high and low. If delt > height * 2/3, it is determined as a high closing type. If delt < height/3, it is determined as a low closing type, otherwise it is a normal type.

Then count the number of high closing, low closing and normal types in the most recent N K-line bars, calculate the percentage they account for, and use EMA to smooth them into rise, fall and middle curves. The rise curve represents the percentage of high closing bars, the fall curve represents the percentage of low closing bars, and the middle curve represents the percentage of normal bars.

When the rise curve crosses above the fall curve, it means that high closing bars begin to increase, indicating the market is entering an upward trend, and a long signal is issued. When the fall curve crosses below the rise curve, it means low closing bars begin to increase, indicating the market is entering a downward trend, and a short signal is issued.

### Advantages of the Strategy

This price action based trend judgment strategy has the following advantages:

1. The principle is clear and easy to understand and master.
2. It does not rely on any indicators, but purely judges the trend direction based on the characteristics of the price itself.
3. There are few configurable parameters, mainly N and EMA smoothing parameters, which are easy to optimize.
4. It can be widely applied to any digital asset with certain liquidity, including stocks, forex, cryptocurrencies, etc.
5. The backtest results are good, and risks can be strictly controlled.
6. It can be further combined with trendlines, support/resistance levels and other technical methods for optimization.
7. Stop loss strategies can be configured to control single loss.

### Risks of the Strategy

Despite the advantages, the strategy also has the following risks:

1. When the market is in a shock state, the K-line type switches frequently, which may generate false signals.
2. Improper N and EMA parameter settings may lead to missing trends or too many invalid signals.
3. Judging the trend direction solely based on K-line types has some lag.
4. It cannot effectively filter common chart patterns like triangle convergence, flags, etc., with the risk of reverse breakthroughs.
5. This strategy belongs to trend following, and cannot effectively capture reversal opportunities.
6. Stop loss should be used to control the risk of loss, otherwise single loss can be large.

### Directions for Strategy Optimization

To reduce risks and improve profitability, the strategy can be optimized in the following aspects:

1. Combine volatility indicators like ATR to adjust N and EMA parameters based on market volatility, avoiding excessive invalid signals in range-bound markets.
2. Add Volume analysis to filter false breakouts in high volume conditions.
3. Combine trendlines and key support/resistance levels to determine trend direction and breakthrough authenticity.
4. Add multiple timeframe analysis to avoid misjudgments on a single timeframe.
5. Add pattern recognition modules to reverse positions in a timely manner when significant reversal signals appear.
6. Optimize stop loss strategies based on market volatility and risk preference.
7. Add trailing stop loss, moving stop loss etc. to lock in profits and prevent profit erosion.

### Summary

This strategy is based on price action to determine the trend direction, with clear principles and good backtest results, suitable for digital asset trading. However, it has certain limitations that require accompanying stop-loss strategies and optimizations to reduce risks. Overall, this strategy provides a simple and practical approach for quantitative trading, worth learning and adopting. Through continuous optimization and combination, stable excess returns can be expected.