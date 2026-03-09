> Name

Triple-Moving-Average-Crossover-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1b1ae79ba4e7a089fdb.png)
[trans]

### Overview

The triple moving average crossover strategy uses the crossovers of different time period moving averages as buy and sell signals, belonging to trend-following strategies. It employs three moving averages—short-term, medium-term, and long-term—to generate trading signals based on their crossovers.

### Strategy Logic

Firstly, the strategy calculates the short-term (default 7 days), medium-term (default 25 days), and long-term (default 99 days) moving averages. Then it generates trading signals according to the following rules:

1. When the short-term moving average crosses above the medium-term moving average, a buy signal is generated.

2. When the short-term moving average crosses below the medium-term moving average, a sell signal is generated.

3. When the short-term moving average crosses above the long-term moving average, a fast buy signal is generated.

4. When the short-term moving average crosses below the long-term moving average, a fast sell signal is generated.

The strategy believes that the short-term moving average crossing above the medium-term moving average indicates an uptrend, so a buy signal is generated. And the short-term moving average crossing below the medium-term moving average indicates a downtrend, so a sell signal is generated. Similarly, the crossover between the short-term moving average and long-term moving average also generates fast trading signals to capture longer-term trend changes.

### Advantage Analysis

- The strategy logic is simple and easy to understand and implement.
- Using multi-timeframe analysis can effectively capture changes in market trends.
- Parameters can be optimized by adjusting the MA periods.
- Visual crossover signals intuitively reflect trend changes.

### Risk Analysis

- Moving averages have lagging issues, which may miss trend reversal points.
- Too many false buy signals when the short-term moving average crosses above the long-term moving average during bull markets.
- Too many false sell signals when the short-term moving average crosses below the long-term moving average during bear markets.
- Fast trading signals may be too sensitive, increasing trading frequency and commissions.

Proper adjustments of MA periods or adding filter conditions can help optimize and reduce false signals. Shortening fast trading periods may also lower trading frequency.

### Optimization Directions

- Add filter conditions, such as generating signals only when meeting certain trading volumes or price change percentages.
- Combine with other indicators like MACD, KDJ to avoid erroneous trades during periods of no clear trend.
- Optimize MA period combinations to reduce false signals.
- Distinguish between bull and bear markets and optimize buy and sell parameters separately.
- Consider trading costs and adjust fast trading parameters to control frequency.

### Summary

The triple moving average crossover strategy is relatively simple, using the crossovers of different time frame moving averages to judge trend direction and generate trading signals. It is easy to implement with flexible parameter adjustments to capture trend changes. However, it also has issues such as MA lagging and excessive false signals. Methods like adding filters and optimizing parameter combinations can improve the strategy. This strategy suits traders interested in trend crossovers for optimization and application.

||

### Overview

The triple moving average crossover strategy uses the crossovers of different time period moving averages as trading signals, belonging to trend-following strategies. It employs three moving averages—short-term, medium-term, and long-term—to generate trading signals based on their crossovers.

### Strategy Logic

Firstly, the strategy calculates the short-term (default 7 days), medium-term (default 25 days), and long-term (default 99 days) moving averages. Then it generates trading signals according to the following rules:

1. When the short-term moving average crosses above the medium-term moving average, a buy signal is generated.

2. When the short-term moving average crosses below the medium-term moving average, a sell signal is generated.

3. When the short-term moving average crosses above the long-term moving average, a fast buy signal is generated.

4. When the short-term moving average crosses below the long-term moving average, a fast sell signal is generated.

The strategy believes that the short-term moving average crossing above the medium-term moving average indicates an uptrend, so a buy signal is generated. And the short-term moving average crossing below the medium-term moving average indicates a downtrend, so a sell signal is generated. Similarly, the crossover between the short-term moving average and long-term moving average also generates fast trading signals to capture longer-term trend changes.

### Advantage Analysis

- The strategy logic is simple and easy to understand and implement.
- Using multi-timeframe analysis can effectively capture changes in market trends.
- Parameters can be optimized by adjusting the MA periods.
- Visual crossover signals intuitively reflect trend changes.

### Risk Analysis

- Moving averages have lagging issues, which may miss trend reversal points.
- Too many false buy signals when the short-term moving average crosses above the long-term moving average during bull markets.
- Too many false sell signals when the short-term moving average crosses below the long-term moving average during bear markets.
- Fast trading signals may be too sensitive, increasing trading frequency and commissions.

Proper adjustments of MA periods or adding filter conditions can help optimize and reduce false signals. Shortening fast trading periods may also lower trading frequency.

### Optimization Directions

- Add filter conditions, such as generating signals only when meeting certain trading volumes or price change percentages.
- Combine with other indicators like MACD, KDJ to avoid erroneous trades during periods of no clear trend.
- Optimize MA period combinations to reduce false signals.
- Distinguish between bull and bear markets and optimize buy and sell parameters separately.
- Consider trading costs and adjust fast trading parameters to control frequency.

### Summary

The triple moving average crossover strategy is relatively simple, using the crossovers of different time frame moving averages to judge trend direction and generate trading signals. It is easy to implement with flexible parameter adjustments to capture trend changes. However, it also has issues such as MA lagging and excessive false signals. Methods like adding filters and optimizing parameter combinations can improve the strategy. This strategy suits traders interested in trend crossovers for optimization and application.

|Argument|Default|Description|
|----|----|----|
|v_input_1|7|Short-Term - Day|
|v_input_2|25|Medium-Term - Day|
|v_input_3|99|Long-Term - Day|
|v_input_4|2020|Backtest Start Date|

> Source (PineScript)

```pinescript
/*backtest
start: 2023-10-06 00:00:00
end: 2023-11-05 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © dadashkadir

//@version=4
strategy("Triple Moving Average Crossover Strategy", overlay=true, initial_capital=10000, commission_value=0.047, default_qty_type=strategy.percent_of_equity, default_qty_value=100, pyramiding=0, calc_on_order_fills=true)

kisa = input(title="Short-Term - Day", defval=7, minval=1)
orta = input(title="Medium-Term - Day", defval=25, minval=1)
uzun = input(title="Long-Term - Day", defval=99, minval=1)

sma7  = sma(close, kisa)
sma25 = sma(close, orta)
sma99  = sma(close, uzun)

alTrend  = plot(sma7, color=#2323F1, linewidth=2, title="Short-Term Moving Average", transp=0)
satTrend = plot(sma25, color=#FF0C00, linewidth=3, title="Medium-Term Moving Average", transp=0)
ort99    = plot(sma99, color=#DFB001, linewidth=3, title="Long-Term Moving Average", transp=0)

zamanaralik = input(2020, title="Backtest Start Date")

al  = crossover(sma7, sma25) and zamanaralik <= year
sat = crossover(sma25, sma7) and zamanaralik <= year

hizlial  = crossover(sma7, sma99) and zamanaralik <= year
hizlisat  = crossunder(sma7, sma99) and zamanaralik <= year
```