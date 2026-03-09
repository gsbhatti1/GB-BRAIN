> Name

Dual-Strong-Trend-Tracking-Stop-Loss-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/6c30d4788579677714.png)
[trans]

## Overview

This strategy is designed with dual trend tracking mechanisms based on Supertrend and Relative Strength Index to accurately determine the market trend and set reasonable stop loss and take profit points. The strategy features stop loss points that track the market movement, take profit points based on the trend, and dual trend judgment, which can effectively control the risk of individual trades and achieve super strong returns in trending markets.

## Strategy Logic

1. Calculate the Supertrend to determine the main trend direction. Supertrend can accurately judge the trend direction and give ideal entry points.
2. Calculate the Relative Strength Index (RSI) as an auxiliary indicator for trend judgment. High RSI indicates a bullish trend in a bull market. Low RSI indicates a bearish trend in a bear market.
3. Go long when the close price crosses above the Supertrend line, and go short when the close price breaks below the Supertrend line.
4. Reasonably set stop loss and take profit points. When going long, set the Supertrend line as the stop loss, and the Supertrend line plus reasonable profit as the take profit. When going short, set the Supertrend line as the stop loss, and the Supertrend line minus reasonable profit as the take profit.
5. The stop loss points will float according to the market fluctuation. As the market moves in a favorable direction, the stop loss line will move towards the favorable direction to secure profits.
6. Only enter trades when RSI aligns with Supertrend, indicating a stronger current trend. Avoid entering when RSI diverges from Supertrend, indicating a potential trend reversal.

## Advantage Analysis

- The dual trend judgment mechanism can reduce false signals and enhance the stability of the strategy.
- Stop loss points move with the trend to maximize profit locking and avoid premature stop loss.
- The application of RSI filters out some weak trading signals.
- Reasonable take profit positioning maximizes profits.
- Adjustable strategy parameters can be optimized for different products and market conditions.
- Controllable drawdowns give the strategy strong risk management capabilities.

## Risk Analysis

- In case of black swan events like significant policy news, huge market swings may stop out positions and cause major losses. Wider stop loss points or timely position exiting prior to events can help manage such risks.
- Improper parameter settings may lead to unreasonable stop loss and take profit points, enlarging losses or shrinking profits. Repeated backtests can help find the optimal parameter combination.
- Divergence between RSI and Supertrend may generate false signals during range-bound markets. Avoid trading and wait for a clear trend in such cases.

## Optimization Directions

- Optimize the ATR period parameter for different products.
- Optimize RSI settings to find more stable auxiliary trend conditions.
- Incorporate other indicators like Bollinger Bands and KDJ to set more precise entry and exit rules.
- Test different take profit strategies like trailing stop, staggered profit taking, wick stop etc. to improve profitability.
- Adjust position sizing based on backtest results to lower single trade risks.

## Conclusion

The strategy demonstrates overall strong stability and profitability. The dual trend judgment filters out noise effectively and the stop loss/profit taking strategy locks in profits and controls risks. Continuous optimization of parameters and entry/exit conditions will enable great performance across different market environments. It can serve as an excellent template strategy for quantitative trading and is worth in-depth research and application.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|════════════ FROM ════════════|
|v_input_4|true|══════════ STRATEGY ══════════|
|v_input_string_1|0|Position Type: LONG|SHORT|
|v_input_float_1|3|Initial Stop Loss|
|v_input_5|true|ATR Period|
|v_input_float_2|3|ATR multplierFactoriplier|
|v_input_int_1|7|RSI|
|v_input_6|true|══════════ LOT CALC ══════════|
|v_input_7|true|══════════ TREND LINE ══════════|
|v_input_int_2|200|Trend Line|
|v_input_8_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_9|true|══════════ MT LOGIN ══════════|
|v_input_string_2|0|EXCHANGE: MT5|MT4|
|v_input_string_6|0|STRATEGY ON: ON|OFF|
|v_input_string_7|0|ENTRY MODE: CLOSE OPEN|OPEN|
|v_