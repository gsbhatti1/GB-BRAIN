> Name

Three-Supertrend-Strategy

> Author

ChaoZhang

> Strategy Description


[trans]

Supertrend strategy principle analysis

The Supertrend strategy is a trend-following strategy that determines trend direction by calculating the Average True Range (ATR) and plotting Supertrend lines. This strategy uses three sets of parameters to plot three Supertrend lines and generate trading signals when the price breaks through the lines.

The strategy first calculates three sets of ATR and factors to plot three Supertrend lines. The ATR reflects price volatility while the factor determines the sensitivity of the Supertrend lines to price. This strategy adopts combinations of short-term, medium-term, and long-term parameters to capture trend changes across different timeframes.

When the price crosses above the Supertrend line, it signals an uptrend and the strategy will go long. When the price crosses below the line, it signals a downtrend and the strategy will go short. The three Supertrend lines can generate more trading opportunities while also validating signals to reduce false signals.

In addition, the strategy uses the change function to check if the Supertrend line direction has changed. New signals are generated only when the direction changes, avoiding new trades immediately after closing positions. Finally, the strategy offers close all and cancel all functions to improve tradability.

In summary, the Supertrend strategy fully utilizes the advantages of the Supertrend indicator to capture trends across timeframes using multiple parameters sets. It also incorporates proper entry and exit systems and can serve as a reference for trend following strategies.

Supertrend Strategy Advantages

The Supertrend strategy has the following advantages:

1. Strong ability to capture trend changes - The dynamic Supertrend lines can flexibly capture trend changes in the market and avoid false signals from ranging markets.
2. Multiple parameter sets - Using three parameter sets to plot three Supertrend lines allows capturing trends across short, medium and long timeframes for more opportunities.
3. Reversal validation mechanism - Generating new signals only when the Supertrend line direction changes avoids unnecessary whipsaws and verifies signal reliability.
4. Practical design - The close all positions and cancel all orders functions improve real-world tradability.
5. Simple and clear logic - Using Supertrend as the basis with straightforward signal rules makes it easy to operate and test. Suitable for quantitative trading beginners.

Supertrend Strategy Risks  

The Supertrend strategy also has the following risks:

1. Prone to false signals - Frequent crosses of the Supertrend lines may generate excessive false signals and losses in ranging markets.
2. Difficult parameter optimization - Optimizing multiple parameter sets can be challenging. Unsuitable parameters may degrade performance.
3. Unable to identify trend reversal points - Relies solely on trend direction without determining potential trend reversions. Requires additional indicators.
4. Extreme events risks - Unable to effectively control risks in extreme market conditions. Requires stop loss strategies to manage risk.
5. Curve fitting bias - Optimized parameters can overfit historical data but may not remain effective in the future. Require prudent evaluation.

Supertrend Strategy Summary

Overall, the Supertrend strategy is a simple and practical trend following system. It capitalizes on the dynamic Supertrend lines to determine trend direction and uses multiple parameter sets to improve performance. The strategy mechanisms are also reasonably designed for tradability. However, issues like false signals and difficult parameter optimization require combining with other technical indicators for improvements. In general, the Supertrend strategy works well for medium to long-term trend tracking and can serve as a reference strategy template for beginners.
[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|false|Close_all_Position|
|v_input_2|false|Check To Cancel|
|v_input_3|7|ATR Length-1|
|v_input_4|1.5|Factor-1|
|v_input_5|10|ATR Length-2|
|v_input_6|2|Factor-2|
|v_input_7|20|ATR Length-3|
|v_input_8|3|Factor-3|

> Source (PineScript)

``` pinescript
/*backtest
start: 2023-08-15 00:00:00
end: 2023-09-14 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to