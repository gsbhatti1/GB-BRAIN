> Name

TFO-and-ATR-Based-Trend-Tracking-Stop-Loss-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/14d3d06c1464e88c7e8.png)
[trans]

## Overview

This strategy is designed based on Dr. John Ehlers' Trend Flex Oscillator (TFO) and Average True Range (ATR) indicators. It is suitable for bull markets and will open long positions when oversold price action appears to reverse. It typically closes positions within a few days unless caught in a bear market, in which case it holds on. This strategy simplifies backtesting by making parameters configurable, but backtest results should never be fully trusted.

## Strategy Logic

This strategy combines the TFO and ATR indicators to determine entries and exits.

Entry conditions: When TFO drops below a threshold (indicating oversold levels) and TFO has risen from the previous bar (indicating TFO reversal upwards), and ATR is above a set volatility threshold (indicating increasing market volatility), long positions are opened.

Exit conditions: When TFO rises above a threshold (indicating overbought levels) and ATR is above a set threshold, all long positions are closed. In addition, a trailing stop loss exits all positions when price drops below the trailing stop level. Users can choose to allow the strategy to exit based on indicator signals or based solely on the stop loss.

The strategy allows up to 15 simultaneous long positions. Parameters can be adjusted for different timeframes.

## Advantages

1. Combining trend and volatility analysis provides steady signals. TFO captures early trend reversal signals and ATR identifies surge in volatility.

2. Adjustable entry, exit and stop loss parameters provide flexibility. Users can optimize based on market conditions.

3. Built-in stop loss protects against extreme moves. Stop losses are essential in quant trading.

4. Support for pyramiding and partial exits allows profit compounding in bull markets.

## Risks

1. Long only, no shorting mechanism. Cannot profit from falling markets. Severe bear markets can cause huge losses.

2. Poor parameter tuning can cause over trading or missed entries and exits. Extensive testing is needed to find optimal parameters.

3. In extreme moves, stop loss can fail and not prevent huge losses. A limitation of all stop loss strategies.

4. Backtest does not fully reflect live performance. Expect some deviation.

## Enhancement Opportunities 

1. A moving stop loss line can be added for timely exits and better downside protection.

2. Shorting mechanism can be added to allow profits during market drops when TFO reverses downwards and ATR is high enough.

3. More filters like volume change can reduce impacts of erratic price moves.

4. Different timeframes and parameters can be tested to find the best performing combination.

## Conclusion

This strategy combines the strengths of trend and volatility analysis using TFO and ATR to determine market direction. Mechanisms like pyramiding, partial close and trailing stop loss allow profit compounding while controlling risk during bull markets. There is room for improvements via more indicators filters and parameter optimization. It achieves the basic goals of a quant strategy and merits further research and application.

||

## Overview

This strategy is designed based on Dr. John Ehlers' Trend Flex Oscillator (TFO) and Average True Range (ATR) indicators. It is suitable for bull markets and will open long positions when oversold price action appears to reverse. It typically closes positions within a few days unless caught in a bear market, in which case it holds on. This strategy simplifies backtesting by making parameters configurable, but backtest results should never be fully trusted.

## Strategy Logic

This strategy combines the TFO and ATR indicators to determine entries and exits.

Entry conditions: When TFO drops below a threshold (indicating oversold levels) and TFO has risen from the previous bar (indicating TFO reversal upwards), and ATR is above a set volatility threshold (indicating increasing market volatility), long positions are opened.

Exit conditions: When TFO rises above a threshold (indicating overbought levels) and ATR is above a set threshold, all long positions are closed. In addition, a trailing stop loss exits all positions when price drops below the trailing stop level. Users can choose to allow the strategy to exit based on indicator signals or based solely on the stop loss.

The strategy allows up to 15 simultaneous long positions. Parameters can be adjusted for different timeframes.

## Advantages

1. Combining trend and volatility analysis provides steady signals. TFO captures early trend reversal signals and ATR identifies surge in volatility.

2. Adjustable entry, exit and stop loss parameters provide flexibility. Users can optimize based on market conditions.

3. Built-in stop loss protects against extreme moves. Stop losses are essential in quant trading.

4. Support for pyramiding and partial exits allows profit compounding in bull markets.

## Risks

1. Long only, no shorting mechanism. Cannot profit from falling markets. Severe bear markets can cause huge losses.

2. Poor parameter tuning can cause over trading or missed entries and exits. Extensive testing is needed to find optimal parameters.

3. In extreme moves, stop loss can fail and not prevent huge losses. A limitation of all stop loss strategies.

4. Backtest does not fully reflect live performance. Expect some deviation.

## Enhancement Opportunities 

1. A moving stop loss line can be added for timely exits and better downside protection.

2. Shorting mechanism can be added to allow profits during market drops when TFO reverses downwards and ATR is high enough.

3. More filters like volume change can reduce impacts of erratic price moves.

4. Different timeframes and parameters can be tested to find the best performing combination.

## Conclusion

This strategy combines the strengths of trend and volatility analysis using TFO and ATR to determine market direction. Mechanisms like pyramiding, partial close and trailing stop loss allow profit compounding while controlling risk during bull markets. There is room for improvements via more indicators filters and parameter optimization. It achieves the basic goals of a quant strategy and merits further research and application.

||

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_int_1|9|(?Back-Testing Start Date)From Month|
|v_input_int_2|true|From Day|
|v_input_int_3|2021|From Year|
|v_input_int_4|3|(?Average True Range)Min Volatility for Buy|
|v_input_int_5|13|Min Volatility for Sell|
|v_input_bool_1|false|Average the Volatility over 3 bars|
|v_input_float_1|1.2|(?Trend Flex Ocillator)TFO Upper Level|
|v_input_float_2|-0.9|TFO Lower Level|
|v_input_int_6|14|TrendFlex Period|
|v_input_bool_2|true|(?Selling Conditions)Allow Stategy to close positions|
|v_input_int_7|false|Value (%) must exceed |
|v_input_bool_3|true|Set Trailing Stop Loss on avg positon value|
|v_input_float_3|15|Trailing Stop Arms At (%)|
|v_input_float_4|2|Trailing Stop Loss (%)|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-11-27 00:00:00
end: 2023-12-03 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Chart0bserver 
//
// Open Source attributions:
// portions © allanster (date window code)
// portions © Dr. John Ehlers (Trend Flex Oscillator)
//
// READ THIS CAREFULLY!!! ----------------//
// This code is provided for educational purposes only.  The results of this strategy
```