> Name

Trend-Following-Strategy-Based-on-Adaptive-Moving-Average

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/a818fb74de2803e068.png)
 [trans]
### Overview

This strategy employs the Kaufman Adaptive Moving Average (KAMA) indicator to design a trend-following trading system. It can track trends quickly when they form and filter out noise during choppy markets. At the same time, the system also integrates Parabolic SAR (PSAR) and Average True Range Trailing Stop as stop loss mechanisms with strong risk control capabilities.

### Strategy Logic

- The length of the KAMA indicator is dynamically adjusted based on recent market volatility. When price changes are greater than recent noise, the EMA window becomes shorter. When price changes are smaller than recent noise, the EMA window becomes longer. This allows KAMA to quickly track trends while filtering out noise during choppy markets.

- The system mainly judges the trend direction based on the fastest KAMA (KAMA 1). It goes long when KAMA 1 points up and goes short when KAMA 1 points down. To filter out false breaks, a KAMA filter is set. Trading signals are only generated when the change in KAMA 1 exceeds one standard deviation of recent fluctuations.

- For stop loss, the system provides three optional stop loss methods: KAMA reversal, PSAR reversal, and ATR trailing stop. Investors can choose one or a combination to use.

### Advantage Analysis

- The unique design of the KAMA indicator allows the system to quickly capture emerging trends, stop trading during choppy markets, effectively control trading frequency, and reduce unnecessary slippage and commission costs.

- The system has multiple built-in stop loss mechanisms. Investors can choose the appropriate stop loss scheme according to their personal risk preferences to effectively control single loss.

- The system is entirely based on indicators and stop loss lines, avoiding common mis-entry problems caused by shifting transactions.

- Multiple parameter settings and condition combinations provide great space for system customization. Users can optimize according to different products and frequencies.

### Risk Analysis

- The system does not consider systemic risks and cannot effectively control losses in extreme market conditions.

- The system parameters may need to be adjusted according to different products and frequencies, otherwise it will produce overly aggressive or overly conservative results.

- If relying solely on the KAMA indicator for stop loss, it is easy to get caught in whipsaws during choppy markets. This needs to be combined with PSAR or ATR trailing stop to solve.

### Optimization Directions

- Add trend filtering indicators such as ADX or implied volatility to avoid generating wrong signals during choppy and trend transition stages.

- Optimize and backtest parameters for individual products and fixed frequencies to improve stability. Optimization dimensions include KAMA parameter combinations, stop loss parameters, etc.

- Try machine learning models instead of parameter optimization. Train neural networks or decision tree models with lots of historical data to judge entry and exit timing and stop loss.

- Try migrating the strategy to other products such as cryptocurrencies. This may require adjusting parameters or adding other auxiliary indicators.

### Summary

This strategy integrates KAMA for trend judgment and multiple stop loss methods to effectively track trend directions and control risks. The uniqueness of the KAMA indicator allows the strategy to quickly determine the direction of emerging trends and avoid false breakout problems. Customizable and optimizable parameters provide users with great space for personalized adjustment. By optimizing parameters and integrating machine learning models for individual products and frequencies, the performance of the strategy can be further improved.

||

### Overview

This strategy employs the Kaufman Adaptive Moving Average (KAMA) indicator to design a trend-following trading system. It can track trends quickly when they form and filter out noise during choppy markets. At the same time, the system also integrates Parabolic SAR (PSAR) and Average True Range Trailing Stop as stop loss mechanisms with strong risk control capabilities.

### Strategy Logic

- The length of the KAMA indicator is dynamically adjusted based on recent market volatility. When price changes are greater than recent noise, the EMA window becomes shorter. When price changes are smaller than recent noise, the EMA window becomes longer. This allows KAMA to quickly track trends while filtering out noise during choppy markets.

- The system mainly judges the trend direction based on the fastest KAMA (KAMA 1). It goes long when KAMA 1 points up and goes short when KAMA 1 points down. To filter out false breaks, a KAMA filter is set. Trading signals are only generated when the change in KAMA 1 exceeds one standard deviation of recent fluctuations.

- For stop loss, the system provides three optional stop loss methods: KAMA reversal, PSAR reversal, and ATR trailing stop. Investors can choose one or a combination to use.

### Advantage Analysis

- The unique design of the KAMA indicator allows the system to quickly capture emerging trends, stop trading during choppy markets, effectively control trading frequency, and reduce unnecessary slippage and commission costs.

- The system has multiple built-in stop loss mechanisms. Investors can choose the appropriate stop loss scheme according to their personal risk preferences to effectively control single loss.

- The system is entirely based on indicators and stop loss lines, avoiding common mis-entry problems caused by shifting transactions.

- Multiple parameter settings and condition combinations provide great space for system customization. Users can optimize according to different products and frequencies.

### Risk Analysis

- The system does not consider systemic risks and cannot effectively control losses in extreme market conditions.

- The system parameters may need to be adjusted according to different products and frequencies, otherwise it will produce overly aggressive or overly conservative results.

- If relying solely on the KAMA indicator for stop loss, it is easy to get caught in whipsaws during choppy markets. This needs to be combined with PSAR or ATR trailing stop to solve.

### Optimization Directions

- Add trend filtering indicators such as ADX or implied volatility to avoid generating wrong signals during choppy and trend transition stages.

- Optimize and backtest parameters for individual products and fixed frequencies to improve stability. Optimization dimensions include KAMA parameter combinations, stop loss parameters, etc.

- Try machine learning models instead of parameter optimization. Train neural networks or decision tree models with lots of historical data to judge entry and exit timing and stop loss.

- Try migrating the strategy to other products such as cryptocurrencies. This may require adjusting parameters or adding other auxiliary indicators.

### Summary

This strategy integrates KAMA for trend judgment and multiple stop loss methods to effectively track trend directions and control risks. The uniqueness of the KAMA indicator allows the strategy to quickly determine the direction of emerging trends and avoid false breakout problems. Customizable and optimizable parameters provide users with great space for personalized adjustment. By optimizing parameters and integrating machine learning models for individual products and frequencies, the performance of the strategy can be further improved.

|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|true|KAMA 1 Stop Loss|
|v_input_3|false|ATR Trailing Stop Loss|
|v_input_4|false|PSAR Stop Loss|
|v_input_5|14|KAMA 1: Length|
|v_input_6|2|KAMA 1: Fast KAMA Length|
|v_input_7|20|KAMA 1: Slow KAMA Length|
|v_input_8|15|KAMA 2: Length 2|
|v_input_9|3|KAMA 2: Fast KAMA Length|
|v_input_10|22|KAMA 2: Slow KAMA Length|
|v_input_11|16|KAMA 3: Length 3|
|v_input_12|4|KAMA 3: Fast KAMA Length|
|v_input_13|24|KAMA 3: Slow KAMA Length|
|v_input_14|17|KAMA 4: Length|
|v_input_15|5|KAMA 4: Fast KAMA Length|
|v_input_16|26|KAMA 4: Slow KAMA Length|