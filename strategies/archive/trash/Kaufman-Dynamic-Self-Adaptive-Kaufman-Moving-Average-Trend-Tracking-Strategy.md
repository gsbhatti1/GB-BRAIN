> Name

Dynamic-Self-Adaptive-Kaufman-Moving-Average-Trend-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/101c228d67d7f7cd717.png)
[trans]
### Overview

This strategy is designed based on the Kaufman Adaptive Moving Average (KAMA) to dynamically adjust trading positions and automatically track market trends. The main functions of the strategy include:

1. Dynamically calculate trading step size (in pips) and adapt to market volatility
2. Generate buy and sell signals based on the direction of KAMA  
3. Set a stop loss distance after signal is triggered, and adjust it accordingly as price moves
4. Optional confirmation of bar close to filter fake signals  

Through the application of these functions, the strategy tries to obtain additional profits from trends while controlling risks.

### Strategy Logic   

The strategy works based on the Kaufman Adaptive Moving Average indicator. KAMA calculates the ratio of price momentum to volatility to dynamically adjust the weight and smoothness of the moving average, allowing it to respond faster to price changes. 

When KAMA crosses above the downside stop loss line, it indicates a trend reversal and triggers a buy signal. When KAMA crosses below the upside stop loss line, it suggests a trend reversal and triggers a sell signal. After entering a position, the strategy calculates a dynamic stop loss distance based on ATR and sets a stop loss line. As KAMA moves in a favorable direction, the stop loss line also adjusts accordingly, moving to a more favorable position to lock in more profits.  

In this way, the strategy can track the trend, gradually move the stop loss line until it is triggered or a reverse signal is triggered to close the position.

### Advantages

Compared with traditional moving average strategies, this strategy has the following advantages:

1. KAMA has high sensitivity and can capture price trends faster;  
2. Dynamic stop loss distance locks more profits as it adjusts with the trend;
3. Optional bar close confirmation filters fake signals and reduces unnecessary entries.   

In general, the strategy is responsive, controllable, and a typical trend tracking system.

### Risks  

The strategy also carries some risks:  

1. Trend reversal risk. KAMA can adapt flexibly to price fluctuations but may not respond timely enough to sudden trend reversals.
2. Overly aggressive stop loss. If the dynamic stop loss distance is set too wide, it may be too aggressive and fail to lock profits in time.   
3. Fake signal risk. Using bar close confirmation helps reduce fake signals but cannot eliminate them completely.  

To manage these risks, methods like optimizing the stop loss distance and setting a maximum stop loss percentage can be used. Combining other indicators for confirmation also avoids mistaken trades.

### Optimization Directions   

Possible directions to optimize the strategy include:  

1. Optimize KAMA parameters: adjust moving average lengths, fine-tune smoothness;  
2. Optimize dynamic stop loss: test optimum stop loss distances and step sizes based on different products; 
3. Add filtering indicators: incorporate other trend indicators to confirm trading signals and improve reliability.  

For example, MACD can be added as an auxiliary confirmation indicator, requiring MACD Dif to be positive and expanding alongside KAMA's golden cross. This can filter out some fake signals and avoid unnecessary repeated entries.

### Conclusion   

The overall operation of this strategy is smooth. By using a dynamic stop loss to track trends and maximize trend profits, coupled with the adaptiveness of the KAMA indicator to swiftly respond to rapid market changes, this strategy can become an efficient trend tracking system after some optimization, suitable for medium- to long-term trading.

||

### Overview

This strategy is designed based on the Kaufman Adaptive Moving Average (KAMA) to dynamically adjust trading positions and automatically track market trends. The main functions of the strategy include:

1. Dynamically calculate trading step size (in pips) and adapt to market volatility
2. Generate buy and sell signals based on the direction of KAMA  
3. Set a stop loss distance after signal is triggered, and adjust it accordingly as price moves
4. Optional confirmation of bar close to filter fake signals  

Through the application of these functions, the strategy tries to obtain additional profits from trends while controlling risks.

### Strategy Logic   

The strategy works based on the Kaufman Adaptive Moving Average indicator. KAMA calculates the ratio of price momentum to volatility to dynamically adjust the weight and smoothness of the moving average, allowing it to respond faster to price changes. 

When KAMA crosses above the downside stop loss line, it indicates a trend reversal and triggers a buy signal. When KAMA crosses below the upside stop loss line, it suggests a trend reversal and triggers a sell signal. After entering a position, the strategy calculates a dynamic stop loss distance based on ATR and sets a stop loss line. As KAMA moves in a favorable direction, the stop loss line also adjusts accordingly, moving to a more favorable position to lock in more profits.

In this way, the strategy can track the trend, gradually move the stop loss line until it is triggered or a reverse signal is triggered to close the position.

### Advantages

Compared with traditional moving average strategies, this strategy has the following advantages:

1. KAMA has high sensitivity and can capture price trends faster;  
2. Dynamic stop loss distance locks more profits as it adjusts with the trend;
3. Optional bar close confirmation filters fake signals and reduces unnecessary entries.   

In general, the strategy is responsive, controllable, and a typical trend tracking system.

### Risks  

The strategy also carries some risks:  

1. Trend reversal risk. KAMA can adapt flexibly to price fluctuations but may not respond timely enough to sudden trend reversals.
2. Overly aggressive stop loss. If the dynamic stop loss distance is set too wide, it may be too aggressive and fail to lock profits in time.   
3. Fake signal risk. Using bar close confirmation helps reduce fake signals but cannot eliminate them completely.

To manage these risks, methods like optimizing the stop loss distance and setting a maximum stop loss percentage can be used. Combining other indicators for confirmation also avoids mistaken trades.

### Optimization Directions   

Possible directions to optimize the strategy include:  

1. Optimize KAMA parameters: adjust moving average lengths, fine-tune smoothness;  
2. Optimize dynamic stop loss: test optimum stop loss distances and step sizes based on different products; 
3. Add filtering indicators: incorporate other trend indicators to confirm trading signals and improve reliability.

For example, MACD can be added as an auxiliary confirmation indicator, requiring MACD Dif to be positive and expanding alongside KAMA's golden cross. This can filter out some fake signals and avoid unnecessary repeated entries.

### Conclusion   

The overall operation of this strategy is smooth. By using a dynamic stop loss to track trends and maximize trend profits, coupled with the adaptiveness of the KAMA indicator to swiftly respond to rapid market changes, this strategy can become an efficient trend tracking system after some optimization, suitable for medium- to long-term trading.

||

### Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_string_1|Buy Message|Buy Alert Message|
|v_input_string_2|Sell Message|Sell Alert Message|
|v_input_string_3|Buy Exit|Buy Exit Alert Message|
|v_input_string_4|Sell Exit|Sell Exit Alert Message|
|v_input_timeframe_1||Timeframe|
|v_input_1|14|Length|
|v_input_2|2|Fast EMA Length|
|v_input_3|30|Slow EMA Length|
|v_input_4_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_5|true|Highlight ?|
|v_input_6|true|Await Bar Confirmation ?|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-26 00:00:00
end: 2024-02-25 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("THMA - Bharath Vc Improved", overlay=true, process_orders_on_close=true)

// Function to calculate pips with higher precision
```