> Name

MACD Golden Cross and Death Cross Strategy - MACD-Golden-Cross-and-Death-Cross-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/d668b94bd6a7c89a46.png)

---

#### Overview
This strategy uses the crossover of the DIF line and DEA line in the MACD indicator to generate trading signals. When the DIF line crosses above the DEA line, it generates a long signal; when the DIF line crosses below the DEA line, it generates a short signal. The backtesting results of this strategy show that on the BTCUSDT trading pair, the win rate is about 40%, and the annualized return is 1.05. However, it will cause the number of assets held to increase continuously, so it cannot be used as an independent arbitrage strategy.

#### Strategy Principle
1. Calculate the fast exponential moving average (EMA) and slow exponential moving average (EMA).
2. Calculate the DIF line, which is the difference between the fast EMA and the slow EMA.
3. Calculate the DEA line, which is the EMA of the DIF line.
4. Calculate the MACD histogram, which is the difference between the DIF line and the DEA line.
5. When the DIF line crosses above the DEA line, generate a long signal and open a long position.
6. When the DIF line crosses below the DEA line, generate a short signal, close the long position, and open a short position.
7. When the opposite crossover signal appears again, close the current position and open a position in the opposite direction.

#### Strategy Advantages
1. This strategy uses the widely used MACD indicator, which is easy to understand and implement.
2. The strategy logic is clear, and the trading signals are explicit.
3. It is suitable for trending markets and can track the main trends of the market.

#### Strategy Risks
1. The win rate of this strategy is low, only 40%, which means that 60% of the trades may be losing.
2. This strategy will cause the number of assets held to increase continuously, which may bring additional risk exposure.
3. In a fluctuating market, this strategy may generate frequent trading signals, leading to high trading costs.
4. This strategy does not consider risk management, such as stop-loss and position management, which may lead to significant losses.

#### Strategy Optimization Directions
1. Introduce trend filters, such as long-term moving averages, to avoid trading in fluctuating markets.
2. Optimize the parameters of the MACD indicator, such as the period of the fast EMA, slow EMA, and signal line, to adapt to different market conditions.
3. Add risk management measures, such as stop-loss and position management, to control potential losses.
4. Combine with other technical indicators or fundamental analysis to improve the reliability of trading signals.

#### Summary
The MACD golden cross strategy is a simple and easy-to-understand trading strategy that is suitable for trending markets. However, the win rate of this strategy is low, and it lacks risk management measures, so it needs further optimization and improvement. By introducing trend filters, optimizing parameters, adding risk management, and combining with other analysis methods, the performance and reliability of this strategy can be improved. Nevertheless, this strategy still cannot be used as an independent arbitrage strategy and needs to be combined with other strategies to obtain better trading results.

---

#### Strategy Arguments

| Argument | Default | Description |
| ---- | ---- | ---- |
| v_input_1 | 12 | Fast line length |
| v_input_2 | 26 | Slow line length |
| v_input_3 | 9 | MACD signal line length |
| v_input_4 | green | MACD bar growth above zero line |
| v_input_5 | #99e69c | MACD bar growth below zero line |
| v_input_6 | orange | MACD bar decline above zero line |
| v_input_7 | red | MACD bar decline below zero line |
| v_input_8 | true | Whether to display entry and exit signals |

---

> Source (PineScript)

```pinescript
// Version=5
// Description: This strategy uses the crossover of DIF and DEA lines in the MACD indicator for long and short operations. Backtesting shows a win rate of about 40% on BTCUSDT, with an annualized return of 1.05, but it causes the number of held assets to increase continuously, making it unsuitable as an independent arbitrage strategy.

strategy("MACD Golden Cross Strategy", overlay=true)

fastLength = input(12, "Fast line length")
slowLength = input(26, "Slow line length")
MACDLength = input(9, "MACD signal line length")

deltaIncreaseOver0 = input(color.green, 'MACD bar growth above zero line')
deltaIncreaseUnder0 = input(color.rgb(153, 230, 156), 'MACD bar growth below zero line')

deltaDecreaseOver0 = input(color.orange, 'MACD bar decline above zero line')
deltaDecreaseUnder0 = input(color.red, 'MACD bar decline below zero line')

buySellEnabled = input(true, 'Whether to display entry and exit signals')

// @variable Long round count
var longRound = 0
// @variable Short round count
var shortRound = 0

DIF = ta.ema(close, fastLength) - ta.ema(close, slowLength) // Fast and slow EMA difference
EDA = ta.ema(DIF, MACDLength) // DIF line's EMA
delta = DIF - EDA // MACD bar height

// plot(0, 'Zero', color.black)
plot(DIF, 'DIF', color.yellow)
plot(EDA, "EDA", color.purple)

isDeltaIncreasing = delta[1] < delta
isDeltaOver0 = delta > 0
deltaColor = isDeltaIncreasing ? (isDeltaOver0? deltaIncreaseOver0: deltaIncreaseUnder0) : (isDeltaOver0?