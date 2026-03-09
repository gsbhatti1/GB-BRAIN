> Name

ATR-and-RSI-Based-Trend-Following-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

## Overview

This strategy designs a trading system with trend following functionality based on Average True Range (ATR) and Relative Strength Index (RSI). It can automatically identify the trend direction and has stop loss and take profit features.

## Strategy Logic

1. Calculate ATR and RSI. ATR reflects the average price volatility over a period. RSI reflects the power comparison between bulls and bears.

2. When ATR is greater than its moving average, it is considered a high volatility period suitable for trading.

3. When RSI is above the overbought line, go long. When RSI is below the oversold area, go short.

4. After going long, use the high point multiplied by a fixed ratio as the trailing stop loss price. After going short, use the low point multiplied by a fixed ratio as the trailing stop loss price.

5. Take profit by profit ratio.

## Advantage Analysis

1. Trailing stop loss can maximize stop loss orders to reduce losses.

2. RSI can effectively judge the power of bulls and bears to avoid repeatedly opening positions in range-bound markets.

3. As a volatility indicator, ATR can filter out range-bound markets and only trade in trending markets.

4. Take profit by profit ratio can lock in some profits.

## Risk Analysis

1. Both ATR and RSI are lagging indicators, which may lead to late entry timing. Parameters can be optimized to make the system more sensitive.

2. Fixed profit and loss ratio for stop loss and take profit is prone to over optimization, should be set prudently based on backtest results.

3. In large cycle range-bound markets, ATR may be greater than moving average for a long time, leading to over trading. Other filters can be added.

## Optimization Directions

1. Optimize parameters of ATR and RSI to make the system more sensitive.

2. Add MA and other indicators to determine trend direction, avoid wrongly entering range-bound markets.

3. Try dynamic stop loss and take profit ratios, instead of fixed settings.

4. Consider adding trading size control measures.

## Summary

This strategy integrates the advantages of ATR and RSI indicators and designs a simple and practical trend following trading system. Further improving system stability by parameter optimization and adding filters. Overall, this strategy has strong practical value for live trading.

||

## Overview

This strategy designs a trading system with trend following functionality based on Average True Range (ATR) and Relative Strength Index (RSI). It can automatically identify the trend direction and has stop loss and take profit features.

## Strategy Logic

1. Calculate ATR and RSI. ATR reflects the average price volatility over a period. RSI reflects the power comparison between bulls and bears.

2. When ATR is greater than its moving average, it is considered a high volatility period suitable for trading.

3. When RSI is above the overbought line, go long. When RSI is below the oversold area, go short.

4. After going long, use the high point multiplied by a fixed ratio as the trailing stop loss price. After going short, use the low point multiplied by a fixed ratio as the trailing stop loss price.

5. Take profit by profit ratio.

## Advantage Analysis

1. Trailing stop loss can maximize stop loss orders to reduce losses.

2. RSI can effectively judge the power of bulls and bears to avoid repeatedly opening positions in range-bound markets.

3. As a volatility indicator, ATR can filter out range-bound markets and only trade in trending markets.

4. Take profit by profit ratio can lock in some profits.

## Risk Analysis

1. Both ATR and RSI are lagging indicators, which may lead to late entry timing. Parameters can be optimized to make the system more sensitive.

2. Fixed profit and loss ratio for stop loss and take profit is prone to over optimization, should be set prudently based on backtest results.

3. In large cycle range-bound markets, ATR may be greater than moving average for a long time, leading to over trading. Other filters can be added.

## Optimization Directions

1. Optimize parameters of ATR and RSI to make the system more sensitive.

2. Add MA and other indicators to determine trend direction, avoid wrongly entering range-bound markets.

3. Try dynamic stop loss and take profit ratios, instead of fixed settings.

4. Consider adding trading size control measures.

## Summary

This strategy integrates the advantages of ATR and RSI indicators and designs a simple and practical trend following trading system. Further improving system stability by parameter optimization and adding filters. Overall, this strategy has strong practical value for live trading.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|26|atr_length|
|v_input_int_2|45|atr_ma_length|
|v_input_int_3|15|rsi_length|
|v_input_int_4|10|rsi_entry|
|v_input_float_1|0.3|atr_ma_norm_min|
|v_input_float_2|0.7|atr_ma_norm_max|
|v_input_float_3|1.5|trailing_percent|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-09-08 00:00:00
end: 2023-10-08 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// © liwei666
//@version=5
// # ========================================================================= #
// #                   |   Strategy  |
// # ========================================================================= #
strategy(
 title                = "ATR_RSI_Strategy v2[liwei666]",
 shorttitle           = "ATR_RSI_Strategy",
 overlay              =  true,
 max_lines_count                 =  500, 
 max_labels_count                =  500, 
 max_boxes_count                 =  500,
 max_bars_back = 5000,
 initial_capital = 10000,
 default_qty_type=strategy.percent_of_equity, 
 default_qty_value=50, commission_type=strategy.commission.percent, pyramiding=1, 
 commission_value=0.05
 )
// # ========================================================================= #
// #                   |   Strategy  |
// # ========================================================================= #

atr_length = input.int(26, "atr_length", minval = 6, maxval = 100, step=1)
atr_ma_length = input.int(45, "atr_ma_length", minval = 6, maxval = 100, step=1)
rsi_length = input.int(15, "rsi_length", minval = 6, maxval = 100, step=1)
rsi_entry = input.int(10, "rsi_entry", minval = 6, maxval = 100, step=1)
atr_ma_norm_min = input.float(0.3, "atr_ma_norm_min", minval = 0.1, maxval = 0.5, step=0.1)
atr_ma_norm_max = input.float(0.7, "atr_ma_norm_max", minval = 0.5, maxval = 1, step=0.1)
trailing_percent= input.float(1.5, "trailing_percent", minval = 0.1, maxval = 2, step=0.1)

var rsi_buy = 50 + rsi_entry
var rsi_sell = 50 - rsi_entry

sma_norm_h_45() => 
    source = high
    n = 45
    sma = ta.sma(source, n) 
    sma_norm = (sma - ta.lowest(sma, n)) / (ta.highest(sma,n) - ta.lowest(sma, n))
    sma_norm

atr_value = ta.atr(atr_length)
atr_ma = ta.sma(atr_value, atr_ma_length) 
rsi_value = ta.rsi(close, length = rsi_length) 
atr_ma_norm = atr_ma / close * 100
sma_norm = sma_norm_h_45()

var intra_trade_high = 0.0
var intra_trade_low = 0.0

if strategy.position_size == 0
    intra_trade_high := high
    intra_trade_low := low

    if atr_ma_norm >= atr_ma_norm_min and atr_ma_norm <= atr_ma_norm_max
        if atr_value > atr_ma
            if rsi_value > rsi_buy
                strategy.entry("B1", strategy.long, limit = 
```