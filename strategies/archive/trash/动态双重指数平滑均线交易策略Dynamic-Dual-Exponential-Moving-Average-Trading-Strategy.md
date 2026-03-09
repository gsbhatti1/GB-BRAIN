> Name

Dynamic Dual Exponential Moving Average Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/c76acb0f5e9b040035.png)
[trans]
### Overview

This strategy is named "Dynamic Dual Exponential Moving Average Trading Strategy," and it is a quantitative trading strategy based on the dual exponential moving average (DEMA). The strategy calculates the price change rate of stocks, then performs dual exponential smoothing on both its absolute value and non-absolute value to obtain the True Strength Index (TSI). Traders generate buy and sell signals based on the golden/dead cross of the TSI value and its signal line.

### Strategy Principle

The core indicator of this strategy is the True Strength Index (TSI). The calculation formula for TSI is:

\[ \text{TSI} = 100 \times \left( \frac{\text{PC1}}{\text{PC2}} \right) \]

Where PC1 and PC2 are the dual exponential moving averages of the price change rate and the absolute value of the price change rate, respectively. The dual exponential moving average is calculated by first applying an exponential moving average with one length to the price change rate, and then applying another shorter exponential moving average to the obtained moving average. This dual smoothing can better eliminate the randomness in the price change rate and improve the stability of the TSI indicator.

After calculating the TSI value, the strategy also calculates a signal line for the TSI value. The signal line is defined as an exponential moving average of the TSI value over a certain period. In actual trading, the strategy judges market trends and generates trading signals by observing the relationship between the TSI value and its signal line. When the TSI value crosses above the signal line, it is a buy signal; when the TSI value crosses below the signal line, it is a sell signal.

Another feature of this strategy is that trade size is dynamically adjusted. The strategy code sets an initial capital and a risk exposure ratio as input parameters. These two parameters combine with the current price of the stock to dynamically calculate the number of contracts traded or risk exposure. This can better control the overall risk of the entire strategy.

### Advantage Analysis

The dynamic dual exponential moving average trading strategy brings several advantages:

1. It utilizes the TSI indicator, which applies dual exponential smoothing, making it less sensitive to market noise and able to generate more accurate signals.
2. It is based on a proven principle, i.e., crossing of an indicator and its signal line to generate trading signals. This eliminates many false signals.
3. The strategy dynamically adjusts position sizing based on the risk budget. This helps prevent overtrading and emotions.
4. It works on daily and weekly timeframes, suitable for both swing trading and positional trading.
5. It is easy to implement in bots and other trading systems due to the simple entry/exit logic.
6. There are not too many parameters to tune, making the system easy to optimize.

These advantages combined make it a robust and versatile trading strategy for stock traders. The careful smoothing and position sizing help prevent false signals and large losses.

### Risk Analysis

While the dynamic dual exponential moving average trading strategy has many advantages, it also carries some inherent risks like most stock strategies:

1. Since the TSI and signal line are based on historical price data, there is always a risk of incorrect signals, especially during volatile market conditions.
2. Whipsaws may occur if the market oscillates around the zero line of the TSI indicator. This can lead to losses.
3. Large gap moves may result in the strategy closing at a loss since it was not able to exit in time.
4. If the market continues in a strong trend, the TSI may prematurely reverse the trend resulting in missed profits.
5. Due to the leverage effect, larger losses than the limit set by the risk parameter

### Optimization Directions

Some ideas for optimizing this strategy include:

1. Testing different combinations of dual smoothing parameters to find those that produce more precise trading signals. Adjusting short and long cycle parameters can optimize performance.
2. Adding filters based on volatility, volume, or other indicators to reduce unnecessary trade signals. This can lower trade frequency while improving profitability per trade.
3. Increasing stop-loss logic, such as exiting trades when the TSI crosses below zero. This can reduce unnecessary losses.
4. Evaluating different trading instruments like indices, commodities, etc., under this strategy and focusing on those that perform best.
5. Implementing position selection filters. For example, assessing liquidity, volatility indicators, and selecting assets with higher parameter rankings for trading.
6. Using machine learning methods for forward-looking analysis to select optimal parameter combinations. This can reduce bias from manual selection and obtain better parameters.
7. Adopting multiple sets of parameters based on different market environments and dynamically switching between them. For example, using more aggressive parameter sets in bull markets and more conservative ones in bear markets.

Through testing and optimizing these various aspects, it is hoped that the stability and returns of this strategy can be further improved.

### Summary

In summary, this strategy, based on the dual exponential smoothing characteristic of the TSI indicator, designs a relatively stable and reliable stock trading strategy. By dynamically adjusting position sizing, it effectively controls overall risk levels. The strategy combines the advantages of both short-term and long-term trading.

Of course, like most quantitative trading strategies, this one also has certain limitations, mainly manifested in its susceptibility to significant market volatility impacts. Additionally, parameter selection and filter conditions need further testing and optimization to achieve stronger adaptability and profitability under complex and changing market conditions.