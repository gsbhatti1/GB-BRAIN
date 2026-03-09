> Name

Breakout-Strategy-with-Confirmation-on-Multiple-Time-Frames

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/6314600bfe7988c227.png)

[trans]

### Overview

This strategy combines breakout signals from the 4-hour and daily timeframes, and verifies candlestick patterns before issuing trading signals, thus implementing a more reliable breakout trading strategy.

### Strategy Logic

The dual confirmation breakout strategy combines breakout signals from both short-term and long-term timeframes to identify more efficient breakouts. Specifically, this strategy calculates moving averages on both the 4-hour and daily timeframes. A buying signal is generated when the short-term MA crosses above the long-term MA, while a selling signal is triggered by the opposite crossover. Additionally, before issuing trading signals, the current candlestick's pattern is verified to avoid opening positions during nasty price actions.

Through mechanisms of dual confirmation and candlestick filtering, this strategy can effectively avoid risks such as long liquidation or short traps, thereby improving the quality of trading signals.

### Advantage Analysis

1. Dual timeframe breakout improves signal quality. The combination of short-term and long-term timeframes enables signals to track short-term trends while still considering long-term trends.
2. Candlestick pattern verification avoids false signals. Validating the candlestick pattern before issuing a signal can filter out fake or aberrant breakouts, preventing losses.
3. Automated optimization provides flexibility. Breakout parameters and timeframe parameters in this strategy are customizable, allowing users to select the optimal parameter combination based on different trading products and market conditions.

### Risk Analysis

1. The dual breakout strategy has relatively weak trend chasing capability against extreme price spikes. When drastic price actions occur simultaneously on both short and long timeframes, this strategy may miss the optimal entry point.
2. The candlestick verification mechanism may miss some opportunities. In extreme market conditions, candlesticks often exhibit distortions, making the verification mechanism more conservative and potentially missing certain chances.
3. Improper parameter settings can also generate false signals. Users need to select appropriate parameters for the dual breakout and candlestick components based on the specific product, otherwise, the strategy's performance may be compromised.

To address these risks, methods such as parameter tuning and setting stop loss/profit limits can be adopted for improvement and optimization.

### Optimization Directions

1. Add volatility index to secondary verify breakout signals. For example, breakout signals issued when Bollinger Bands are squeezed tend to have higher quality.
2. Add stop loss/profit modules. Proper configuration helps lock in profits and cut losses proactively.
3. Optimize the dual breakout parameters. The parameters can be adjusted according to the characteristics of the product such as intraday and daily volatility.
4. Optimize K-line verification parameters. Different combinations of cycle and parameters for K-line verification can produce more stable results.

### Conclusion

The dual confirmation breakout strategy strikes an efficient balance between capital efficiency and signal quality by combining dual timeframes and candlestick pattern verification mechanisms, making it a recommended short-term breakout strategy. Users can adjust relevant parameters according to their own needs for better results.

||

### Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|1440|Timeframe: 4-hour or daily|
|v_input_2|370|Simulation Timeframe: 4-hour or daily|
|v_input_3|20|Bollinger Bands Length|
|v_input_4|2|Bollinger Bands Multiplication Factor|
|v_input_5|20|Keltner Channels Length|
|v_input_6|1.5|Keltner Channels Multiplication Factor|
|v_input_7|true|Use TrueRange (for Keltner Channels)|
|v_input_8|HullMA|Fast MA Type: SMA, EMA, WMA, VWMA, SMMA, DEMA, TEMA, HullMA, TMA, ZEMA (case sensitive)|
|v_input_9|20|Moving Average Length|
|v_input_10_close|0|Moving average Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_11|false|hidefractals|
|v_input_12|false|hidelevels|
|v_input_13|false|Use Fractal S/R Cross Patterns|
|v_input_14|true|Use Dark Cloud Cover Patterns|
|v_input_15|true|Use Piecing Line Patterns|
|v_input_16|true|Use Engulfing Candle Patterns|
|v_input_17|true|Use Harami Candle Patterns|
|v_input_18|true|Use Defined PinBar Patterns|
|v_input_19|66|Directional PBars, % of Range of Candle the Long Wick Has To Be|
|v_input_20|false|Use CM Price Action Reversal Pin Bars|
|v_input_21|false|Use CM Price Action Shaved Bars|
|v_input_22|false|Use CM Price Action Outside Bars|
|v_input_23|false|Use CM Price Action Inside Bars|
|v_input_24|72|CM Reversal PBars, % of Range of Candle the Long Wick Has To Be