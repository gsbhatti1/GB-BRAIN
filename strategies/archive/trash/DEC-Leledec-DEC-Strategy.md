> Name

DEC Strategy Leledec-DEC-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1888333f2986e2f4add.png)
[trans]

## Overview

The Leledec DEC strategy identifies market trend reversals by detecting exhaustion patterns of the Leledec indicator. Long positions are taken when major exhaustion occurs, and short positions when minor exhaustion is detected. This strategy is primarily suitable for medium to long-term trading.

## Strategy Logic

The Leledec indicator is used to identify local price extremum points by analyzing the relationship between closing and opening prices over several bars. 

The core logic of the strategy is:

1. Calculate the major Leledec indicator (maj) using parameters bar count (maj_qual) and lookback period (maj_len).

2. When major Leledec breaks above `maj_qual` consecutive bars, and the high of this bar exceeds the highest high over the previous `maj_len` bars, a major upside exhaustion is identified which generates a long signal.

3. Calculate the minor Leledec indicator (min) using parameters bar count (min_qual) and lookback period (min_len).

4. When minor Leledec breaks below `min_qual` consecutive bars, and the low of this bar falls below the lowest low over the previous `min_len` bars, a minor downside exhaustion is identified which generates a short signal.

According to the Leledec indicator logic, exhaustion patterns indicate potential extremum points and trend reversals, thus generating trading signals.

## Advantage Analysis

- The strategy has strong trend identification capabilities. The Leledec indicator can effectively identify local price extremum points.

- Flexibility in adapting to different timeframes and market conditions through parameter tuning.

- Can use major Leledec alone or incorporate minor Leledec for more comprehensive signals.

- Customizable sensitivity through bar count and lookback period parameters.

## Risk Analysis

- Potential for false signals, requires validation using other indicators.

- Parameter optimization needed for different products and timeframes. Improper parameters may cause over-trading or missed trades.

- Mainly relies on candlestick patterns, may miss opportunities during short-term price oscillations.

- Need to watch real bodies of signal bars for failed trend reversals.

## Optimization

- Optimize parameter combinations for better adaptability. Consider dynamic optimization.

- Incorporate other indicators like volume, moving averages etc. to filter signals.

- Implement stop loss to control downside on single trades.

- Incorporate short-term indicators to catch opportunities from minor oscillations.

- Test on different products to find optimal environment.

- Optimize money management strategies like position sizing, risk per trade etc.

## Conclusion

The Leledec strategy identifies trend reversals by detecting extremum patterns in the Leledec indicator. It is an effective trend-following methodology. While advantageous in assessing trends, further optimization, additional signal validation, and proper risk management are needed for long-term profitability. Overall, the Leledec strategy provides a valuable addition to a trader's toolkit.

|||

## Overview

The Leledec strategy identifies market trend reversals by detecting exhaustion patterns of the Leledec indicator. Long positions are taken when major exhaustion occurs, and short positions when minor exhaustion is detected. The strategy is suitable for medium to long-term trading.

## Strategy Logic

The Leledec indicator identifies local price extremum points by analyzing the relationship between closing and opening prices over several bars.

The core logic of the strategy is:

1. Calculate the major Leledec indicator (maj) using parameters bar count (`maj_qual`) and lookback period (`maj_len`).

2. When major Leledec breaks above `maj_qual` consecutive bars, and the high of this bar exceeds the highest high over the previous `maj_len` bars, a major upside exhaustion is identified which generates a long signal.

3. Calculate the minor Leledec indicator (min) using parameters bar count (`min_qual`) and lookback period (`min_len`).

4. When minor Leledec breaks below `min_qual` consecutive bars, and the low of this bar falls below the lowest low over the previous `min_len` bars, a minor downside exhaustion is identified which generates a short signal.

According to the logic of the Leledec indicator, exhaustion patterns represent potential extremum points and trend reversals, hence generating trading signals.

## Advantage Analysis

- The strategy has strong capabilities in trend identification. The Leledec can effectively detect local price extremum points.

- Flexibility in adapting to different timeframes and market conditions through parameter tuning.

- Can use major Leledec alone or incorporate minor Leledec for more comprehensive signals.

- Customizable sensitivity through bar count and lookback period parameters.

## Risk Analysis

- Potential for false signals, requires validation using other indicators.

- Parameter optimization needed for different products and timeframes. Improper parameters may cause over-trading or missed trades.

- Mainly relies on candlestick patterns, may miss opportunities during short-term price oscillations.

- Need to watch real bodies of signal bars for failed trend reversals.

## Optimization

- Optimize parameter combinations for better adaptability. Consider dynamic optimization.

- Incorporate other indicators like volume, moving averages etc. to filter signals.

- Implement stop loss to control downside on single trades.

- Incorporate short term indicators to catch opportunities from minor oscillations.

- Test on different products to find optimal environment.

- Optimize money management strategies like position sizing, risk per trade etc.

## Conclusion

The Leledec strategy catches trend reversals by identifying extremum patterns in the Leledec indicator. It is an effective trend-following methodology. While advantageous in assessing trends, further optimization, additional signal validation, and proper risk management are needed for long-term profitability. Overall, the Leledec strategy provides a valuable addition to a trader's toolkit.

|||

> Strategy Arguments

|Argument|Default|Description|
|---|---|---|
|v_input_1|true|Major Leledec Exhausion Bar ::  Show|
|v_input_2|false|Minor Leledec Exhausion Bar ::  Show|
|v_input_3_close|0|Major Leledec Exhausion Bar ::  Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_4|6|Major Leledec Exhausion Bar ::  Bar count no|
|v_input_5|30|Major Leledec Exhausion Bar ::  Highest / Lowest|
|v_input_6|5|Minor Leledec Exhausion Bar ::  Bar count no|
|v_input_7|5|Minor Leledec Exhausion Bar ::  Bar count no|
|v_input_8|true|bindexSindex|
|v_input_9|4|Close|
|v_input_10|true|From Month|
|v_input_11|true|From Day|
|v_input_12|2018|From Year|
|v_input_13|12|Thru Month|
|v_input_14|true|Thru Day|
|v_input_15|2030|Thru Year|
|v_input_16|true|Show Date Range|

> Source (PineScript)

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Joy_Bangla

//@version=4
strategy("A Strategy for Leledec", shorttitle ="Leledec Strategy", overlay=true, commission_value=0.075, initial_capital=10000, default_qty_type = strategy.percent_of_equity, default_qty_value = 10)

maj = input(true, "Major Leledec Exhausion Bar ::  Show")
min=input(false, "Minor Leledec Exhausion Bar ::  Show")
leledcSrc = input(close, "Major Leledec Exhausion Bar ::  Source")
maj_qual = input(6, "Major Leledec Exhausion Bar ::  Bar count no")
maj_len = input(30