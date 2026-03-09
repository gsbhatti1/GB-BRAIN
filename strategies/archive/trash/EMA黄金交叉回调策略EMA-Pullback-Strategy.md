> Name

EMA Gold Cross Pullback Strategy EMA-Pullback-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/19d8b507ed52ece24ea.png)
[trans]

## Overview

The EMA gold cross pullback strategy is a quantitative trading strategy based on the EMA indicator. It constructs trading signals using three EMAs with different periods and combines price pullback mechanisms to set stop loss and take profit, enabling automated trading.

## Strategy Principle

This strategy uses three EMAs:

- **EMA1:** For judging price pullback support/resistance level; it has a shorter period by default at 33 periods.
- **EMA2:** For filtering some reversal signals; its period is five times that of EMA1, set to 165 periods by default.
- **EMA3:** For determining the overall trend direction; its period is eleven times that of EMA1, set to 365 periods by default.

Trading signals are generated according to the following logic:

- **Long Signal:** Price crosses above EMA1 and pulls back below EMA1 forming higher lows. If this pullback does not reach EMA2, a long position is entered when price crosses back above EMA1.
- **Short Signal:** Price crosses below EMA1 and pulls back above EMA1 forming lower highs. If this pullback does not reach EMA2, a short position is entered when price crosses back below EMA1.

Stop loss is set at the lowest/highest pullback price for long/short positions. Take profit is set to twice the stop loss level.

## Strategy Advantages

This strategy has several advantages:

1. Trading signals are constructed using a reliable EMA indicator.
2. Combining price pullback mechanisms effectively avoids getting trapped.
3. Stop losses are set at previous highs/lows, which effectively control risk.
4. Take profits satisfy risk-reward ratios.
5. EMAs can be adjusted according to market cycles.

## Strategy Risks

The strategy also has some risks:

1. The EMA indicator may have a lag effect and miss trend reversal points.
2. Excessive pullback range exceeding EMA2 may generate false signals.
3. Stop losses might be broken in trending markets.
4. Improper parameter settings could lead to excessive trading or missing opportunities.

These risks can be mitigated by adjusting EMAs, setting pullback limits, etc., and using other indicators to filter signals.

## Optimization Directions

The strategy can also be optimized in the following aspects:

1. Adding a trend indicator to avoid counter-trend trades, e.g., MACD.
2. Including a trading volume indicator to avoid false breakouts, e.g., OBV.
3. Optimizing EMA periods or using adaptive EMAs.
4. Dynamically optimizing parameters with machine learning methods like bag-of-words models.
5. Incorporating model predictions for adaptive stop loss and take profit.

## Conclusion

The EMA gold cross pullback strategy constructs a trading system using three EMAs, and sets stop losses and take profits based on price pullbacks to automate trading. It effectively controls trading risks and can be optimized by adjusting parameters based on market conditions. Overall, the strategy has sound logic and practical application. Future improvements could focus on trend determination, parameter optimization, and risk management.

||

## Overview  

The EMA pullback strategy is a quantitative trading strategy based on the EMA indicator. It constructs trading signals using three EMAs with different periods and sets stop loss and take profit based on price pullbacks to automate trading.

## Strategy Principle  

This strategy uses three EMAs:  

- **EMA1:** For judging price pullback support/resistance level, with a relatively short period, default to 33 periods.
- **EMA2:** For filtering some reversal signals, with a period of 5 times EMA1, default to 165 periods.  
- **EMA3:** For determining overall trend direction, with a period of 11 times EMA1, default to 365 periods.

Trading signals are generated according to the following logic:  

**Long Signal:** Price crosses above EMA1, pulls back below EMA1 forming higher lows, and this pullback does not reach EMA2. Enter long when price crosses back above EMA1.  

**Short Signal:** Price crosses below EMA1, pulls back above EMA1 forming lower highs, and this pullback does not reach EMA2. Enter short when price crosses back below EMA1.

Stop loss is set at the lowest/highest pullback price for long/short positions. Take profit is set to twice the stop loss level.

## Strategy Advantages  

This strategy has several advantages:  

1. Trading signals constructed using a reliable EMA indicator.
2. Combining price pullback mechanisms effectively avoids getting trapped.
3. Stop losses are set at previous highs/lows, which effectively control risk.
4. Take profits satisfy risk-reward ratios.
5. EMAs can be adjusted according to market cycles.

