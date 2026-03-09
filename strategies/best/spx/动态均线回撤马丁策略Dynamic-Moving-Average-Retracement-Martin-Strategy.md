> Name

Dynamic-Moving-Average-Retracement-Martin-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f353fcad2ccf4c6578.png)
[trans]

### Overview

The Dynamic Moving Average Retracement Martin strategy is a frequent trading strategy that combines moving average crossovers and bottom divergence signals to generate entry and exit signals. The strategy uses the crossover and divergence of 3-day and 8-day simple moving averages to capture short-term trends, and employs stop losses and take profits to control risks. This strategy allows choosing trading directions according to different market conditions.

### Strategy Principle

The strategy utilizes 3-day and 8-day simple moving averages and their cross signals. A long signal is generated when the 3-day MA crosses above the 8-day MA; a short signal is generated when the 3-day MA crosses below the 8-day MA. Long signals will trigger long entry, while short signals will trigger short entry.

If there is no position, the strategy will determine entry based on cross signals. After entry, the stop loss price and take profit price will be calculated based on the latest close price, stop loss percentage, and take profit percentage. For example, when holding a long position, the stop loss price is the latest close price minus the stop loss percentage multiplied by the 8-day MA; the take profit price is the latest close price plus the take profit percentage multiplied by the 8-day MA.

If there is an existing long position and the price triggers the stop loss or take profit, if a bottom divergence signal of the 8-day MA occurs, the position will be closed. At this time, the stop loss price and take profit price will be reset to 0. The logic for handling short positions is similar.

The strategy also plots entry and exit points on the chart. For example, a long entry is plotted as an upward triangle, and a long exit as a downward triangle. This helps to visually determine entries and exits.

### Advantage Analysis

The advantages of this strategy include:

1. Captures short-term trends using moving average crossover signals, allowing frequent trading.
2. The stop loss mechanism can control single loss.
3. Take profit setting can lock in partial profits.
4. Trading directions can be selected according to different market conditions.
5. Visualizes entry and exit points on the chart for clarity.

### Risk Analysis

The main risks of this strategy include:

1. Short-term MA strategies are prone to whipsawing.
2. Possibility of lagging signals from moving averages.
3. Consecutive losses may lead to aggravated losses.
4. Incorrectly set stop loss percentage may be too loose or too tight.

Risks can be reduced by reasonably widening the stop loss percentage, optimizing Moving Average (MA) parameters, introducing additional filter conditions, etc. Additionally, correctly assessing personal tolerance and avoiding overtrading is important.

### Optimization Directions

This strategy can be optimized in the following ways:

1. Test more MA combinations to find optimal parameters.
2. Add other indicators such as RSI, KD, etc., to improve signal quality.
3. Adjust stop loss percentage according to different products and timeframes.
4. Implement position sizing control such as fixed quantity or fixed capital.
5. Add entry order rules.
6. Optimize and evaluate stop loss or take profit levels.

### Summary

The Dynamic Moving Average Retracement Martin strategy is a short-term trading strategy that captures short-term trends formed by moving average crossovers and manages risks with appropriate stops and take profits. The frequent trading nature provides both profit opportunities and risks. By optimizing parameters, filtering signals, and controlling risks, this strategy can be further improved for greater reliability.

||

### Overview

The Dynamic Moving Average Retracement Martin strategy is a frequent trading strategy that combines moving average crossovers and bottom divergence signals to generate entry and exit signals. The strategy uses the crossover and divergence of 3-day and 8-day simple moving averages to capture short-term trends, and employs stop losses and take profits to control risks. This strategy allows choosing trading directions according to different market conditions.

### Strategy Logic

The strategy utilizes 3-day and 8-day simple moving averages and their cross signals. A long signal is generated when the 3-day MA crosses above the 8-day MA; a short signal is generated when the 3-day MA crosses below the 8-day MA. Long signals will trigger long entry, while short signals will trigger short entry.

If there is no position, the strategy will determine entry based on cross signals. After entry, the stop loss price and take profit price will be calculated based on the latest close price, stop loss percentage, and take profit percentage. For example, when holding a long position, the stop loss price is the latest close price minus the stop loss percentage multiplied by the 8-day MA; the take profit price is the latest close price plus the take profit percentage multiplied by the 8-day MA.

If there is an existing long position and the price triggers the stop loss or take profit, if a bottom divergence signal of the 8-day MA occurs, the position will be closed. At this time, the stop loss price and take profit price will be reset to 0. The logic for handling short positions is similar.

The strategy also plots entry and exit points on the chart. For example, a long entry is plotted as an upward triangle, and a long exit as a downward triangle. This helps to visually determine entries and exits.

### Advantage Analysis

1. Captures short-term trends using moving average crossover signals, allowing frequent trading.
2. The stop loss mechanism can control single loss.
3. Take profit setting can lock in partial profits.
4. Trading directions can be selected according to different market conditions.
5. Visualizes entry and exit points on the chart for clarity.

### Risk Analysis

The main risks of this strategy include:

1. Short-term MA strategies are prone to whipsawing.
2. Possibility of lagging signals from moving averages.
3. Consecutive losses may lead to aggravated losses.
4. Incorrectly set stop loss percentage may be too loose or too tight.

Risks can be reduced by reasonably widening the stop loss percentage, optimizing Moving Average (MA) parameters, introducing additional filter conditions, etc. Additionally, correctly assessing personal tolerance and avoiding overtrading is important.

### Optimization Directions

This strategy can be optimized in the following ways:

1. Test more MA combinations to find optimal parameters.
2. Add other indicators such as RSI, KD, etc., to improve signal quality.
3. Adjust stop loss percentage according to different products and timeframes.
4. Implement position sizing control such as fixed quantity or fixed capital.
5. Add entry order rules.
6. Optimize and evaluate stop loss or take profit levels.

### Summary

The Dynamic Moving Average Retracement Martin strategy is a short-term trading strategy that captures short-term trends formed by moving average crossovers and manages risks with appropriate stops and take profits. The frequent trading nature provides both profit opportunities and risks. By optimizing parameters, filtering signals, and controlling risks, this strategy can be further improved for greater reliability.

||

> Strategy Arguments


| Argument | Default | Description |
| --- | --- | --- |
| v_input_1 | 1.03 | Take Profit |
| v_input_2 | 0.95 | Stop Loss |
| v_input_string_1 | 0 | Trading Mode: Long | Short | BiDir |


> Source (PineScript)

```pinescript
/*backtest
start: 2022-11-17 00:00:00
end: 2023-11-23 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

    // ____  __    ___   ________ ___________  ___________ __  ____ ___ 
   // / __ )/ /   /   | / ____/ //_/ ____/   |/_  __<  / // / / __ |__ \
  // / __  / /   / /| |/ /   / ,< / /   / /| | / /  / / // /_/ / / __/ /
 // / /_/ / /___/ ___ / /___/ /| / /___/ ___ |/ /  / /__  __/ /_/ / __/ 
// /_____/_____/_/  |_\____/_/ |_\____/_/  |_/_/  /_/  /_/  \____/____/                                              

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © blackcat1402
//@version=5
strategy('[blackcat] L1 MartinGale Scalping Strategy', overlay=true, pyramiding = 5)

// Define input variables
```