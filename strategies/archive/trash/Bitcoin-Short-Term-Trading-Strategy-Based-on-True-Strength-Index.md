> Name

Bitcoin-Short-Term-Trading-Strategy-Based-on-True-Strength-Index

> Author

ChaoZhang

> Strategy Description

## Overview

This strategy identifies Bitcoin market trends by calculating the True Strength Index (TSI) and enters long/short positions filtered by the Relative Strength Index (RSI) indicator to implement algorithmic trading of Bitcoin. It is suitable for investors who want to trade Bitcoin tick data programmatically.

## Strategy Logic

The core of this strategy is the True Strength Index (TSI). TSI measures the absolute magnitude and direction of price changes by double smoothing the percentage price change, thereby identifying the absolute strength of price up and down moves. The specific calculation is as follows:

1. Calculate the percentage price change `Pc`
2. Double smooth `Pc` using long-term Exponential Moving Average (EMA) and short-term EMA to generate `double_smoothed_pc`
3. Double smooth the absolute value of `Pc` to generate `double_smoothed_abs_pc`
4. TSI value equals `double_smoothed_pc` divided by `double_smoothed_abs_pc` multiplied by 100

When TSI crosses over its signal line `tsi2`, a long signal is generated. When TSI crosses below `tsi2`, a short signal is generated. In addition, the strategy filters TSI signals with the RSI - only taking long signals when RSI is above 50 and short signals when RSI is below 50, to avoid some false signals.

## Advantage Analysis

The advantages of this strategy include:

1. TSI can detect the absolute strength and direction of price moves, and is sensitive in capturing trends.
2. The double EMA smooths price change rate and is resilient to market noise and spikes.
3. RSI filter further avoids wrong trades due to noise.
4. Short-term trading allows capturing temporary opportunities in the market.
5. The strategy has large parameter tuning space for optimization, like EMA periods, RSI parameters etc.

## Risk Analysis

The risks of this strategy include:

1. As a trend following indicator, TSI has a lagging issue and may miss price reversal points.
2. The RSI filter condition is too strict and may miss some trading chances.
3. The double EMA filter may also filter out some valid signals.
4. High trading frequency of short-term trading introduces higher trading cost and slippage risks.

The lagging issue and filter effect can be reduced by relaxing RSI filter rules and shortening EMA periods. Proper stop loss strategy should be used to strictly control per trade risks.

## Optimization Directions

The strategy can be optimized in the following aspects:

1. Optimize TSI and RSI parameters to find the best combination. Tuning long/short EMA periods, RSI parameters etc.
2. Introduce more technical indicators to build a multifactor model. MA, KD etc can be added to take advantage of each indicator.
3. Optimize entry rules to avoid long in downtrend and short in uptrend. Judge direction based on higher timeframe trends.
4. Optimize stop loss strategies like trailing stop loss, time-based stop loss, breakout stop loss etc.
5. Optimize exit rules to avoid premature or late exits. Volatility indicators can help determine proper exit points.
6. Optimize trading products, trading sessions to focus on the most effective ones.

## Conclusion

This strategy identifies Bitcoin short-term trends with True Strength Index and filters signals with RSI for algorithmic trading. It has the advantage of sensitively capturing trends and filtering noise, but also has some lagging issues and trading risks. Multi-faceted optimizations can further improve strategy performance to develop a reliable Bitcoin trading expert advisor.

|||

## Overview

This strategy identifies Bitcoin market trends by calculating the True Strength Index (TSI) and enters long/short positions filtered by the Relative Strength Index (RSI) indicator to implement algorithmic trading of Bitcoin. It is suitable for investors who want to trade Bitcoin tick data programmatically.

## Strategy Logic

The core of this strategy is the True Strength Index (TSI). TSI measures the absolute magnitude and direction of price changes by double smoothing the percentage price change, thereby identifying the absolute strength of price up and down moves. The specific calculation is as follows:

