> Name

Volatility-and-Trend-Tracking-Strategy-Across-Timeframes-Based-on-Williams-VIX-and-DEMA

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11da0f7064c6bb3d555.png)
 [trans]

## Overview

This strategy first calculates the Williams VIX indicator by getting the difference between the highest price and the lowest price over a certain period divided by the highest price. Then, combining the idea of standard deviation from Bollinger Bands, it sets the upper and lower bands. At the same time, it sets the take profit range based on percentile over a certain period. In the entry part, when the price crosses below the upper band and is lower than the DEMA indicator, it goes long. When the price crosses above the lower band and is higher than the DEMA indicator, it goes short.

## Strategy Logic

This strategy mainly utilizes the Williams VIX indicator to gauge market volatility and risk, while using the DEMA indicator to judge the price trend.

Firstly, the calculation formula for Williams VIX indicator is:

```
WVF = ((Highest(close, n) - Low) / (Highest(close, n))) * 100
```

Where `n` is the parameter period. This indicator reflects the volatility between the highest price and the lowest price over a certain period. The higher the value, the greater the volatility and higher the risk.

On this basis, the strategy employs the idea of Bollinger Bands. The upper band is set as middle band + n times standard deviation, and the lower band is set as middle band - n times standard deviation. When price approaches the upper band, it indicates expanding volatility and long opportunity; when price approaches the lower band, it indicates contracting volatility and short opportunity.

In addition, the strategy also sets a take profit range based on percentile principle over a period. For example, 90th percentile means the latest 90% of prices over the statistical period. When price surpasses this percentile, it indicates that the volatility has been quite big and it’s time to consider taking profit.

In the actual trading strategy, it incorporates DEMA indicator to judge the trend. It only goes long when price crosses below upper band and is lower than DEMA; it only goes short when price crosses above lower band and is higher than DEMA.

## Advantage Analysis

This strategy combines the Williams VIX indicator which judges volatility, Bollinger Bands based on standard deviation, and DEMA indicator which judges the trend, making it very comprehensive to grasp the two key market factors: risk and trend.

Specifically, the Williams VIX combined with BB upper and lower bands can make risk and volatility judgments; the DEMA indicator can determine the price trend direction; the take profit range setting can lock in profits and avoid being too greedy.

Therefore, this strategy does very well in capturing risks and trends. It not only chooses better entry timing but also avoids the reversal risk when decent profits have been made through the take profit range, making it a stable and conservative strategy.

## Risk Analysis

The biggest risk of this strategy is that the volatility indicator and trend indicator may diverge. That is when the Williams VIX indicator shows increasing volatility and price nears the BB upper or lower bands, the DEMA indicator’s judgement contradicts it. For example, volatility shows long opportunity but DEMA displays downward trend. There could be losses in situations like this.

In addition, excessively conservative take profit range settings could also hurt the strategy's profitability. If the percentile parameter is set too low, it would be hard to trigger taking profit, failing to lock in gains.

## Optimization Directions

We could consider making take profit range parameters adjustable for different market environments. Specifically, in range-bound markets, appropriately lift percentile parameters to expand the profit-taking range. But in obvious trending markets, lower the percentile parameter to take profits in time.

Also, we could consider adding other indicators to judge the trend. When the original DEMA diverges from the new indicators, suspend opening positions to avoid losses from false signals.

## Conclusion

This strategy comprehensively utilizes volatility indicators, standard deviation principles, trend judgements and profit-taking ideas to address market risk and trend changes very well. It is stable and conservative, suitable for long-term holdings. Through parameter optimization, the strategy's stability and profitability could be further enhanced.