> Name

One-Point Fairness Cloud Without Offset RSI Filtering Strategy No-Offset-Ichimoku-Cloud-with-RSI-Filter-Strategy

> Author

ChaoZhang

> Strategy Description


![IMG](https://www.fmz.com/upload/asset/af846716fea1ada703.png)
[trans]


## Overview

This is a trend-following strategy that uses the Ichimoku Cloud indicator for trend identification and combines it with the RSI indicator for signal filtering. The strategy disregards observation offset, enabling timely capture of trend changes while using the RSI indicator to filter false breakouts to control trading risks.

## Strategy Logic

The strategy mainly relies on the direction of the trend identified by the Ichimoku Cloud indicator. The Ichimoku Cloud consists of the conversion line, base line, leading span 1, leading span 2, and lagging span. The strategy uses a non-offset Ichimoku Cloud, meaning lines like the conversion line and base line use future values to avoid trend judgment delays caused by observation offset.

The strategy first checks if the price breaks through the cloud lines. An upward trend is initiated when the lagging span crosses above the cloud; a downward trend starts when it crosses below the cloud. Once a trend begins, the strategy continues tracking the relationship between the price and the cloud to determine the persistent direction of the trend. The uptrend remains intact if the lagging span stays above the cloud, and vice versa.

In addition to trend identification, the strategy generates buy signals when the conversion line and base line form a golden cross and sell signals during a death cross. These trading signals are only accepted if they align with the trend direction. For example, a golden cross between the conversion line and base line is only considered valid in an uptrend.

Finally, the RSI indicator is introduced to filter these signals. Only buy signals when the RSI is below the oversold level and sell signals when it's above the overbought level are accepted. This helps filter out false breakouts to some extent.

## Advantage Analysis

- Using a non-offset Ichimoku Cloud allows for timely trend identification without missing reversal opportunities.
- Multiple conditions combine effectively to filter out false breakout signals.
- The RSI indicator can avoid undesirable market entry during overbought or oversold conditions.
- The strategy is optimized with future data, which can yield good results in live trading.

## Risk Analysis

- Using future data may cause errors and needs code optimization for live trading use.
- The Ichimoku Cloud is sensitive to parameters, requiring parameter tuning for different products.
- Better performance when trading a single product. Consider inter-market correlation when dealing with multiple products.
- Many trend identification rules require adequate backtesting periods to validate.

Parameters can be optimized to find the best combination. In live trading, consider only trading specific products or reducing position sizes to control risks. Stop loss strategies may also be introduced to limit per-trade losses.

## Optimization Directions

The strategy can be further improved in the following areas:

1. Optimize Ichimoku Cloud parameters to find the best settings for different trading instruments.
2. Add stop loss mechanisms to limit per-trade losses to an acceptable level.
3. Introduce position management strategies to manage overall risk exposure precisely.
4. Incorporate more indicators like volatility and volume for comprehensive signal verification.
5. Optimize entry techniques such as confirmation or pullback entries for better execution.
6. Perform walk-forward optimization to determine the optimal Bollinger Bands lookback period based on product characteristics.

## Conclusion

Overall, this is a relatively robust trend-following strategy that uses the Ichimoku Cloud for direction identification and conversion/base line crosses for trade signals, filtered by RSI. There is still significant room for optimization through parameter tuning, stop loss mechanisms, position management, etc. The logic is clear and easy to understand. It considers both trend and risk factors, making it a worthwhile strategy for live trading verification.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Standard Ichimoku Cloud|
|v_input_2|true|Ichimoku Cloud - no offset - no repaint|
|v_input_3|9|Conversion Line Period - Tenkan-Sen|
|v_input_4|26|Base Line Period - Kijun-Sen|
|v_input_5|52|Base Line Period - Kijun-Sen (auxiliary)|
|v_input_6|52|Lagging Span 2 Periods - Senkou Span B|
|v_input_7|26|Displacement: (-) Chikou Span; (+) Senkou Span A|
|v_input_8|true|Displacement: additional bars|
|v_input_9_close|0|Lagging