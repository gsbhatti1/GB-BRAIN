> Name

DEC Strategy Leledec-DEC-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1888333f2986e2f4add.png)
[trans]

## Overview

The Leledec DEC strategy identifies market trend reversals by detecting the exhaustion patterns of the Leledec DEC indicator. When a major exhaustion pattern of Leledec DEC appears, it goes long; when a minor exhaustion pattern appears, it goes short. This strategy is mainly suitable for medium to long-term trading.

## Strategy Logic

The Leledec DEC indicator is used to identify local extreme points in prices. It does so by analyzing the relationship between close and open prices over several bars.

The core logic of the strategy is:

1. Calculate the major Leledec DEC indicator (maj) using parameters bar count (maj_qual) and lookback period (maj_len).

2. When the major Leledec DEC breaks above `maj_qual` consecutive bars, and the high of this bar exceeds the highest high over the past `maj_len` bars, it is considered a major Leledec DEC upside exhaustion, generating a long signal.

3. Calculate the minor Leledec DEC indicator (min) using parameters bar count (min_qual) and lookback period (min_len).

4. When the minor Leledec DEC breaks below `min_qual` consecutive bars, and the low of this bar is below the lowest low over the past `min_len` bars, it is considered a minor Leledec DEC downside exhaustion, generating a short signal.

According to the logic of the Leledec DEC indicator, exhaustion patterns represent potential extreme points and trend reversals, thus generating trading signals.

## Advantage Analysis

- The strategy has strong capabilities in trend identification. Leledec can effectively detect local extreme points.

- Flexibility in adapting to different timeframes and market conditions through parameter tuning.

- Can use major Leledec DEC alone or incorporate minor Leledec DEC for more comprehensive signals.

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

The Leledec DEC strategy catches trend reversals by identifying extreme patterns in the Leledec DEC indicator. It is an effective trend-following methodology. While advantageous in assessing trends, further optimization, additional signal validation, and proper risk management are needed for long-term profitability. Overall, the Leledec DEC strategy provides a valuable addition to a trader's toolkit.

[/trans]

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

``` pinescript
/*backtest
start: 2023-09-01 00:00:00
end: 2023-09-30 23:59:59
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Joy_Bangla

//@version=4
strategy("A Strategy for Leledec", shorttitle ="Leledec Strategy", overlay=true, commission_value=0.075, initial_capital=10000, default_qty_type = strategy.percent_of_equity, default_qty_value = 10)

maj = input(true, "Major Leledec Exhausion Bar ::  Show")
min=input(false, "Minor Leledec Exhausion Bar ::  Show")
leledcSrc = input(close, "Major Leledec Exhausion Bar ::  Source")
maj_qual = input(6, "Major Leledec Exhausion Bar ::  Bar count no")
maj_len = input(30
```