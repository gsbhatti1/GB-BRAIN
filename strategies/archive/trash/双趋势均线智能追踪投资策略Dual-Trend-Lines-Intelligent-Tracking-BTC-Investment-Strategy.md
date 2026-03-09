> Name

Dual-Trend-Lines-Intelligent-Tracking-BTC-Investment-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/157bc32bf38e4509773.png)

[trans]

### Overview

This strategy is mainly used for the automated long-term investment in BTC. It uses the crossover of dual EMA and LSMA to determine the trend direction and uses the ATR indicator to calculate a dynamic stop loss to effectively track the BTC bullish trend.

### Strategy Logic

1. Use 25-period EMA and 100-period LSMA to form a dual moving average. Their crossover is used to determine the market trend. The EMA responds quickly to price changes while the LSMA filters out false breakouts.

2. When the fast EMA crosses above the slow LSMA, it is determined that the uptrend is still intact and long positions are taken. On the contrary, when the fast EMA crosses below the slow LSMA, it is determined that a downtrend has begun and existing positions are closed.

3. After taking long positions, the dynamic stop loss calculated using the ATR indicator keeps adjusting to effectively track the uptrend of BTC. Specifically, the initial point of the stop loss line is the entry price. After that, each adjustment will slide up by a fixed percentage of the ATR amplitude.

4. The stop loss line can effectively lock in the floating profit brought by the BTC uptrend, while preventing the stop loss point from getting too close to the latest price to avoid frequent stop loss. In addition, the strategy also sets two moving stop profits of different proportions to lock in more profits.

### Advantage Analysis

1. Using dual moving averages to determine the trend is more reliable and can effectively prevent false signals.

2. The ATR dynamic trailing stop loss can lock in most profits while avoiding frequent small stop losses.

3. No matter whether the bullish trend ends or not, as long as the moving average issues an exit signal, the position will be stopped out to control risks.

4. The strategy has a high degree of automation without manual intervention, making it suitable for long-term live trading.

### Risk Analysis

1. Still need to pay attention to sudden major news to avoid huge slippage losses.

2. Although the combination of dual moving averages can reduce false signals, it is still difficult to completely avoid them in range-bound markets.

3. Improper parameter settings of ATR can also affect the stop loss effect. Adjustments are needed based on different products.

4. Unreasonable moving average periods or failure to update them in time can lead to signal lag.

5. Ensure server stability to avoid abnormal crashes that interrupt automated trading.

### Optimization Directions

1. More indicators such as Bollinger Bands can be added to determine the trend. Machine learning models can also be used to predict prices.

2. The calculation method of the ATR dynamic stop loss can also be adjusted and optimized to make the stop loss smoother.

3. Trading volume based alert mechanisms and intraday rotation features can be added to guard against impacts from major news.

4. Parameters vary for different coins. More historical data can be used to train personalized parameters.

### Summary

Overall, this is a very practical automated BTC investment program. Using dual EMAs to determine the major trend is very reliable. With ATR trailing stop loss, it can achieve decent profits and the validity period can be very long. As parameters continue to be optimized, there is still much room for improvement in the performance of this strategy. It is well worth live trading verification.

[/trans]

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|v_input_1|0|What trades should be taken : : LONG|SHORT|BOTH|NONE|
|v_input_2|0|First Trend Line : : TEMA|LSMA|EMA|SMA|
|v_input_3|0|First Trend Line : : LSMA|TEMA|EMA|SMA|
|v_input_4|25|Length of the First Trend Line|
|v_input_5|100|Length of the Second Trend Line|
|v_input_6|15|Long Take Profit 1 %|
|v_input_7|20|Long Take Profit 1 Qty|
|v_input_8|30|Long Take Profit 2%|
|v_input_9|20|Long Take Profit 2 Qty|
|v_input_10|5|Stop Loss in %|
|v_input_11|3.5|SL Multiplier|
|v_input_12|8|ATR Period|
|v_input_13_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_14|2016|Backtest Start Year|
|v_input_15|true|Backtest Start Month|
|v_input_16|true|Backtest Start Day|
|v_input_17|9999|Backtest Stop Year|
|v_input_18|12|Backtest Stop Month|
|v_input_19|31|Backtest Stop Day|


> Source (PineScript)

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Wunderbit Trading

//@version=4
strategy("Automated Bitcoin (BTC) Investment Strategy", overlay=true, initial_capital=5000, pyramiding=0, currency="USD", default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent)
```