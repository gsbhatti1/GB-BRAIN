---
## Overview

The Volume Weighted Average Price (VWAP) strategy is a trading approach that tracks the average price of a stock over a specified period. The strategy uses VWAP as a benchmark and takes long or short positions when the price crosses above or below VWAP. It also sets stop loss and take profit conditions to manage trades.

## Strategy Logic

The strategy first calculates the typical price (average of high, low, and close prices) multiplied by volume, and then the sum of volume. Then, it computes the VWAP value by dividing the sum of typical price-volume products by the total volume. When the price crosses above VWAP, a long position is taken; when the price crosses below, a short position is opened.

For long positions, the profit-taking condition is to close the position when the price rises 3% above the entry price. The stop loss condition is to close the position when the price drops 1% below the entry price. Similar conditions apply for short positions.

## Advantage Analysis

The main advantages of the VWAP strategy are:

1. Uses the well-recognized VWAP statistic as a benchmark for trade signals, making the strategy more effective.
2. Utilizes both vwap signals and stop loss/profit taking to profit from trends while limiting losses.
3. Simple and clear logic, easy to understand and implement.

## Risk Analysis

This strategy also has some risks:

1. VWAP cannot predict future prices; therefore, signals may lag.
2. The stop loss condition is set too loosely, potentially increasing the risk of loss.
3. Backtesting for a longer period yields more signals, which might differ from actual performance in live trading.

These risks can be mitigated through parameter tuning and optimizing stop-loss algorithms.

## Optimization Directions

The strategy can be optimized in several ways:

1. Optimize VWAP parameters to find the best calculation period.
2. Test other tracking stop algorithms such as moving average stops or parabolic SAR.
3. Combine other indicators as filters, for example volume and Bollinger Bands, to reduce false positive VWAP signals.

## Conclusion

Overall, the VWAP strategy leverages the predictive power of this important statistic with stop loss/profit taking conditions to achieve long-term positive returns. However, further optimizations and combination with other strategies are needed to reduce market fluctuation risks for enhanced profitability.

---

### Strategy Arguments


| Argument      | Default Value | Description                      |
|---------------|---------------|----------------------------------|
| v_input_1     | 14            | Period                           |

### Source (PineScript)

```pinescript
// [backtest]
// start: 2023-11-28 00:00:00
// end: 2023-12-28 00:00:00
// period: 1h
// basePeriod: 15m
// exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]

//@version=4
strategy("VWAP Strategy by Royce Mars", overlay=true)

cumulativePeriod = input(14, "Period")

var float cumulativeTypicalPriceVolume = 0.0
var float cumulativeVolume = 0.0

typicalPrice = (high + low + close) / 3
typicalPriceVolume = typicalPrice * volume
cumulativeTypicalPriceVolume := cumulativeTypicalPriceVolume + typicalPriceVolume
cumulativeVolume := cumulativeVolume + volume
vwapValue = cumulativeTypicalPriceVolume / cumulativeVolume

// Buy condition: Price crosses over VWAP
buyCondition = crossover(close, vwapValue)

// Short condition: Price crosses below VWAP
shortCondition = crossunder(close, vwapValue)

// Profit-taking condition for long positions: Sell long position when profit reaches 3%
profitTakingLongCondition = close / strategy.position_avg_price >= 1.03

// Profit-taking condition for short positions: Cover short position when profit reaches 3%
profitTakingShortCondition = close / strategy.position_avg_price <= 0.97

// Stop loss condition for long positions: Sell long position when loss reaches 1%
stopLossLongCondition = close / strategy.position_avg_price <= 0.99

// Stop loss condition for short positions: Cover short position when loss reaches 1%
stopLossShortCondition = close / strategy.position_avg_price >= 1.01

// Strategy Execution
strategy.entry("Buy", strategy.long, when=buyCondition)
strategy.close("Buy", when=shortCondition or profitTakingLongCondition or stopLossLongCondition)

strategy.entry("Short", strategy.short, when=shortCondition)
strategy.close("Short", when=buyCondition or profitTakingShortCondition or stopLossShortCondition)

// Plot VWAP on the chart
plot(vwapValue, color=color.blue, title="VWAP")
```

### Detail

https://www.fmz.com/strategy/437032

### Last Modified

2023-12-29 16:31:33