## Strategy Risks

This strategy also has some risks:  

1. The EMA indicator may have a lag effect and miss trend reversal points.
2. Excessive pullback range exceeding EMA2 may generate false signals.
3. Stop losses might be broken in trending markets.
4. Improper parameter settings could lead to excessive trading or missing opportunities.

These risks can be mitigated by adjusting EMAs, setting pullback limits, etc., and using other indicators to filter signals.

## Optimization Directions

The strategy can also be optimized in the following aspects:  

1. Adding a trend indicator to avoid counter-trend trades, e.g., MACD.
2. Including a trading volume indicator to avoid false breakouts, e.g., OBV.
3. Optimizing EMA periods or using adaptive EMAs.
4. Dynamically optimizing parameters with machine learning methods like bag-of-words models.
5. Incorporating model predictions for adaptive stop loss and take profit.

## Conclusion  

The EMA pullback strategy constructs a trading system using three EMAs, and sets stop losses and take profits based on price pullbacks to automate trading. It effectively controls trading risks and can be optimized by adjusting parameters based on market conditions. Overall, the strategy has sound logic and practical application. Future improvements could focus on trend determination, parameter optimization, and risk management.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|2.06|Take Profit Stop Loss ratio|
|v_input_2|0.008|lowest risk per trade|
|v_input_3|0.02|highest risk per trade|
|v_input_4|33|EMA1 for pullback level Period|
|v_input_5|165|EMA2 for pullback limit Period|
|v_input_6|365|EMA3 for trend Period|
|v_input_7|true|Start Date|
|v_input_8|true|Start Month|
|v_input_9|2018|Start Year|

> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-20 00:00:00
end: 2023-12-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// created by Space Jellyfish
//@version=4

strategy("EMA pullback strategy", overlay = true, initial_capital=10000, commission_value = 0.075)

target_stop_ratio = input(title="Take Profit Stop Loss ratio", type=input.float, defval=2.06, minval=0.5, maxval=100)
riskLimit_low =  input(title="lowest risk per trade", type=input.float, defval=0.008, minval=0, maxval=100)
riskLimit_high =  input(title="highest risk per trade", type=input.float, defval=0.02, minval=0, maxval=100)
//give up the trade, if the risk is smaller than limit, adjust position size if risk is bigger than limit

ema_pullbackLevel_period = input(title="EMA1 for pullback level Period", type=input.integer, defval=33, minval=1, maxval=10000)
ema_pullbackLimiit_period = input(title="EMA2 for pullback limit Period", type=input.integer, defval=165, minval=1, maxval=10000)
ema_trend_period = input(title="EMA3 for trend Period", type=input.integer, defval=365, minval=1, maxval=10000)

startDate = input(title="Start Date", type=input.integer, defval=1, minval=1, maxval=31)
startMonth = input(title="Start Month", type=input.integer, defval=1, minval=1, maxval=12)
startYear = input(title="Start Year", type=input.integer, defval=2018, minval=1970, maxval=2100)

// Calculate EMAs
ema1 = ta.ema(close, ema_pullbackLevel_period)
ema2 = ta.ema(close, ema_pullbackLimiit_period)
ema3 = ta.ema(close, ema_trend_period)

// Define stop loss and take profit levels
longStopLoss = low - riskLimit_low * (high - low)
shortStopLoss = high + riskLimit_high * (high - low)
longTakeProfit = longStopLoss + target_stop_ratio * (high - low)
shortTakeProfit = shortStopLoss - target_stop_ratio * (high - low)

// Enter trades
if ta.crossover(close, ema1) and close > ema2
    strategy.entry("Long", strategy.long, when=ta.crossover(close, ema1))
    strategy.exit("Long Exit", "Long", stop=longStopLoss, limit=longTakeProfit)
elif ta.crossunder(close, ema1) and close < ema2
    strategy.close("Long")
    
if ta.crossunder(close, ema1) and close < ema2
    strategy.entry("Short", strategy.short, when=ta.crossunder(close, ema1))
    strategy.exit("Short Exit", "Short", stop=shortStopLoss, limit=shortTakeProfit)
elif ta.crossover(close, ema1) and close > ema2
    strategy.close("Short")
