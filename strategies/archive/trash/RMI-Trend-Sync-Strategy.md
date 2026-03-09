> Name

RMI-Trend-Sync-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/147d03e3135524eb14f.png)

[trans]

## Overview
The RMI Trend Sync strategy effectively combines the strengths of the Relative Momentum Index (RMI) and the Super Trend indicator to realize the integration of momentum analysis and trend judgment. By concurrently monitoring price change trends and market momentum levels, the strategy determines market trends from a more comprehensive perspective.

## Strategy Principles  
### Relative Momentum Index (RMI)
RMI is an enhanced version of the Relative Strength Index (RSI). It incorporates more features of price changes such as directionality and magnitude to more precisely gauge market momentum.  

### RMI Calculation Method
The RMI calculation method is: first calculate the average gain and average loss over a certain period. Unlike RSI, RMI uses the change between the current closing price and the previous closing price, rather than simple positive and negative growth. Then divide the average gain by the average loss and normalize the value to fit within a 0-100 scale.

### Momentum Judgment 
This strategy uses the mean value of RMI and MFI to compare with preset positive momentum and negative momentum thresholds to determine the current market momentum level for entry and exit decisions.  

### Super Trend Indicator
The Super Trend indicator is calculated based on a higher timeframe, which can provide judgments on major trends. It dynamically adjusts parameters based on the true volatility ATR to effectively identify trend reversals.   
This strategy also incorporates the Volume Weighted Moving Average (VWMA) to further enhance its capability to detect important trend shifts.

### Trading Direction Selection 
This strategy allows choosing long, short or two-way trading. This flexibility enables traders to adapt to their market views and risk appetite.

## Advantage Analysis
### Combining Momentum and Trend Analysis 
Compared with strategies relying solely on momentum or trend indicators, this strategy realizes more accurate market trend identification through integrating the strengths of RMI and Super Trend.

### Multi-Timeframe Analysis 
The application of RMI and Super Trend in different timeframes leads to a more appropriate grasp of both short-term and long-term trends.  

### Real-time Stop Loss
The real-time stop loss mechanism based on the Super Trend can effectively limit per trade loss.  

### Flexible Trading Direction  
The choice among long, short or two-way trading allows this strategy to adapt to different market environments.

## Risk Analysis
### Difficult Parameter Optimization 
The optimization for parameters like RMI and Super Trend is quite complex. Inappropriate settings may undermine strategy performance.
 
### Stop Loss too Tight  
Being overly sensitive to small fluctuations may result in excessive stop loss triggers.

Solution: Appropriately loosen the stop loss range or adopt other volatility-based stop loss methods.

## Optimization Directions
### Cross Asset Adaptiveness  
Expanding applicable assets and identifying parameter optimization directions for different assets, to enable broader replication across more markets.

### Dynamic Stop Loss
Incorporate dynamic stop loss mechanisms to better track current swing waves and reduce excessive stop loss caused by minor retracements.   

### Additional Filter Conditions
Add judgments from more indicators as filter conditions to avoid entering positions without clear signals.

## Conclusion  
Through the ingenious combination of RMI and Super Trend, this strategy realizes accurate market condition judgments. It also excels in risk control. With in-depth optimization, it is believed that its performance across more assets and timeframes will become increasingly remarkable.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_string_1|0|Select Trading Direction: Both|Short|Long|
|v_input_int_1|21|(?RMI Settings)RMI Length|
|v_input_int_2|70|Positive Momentum Threshold|
|v_input_int_3|30|Negative Momentum Threshold|
|v_input_int_4|30|(?Momentum Settings)Band Length|
|v_input_int_5|20|RWMA Length|
|v_input_int_6|10|(?Super Trend Settings)Super Trend Length|
|v_input_timeframe_1|480|Higher Time Frame|
|v_input_float_1|3.5|Super Trend Factor|
|v_input_string_2|0|MA Source: WMA|EMA|SMA|RMA|VWMA|
|v_input_bool_1|true|(?Visual Settings)Display Range MA|
|v_input_color_1|#00bcd4|Bullish Color|
|v_input_color_2|#ff5252|Bearish Color|

> Source (PineScript)

```pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","cur