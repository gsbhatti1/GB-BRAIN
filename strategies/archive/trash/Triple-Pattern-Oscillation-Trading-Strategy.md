> Name

Triple-Pattern-Oscillation-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/189faac7cf9959c9167.png)

[trans]

## Overview

The Triple Pattern Oscillation Trading Strategy is a short-term trading strategy based on a combination of multiple technical indicators. It incorporates the Super Trend, SSL Hybrid Moving Average and Improved QQE to generate stable trading signals. The strategy works well with volatile trading instruments like cryptocurrencies and stocks, especially during post-breakout periods.

## Principles 

### Entry Signals

Long Entry:

- Super Trend flipping from down to up
- Close above SSL Hybrid upper band  
- Improved QQE is blue (bullish)

Short Entry:

- Super Trend flipping from up to down
- Close below SSL Hybrid lower band
- Improved QQE is red (bearish)

### Exit Signals

Long Exit: Super Trend flipping from up to down  

Short Exit: Super Trend flipping from down to up

### Stop Loss

Options of percentage, ATR or recent highest/lowest price

### Take Profit 

Can set a risk-reward ratio for take profit levels

### Risk Management

Option to enable position sizing based on account risk 

### Plotting

- Plot Super Trend line, SSL Hybrid bands
- Option for EMA line
- Plot entry, stop loss and take profit lines
- Entry arrow labels 

## Advantages

1. Stable signals from multiple indicators

Combining Super Trend, SSL Hybrid MA and Improved QQE verifies signals across indicators, filtering false breakouts. Quality trading signals are generated.

2. Suitable for oscillation trading of volatile instruments 

Short-term trading approach focuses on capturing medium-term price swings. Super Trend tracks trends smoothly while SSL Hybrid identifies support/resistance levels clearly. Profitable in ranging markets.

3. Flexible stop loss and take profit

Choice of percentage, ATR or recent extreme for stop loss. Risk-reward ratio sets take profit. Options suit different trading instruments and risk preferences.

4. Clear plotting 

Clean plotting visually displays stop loss, take profit levels. Entry arrows easy to identify.

## Risks and Improvements

1. Occasional minor losses

Short-term trading cannot fully avoid normal ranging market losses. Can optimize stop loss and risk management.

2. False breakout risks

False breakouts may generate wrong signals. Test EMA periods to filter. Optimize trend identification parameters.

3. Monitor indicator failure

Invalid indicators cause multiple false signals. Regularly check indicator validity, adjust promptly if issues found.

4. Optimize backtest period 

Current fixed backtest period does not match instruments' active hours. Optimize to trading sessions.

5. Enhance instrument adaptability

Fine tune parameters for each instrument's data characteristics, improving win rates. Stepwise optimize parameter impact.

## Conclusion

This strategy combines multiple indicators for robust signals, filtering false breakouts. It excels trading volatile cryptocurrencies and equities short-term. Numerous stop loss and take profit choices provide flexibility. Overall, stable signals are generated for medium-term range trading. Further optimizations can improve profit factor across instruments. A promising high-performance trading system worth in-depth research.

[/trans]


> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_3_close|0|RSI Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_1|timestamp(20 Jan 1990 00:00 +0900)|(?Time)Start Date|
|v_input_2|timestamp(20 Dec 2030 00:00 +0900)|End Date|
|v_input_bool_1|true|(?Long / Short)Long?|
|v_input_bool_2|true|Short?|
|v_input_bool_3|false|(?Filters)ATR Filter On?|
|v_input_int_1|14|Length for ATR Filter|
|v_input_int_2|40|SMA Length for ATR SMA|
|v_input_bool_4|false|EMA Filter On?|
|v_input_int_3|200|EMA Length|
|v_input_bool_5|false|ADX Filter On?|
|v_input_bool_6|false|DMI Filter On?|
|v_input_int_4|20|ADX Length|
|v_input_int_5|25|ADX Threshold|
|v_input_int_6|10|(?1: SuperTrend)ATR Length|
|v_input_float_1|3|Factor|
|v_input_bool_7|true|(?2: SSL Hybrid)use true range for Keltner Channel?|
|v_input_string_1|0|Baseline Type: EMA|SMA|DEMA|TEMA|LSMA|WMA|VAMA|TMA|HMA|McGinley|
|v_input_int_7|30|Baseline Length|
|v_input_float_2|0.2|Base Channel Multiplier|
|v_input_int_8|10|Volatility lookback length(for VAMA)|
|v_input_int_9|6|(?3: QQE MOD)RSI Length|
|v_input_int_10|5|RSI Smoothing|
|v_input_float_3|3|Fast QQE Factor|
|v_input_int_11|3|Thresh-hold|
|v_input_int_12|50|Bollinger Length|
|v_input_float_4|0.35|BB Multiplier|
|v_input_int_13|6|RSI 2  Length|
|v_input_int_14|5|RSI Smoothin