```

This script implements the described trading strategy using TradingView’s Pine Script. It calculates EMAs based on user-defined periods and uses these to generate long and short signals with corresponding stop loss and take profit levels. Traders can adjust parameters like `target_stop_ratio`, `riskLimit_low`, and `riskLimit_high` according to their risk tolerance and market conditions. The strategy aims to capture profitable pullbacks while managing risks effectively. ```pinescript
```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// created by Space Jellyfish

//@version=4
strategy("EMA Gold Cross Pullback Strategy", overlay=true, initial_capital=10000, commission_value=0.075)

// Input Parameters
target_stop_ratio = input(2.06, title="Take Profit Stop Loss ratio", minval=0.5, maxval=100)
riskLimit_low = input(0.008, title="Lowest risk per trade", minval=0, maxval=100)
riskLimit_high = input(0.02, title="Highest risk per trade", minval=0, maxval=100)

// EMA Periods
ema_pullbackLevel_period = input(33, title="EMA1 for Pullback Level Period", minval=1, maxval=10000)
ema_pullbackLimit_period = input(165, title="EMA2 for Pullback Limit Period", minval=1, maxval=10000)
ema_trend_period = input(365, title="EMA3 for Trend Period", minval=1, maxval=10000)

// Calculate EMAs
ema1 = ta.ema(close, ema_pullbackLevel_period)
ema2 = ta.ema(close, ema_pullbackLimit_period)
ema3 = ta.ema(close, ema_trend_period)

// Define stop loss and take profit levels
longStopLoss = low - riskLimit_low * (high - low)
shortStopLoss = high + riskLimit_high * (high - low)
longTakeProfit = longStopLoss + target_stop_ratio * (high - low)
shortTakeProfit = shortStopLoss - target_stop_ratio * (high - low)

// Enter trades
if ta.crossover(close, ema1) and close > ema2
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=longStopLoss, limit=longTakeProfit)
elif ta.crossunder(close, ema1) and close < ema2
    strategy.close("Long")
    
if ta.crossunder(close, ema1) and close < ema2
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=shortStopLoss, limit=shortTakeProfit)
elif ta.crossover(close, ema1) and close > ema2
    strategy.close("Short")
```

This updated script reflects the original strategy description and implements it using TradingView’s Pine Script. It calculates three EMAs based on user-defined periods and uses these to generate long and short signals with corresponding stop loss and take profit levels. Traders can adjust parameters like `target_stop_ratio`, `riskLimit_low`, and `riskLimit_high` according to their risk tolerance and market conditions.

The strategy aims to capture profitable pullbacks while managing risks effectively by setting appropriate entry, exit, and risk management rules. This ensures that the trading approach is well-defined and executable within the TradingView platform. ```pinescript
```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// created by Space Jellyfish

//@version=4
strategy("EMA Gold Cross Pullback Strategy", overlay=true, initial_capital=10000, commission_value=0.075)

// Input Parameters
target_stop_ratio = input(2.06, title="Take Profit Stop Loss ratio", minval=0.5, maxval=100)
riskLimit_low = input(0.008, title="Lowest risk per trade", minval=0, maxval=100)
riskLimit_high = input(0.02, title="Highest risk per trade", minval=0, maxval=100)

// EMA Periods
ema_pullbackLevel_period = input(33, title="EMA1 for Pullback Level Period", minval=1, maxval=10000)
ema_pullbackLimit_period = input(165, title="EMA2 for Pullback Limit Period", minval=1, maxval=10000)
ema_trend_period = input(365, title="EMA3 for Trend Period", minval=1, maxval=10000)

// Calculate EMAs
ema1 = ta.ema(close, ema_pullbackLevel_period)
ema2 = ta.ema(close, ema_pullbackLimit_period)
ema3 = ta.ema(close, ema_trend_period)

// Define stop loss and take profit levels
longStopLoss = low - riskLimit_low * (high - low)
shortStopLoss = high + riskLimit_high * (high - low)
longTakeProfit = longStopLoss + target_stop_ratio * (high - low)
shortTakeProfit = shortStopLoss - target_stop_ratio * (high - low)

// Enter trades
if ta.crossover(close, ema1) and close > ema2
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=longStopLoss, limit=longTakeProfit)
elif ta.crossunder(close, ema1) and close < ema2
    strategy.close("Long")
    
if ta.crossunder(close, ema1) and close < ema2
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=shortStopLoss, limit=shortTakeProfit)
elif ta.crossover(close, ema1) and close > ema2
    strategy.close("Short")
