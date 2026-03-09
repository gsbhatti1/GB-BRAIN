> Name

Quantitative-Moving-Average-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

### Overview

This strategy calculates two volume-weighted moving averages as fast and slow lines. It determines the trend direction based on the difference between the two lines and takes long or short positions accordingly. The strategy is simple and effective in tracking market trends.

### Strategy Logic

1. Calculate fast and slow lines using volume-weighted moving averages based on user-defined fast and slow periods.
2. Calculate the difference between the fast and slow lines.
3. Determine trend direction. A crossover of the fast line above the slow line indicates an upward trend, while a crossover below indicates a downward trend.
4. Issue long/short signals. Enter long positions when the fast line crosses above the slow line. Enter short positions when the fast line crosses below the slow line.
5. Set stop loss based on user-defined fixed percentage or dynamic ATR.
6. Exit rules. Close position if stop loss is hit or a reverse signal occurs.

### Advantages

1. Uses quantitative indicators to identify trends, avoiding false breakouts.
2. Fast and slow line combination filters out market noise and avoids overtrading.
3. Stop loss effectively controls downside risk.
4. Simple and easy-to-understand logic.
5. Customizable parameters for different products and timeframes.

### Risks

1. Improper parameter setting may cause overtrading or missed trends.
2. Fixed stop loss may be too rigid for changing market conditions.
3. Changes in volume and price relationships may impact effectiveness.

- Risk 1 can be mitigated through parameter optimization.
- Risk 2 can be addressed via dynamic ATR stop loss.
- Risk 3 needs monitoring of volume changes.

### Enhancement Opportunities

1. Test different fast and slow line parameter combinations.
2. Try other volume-price indicators like OBV, William's %R, etc.
3. Add volatility-based stops.
4. Evaluate combining with other indicators.
5. Test effectiveness across different trading instruments.

### Conclusion

This strategy uses fast and slow quantified moving averages to track trends with simple logic. Parameters can be optimized, and stop losses control risk. Further evaluations on combining indicators may improve effectiveness.

||

### Overview 

This strategy calculates two volume-weighted moving averages as fast and slow lines. It determines the trend direction based on the difference between the two lines and takes long or short positions accordingly. The strategy is simple and effective in tracking market trends.

### Strategy Logic

1. Calculate fast and slow lines using volume-weighted moving averages based on user-defined fast and slow periods.
2. Calculate the difference between the fast and slow lines.
3. Determine trend direction. Crossover of the fast line above the slow line indicates an upward trend, while a crossover below indicates a downward trend.
4. Issue long/short signals. Enter long positions when the fast line crosses above the slow line. Enter short positions when the fast line crosses below the slow line.
5. Set stop loss based on user-defined fixed percentage or dynamic ATR.
6. Exit rules. Close position if stop loss is hit or a reverse signal occurs.

### Advantages

1. Uses quantitative indicators to identify trends and avoid false breakouts.
2. Fast and slow line combination filters out market noise and avoids overtrading.
3. Stop loss effectively controls downside risk.
4. Simple and easy-to-understand logic.
5. Customizable parameters for different products and timeframes.

### Risks

1. Improper parameter setting may cause overtrading or missed trends.
2. Fixed stop loss may be too rigid for changing market conditions.
3. Changes in volume and price relationships may impact effectiveness.

- Risk 1 can be mitigated through parameter optimization.
- Risk 2 can be addressed via dynamic ATR stop loss.
- Risk 3 needs monitoring of volume changes.

### Enhancement Opportunities

1. Test different fast and slow line parameter combinations.
2. Try other volume-price indicators like OBV, William's %R, etc.
3. Add volatility-based stops.
4. Evaluate combining with other indicators.
5. Test effectiveness across different trading instruments.

### Conclusion

This strategy uses fast and slow quantified moving averages to track trends with simple logic. Parameters can be optimized, and stop losses control risk. Further evaluations on combining indicators may improve effectiveness.

---

### Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|false|════════ Test Period ═══════|
|v_input_2|2017|Backtest Start Year|
|v_input_3|true|Backtest Start Month|
|v_input_4|true|Backtest Start Day|
|v_input_5|2019|Backtest Stop Year|
|v_input_6|12|Backtest Stop Month|
|v_input_7|31|Backtest Stop Day|
|v_input_8|false|════════ EVMA ═══════|
|v_input_9|5|Fast Sum Length|
|v_input_10|11|Slow Sum Length|
|v_input_11|false|════════ Stop Loss ═══════|
|v_input_12|0|Stop Loss Type: Fixed|ATR Derived|
|v_input_13|9|Fixed Stop Loss %|
|v_input_14|20|ATR Stop Period|
|v_input_15|1.5|ATR Stop Multiplier|
|v_input_16|false|══════ Longs or Shorts ═════|
|v_input_17|true|Use Longs|
|v_input_18|true|Use Shorts|


### Source (PineScript)

```pinescript
/*backtest
start: 2023-08-18 00:00:00
end: 2023-09-17 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("EVWMA 6HR", overlay=false, precision=2, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.075)
// Credit to QuantNomad for the main idea behind this code
/////////////// Time Frame ///////////////
_1 = input(false,  "════════ Test Period ═══════")
testStartYear = input(2017, "Backtest Start Year") 
testStartMonth = input(1, "Backtest Start Month")
testStartDay = input(1, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear,testStartMonth,testStartDay, 0, 0)

testStopYear = input(2019, "Backtest Stop Year")
testStopMonth = input(12, "Backtest Stop Month")
testStopDay = input(31, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear,testStopMonth,testStopDay, 0, 0)

testPeriod() => true

///////////// EVWMA /////////////
_2 = input(false,  "════════ EVMA ═══════")

fast_sum_length = input(5, title = "Fast Sum Length",  type = input.integer)
slow_sum_length = input(11, title = "Slow Sum Length",  type = input.integer)

fast_vol_period = sum(volume, fast_sum_length)
slow_vol_period = sum(volume, slow_sum_length)

fast_evwma = 0.0
fast_evwma := ((fast_vol_period - volume) * nz(fast_evwma[1], close) + volume * close) / (fast_vol_period)
slow_evwma = 0.0
slow_evwma := ((slow_vol_period - volume) * nz(slow_evwma[1], close) + volume * close) / (slow_vol_period)

diff = fast_evwma - slow_evwma

///////////////  Strategy  /////////////// 
long = fast_evwma > slow_evwma 
short = fast_evwma < slow_evwma 

last_long = 0.0
last_short = 0.0
last_long := long ? time : nz(last_long[1])
last_short := short ? time : nz(last_short[1])

long_signal = crossover(last_long, last_short)
short_signal = crossover(last_short, last_long)

last_open_long_signal = 0.0
last_open_short_signal = 0.0
last_open_long_signal := long_signal ?