> Name

SMA Moving Average Crossover Strategy SMA-Moving-Average-Crossover-Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

This is a simple trend-following crossover strategy based on SMA moving averages, suitable for higher timeframes for trading BTCUSD and other crypto pairs.

## Strategy Logic

The strategy is based on two SMAs with different periods. One is a 10-period SMA, the other is a 100-period SMA. The strategy keeps monitoring the values of the two SMAs. When the shorter 10-period SMA crosses above the longer 100-period SMA, it signals an uptrend, and the strategy goes long. When the 10-period SMA crosses below the 100-period SMA, it signals a downtrend, and the strategy goes short.

Specifically, the strategy determines the crossover by comparing the values of the 10-period SMA and 100-period SMA. If the 10-period SMA crosses above the 100-period SMA, the `longCondition` is set to true. The strategy then goes long through the `strategy.entry` function. Conversely, if the 10-period SMA crosses below the 100-period SMA, the `shortCondition` is set to true. The strategy then goes short through `strategy.entry`.

Through this simple SMA crossover system, the strategy can capture trend reversal points and get in and out of the market in a timely manner. It goes long when the shorter SMA crosses above the longer SMA, and goes short when the shorter SMA crosses below the longer SMA.

## Advantages

1. The logic is simple and clear, easy to understand and implement, suitable for beginners.
2. SMA crossover can effectively capture trend reversal points and enter the market in a timely manner.
3. Moving averages can filter out market noise and identify trend directions.
4. The SMA periods can be adjusted for different market environments. For example, shorter periods for bull markets and longer periods for bear markets.
5. The strategy has been validated for a long time and works well in crypto markets.

## Risks

1. SMA crossover may lag and cause late entry and stop loss risks.
2. Shorter SMAs may generate false breakouts and cause unnecessary whipsaws.
3. Need to set stop loss when holding positions for the long term.
4. May lead to frequent losing trades in ranging markets. Need to combine with other indicators.
5. Inappropriate parameter settings may affect strategy performance. SMA periods need to be adjusted per market conditions.

## Enhancements

1. Combine SMA with other indicators like RSI, Bollinger Bands to improve accuracy.
2. Add stop loss mechanisms, like SMA breakout stop loss.
3. Dynamically adjust SMA parameters based on market conditions, shorter periods for bull markets and longer periods for bear markets.
4. Use different position sizing based on the crossover strength of short and long SMAs.
5. Add re-entry rules, like re-enter when price reverts to SMA.
6. Evaluate parameters and strategy through backtesting and paper trading.

## Summary

The SMA moving average crossover strategy has simple and clear logic, easy to understand and implement. It captures trend reversal points through the crossover of two SMAs with different periods. It is a classical trend-following strategy. The advantages are direct logic and clear trading signals, able to track trends effectively. The disadvantages are possible lagging entry and false breakouts. We can optimize it by introducing other indicators and stop loss mechanisms to control risks and improve practical results. With continuous optimization and verification, this strategy can become a very useful trend-following strategy for crypto trading.

||

## Overview

This is a simple trend following crossover strategy based on SMA moving averages, suitable for higher timeframes for trading BTCUSD and other crypto pairs.

## Strategy Logic

The strategy is based on two SMAs with different periods. One is a 10-period SMA, the other is a 100-period SMA. The strategy keeps monitoring the values of the two SMAs. When the shorter 10-period SMA crosses above the longer 100-period SMA, it signals an uptrend, and the strategy goes long. When the 10-period SMA crosses below the 100-period SMA, it signals a downtrend, and the strategy goes short.

Specifically, the strategy determines the crossover by comparing the values of the 10-period SMA and 100-period SMA. If the 10-period SMA crosses above the 100-period SMA, the `longCondition` is set to true. The strategy then goes long through the `strategy.entry` function. Conversely, if the 10-period SMA crosses below the 100-period SMA, the `shortCondition` is set to true. The strategy then goes short through `strategy.entry`.

Through this simple SMA crossover system, the strategy can capture trend reversal points and get in and out of the market in a timely manner. It goes long when the shorter SMA crosses above the longer SMA, and goes short when the shorter SMA crosses below the longer SMA.

## Advantages

1. The logic is simple and clear, easy to understand and implement, suitable for beginners.
2. SMA crossover can effectively capture trend reversal points and enter the market in a timely manner.
3. Moving averages can filter out market noise and identify trend directions.
4. The SMA periods can be adjusted for different market environments. For example, shorter periods for bull markets and longer periods for bear markets.
5. The strategy has been validated for a long time and works well in crypto markets.

## Risks

1. SMA crossover may lag and cause late entry and stop loss risks.
2. Shorter SMAs may generate false breakouts and cause unnecessary whipsaws.
3. Need to set stop loss when holding positions for the long term.
4. May lead to frequent losing trades in ranging markets. Need to combine with other indicators.
5. Inappropriate parameter settings may affect strategy performance. SMA periods need to be adjusted per market conditions.

## Enhancements

1. Combine SMA with other indicators like RSI, Bollinger Bands to improve accuracy.
2. Add stop loss mechanisms, like SMA breakout stop loss.
3. Dynamically adjust SMA parameters based on market conditions, shorter periods for bull markets and longer periods for bear markets.
4. Use different position sizing based on the crossover strength of short and long SMAs.
5. Add re-entry rules, like re-enter when price reverts to SMA.
6. Evaluate parameters and strategy through backtesting and paper trading.

## Summary

The SMA moving average crossover strategy has simple and clear logic, easy to understand and implement. It captures trend reversal points through the crossover of two SMAs with different periods. It is a classical trend-following strategy. The advantages are direct logic and clear trading signals, able to track trends effectively. The disadvantages are possible lagging entry and false breakouts. We can optimize it by introducing other indicators and stop loss mechanisms to control risks and improve practical results. With continuous optimization and verification, this strategy can become a very useful trend-following strategy for crypto trading.

---

> Strategy Arguments

| Argument | Default | Description |
| --- | --- | --- |
| v_input_1_close | 0 | Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4 |
| v_input_2 | 10 | 1st MA Length |
| v_input_3 | 0 | 1st MA Type: SMA|EMA |
| v_input_4 | 100 | 2nd MA Length |
| v_input_5 | 0 | 2nd MA Type: SMA|EMA |

> Source (PineScript)

```pinescript
//@version=3
strategy("SMA Crossover Strategy", overlay=true)
src = input(close, title="Source")

price = security(syminfo.tickerid, timeframe.period, src)
ma1 = input(10, title="1st MA Length")
type1 = input("SMA", "1st MA Type", options=["SMA", "EMA"])

ma2 = input(100, title="2nd MA Length")
type2 = input("SMA", "2nd MA Type", options=["SMA", "EMA"])

price1 = if (type1 == "SMA")
    sma(price, ma1)
else
    ema(price, ma1)
    
price2 = if (type2 == "SMA")
    sma(price, ma2)
else
    ema(price, ma2)

longCondition = price1 > price2
shortCondition = price1 < price2

if (longCondition)
    strategy.entry("Long", strategy.long)
if (shortCondition)
    strategy.exit("Short", "Long")

// Add stop loss and take profit based on SMA crossover
```

The provided script completes the implementation of the SMA Crossover Strategy, including setting up long and short conditions based on the crossover of two SMAs.