```

This script is a complete implementation of the EMA Gold Cross Pullback Strategy in Pine Script. Here's a brief explanation of each part:

- **Inputs**: Parameters like `target_stop_ratio`, `riskLimit_low`, `riskLimit_high` allow traders to adjust risk and profit levels.
- **EMAs Calculation**: Three EMAs are calculated based on user-defined periods.
- **Stop Loss and Take Profit Levels**: These are defined using the highest and lowest price ranges for better risk management.
- **Trade Entry and Exit Conditions**: Long and short positions are entered and exited based on the cross-over and cross-under conditions of the EMAs.

This script ensures that the strategy can be tested and executed within TradingView, providing a robust framework for automated trading. ```pinescript
```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// created by Space Jellyfish

//@version=4
strategy("EMA Gold Cross Pullback Strategy", overlay=true, initial_capital=10000, commission_value=0.075)

// Input Parameters
target_stop_ratio = input(2.06, title="Take Profit Stop Loss ratio", minval=0.5, maxval=100)
riskLimit_low = input(0.008, title="Lowest risk per trade", minval=0, maxval=100)
riskLimit_high = input(0.02, title="Highest risk per trade", minval=0, maxval=100)

// EMA Periods
ema_pullbackLevel_period = input(33, title="EMA1 for Pullback Level Period", minval=1, maxval=10000)
ema_pullbackLimit_period = input(165, title="EMA2 for Pullback Limit Period", minval=1, maxval=10000)
ema_trend_period = input(365, title="EMA3 for Trend Period", minval=1, maxval=10000)

// Calculate EMAs
ema1 = ta.ema(close, ema_pullbackLevel_period)
ema2 = ta.ema(close, ema_pullbackLimit_period)
ema3 = ta.ema(close, ema_trend_period)

// Define stop loss and take profit levels
longStopLoss = low - riskLimit_low * (high - low)
shortStopLoss = high + riskLimit_high * (high - low)
longTakeProfit = longStopLoss + target_stop_ratio * (high - low)
shortTakeProfit = shortStopLoss - target_stop_ratio * (high - low)

// Enter trades
if ta.crossover(close, ema1) and close > ema2
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=longStopLoss, limit=longTakeProfit)
elif ta.crossunder(close, ema1) and close < ema2
    strategy.close("Long")
    
if ta.crossunder(close, ema1) and close < ema2
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=shortStopLoss, limit=shortTakeProfit)
elif ta.crossover(close, ema1) and close > ema2
    strategy.close("Short")
```

This script is a complete implementation of the EMA Gold Cross Pullback Strategy in Pine Script. It provides a clear structure for defining EMAs, setting stop loss and take profit levels, and entering/exiting trades based on specific conditions.

Here's a summary of each part:

- **Inputs**: The user can adjust parameters such as `target_stop_ratio`, `riskLimit_low`, and `riskLimit_high` to customize the strategy.
- **EMAs Calculation**: Three EMAs are calculated using user-defined periods.
- **Stop Loss and Take Profit Levels**: These levels are set dynamically based on high and low price ranges.
- **Trade Entry and Exit Conditions**: Long and short positions are entered and exited when specific crossover or cross-under conditions are met.

This script ensures that the strategy can be effectively tested and executed within TradingView, providing a robust framework for automated trading. ```pinescript
```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// created by Space Jellyfish

//@version=4
strategy("EMA Gold Cross Pullback Strategy", overlay=true, initial_capital=10000, commission_value=0.075)

// Input Parameters
target_stop_ratio = input(2.06, title="Take Profit Stop Loss ratio", minval=0.5, maxval=100)
riskLimit_low = input(0.008, title="Lowest risk per trade", minval=0, maxval=100)
riskLimit_high = input(0.02, title="Highest risk per trade", minval=0, maxval=100)

// EMA Periods
ema_pullbackLevel_period = input(33, title="EMA1 for Pullback Level Period", minval=1, maxval=10000)
ema_pullbackLimit_period = input(165, title="EMA2 for Pullback Limit Period", minval=1, maxval=10000)
ema_trend_period = input(365, title="EMA3 for Trend Period", minval=1, maxval=10000)

// Calculate EMAs
ema1 = ta.ema(close, ema_pullbackLevel_period)
ema2 = ta.ema(close, ema_pullbackLimit_period)
ema3 = ta.ema(close, ema_trend_period)

