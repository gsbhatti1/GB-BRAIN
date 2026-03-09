> Name

RePaNoCHa Quantitative Trading Strategy RePaNoCHa-Quantitative-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

The RePaNoCHa strategy is a quantitative trading strategy that integrates multiple indicators and risk management mechanisms. It primarily generates buy and sell signals by identifying trend direction and potential reversal points. The strategy also includes trailing stop loss, fixed stop loss, and take profit settings to lock in profits and control risks.

## Strategy Logic

The strategy integrates the following indicators:

- T3 Moving Average: To gauge price trend.
- Average Range Filter: To identify price fluctuation zones.
- ADX: To determine trend strength.
- SAR: To mark potential reversal points.
- RSI: To identify overbought/oversold levels.
- MACD: To display price momentum.

When the indicators give aligned signals, the strategy determines a trend has started and produces entry signals. After entering, it uses a linear trailing stop loss to follow a percentage of the highest/lowest price, gradually moving up as profits increase to lock in gains. Fixed percentage stop loss is also used to limit maximum loss per trade.

Specifically, when price is above range upper band, T3 rising, ADX bullish, SAR bullish, RSI above midpoint, MACD positive, long signal is generated. The opposite conditions generate short signal. Take profit and stop loss are fixed at 1% and 3% of entry price. Trailing stop distance is linearly set based on current profit relative to entry price.

## Advantage Analysis

- Multiple indicators improve accuracy  
Combining trend, momentum, and reversal indicators avoids single indicator pitfalls.

- Flexible trailing stop locks in profits  
Trailing stop level adjusts with changing profits to better follow price fluctuations and secure gains.

- Fixed stop controls max loss  
The fixed stop loss percentage limits maximum loss per trade and prevents loss expansion.

- Customizable parameters  
Indicators parameters can be freely tuned for optimizing across different trading products.

## Risk Analysis

- Increased decision difficulty with more indicators  
Too many indicators may cause contradiction and increased difficulty in decision making. Indicator effectiveness needs proper evaluation.

- Whipsaw and stop loss trigger during high volatility  
Sharp volatile moves can cause whipsaw and frequent stop loss triggering, rendering take profit useless.

- Increased trading costs from higher frequency  
More short-term signals increase trade frequency and slippage costs, impacting actual profitability.

- Difficult optimization with multiple parameters  
Testing various parameter combinations of indicators makes optimization challenging and requires sufficient history.

## Improvement Directions

- Evaluate actual indicator effects to avoid redundancy  
Compare test results to examine the actual incremental benefits of each indicator and remove redundant ones.

- Optimize trailing stop algorithms  
Test different trailing stop algorithms to find better ways to trail profits.

- Account for real slippage and commissions  
Incorporate actual trading costs into backtest to aid entry decision making.

- Separate parameter optimization by volatility  
Optimize parameters separately for high/low volatility sessions to improve robustness.

## Summary

The RePaNoCHa strategy realizes relatively stable automated trading decisions and profit management through integrating multiple indicators and stop mechanisms. But its high trading frequency and complex optimization process need further improvement. More real-world factors should be introduced into backtests, and techniques like benchmark testing should be adopted to simplify the model and reduce overfitting risks, in order to achieve consistent long-term returns from its relatively active trading approach.

---

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|0|POSITIONS: BOTH|LONG|SHORT|
|v_input_2_hlc3|0|SOURCE: hlc3|high|low|open|hl2|close|hlcc4|ohlc4|
|v_input_3|3|T3 LENGTH|
|v_input_4|0.4|T3 VOLUME FACTOR|
|v_input_5|23|SAMPLING PERIOD|
|v_input_6|1.5|RANGE MULTIPLIER|
|v_input_7|12|ADX LENGTH|
|v_input_8|8|ADX THRESHOLD|
|v_input_9|0.07|SAR STAR|
|v_input_10|0.05|SAR INC|
|v_input_11|0.15|SAR MAX|
|v_input_12|14|RSI LENGTH|
|v_input_13|52|RSI CENTER LINE|
|v_input_14|10|MACD FAST LENGTH|
|v_input_15|19|MACD SLOW LENGTH|
|v_input_16|9|MACD SIGNAL SMOOTHING|
|v_input_17|false|MACD SIMPLE MA(Oscillator)|
|v_input_18|0.5|TRAILING STOP ACTIVATION %|
|v_input_19|0.25|TRAILING STOP OFFSET % WHEN PROFIT=0.5% (MINIMUM)|
|v_input_20|true|TRAILING STOP OFFSET % WHEN PROFIT=10% (LINEAR_EXTRAPOLATION)|
|v_input_21|120|TRAILING STOP DELAY (SECONDS)|
|v_input_22|100|MAX_TRAIL_LOSS (Pips)|
|v_input_23|100|MAX_TRAIL_PROFIT (Pips)|
|v_input_24|0|TRAILING STOP PIPS|
|v_input_25|0|TRAILING STOP PIPS WHEN PROFIT=0 (MINIMUM)|
|v_input_26|1|TRAILING STOP PIPS WHEN PROFIT=10 (LINEAR_EXTRAPOLATION)|
|v_input_27|0|FIXED STOP LOSS PIPS|
|v_input_28|0|FIXED STOP LOSS PIPS WHEN PROFIT=0 (MINIMUM)|
|v_input_29|1|FIXED STOP LOSS PIPS WHEN PROFIT=10 (LINEAR_EXTRAPOLATION)|
|v_input_30|0|FIXED TAKE PROFIT PIPS|
|v_input_31|0|FIXED TAKE PROFIT PIPS WHEN PROFIT=0 (MINIMUM)|
|v_input_32|1|FIXED TAKE PROFIT PIPS WHEN PROFIT=10 (LINEAR_EXTRAPOLATION)|