1. Calculate the percentage price change `Pc`
2. Double smooth `Pc` using long-term EMA and short-term EMA to generate `double_smoothed_pc`
3. Double smooth the absolute value of `Pc` to generate `double_smoothed_abs_pc`
4. TSI value equals `double_smoothed_pc` divided by `double_smoothed_abs_pc` multiplied by 100

When TSI crosses over its signal line `tsi2`, a long signal is generated. When TSI crosses below `tsi2`, a short signal is generated. In addition, the strategy filters TSI signals with the RSI - only taking long signals when RSI is above 50 and short signals when RSI is below 50, to avoid some false signals.

## Advantage Analysis

The advantages of this strategy include:

1. TSI can detect the absolute strength and direction of price moves, and is sensitive in capturing trends.
2. The double EMA smooths price change rate and is resilient to market noise and spikes.
3. RSI filter further avoids wrong trades due to noise.
4. Short-term trading allows capturing temporary opportunities in the market.
5. The strategy has large parameter tuning space for optimization, like EMA periods, RSI parameters etc.

## Risk Analysis

The risks of this strategy include:

1. As a trend following indicator, TSI has a lagging issue and may miss price reversal points.
2. The RSI filter condition is too strict and may miss some trading chances.
3. The double EMA filter may also filter out some valid signals.
4. High trading frequency of short-term trading introduces higher trading cost and slippage risks.

The lagging issue and filter effect can be reduced by relaxing RSI filter rules and shortening EMA periods. Proper stop loss strategy should be used to strictly control per trade risks.

## Optimization Directions

The strategy can be optimized in the following aspects:

1. Optimize TSI and RSI parameters to find the best combination. Tuning long/short EMA periods, RSI parameters etc.
2. Introduce more technical indicators to build a multifactor model. MA, KD etc can be added to take advantage of each indicator.
3. Optimize entry rules to avoid long in downtrend and short in uptrend. Judge direction based on higher timeframe trends.
4. Optimize stop loss strategies like trailing stop loss, time-based stop loss, breakout stop loss etc.
5. Optimize exit rules to avoid premature or late exits. Volatility indicators can help determine proper exit points.
6. Optimize trading products, trading sessions to focus on the most effective ones.

## Conclusion

This strategy identifies Bitcoin short-term trends with True Strength Index and filters signals with RSI for algorithmic trading. It has the advantage of sensitively capturing trends and filtering noise, but also has some lagging issues and trading risks. Multi-faceted optimizations can further improve strategy performance to develop a reliable Bitcoin trading expert advisor.

|||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|15|Timeframe|
|v_input_2|25|Long Length|
|v_input_3|13|Short Length|
|v_input_4|13|Signal Length|


> Source (PineScript)

```pinescript
//@version=5
strategy("True Strength Indicator BTCUSD 15p", shorttitle="TSI BTCUSD 15p", initial_capital=1000, commission_value=0.15, commission_type=strategy.commission.percent, default_qty_value=100, overlay=false, pyramiding=10, default_qty_type=strategy.percent_of_equity)

resCustom = input.int(title="Timeframe", defval=15)
long = input.int(title="Long Length", defval=25)
short = input.int(title="Short Length", defval=13)
signal = input.int(title="Signal Length", defval=13)
price = request.security(syminfo.tickerid, resCustom, close)

double_smooth(src, long, short) =>
    first_smooth = ta.ema(src, short)
    second_smooth = ta.ema(first_smooth, long)
    second_smooth

tsi = double_smooth(price, long, short) / double_smooth(abs(price), long, short) * 100
tsi2 = sma(tsi, signal)

long_condition = tsi > tsi2 and rsi(price, 14) > 50
short_condition = tsi < tsi2 and rsi(price, 14) < 50

if (long_condition)
    strategy.entry("Long", strategy.long)

if (short_condition)
    strategy.entry("Short", strategy.short)

strategy.exit("Exit Long", "Long", stop = tsi < tsi2)
strategy.exit("Exit Short", "Short", stop = tsi > tsi2)

// Add your own plotting and drawing code here
```