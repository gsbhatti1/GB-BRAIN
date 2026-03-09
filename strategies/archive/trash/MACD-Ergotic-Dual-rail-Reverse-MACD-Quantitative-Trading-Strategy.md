> Name

Dual-Rail Reverse MACD Quantitative Trading Strategy Ergotic-Dual-rail-Reverse-MACD-Quantitative-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1093f37488bfd69f2a2.png)
[trans]

### Overview
This strategy is a dual-rail reverse MACD quantitative trading strategy. It draws on the technical indicators described by William Blau in his book "Momentum, Direction and Divergence" and expands upon them. The strategy also has backtesting capabilities and can incorporate additional features like alerts, filters, trailing stop loss, etc.

### Principles  
The core indicator of this strategy is MACD. It calculates the fast moving average EMA(r) and slow moving average EMA(slowMALen), then computes their difference xmacd. It also calculates the EMA(signalLength) of xmacd to get xMA_MACD. A long signal triggers when xmacd crosses above xMA_MACD, and a short signal triggers on a cross below. The key aspect of this strategy is the reverse trading signals, i.e., the relationship between xmacd and xMA_MACD is opposite to that of the conventional MACD indicator, which is also where the name "Reverse MACD" comes from.

In addition, the strategy incorporates trend filters. When a long signal fires, if the bullish trend filter is configured, it will check if the price is increasing. Similarly, the short signal checks for a downward price trend. RSI and MFI indicators can also be used to filter out signals. A stop loss mechanism is included to prevent losses beyond a threshold.

### Advantage Analysis
The biggest advantage of this strategy is the powerful backtesting capabilities. You can choose different trading instruments, set the backtest timeframe, and optimize the strategy parameters based on specific instrument data. Compared to a simple MACD strategy, it incorporates trend and overbought/oversold analysis to filter out some identical signals. The dual-rail reverse MACD is different from the traditional MACD, allowing it to capitalize on some opportunities that the traditional MACD may miss.

### Risk Analysis 
The primary risk of this strategy comes from the reverse trading logic. While reverse signals can capture some opportunities missed by traditional signals, it also means forfeiting some conventional MACD entry points, necessitating careful assessment. Moreover, the MACD itself is prone to generating false bullish signals. The strategy may result in excessive trades and increased costs during choppy, directionless markets.

To mitigate risks, parameters can be optimized - tuning the moving average lengths; combining trends and indicator filters avoids signals in choppy markets; raising stop loss distances ensures capped losses on individual trades.

### Optimization Directions
The strategy can be improved in several aspects:
1. Adjust fast and slow rail parameters, optimize moving average lengths, backtest to find optimal parameter sets for specific instruments  
2. Add or tune trend filters, judge from backtest results whether it improves return  
3. Test different stop loss mechanisms, fixed or trailing, to determine the better performer
4. Try combining other indicators like KD, Bollinger Bands to set additional filter conditions and ensure signal quality

### Summary
The dual-rail reverse MACD quantitative strategy builds upon the classic MACD indicator with extensions and improvements. With flexible parameter configurations, abundant filter choices, and powerful backtesting functionality, it can be tuned to suit different trading instruments. Hence it is an intriguing and promising quantitative trading strategy worthy of further exploration.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|0|strategyType: Long Only|Long & Short|Short Only|
|v_input_3|7|From Month|
|v_input_4|true|From Day|
|v_input_5|2018|From Year|
|v_input_6|12|To Month|
|v_input_7|true|To Day|
|v_input_8|2030|To Year|
|v_input_9|144|R (32,55,89,100,144,200)|
|v_input_10|6|slowMALen|
|v_input_11|6|signalLength|
|v_input_12|false|Trade reverse (long/short switch)|
|v_input_13|true|Long only if price has increased|
|v_input_14|false|Short only if price has decreased|
|v_input_15|2|trending_price_length|
|v_input_16|false|trending_price_with_ema|
|v_input_17|3|trending_price_ema|
|v_input_18|14|rsi_length|
|v_input_19|14|RSI Sell Cutoff (Sell only if >= #)|
|v_input_20|82|RSI Buy Cutoff (Buy only if <= #)|
|v_input_21|false|Long only if RSI has increased|
|v_input_22|2|trending_rsi_length|
|v_input_23|14|mfi_length|
|v_input_24|14|mfi_lower|
|v_input_25|82|mfi_upper|
|v_input_26|false|Long only if MFI has increased|
|v_input_27|2|trending_mfi_length|
|v_input_28_hlc3|0|TSL source: hlc3|high|low|open|hl2|close|hlcc4|