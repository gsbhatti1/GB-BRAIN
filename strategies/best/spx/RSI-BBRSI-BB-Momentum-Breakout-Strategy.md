> Name

RSI-BB Momentum Breakout Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16aac6830cf06137396.png)
[trans]


## Overview

The RSI-BB momentum breakout strategy is a breakout trading strategy that combines the Relative Strength Index (RSI) and Bollinger Bands (BB). The strategy uses RSI to identify market trends and overbought/oversold conditions, while BB identifies breakouts. When both RSI and BB signals align, corresponding long or short trades are executed.

## Strategy Logic

The code first calculates the RSI and BB indicators.

The RSI is calculated as:

```pine
up = rma(max(change(close), 0), 30) 
down = rma(-min(change(close), 0), 30)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
```

Where `up` measures the upward price movement over 30 periods, `down` measures the downward price movement, and `rsi` is computed based on the ratio of `up` to `down`.

The BB is calculated as:

```pine
basis = sma(close, 50)
dev = 0.2 * stdev(close, 50) 
upper = basis + dev
lower = basis - dev
```

Where `basis` is the 50-period moving average, `dev` is 0.2 times the standard deviation, and `upper` and `lower` are the bands.

The bbi (bollinger bandwidth index) is computed as:

```pine 
bbr = close>upper? 1 : close<lower? -1 : 0
bbi = bbr - bbr[1]
```

`bbr` checks if `close` breaks the upper or lower band. A breakout is 1, a breakdown is -1, otherwise 0. `bbi` is the difference between the current and previous `bbr`. Positive `bbi` indicates an upward breakout, negative indicates a downward.

The strategy's trading signals are determined as:

```
long = rsi>52 and rsi<65 and bbi>0.11 and bbi<0.7 
short = rsi<48 and rsi>35 and bbi<-0.11 and bbi>-0.7
```

A long position is taken when RSI is between 52-65, and BBI is between 0.11 and 0.7. A short position is taken when RSI is between 35-48, and BBI is between -0.11 and -0.7.

## Advantages

1. Combining the RSI and BB indicators allows for more accurate signal identification. RSI gauges trends and overbought/oversold levels, while BB identifies breakouts, making the combined signals more reliable.
2. The 30-period RSI helps filter out some market noise and focuses on major trends.
3. The 50-period BB with a 0.2 standard deviation helps filter out false breakouts.
4. BBI thresholds further filter out fake breakouts.
5. Setting the RSI long/short zones to 52-65 and 35-48 provides some buffer to avoid missing trades.

## Risks

1. Breakout trading strategies can easily get caught in whipsaws, so stop loss management is crucial.
2. Backtest results may be overfitted, leading to different live performance.
3. Extreme market movements can hit the stop loss and result in significant losses.
4. Optimizing RSI and BB parameters, including periods and thresholds, is necessary.
5. Order price settings significantly impact real-world performance.

## Enhancement Opportunities

1. Test different combinations of RSI and BB parameters to find optimal settings.
2. Add other indicators like MACD or KD for signal filtration.
3. Optimize the RSI long/short zones to filter out more noise.
4. Optimize dynamic BBI thresholds to better filter false breakouts.
5. Introduce a trend filter to avoid trading against major trends.
6. Test different stop loss techniques to find optimal risk control.
7. Test different order types to minimize slippage impact.

## Conclusion

The RSI-BB strategy combines the strengths of using trend and momentum indicators, showing promising backtest results. However, live performance can vary due to real-world factors such as slippage and stop loss management. Parameters and filters need to be optimized based on backtest results, and stop loss and order placement should also be evaluated for their effectiveness in live trading. While the strategy has merit, it requires ongoing improvements and robustness testing to generate consistent results.

|||


## Overview

The RSI-BB momentum breakout strategy combines Relative Strength Index (RSI) and Bollinger Bands (BB) indicators for breakout trading. It uses RSI to identify market trends and overbought/oversold levels, and BB to determine breakouts. When both RSI and BB signals align, the strategy executes long or short trades accordingly.

## Strategy Logic

The code first calculates the RSI and BB indicators.

The RSI is calculated as:

```pine
up = rma(max(change(close), 0), 30)
down = rma(-min(change(close), 0), 30) 
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
```

Where `up` measures the upward price movement over 30 periods, `down` measures the downward price movement, and `rsi` is computed based on the ratio of `up` to `down`.

The BB is calculated as:

```pine
basis = sma(close, 50)
dev = 0.2 * stdev(close, 50) 
upper = basis + dev
lower = basis - dev
```

Where `basis` is the 50-period moving average, `dev` is 0.2 times the standard deviation, and `upper` and `lower` are the bands.

The bbi (bollinger bandwidth index) is computed as:

```pine 
bbr = close>upper? 1 : close<lower? -1 : 0
bbi = bbr - bbr[1]
```

`bbr` checks if `close` breaks the upper or lower band. A breakout is 1, a breakdown is -1, otherwise 0. `bbi` is the difference between the current and previous `bbr`. Positive `bbi` indicates an upward breakout, negative indicates a downward.

The strategy signals are determined as:

```
long = rsi>52 and rsi<65 and bbi>0.11 and bbi<0.7
short = rsi<48 and rsi>35 and bbi<-0.11 and bbi>-0.7
```

A long position is taken when RSI is between 52-65, and BBI is between 0.11 and 0.7. A short position is taken when RSI is between 35-48, and BBI is between -0.11 and -0.7.

## Advantages

1. Combining the RSI and BB indicators allows for more accurate signal identification. RSI gauges trends and overbought/oversold levels, while BB identifies breakouts, making the combined signals more reliable.
2. The 30-period RSI helps filter out some market noise and focuses on major trends.
3. The 50-period BB with a 0.2 standard deviation helps filter out false breakouts.
4. BBI thresholds further filter out fake breakouts.
5. Setting the RSI long/short zones to 52-65 and 35-48 provides some buffer to avoid missing trades.

## Risks

1. Breakout trading strategies are prone to being caught in whipsaws, so stop loss management is crucial.
2. Backtest results may be overfitted, leading to different live performance.
3. Extreme market movements can hit the stop loss and result in significant losses.
4. Optimizing RSI and BB parameters, including periods and thresholds, is necessary.
5. Order price settings significantly impact real-world performance.

## Enhancement Opportunities

1. Test different combinations of RSI and BB parameters to find optimal settings.
2. Add other indicators like MACD or KD for signal filtration.
3. Optimize the RSI long/short zones to filter out more noise.
4. Optimize dynamic BBI thresholds to better filter false breakouts.
5. Introduce a trend filter to avoid trading against major trends.
6. Test different stop loss techniques to find optimal risk control.
7. Test different order types to minimize slippage impact.

## Conclusion

The RSI-BB strategy combines the strengths of using trend and momentum indicators, showing promising backtest results. However, live performance can vary due to real-world factors such as slippage and stop loss management. Parameters and filters need to be optimized based on backtest results, and stop loss and order placement should also be evaluated for their effectiveness in live trading. While the strategy has merit, it requires ongoing improvements and robustness testing to generate consistent results.

``` pinescript
//@version=4
// Based on Larry Connors RSI-2 Strategy - Lower RSI
strategy(title="Spyfrat Strat", shorttitle="SpyfratStrat",
```