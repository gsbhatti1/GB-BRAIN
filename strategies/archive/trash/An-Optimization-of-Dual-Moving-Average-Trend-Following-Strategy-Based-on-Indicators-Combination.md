> Name

An-Optimization-of-Dual-Moving-Average-Trend-Following-Strategy-Based-on-Indicators-Combination

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/15961e9eefd6dacced0.png)
[trans]
### Overview
This strategy generates trading signals by calculating fast and slow moving average lines and combining Parabolic SAR indicator. It belongs to the trend following strategy. When the fast MA crosses over the slow MA, long position will be opened. When the fast MA crosses below the slow MA, short position will be opened. Parabolic SAR is used to filter fake breakouts.

### Strategy Principle  
1. Calculate fast and slow moving average lines. The parameters can be customized.
2. Compare the two MA lines to determine market trend. When the fast MA crosses over the slow MA, it indicates a bullish trend. When the fast MA crosses below the slow MA, it indicates a bearish trend.
3. Further confirmation is made by checking if the close price is above/below the fast MA. Only when the fast MA crosses over the slow MA and the close price is above the fast MA, a long signal is generated. Only when the fast MA crosses below the slow MA and the close price is below the fast MA, a short signal is generated.  
4. Parabolic SAR is used to filter fake signals. Only when all the three criteria are met, a final signal is generated.
5. Stop loss is set based on maximum tolerable loss. ATR indicator is used to calculate dynamic stop loss price.

### Advantages  
1. MA lines determine market trend and avoid excessive trading in range-bound market.  
2. Dual filters lower risk of fake breakout significantly.
3. Stop loss strategy effectively limits per trade loss.

### Risks  
1. Indicator strategies tend to generate false signals
2. No consideration of currency exposure risk
3. Potentially miss initial trend in opposite direction

The strategy can be optimized in below aspects:
1. Optimize MA parameters to fit specific product  
2. Add other indicators or models for signal filtering
3. Consider real-time hedging or auto currency conversion  

### Directions for Optimization
1. Optimize MA parameters to better capture trends
2. Increase model diversity to improve signal accuracy
3. Multi-timeframe verification to avoid being trapped
4. Enhance stop loss strategy to increase stability

### Conclusion
This is a typical dual moving average cross and indicators combination trend following strategy. By comparing fast and slow MA directions, market trend is determined. Various filter indicators are used to avoid false signals. At the same time, a stop loss function is implemented to control per trade loss. The advantage is that the strategy logic is simple and easy to understand and optimize. The disadvantage is that as a coarse trend tool, there is still room to improve signal accuracy, by introducing machine learning models for example.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_bool_1|true|(?Backtest Time Period)Filter Date Range of Backtest|
|v_input_1|timestamp(1 jan 2000)|Start Date|
|v_input_2|timestamp(1 Jul 2100)|End Date|
|v_input_bool_2|true|(?Long & Short Position)On/Off Long Postion|
|v_input_bool_3|true|On/Off Short Postion|
|v_input_string_1|0|(?Slow MA Inputs)Slow MA Type: SMA|EMA|WMA|HMA|RMA|SWMA|ALMA|VWMA|VWAP|
|v_input_int_1|160|Slow MA Length|
|v_input_3_close|0|Slow MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_string_2|0|(?Fast MA Inputs)Fast MA Type: SMA|EMA|WMA|HMA|RMA|SWMA|ALMA|VWMA|VWAP|
|v_input_int_2|40|Fast MA Length|
|v_input_4_close|0|Fast MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_bool_4|true|(?Parabolic SAR Inputs)Use Parabolic Sar?|
|v_input_bool_5|false|Display Parabolic Sar?|
|v_input_float_1|0.02|Start|
|v_input_float_2|0.02|Increment|
|v_input_float_3|0.2|Maximum|
|v_input_int_3|14|(?Risk Management Inputs)ATR Length|
|v_input_float_4|2|Long Position - Stop Loss - ATR Multiplier|
|v_input_float_5|2|Short Position - Stop Loss - ATR Multiplier|
|v_input_float_6|2|% of Equity at Risk|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 00:00:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © sosacur01

//@version=5
strategy(title="2 MA | Trend Following", overlay=true, pyramiding=1, commission_type=strategy.commission.percent, commission_value=0.2, initial_capital=10000)

//==========================================


//BACKTEST RANGE
useDateFilter = input.bool(true, title="Filter Date Range of Backtest",
     group="Backtest Time Period")
backtestStartDate = input(timestamp("1 jan 2000"), 
     title="Start Date", group="Backtest Time Period",
     tooltip="This start date is in the time zone of the exchange " + 
     "where the chart's instrument trades. It doesn't use the time " + 
     "zone of the chart or of your computer.")
backtestEndDate = input(timestamp("1 jul 2100"), 
     title="End Date", group="Backtest Time Period",
     tooltip="This end date is in the time zone of the exchange " + 
     "where the chart's instrument trades. It doesn't use the time " + 
     "zone of the chart or of your computer.")
```