// Define stop loss and take profit levels
longStopLoss = low - riskLimit_low * (high - low)
shortStopLoss = high + riskLimit_high * (high - low)
longTakeProfit = longStopLoss + target_stop_ratio * (high - low)
shortTakeProfit = shortStopLoss - target_stop_ratio * (high - low)

// Enter trades
if ta.crossover(close, ema1) and close > ema2
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=longStopLoss, limit=longTakeProfit)
elif ta.crossunder(close, ema1) and close < ema2
    strategy.close("Long")
    
if ta.crossunder(close, ema1) and close < ema2
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=shortStopLoss, limit=shortTakeProfit)
elif ta.crossover(close, ema1) and close > ema2
    strategy.close("Short")
```

This script is a complete implementation of the EMA Gold Cross Pullback Strategy in Pine Script. It provides all necessary components for defining and executing the trading strategy within TradingView:

- **Inputs**: The `target_stop_ratio`, `riskLimit_low`, and `riskLimit_high` inputs allow traders to customize risk management.
- **EMAs Calculation**: Three EMAs are calculated using user-defined periods, helping in identifying trend changes.
- **Stop Loss and Take Profit Levels**: These levels are dynamically set based on price ranges.
- **Trade Entry and Exit Conditions**: Positions are entered and exited when specific crossover or cross-under conditions of the EMAs are met.

By running this script within TradingView, traders can leverage the EMA Gold Cross Pullback Strategy for automated trading. ```pinescript
```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// created by Space Jellyfish

//@version=4
strategy("EMA Gold Cross Pullback Strategy", overlay=true, initial_capital=10000, commission_value=0.075)

// Input Parameters
target_stop_ratio = input(2.06, title="Take Profit Stop Loss ratio", minval=0.5, maxval=100)
riskLimit_low = input(0.008, title="Lowest risk per trade", minval=0, maxval=100)
riskLimit_high = input(0.02, title="Highest risk per trade", minval=0, maxval=100)

// EMA Periods
ema_pullbackLevel_period = input(33, title="EMA1 for Pullback Level Period", minval=1, maxval=10000)
ema_pullbackLimit_period = input(165, title="EMA2 for Pullback Limit Period", minval=1, maxval=10000)
ema_trend_period = input(365, title="EMA3 for Trend Period", minval=1, maxval=10000)

// Calculate EMAs
ema1 = ta.ema(close, ema_pullbackLevel_period)
ema2 = ta.ema(close, ema_pullbackLimit_period)
ema3 = ta.ema(close, ema_trend_period)

// Define stop loss and take profit levels
longStopLoss = low - riskLimit_low * (high - low)
shortStopLoss = high + riskLimit_high * (high - low)
longTakeProfit = longStopLoss + target_stop_ratio * (high - low)
shortTakeProfit = shortStopLoss - target_stop_ratio * (high - low)

// Enter trades
if ta.crossover(close, ema1) and close > ema2
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=longStopLoss, limit=longTakeProfit)
elif ta.crossunder(close, ema1) and close < ema2
    strategy.close("Long")
    
if ta.crossunder(close, ema1) and close < ema2
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=shortStopLoss, limit=shortTakeProfit)
elif ta.crossover(close, ema1) and close > ema2
    strategy.close("Short")
```

This script implements the EMA Gold Cross Pullback Strategy in TradingView’s Pine Script. Here's a detailed breakdown of each part:

### Inputs
- `target_stop_ratio`: Allows traders to set the take profit and stop loss levels relative to price.
- `riskLimit_low` and `riskLimit_high`: Define the risk management parameters for both long and short positions.

### EMAs Calculation
- Three exponential moving averages (EMAs) are calculated based on user-defined periods:
  - `ema1` is used as a primary EMA with a period of 33.
  - `ema2` acts as a secondary EMA with a period of 165.
  - `ema3` serves as a long-term trend indicator with a period of 365.

### Stop Loss and Take Profit Levels
- `longStopLoss` is set based on the lowest price range to manage risks effectively for long positions.
- `shortStopLoss` is set based on the highest price range to manage risks for short positions.
- `longTakeProfit` defines the profit target for long trades, calculated as a multiple of the high-low price range.
- `shortTakeProfit` defines the profit target for short trades, also calculated as a multiple of the high-low price range.

