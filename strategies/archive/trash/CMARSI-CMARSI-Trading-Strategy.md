> Name

CMARSI Trading Strategy CMARSI-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

The CMARSI trading strategy is a trend-following approach that combines the RSI indicator and moving averages. It uses an improved RSI (Connors RSI) to identify trends, with moving averages serving as signals for entry and exit points. This strategy is suitable for medium-to-long term trading, aiming to profit by following the prevailing trend.

## Principle Analysis

The CMARSI strategy employs a modified RSI indicator called Connors RSI, which integrates three indicators: classical RSI, RSI Up/Down lines, and ROC percentile. The calculation formula is:

Connors RSI = (RSI + RSI Up/Down + ROC Percentile) / 3

Where RSI uses a 3-day period, RSI Up/Down uses a 2-day period, and ROC Percentile uses a 100-day period.

The advantage of Connors RSI is that it combines multiple indicators to more accurately identify trend changes. A crossing above 40 is interpreted as a long signal, while a crossing below 70 is seen as a short signal.

On top of this, the CMARSI strategy introduces a moving average factor. It calculates a 2-day moving average and uses golden crosses and death crosses between Connors RSI and the MA as trading signals. The specific rules are:

1. Enter long when Connors RSI crosses above 40 and has a golden cross of the 2-day MA.
2. Exit when Connors RSI crosses below 70 and has a death cross of the 2-day MA.

Using moving averages helps filter out some false signals from Connors RSI, thereby improving the stability of the strategy.

## Advantage Analysis

The biggest advantage of the CMARSI strategy is the combination of multiple indicators to identify trends, avoiding the limitations of single RSI indicators. Specifically, this strategy has the following advantages:

1. Connors RSI is more stable than classical RSI for identifying trend turning points.
2. The introduction of moving averages effectively filters out some noise and prevents chasing highs and selling lows.
3. The combination of multiple indicators can improve win rate by following trends.
4. The trading rules are simple and easy to implement.
5. As a trend-following strategy, it can fully capture profits from medium-to-long term trends.

## Risk Analysis

The main risks of the CMARSI strategy come from incorrect trend judgment and stop loss placement. Specific risks include:

1. Connors RSI gives incorrect signals, causing unnecessary entries. Parameters can be adjusted or additional indicators added for confirmation.
2. Stop loss placement is unreasonable, which may cause premature stop out or overly large stop losses. Stop loss should be optimized for different products and market environments.
3. Moving average filters may not work well in ranging markets. Strategy parameters should be optimized accordingly.
4. Prolonged use may lead to overfitting. Regular backtesting and parameter tuning based on market conditions are necessary.

## Optimization Directions

The CMARSI strategy can be optimized in the following areas:

1. Optimize Connors RSI parameters for different periods and products.
2. Try different types of moving averages to further improve filtering effects.
3. Add other indicators like MACD, Bollinger Bands for trade confirmation.
4. Optimize stop loss strategies, such as trailing stop losses or staggered stop losses.
5. Select products that fit the strategy better through screening.
6. Use Walk Forward Analysis to regularly optimize parameters and prevent overfitting.

## Conclusion

The CMARSI strategy combines Connors RSI and moving averages to follow trends for medium-to-long term trading. It is stable, easy to implement, and can effectively capture trend profits. We should continuously optimize parameters based on market conditions, manage risks, and generate good profitability. Overall, CMARSI is a recommended trend trading strategy.

|||


## Overview

The CMARSI trading strategy is a trend-following approach that combines the RSI indicator and moving averages. It uses an improved RSI (Connors RSI) to identify trends and moving averages as signals for entry and exit points. This strategy is suitable for medium-to-long term trading and aims to profit by following the prevailing trend.

## Principle Analysis

The CMARSI strategy employs a modified RSI indicator called Connors RSI, which incorporates three indicators: classical RSI, RSI Up/Down lines, and ROC percentile. The calculation formula is:

Connors RSI = (RSI + RSI Up/Down + ROC Percentile) / 3

Where RSI uses a 3-day period, RSI Up/Down uses a 2-day period, and ROC Percentile uses a 100-day period.

The advantage of Connors RSI is that it combines multiple indicators to more accurately identify trend changes. A crossing above 40 is interpreted as a long signal, while a crossing below 70 is seen as a short signal.

On top of this, the CMARSI strategy introduces a moving average factor. It calculates a 2-day moving average and uses golden crosses and death crosses between Connors RSI and the MA as trading signals. The specific rules are:

1. Enter long when Connors RSI crosses above 40 and has a golden cross of the 2-day MA.
2. Exit when Connors RSI crosses below 70 and has a death cross of the 2-day MA.

Using moving averages helps filter out some false signals from Connors RSI, thereby improving the stability of the strategy.

## Advantage Analysis

The biggest advantage of the CMARSI strategy is the combination of multiple indicators to identify trends, avoiding the limitations of single RSI indicators. Specifically, this strategy has the following advantages:

1. Connors RSI is more stable than classical RSI for identifying trend turning points.
2. The introduction of moving averages effectively filters out some noise and prevents chasing highs and selling lows.
3. The combination of multiple indicators can improve win rate by following trends.
4. The trading rules are simple and easy to implement.
5. As a trend-following strategy, it can fully capture profits from medium-to-long term trends.

## Risk Analysis

The main risks of the CMARSI strategy come from incorrect trend judgment and stop loss placement. Specific risks include:

1. Connors RSI gives incorrect signals, causing unnecessary entries. Parameters can be adjusted or additional indicators added for confirmation.
2. Stop loss placement is unreasonable, which may cause premature stop out or overly large stop losses. Stop loss should be optimized for different products and market environments.
3. Moving average filters may not work well in ranging markets. Strategy parameters should be optimized accordingly.
4. Prolonged use may lead to overfitting. Regular backtesting and parameter tuning based on market conditions are necessary.

## Optimization Directions

The CMARSI strategy can be optimized in the following areas:

1. Optimize Connors RSI parameters for different periods and products.
2. Try different types of moving averages to further improve filtering effects.
3. Add other indicators like MACD, Bollinger Bands for trade confirmation.
4. Optimize stop loss strategies, such as trailing stop losses or staggered stop losses.
5. Select products that fit the strategy better through screening.
6. Use Walk Forward Analysis to regularly optimize parameters and prevent overfitting.

## Conclusion

The CMARSI strategy combines Connors RSI and moving averages to follow trends for medium-to-long term trading. It is stable, easy to implement, and can effectively capture trend profits. We should continuously optimize parameters based on market conditions, manage risks, and generate good profitability. Overall, CMARSI is a recommended trend trading strategy.

```

```pinescript
/*backtest
start: 2022-09-19 00:00:00
end: 2023-09-25 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
src = close, lenrsi = 3, lenupdown = 2, lenroc = 100, malengt = 2, low = 40, high = 70, a = 1
updown(s) => 
    isEqual = s == s[1]
    isGrowing = s > s[1]
    ud = 0.0
    ud := isEqual ? 0 : isGrowing ? (nz(ud[1]) <= 0 ? 1 : nz(ud[1])+1) : (nz(ud[1]) >= 0 ? -1 : nz(ud[1])-1)
    ud
rsi = rsi(src, lenrsi)
updownrsi = rsi(updown(src), lenupdown)
percentrank = percentrank(roc(src, 1), lenroc)
crsi = avg(rsi, updownrsi, percentrank)
MA = sma(crsi, malengt)

band1 = 70
band0 = 40
```