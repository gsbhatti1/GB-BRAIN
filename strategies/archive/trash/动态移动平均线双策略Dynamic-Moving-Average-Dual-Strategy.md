> Name

Dynamic-Moving-Average-Dual-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/12886e688e2451c3d7a.png)
[trans]

### Overview

This strategy utilizes the slope of the Moving Average (MA) and the slope of momentum indicators for trading decisions. It compares the MA slope and momentum slope with set thresholds, and generates trading signals when both slopes exceed the thresholds. The strategy also includes a low volatility filter that uses a different MA to generate signals when market volatility is low.

### Strategy Logic

The core of this strategy lies in comparing two slope curves. Firstly, it calculates the slope of the MA and momentum indicator. The slope reflects the rate of change and direction of the curve. Then, two thresholds are used, and when both the MA slope and the momentum slope exceed the corresponding thresholds, trading signals are generated.

For example, when both the MA slope and momentum slope exceed the upper line, a buy signal is generated; when both curves fall below the lower line, a sell signal is generated. This can filter out some false signals.

The low volatility filter uses a long-term MA to determine market volatility. When volatility is low, a MA with different parameters is used to generate trading signals to adapt to different market states.

### Advantage Analysis

This strategy has the following advantages:

1. The dual filter for setting up trading signals can filter out some noise and improve signal quality.
2. The low volatility filter allows the strategy to adapt to different market conditions with elasticity.
3. High customizability for different parameters can be optimized for different products.
4. It contains no repainting function to reduce the impact from curve fitting.

### Risk Analysis

This strategy also has some risks:

1. The dual filter may filter out some real signals and miss opportunities. This can be optimized by adjusting parameters.
2. The threshold determination of the low volatility filter needs careful testing. Improper settings may cause signal deviations.
3. Parameter settings for MA and momentum indicators need to be optimized for specific products, and universal parameters are hard to determine.
4. The no repainting function cannot completely avoid the backtest curve fitting problem, and real trading performance still needs verification.
5. High customizability increases the complexity of the parameter space and the difficulty of optimization.

### Optimization Directions

The strategy can be optimized in the following directions:

1. Test more combinations of MA and momentum indicators to find the best matching indicators.
2. Optimize the length parameters of MA and momentum indicators to balance lag and noise.
3. Optimize the parameters for calculating slope to find more stable indicator combinations.
4. Test different low volatility indicators and parameters to improve elasticity.
5. Test on different products and timeframes to find the best applicable scope.
6. Build parameter adaptive mechanisms to reduce manual optimization workload.

### Conclusion

This is a very flexible and customizable dual MA strategy. It references both price and momentum information for decision making, which can effectively filter out false signals. The low volatility filter also makes the strategy more elastic to adapt to market changes.

With improvements in parameter optimization and indicator selection, this strategy can become a viable choice for real-life trading. It provides a reference template for trading decisions using MA and momentum indicators.

|Argument|Default|Description|
|----|----|----|
|v_input_1|7|(?Moving Average)1=SMA, 2=EMA, 3=WMA, 4=HullMA, 5=VWMA, 6=RMA, 7=TEMA, 8=Tilson T3|
|v_input_2_close|0|MA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_3|5|Moving Average Length - LookBack Period|
|v_input_4|7|Tilson T3 Factor - *.10 - so 7 = .7 etc.|
|v_input_5|3|MA Slope Lookback|
|v_input_6|5|MA Slope Smoothing|
|v_input_7|3|(?Momentum Moving Average)1=RSI, 2=CCI, 3=RSI/ROC|
|v_input_8_close|0|Momentum Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_9|3|Momentum Length|
|v_input_10|8|Momentum Slope Lookback|
|v_input_11|7|Momentum Slope Smoothing|
|v_input_12|1|(?Time Resolution)Higher timeframe?|
|v_input_13|130|MA Slope multiplier for Alternate Resolutions (Make the waves of the blue line similar size as the orange line)|
|v_input_14|0.02|(?Buy and Sell Threshold)Buy when both slopes cross this line|
|v_input_15|-0.03|Sell when both slopes cross this line|
|v_input_16|28|(?Low Volatility Function)Big MA Length|
|v_input_17|10|Low Volatility Moving Average Length|
|v_input_18|0.05|Low Volatility Buy and Sell Threshold|
|v_input_19|2.5|Minimum volatility to trade|