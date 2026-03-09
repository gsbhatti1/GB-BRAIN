> Name

Momentum-Breakthrough-Moving-Average-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16ef216bbf3c1dbbd54.png)
 [trans]

### Overview

This strategy is a trend-following approach that combines momentum and moving average indicators. It uses an exponential moving average (EMA) as the primary tool for trend determination, issuing buy and sell signals based on significant trading volume. The strategy is suitable for medium to long-term positions to track major market trends.

### Strategy Principles  

1. Use a 34-period EMA as the main tool for trend judgment. When the price crosses above the EMA, it generates a bullish signal; when it crosses below, it generates a bearish signal.

2. Compare the 21-day moving average of volume with 1.5 times the recent average. If the current volume is greater than 1.5 times the average, it is considered high volume.

3. Buy signals are only issued when the price crosses the EMA upward and the volume is high. Sell signals are only issued when the price crosses the EMA downward and the volume is high.  

4. After opening a position, set stop loss and take profit ratios, which can be customized.

By comprehensively considering factors such as trends, momentum, and risk control, this strategy is relatively comprehensive and stable.

### Advantage Analysis   

1. Using EMA to determine the main trend direction of the market can effectively track medium and long-term trends.

2. Combining with high trading volume filtering helps avoid being misled by false breakouts.  

3. Setting stop loss and take profit ratios can effectively control the risk of single trades.

4. Adopting a medium to long-term holding strategy is not affected by high-frequency market noise and ensures steady profits.

### Risks and Solutions

1. There is a higher probability of being misled by frequent false breakouts. The solution is to add volume verification.

2. Medium to long-term holdings increase capital utilization. The solution is to appropriately control the position size.

3. Moving average trading strategies may lag, missing short-term opportunities. The solution is to integrate other short-term signals.

4. Significant fluctuations in volatile markets can lead to large losses. The solution is to set an appropriate stop loss level.

### Optimization Directions  

1. Test different EMA cycle parameters to find the optimal parameters.

2. Test the impact of different stop loss and take profit ratio parameters on strategy returns and risk resistance.  

3. Try combining other indicators such as MACD and KDJ to determine short-term opportunities.

4. Optimize capital management strategies, such as position control and dynamic stop-loss methods.

### Summary  

Overall, this is a stable medium-to-long-term holding strategy. It can effectively track major market trends while using volume indicators to filter out misleading signals. Appropriate stop loss and take profit measures are taken to control the risk of single trades. This strategy can be described as a "steady and light" trend trading approach. With proper optimization, it is expected to achieve an even more ideal rate of return.

|| 

### Overview

This strategy is a trend-following approach that combines momentum and moving average indicators. It uses an exponential moving average (EMA) as the primary tool for trend determination, issuing buy and sell signals based on significant trading volume. The strategy is suitable for medium to long-term positions to track major market trends.

### Strategy Principles  

1. Use a 34-period EMA as the main tool for trend judgment. When the price crosses above the EMA, it generates a bullish signal; when it crosses below, it generates a bearish signal.

2. Compare the 21-day moving average of volume with 1.5 times the recent average. If the current volume is greater than 1.5 times the average, it is considered high volume.

3. Buy signals are only issued when the price crosses the EMA upward and the volume is high. Sell signals are only issued when the price crosses the EMA downward and the volume is high.  

4. After opening a position, set stop loss and take profit ratios, which can be customized.

By comprehensively considering factors such as trends, momentum, and risk control, this strategy is relatively comprehensive and stable.

### Advantage Analysis   

1. Using EMA to determine the main trend direction of the market can effectively track medium and long-term trends.

2. Combining with high trading volume filtering helps avoid being misled by false breakouts.  

3. Setting stop loss and take profit ratios can effectively control the risk of single trades.

4. Adopting a medium to long-term holding strategy is not affected by high-frequency market noise and ensures steady profits.

### Risks and Solutions

1. There is a higher probability of being misled by frequent false breakouts. The solution is to add volume verification.

2. Medium to long-term holdings increase capital utilization. The solution is to appropriately control the position size.

3. Moving average trading strategies may lag, missing short-term opportunities. The solution is to integrate other short-term signals.

4. Significant fluctuations in volatile markets can lead to large losses. The solution is to set an appropriate stop loss level.

### Optimization Directions  

1. Test different EMA cycle parameters to find the optimal parameters.

2. Test the impact of different stop loss and take profit ratio parameters on strategy returns and risk resistance.  

3. Try combining other indicators such as MACD and KDJ to determine short-term opportunities.

4. Optimize capital management strategies, such as position control and dynamic stop-loss methods.

### Summary  

Overall, this is a stable medium-to-long-term holding strategy. It can effectively track major market trends while using volume indicators to filter out misleading signals. Appropriate stop loss and take profit measures are taken to control the risk of single trades. This strategy can be described as a "steady and light" trend trading approach. With proper optimization, it is expected to achieve an even more ideal rate of return.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|(?Cài đặt thời gian)Ngày bắt đầu|
|v_input_2|true|Tháng bắt đầu|
|v_input_3|2023|Năm bắt đầu|
|v_input_4|31|Đến ngày|
|v_input_5|12|Đến tháng|
|v_input_6|2033|Đến năm|
|v_input_int_1|34|(?Cài đặt EMA)EMA 34|
|v_input_7|21|(?Cài thiết Volume)Đường Trung Bình Vol|
|v_input_8|1.5|Mức trung bình|
|v_input_float_1|true|(?Cài đặt TP & SL %)Stop Loss %|
|v_input_float_2|2|Take Profit %|

``` pinescript
/*backtest
start: 2023-12-10 00:00:00
end: 2023-12-17 00:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © TradingSignalHub

//@version=5
strategy("Momentum-Breakthrough-Moving-Average-Trading-Strategy", overlay=true)

//date setting
fromDay = input.int(1, title="Ngày bắt đầu")
fromMonth = input.int(1, title="Tháng bắt đầu")
fromYear = input.int(2023, title="Năm bắt đầu")

toDay = input.int(31, title="Đến ngày")
toMonth = input.int(12, title="Đến tháng")
toYear = input.int(2033, title="Đến năm")

startDate = timestamp(fromYear, fromMonth, fromDay, 00, 00)
finishDate = timestamp(toYear, toMonth, toDay, 00, 00)
time_cond() =>
    time >= startDate and time <= finishDate ? true : false

//snr setting
price = close
ema34     = input.int(34, minval=2, title="EMA 34", group="Cài đặt EMA")
pacC        = ta.ema(close, ema34)
pacL        = ta.ema(low, ema34)
pacH        = ta.ema(high, ema34)
L = plot(pacL, color=color.rgb(3, 139, 251), linewidth=2, title="Lower EMA")
plotshape(series=time_cond() and pacC > pacL, location=location.belowbar, color=color.green, style=shape.labelup, text="BUY", title="Buy Signal")
```