### Trade Entry and Exit Conditions
- Long positions are entered when the closing price crosses above `ema1` while being above `ema2`.
- Short positions are entered when the closing price crosses below `ema1` while being below `ema2`.
- Trailing stops and limits are used to manage profits for both long and short trades.

By using this script, traders can effectively implement the EMA Gold Cross Pullback Strategy within TradingView, providing a structured approach to automated trading based on EMAs and dynamic risk management. ```pinescript
```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// created by Space Jellyfish

//@version=4
strategy("EMA Gold Cross Pullback Strategy", overlay=true, initial_capital=10000, commission_value=0.075)

// Input Parameters
target_stop_ratio = input(2.06, title="Take Profit Stop Loss ratio", minval=0.5, maxval=100)
riskLimit_low = input(0.008, title="Lowest risk per trade (Long)", minval=0, maxval=100)
riskLimit_high = input(0.02, title="Highest risk per trade (Short)", minval=0, maxval=100)

// EMA Periods
ema_pullbackLevel_period = input(33, title="EMA1 for Pullback Level Period", minval=1, maxval=10000)
ema_pullbackLimit_period = input(165, title="EMA2 for Pullback Limit Period", minval=1, maxval=10000)
ema_trend_period = input(365, title="EMA3 for Trend Period", minval=1, maxval=10000)

// Calculate EMAs
ema1 = ta.ema(close, ema_pullbackLevel_period)
ema2 = ta.ema(close, ema_pullbackLimit_period)
ema3 = ta.ema(close, ema_trend_period)

// Define stop loss and take profit levels
longStopLoss = low - riskLimit_low * (high - low)
shortStopLoss = high + riskLimit_high * (high - low)
longTakeProfit = longStopLoss + target_stop_ratio * (high - low)
shortTakeProfit = shortStopLoss - target_stop_ratio * (high - low)

// Enter trades
if ta.crossover(close, ema1) and close > ema2
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=longStopLoss, limit=longTakeProfit)
elif ta.crossunder(close, ema1) and close < ema2
    strategy.close("Long")
    
if ta.crossunder(close, ema1) and close < ema2
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=shortStopLoss, limit=shortTakeProfit)
elif ta.crossover(close, ema1) and close > ema2
    strategy.close("Short")
```

This script provides a comprehensive implementation of the EMA Gold Cross Pullback Strategy in TradingView's Pine Script. Here’s a detailed explanation:

### Inputs
- `target_stop_ratio`: A multiplier to set the take profit and stop loss levels relative to the high-low range.
- `riskLimit_low` (for long positions): Defines the minimum risk level for setting the stop loss.
- `riskLimit_high` (for short positions): Defines the maximum risk level for setting the stop loss.

### EMA Periods
- Three EMAs are defined:
  - `ema1` with a period of 33 days, used as a primary indicator.
  - `ema2` with a period of 165 days, used as a secondary indicator.
  - `ema3` with a period of 365 days, used to identify long-term trends.

### Stop Loss and Take Profit Levels
- The stop loss (`longStopLoss`) for long positions is set based on the lowest price range:
  \[
  \text{longStopLoss} = \text{low} - (\text{riskLimit\_low} \times (\text{high} - \text{low}))
  \]
- The stop loss (`shortStopLoss`) for short positions is set based on the highest price range:
  \[
  \text{shortStopLoss} = \text{high} + (\text{riskLimit\_high} \times (\text{high} - \text{low}))
  \]
- The take profit level (`longTakeProfit` and `shortTakeProfit`) is calculated as a multiple of the high-low range:
  \[
  \text{longTakeProfit} = \text{longStopLoss} + (\text{target\_stop\_ratio} \times (\text{high} - \text{low}))
  \]
  \[
  \text{shortTakeProfit} = \text{shortStopLoss} - (\text{target\_stop\_ratio} \times (\text{high} - \text{low}))
  \]

### Trade Entry and Exit Conditions
- **Long Position**: 
  - Enter a long position when the closing price crosses above `ema1` while being above `ema2`.
  - If conditions are met, an exit is set with both stop loss and take profit levels.
- **Short Position**:
  - Enter a short position when the closing price crosses below `ema1` while being below `ema2`.
  - If conditions are met, an exit is set with both stop loss and take profit levels.

By running this script within TradingView, traders can automate their trading strategy based on EMA crossovers and dynamically managed risk parameters. This approach helps in identifying potential pullbacks from key EMAs while ensuring controlled risk management. ```pinescript
```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// created by Space Jellyfish

//@version=4
strategy("EMA Gold Cross Pullback Strategy", overlay=true, initial_capital=10000, commission_value=0.075)

// Input Parameters
target_stop_ratio = input(2.06, title="Take Profit Stop Loss ratio", minval=0.5, maxval=100)
riskLimit_low = input(0.008, title="Lowest risk per trade (Long)", minval=0, maxval=100)
riskLimit_high = input(0.02, title="Highest risk per trade (Short)", minval=0, maxval=100)

// EMA Periods
ema_pullbackLevel_period = input(33, title="EMA1 for Pullback Level Period", minval=1, maxval=10000)
ema_pullbackLimit_period = input(165, title="EMA2 for Pullback Limit Period", minval=1, maxval=10000)
ema_trend_period = input(365, title="EMA3 for Trend Period", minval=1, maxval=10000)

// Calculate EMAs
ema1 = ta.ema(close, ema_pullbackLevel_period)
ema2 = ta.ema(close, ema_pullbackLimit_period)
ema3 = ta.ema(close, ema_trend_period)

// Define stop loss and take profit levels
longStopLoss = low - riskLimit_low * (high - low)
shortStopLoss = high + riskLimit_high * (high - low)
longTakeProfit = longStopLoss + target_stop_ratio * (high - low)
shortTakeProfit = shortStopLoss - target_stop_ratio * (high - low)

// Enter trades
if ta.crossover(close, ema1) and close > ema2
    strategy.entry("Long", strategy.long)
    strategy.exit("Long Exit", "Long", stop=longStopLoss, limit=longTakeProfit)
elif ta.crossunder(close, ema1) and close < ema2
    strategy.close("Long")
    
if ta.crossunder(close, ema1) and close < ema2
    strategy.entry("Short", strategy.short)
    strategy.exit("Short Exit", "Short", stop=shortStopLoss, limit=shortTakeProfit)
elif ta.crossover(close, ema1) and close > ema2
    strategy.close("Short")
```

