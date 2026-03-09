> Name

Quantitative Trading Strategy Based on Price Crossover with SMA

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f67bea4bd7ce1bce53.png)
[trans]

## Overview

This strategy is named "Quantitative Trading Strategy Based on Price Crossover with SMA". It mainly generates trading signals by calculating SMAs of different periods and tracking price crossover with SMAs. When the price breaks above the SMA, a buy signal is triggered; when the price breaks below the SMA, a sell signal is generated.

## Strategy Logic

The core logic of this strategy is to track the price crossover with a 21-day simple moving average (SMA). Additionally, it calculates 50-day and 200-day SMAs to help determine the general trend.

Specifically, the strategy requests close prices within a given date range and then calculates different SMAs based on input periods. If the price breaks above the 21-day SMA, it sets a buy signal. If the price breaks below the 21-day SMA, it sets a sell signal.

Along with calculating SMAs and determining crossovers, the strategy tracks current position as well. It enters position when a buy signal triggers, and closes position when a sell signal triggers. This way, it realizes an automated trading system based on SMA crossover.

## Advantage Analysis

The biggest advantage of this strategy is its simplicity and ease of understanding and implementation. SMA is a commonly used technical indicator, and SMA crossovers are one of the most common trading signals. These type of indicator-based strategies can be easily applied to different stocks and time ranges for automated trading.

Another advantage is that this strategy can be optimized by adjusting SMA parameters. For example, we can test different combinations of SMA periods to find the optimal ones for specific stocks. Additionally, the strategy can be improved by adding other indicators for confirmation and optimization.

## Risks and Solutions

The biggest risk of this strategy lies in indicator-based strategies generating excessive false signals. For instance, during range-bound periods, price may frequently crossover SMA, leading to unnecessary trading signals.

Common solutions include setting stop loss, tuning parameters, or adding filter conditions. For example, we can set a maximum loss ratio to limit risks; adjust SMA periods to find more stable parameter combinations; or use other indicators to filter some trading signals.

## Optimization Directions

This strategy can be optimized in the following ways:

1. Test and select optimal SMA parameter combinations by backtesting different SMA lengths to find the best periods.
2. Add other indicators for filterSignal confirmation, such as RSI, MACD, etc., to help filter false signals.
3. Incorporate stop loss logic. Set a maximum tolerable loss or trailing stop to better control risks.
4. Optimize entry timing by considering entering around major breakouts rather than strictly following SMA crossovers.
5. Test composite strategies. Combine with other strategy types like trend following.

## Conclusion

This strategy realizes automated trading using simple SMA crossover signals. The pros are being easy to understand and implement, but the cons include excessive signals that can lead to whipsaws. We can improve it by parameter tuning, adding filters, stop loss, etc. This strategy provides a basic framework for us. We can enrich it by incorporating more components.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|2022|Start Year|
|v_input_int_2|2022|End Year|
|v_input_int_3|true|Start Month|
|v_input_int_4|12|End Month|
|v_input_int_5|21|SMA Length|
|v_input_int_6|50|50 SMA Length|
|v_input_int_7|200|200 SMA Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-02-15 00:00:00
end: 2024-02-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Price Cross Above/Below SMA Strategy", shorttitle="Tressy Strat", overlay=true)

// Define start and end year inputs
start_year = input.int(2022, title="Start Year")
end_year = input.int(2022, title="End Year")

// Define start and end month inputs
start_month = input.int(1, title="Start Month", minval=1, maxval=12)
end_month = input.int(12, title="End Month", minval=1, maxval=12)

// Define SMA length inputs
sma_length = input.int(21, title="SMA Length")
sma_length_50 = input.int(50, title="50 SMA Length")
sma_length_200 = input.int(200, title="200 SMA Length")

// Filter data within the specified date range
filter_condition = true
filtered_close = request.security(syminfo.tickerid, "D", close[0], lookahead=barmerge.lookahead_on)

// Define SMAs using the input lengths
sma = ta.sma(filtered_close, sma_length)
sma_50 = ta.sma(filtered_close, sma_length_50)
sm