> Name

Dual-SuperTrend-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/145cbf84b133a308352.png)

[trans]

### Overview

The Dual-SuperTrend strategy is a short-term quantitative trading strategy that integrates a dual SuperTrend channel system. It calculates true range volatility and constructs a two-band channel system to monitor price breakthroughs, enabling trend following and reversal trading.

### Strategy Logic

The Dual-SuperTrend strategy is derived from the SuperTrend indicator. SuperTrend consists of upper and lower bands to determine price trends and key support/resistance levels. The Dual-SuperTrend builds two channels: the consolidating channel and the breaking channel.

- **Consolidating Channel**: made up of the basic upper and lower bands to judge the ongoing trend.
- **Breaking Channel**: formed by the heuristic upper and lower bands to capture trend reversals.

The strategy first calculates the true range and average true range. It then calculates the basic bands based on the length and multiplier parameters. Next, it constructs the breaking channel if the price breaks through the basic bands. The dual-channel system is thus established.

Under the dual-channel structure, trading signals are generated when the price crosses different channels:

- A buy signal is triggered when the price crosses above the lower band of the consolidating channel.
- A sell signal is triggered when the price crosses below the upper band of the consolidating channel.

The dual-channel monitoring enables both trend following and reversal capturing.

### Advantage Analysis

The Dual-SuperTrend strategy with the dual-channel system has the following advantages:

- Capturing trend reversals and avoiding false breakouts. The breaking channel effectively identifies true reversals.
- Persistence in trades. The dual-channel prolongs each trade compared to the single SuperTrend.
- Large parameter optimization space. The channels can be tuned for different products and timeframes.
- Reduced strategy whipsaws. The dual-channel enhances stability.
- Easy backtesting and optimization. The intuitive channels facilitate evaluating the strategy.

### Risk Analysis

The Dual-SuperTrend strategy also has the following risks:

- Channel range selection requires expertise. Too narrow channels cause frequent invalid breakouts. Too wide channels fail to capture reversals timely.
- Impact from external events. Non-technical events may trigger abnormal price moves that invalidate the channel system.
- High trading frequency. The dual-channel structure tends to increase trading frequency and position sizing needs control.
- Difficult parameter optimization. It is challenging to optimize both channels simultaneously. Sufficient time is required.
- No stop loss guarantee. The strategy does not have a stop loss mechanism.

The risks can be mitigated by adjusting parameter range, adding filters, controlling position sizing, etc.

### Optimization Directions

The Dual-SuperTrend strategy can be optimized in the following aspects:

- Adding filters to avoid false breakouts. Volume or volatility indicators can be used to confirm valid breakouts.
- Incorporating trend indicators to determine the macro trend. Trading along the major trend avoids counter-trend trades.
- Dynamically adjusting channel parameters to adapt to changing markets. Adaptive algorithms can optimize parameters.
- Optimizing exit mechanisms for profit protection. Trailing stop or time-based exit can be incorporated.
- Separating long and short states for directional trading. Different parameters can be used for bullish and bearish stages.
- Introducing quant risk control for maximum drawdown limit. Position sizing control and overall stop loss can be set.

Further optimizations can improve Parameter Fitting and Walk Forward Analysis for more robust performance.

### Conclusion

The Dual-SuperTrend strategy leverages the dual-channel mechanism for trend following and reversal capturing. Stable trading strategies can be developed through parameter optimization, but limitations exist. Risk control addons are required. Overall, the Dual-SuperTrend provides a solid framework for short-term quantitative trading strategies.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|10|Length|
|v_input_2|3|Multiplier|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-11-08 00:00:00
end: 2023-11-14 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTCUSDT"}]
*/
```