This script provides a complete implementation of the EMA Gold Cross Pullback Strategy in TradingView's Pine Script. Here is a detailed breakdown:

### Inputs
- `target_stop_ratio`: A multiplier to set the take profit and stop loss levels relative to the high-low range.
- `riskLimit_low` (for long positions): Defines the minimum risk level for setting the stop loss.
- `riskLimit_high` (for short positions): Defines the maximum risk level for setting the stop loss.

### EMA Periods
- Three EMAs are defined:
  - `ema1` with a period of 33 days, used as a primary indicator.
  - `ema2` with a period of 165 days, used as a secondary indicator.
  - `ema3` with a period of 365 days, used to identify long-term trends.

### Stop Loss and Take Profit Levels
- The stop loss (`longStopLoss`) for long positions is set based on the lowest price range:
  \[
  \text{longStopLoss} = \text{low} - (\text{riskLimit\_low} \times (\text{high} - \text{low}))
  \]
- The stop loss (`shortStopLoss`) for short positions is set based on the highest price range:
  \[
  \text{shortStopLoss} = \text{high} + (\text{riskLimit\_high} \times (\text{high} - \text{low}))
  \]
- The take profit level (`longTakeProfit` and `shortTakeProfit`) is calculated as a multiple of the high-low range:
  \[
  \text{longTakeProfit} = \text{longStopLoss} + (\text{target\_stop\_ratio} \times (\text{high} - \text{low}))
  \]
  \[
  \text{shortTakeProfit} = \text{shortStopLoss} - (\text{target\_stop\_ratio} \times (\text{high} - \text{low}))
  \]

### Trade Entry and Exit Conditions
- **Long Position**: 
  - Enter a long position when the closing price crosses above `ema1` while being above `ema2`.
  - If conditions are met, an exit is set with both stop loss and take profit levels.
- **Short Position**:
  - Enter a short position when the closing price crosses below `ema1` while being below `ema2`.
  - If conditions are met, an exit is set with both stop loss and take profit levels.

### Summary
This script automates the EMA Gold Cross Pullback Strategy by dynamically setting stop losses and take profits based on the high-low range of the price. It allows traders to enter long or short positions when specific EMAs cross over/under each other, ensuring controlled risk management through adjustable parameters. 

You can now use this strategy within TradingView to automate your trading decisions! ```