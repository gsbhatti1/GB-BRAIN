> Name

Dual-Moving-Average-Crossover-Entry-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1815bf480bdcc2b8bfe.png)

[trans]
#### Overview
This is a double moving average crossover entry strategy based on the 5-day moving average (MA5). The main idea of this strategy is to enter positions at a certain distance above or below the MA5, and close positions when the closing price is higher than the entry price or returns to the entry price. This strategy aims to capture short-term trends while controlling risks.

#### Strategy Principle
This strategy uses the 5-day simple moving average (SMA) as the primary indicator. When the opening price of a new candle is above the MA5, it executes buy scenario 1; when the opening price of a new candle is below the MA5 and the distance from the MA5 exceeds 0.002 points, it executes buy scenario 2. For sell conditions, when the closing price is higher than or equal to the average entry price, it executes sell scenario 1; if the closing price is 0.1% lower than the average entry price, it executes sell scenario 2.

#### Advantage Analysis
1. This strategy is based on short-term trends and can quickly capture market changes.
2. By setting a threshold for the distance from the MA5, some noise signals can be filtered out.
3. By setting stop-loss conditions, risks can be effectively controlled.
4. The strategy logic is clear and easy to understand and implement.

#### Risk Analysis
1. This strategy relies on a single indicator and may face the risk of indicator failure.
2. Short-term trend strategies may face the risk of frequent transactions and increased transaction costs.
3. Fixed stop-loss ratios may not be adaptable to different market environments.

#### Optimization Direction
1. You can consider introducing other indicators, such as RSI, MACD, etc., to improve the reliability of the signal.
2. Stop loss and take profit conditions can be optimized, such as using trailing stop loss or dynamic stop loss ratio.
3. Different parameters can be set for different market environments to improve the adaptability of the strategy.

#### Summary
This double moving average crossover entry strategy is a simple strategy based on short-term trends. Through the upper and lower crossing of MA5 and setting distance thresholds, short-term trend opportunities can be captured. At the same time, fixed proportion stop loss can control risks. However, this strategy also has some limitations, such as reliance on a single indicator, frequent trading, etc. In the future, you can consider introducing more indicators, optimizing stop-loss and stop-profit conditions, and improving the robustness and adaptability of the strategy.

||

#### Overview
This is a dual moving average crossover entry strategy based on the 5-day moving average (MA5). The main idea of this strategy is to enter positions at a certain distance above or below the MA5, and close positions when the closing price is higher than the entry price or returns to the entry price. This strategy aims to capture short-term trends while controlling risks.

#### Strategy Principle
This strategy uses the 5-day simple moving average (SMA) as the main indicator. When the opening price of a new candle is above the MA5, it executes buy scenario 1; when the opening price of a new candle is below the MA5 and the distance from the MA5 exceeds 0.002 points, it executes buy scenario 2. For sell conditions, when the closing price is higher than or equal to the average entry price, it executes sell scenario 1; if the closing price is 0.1% lower than the average entry price, it executes sell scenario 2.

#### Advantage Analysis
1. This strategy is based on short-term trends and can quickly capture market changes.
2. By setting a threshold for the distance from the MA5, some noise signals can be filtered out.
3. By setting stop-loss conditions, risks can be effectively controlled.
4. The strategy logic is clear and easy to understand and implement.

#### Risk Analysis
1. This strategy relies on a single indicator and may face the risk of indicator failure.
2. Short-term trend strategies may face frequent trading and increase the risk of transaction costs.
3. Fixed stop-loss percentages may not be able to adapt to different market environments.

#### Optimization Direction
1. Other indicators such as RSI and MACD can be considered to improve the reliability of signals.
2. Stop-loss and take-profit conditions can be optimized, such as using trailing stops or dynamic stop-loss percentages.
3. For different market environments, different parameters can be set to improve the adaptability of the strategy.

#### Summary
This dual moving average crossover entry strategy is a simple strategy based on short-term trends. By crossing above and below the MA5, and setting distance thresholds, short-term trend opportunities can be captured. At the same time, fixed percentage stop-losses can control risks. However, this strategy also has some limitations, such as relying on a single indicator and frequent trading. In the future, more indicators can be introduced, and stop-loss and take-profit conditions can be optimized to improve the robustness and adaptability of the strategy.

| |

```pinescript
/*backtest
start: 2023-04-24 00:00:00
end: 2024-04-29 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("YBS Strategy 1.1", overlay=true)

// Moving Average Settings
ma5 = ta.sma(close, 5)

// Buy Scenario 1: Enter when a new candle opens above the MA5
buy_condition_scenario1 = open > ma5

// Buy Scenario 2: Enter when a new candle opens below the MA5 and is at a significant distance from the MA5
distance_from_ma5 = open - ma5
buy_condition_scenario2 = open < ma5 and distance_from_ma5 > 0.002 // Define distance in points here

// Sell Conditions:
// Scenario 1: Sell if closing price is higher than or equal to the average entry price
sell_condition_scenario1 = close >= strategy.entry_price

// Scenario 2: Sell if closing price is 0.1% lower than the average entry price
sell_condition_scenario2 = close <= (strategy.entry_price * 0.999) // Use dynamic stop-loss here

// Execute buy scenario 1
if (buy_condition_scenario1)
    strategy.entry("Buy Scenario 1", strategy.long)

// Execute buy scenario 2
if (buy_condition_scenario2)
    strategy.entry("Buy Scenario 2", strategy.long)

// Sell: Execute sell scenarios based on closing price conditions
if (sell_condition_scenario1 or sell_condition_scenario2)
    strategy.exit("Sell Scenario 1", "Buy Scenario 1")
    strategy.exit("Sell Scenario 2", "Buy Scenario 2")

```