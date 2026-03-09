> Name

Enhanced-Bollinger-Bands-RSI-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/16ce40fe21e910b0e60.png)
[trans]
####Overview
This strategy combines two technical indicators, Bollinger Bands and Relative Strength Index (RSI). It uses Bollinger Bands to capture the price fluctuation range and RSI to confirm the overbought and oversold status of the price, which serves as the basis for judging trading signals. When the price breaks through the lower band of Bollinger Bands and RSI is below 30, a long signal is generated; when the price breaks through the upper band and RSI is above 70, a short signal is generated.

####Strategy Principle
1. Calculate the upper, middle, and lower bands of Bollinger Bands. The middle band is the simple moving average of the closing price, and the upper and lower bands are the middle band plus or minus a certain standard deviation.
2. Calculate the RSI indicator. RSI is used to measure the magnitude of price increases and decreases over a period of time to determine the overbought and oversold status of the price.
3. Generate trading signals. When the closing price breaks through the lower band of Bollinger Bands and RSI is below 30, a long signal is generated; when the closing price breaks through the upper band and RSI is above 70, a short signal is generated.
4. Execute trades. Set limit orders based on trading signals, short when breaking through the upper band of Bollinger Bands, and long when breaking through the lower band. At the same time, cancel the previous pending orders in the opposite direction.

####Advantage Analysis
1. Bollinger Bands can well quantify the fluctuation range of prices, and the RSI indicator can well quantify the overbought and oversold degree of prices. The combination of the two can predict the timing of price reversals relatively reliably.
2. The setting of limit orders can avoid incorrect opening or chasing up and killing down, and the setting of stop-loss orders can control risks.
3. The setting of canceling previous pending orders in the opposite direction can prevent the strategy from trading too frequently.

####Risk Analysis
1. There may be a large drawdown in trending markets. Bollinger Bands and RSI indicators are more suitable for judging the reversal points of oscillating markets and have a weaker ability to grasp trending markets.
2. Parameter settings have a greater impact on the strategy performance. The parameter settings of Bollinger Bands will affect the frequency of price breakthroughs, and the parameter settings of the RSI indicator will affect the sensitivity of overbought and oversold signals, which need to be optimized according to different market characteristics and trading cycles.

####Optimization Direction
1. Consider adding trend judgment indicators, such as MACD, etc., and combine Bollinger Bands and RSI indicators with trend indicators for adaptive adjustment of long and short positions.
2. Consider using dynamic parameter optimization methods to adaptively adjust the parameters of Bollinger Bands and RSI indicators based on characteristics such as price volatility and trend strength, improving the adaptability of the strategy.
3. Add money management and position management modules to the strategy to dynamically adjust the amount of funds and leverage for each transaction based on factors such as account funds, risk preferences, and historical drawdowns.

####Summary
By combining Bollinger Bands and RSI indicators, this strategy can effectively capture the overbought and oversold status of prices and use it as a trading signal. However, the strategy may perform poorly in trending markets, and the strategy performance is more sensitive to parameter settings. In the future, we can consider introducing trend judgment, dynamic parameter optimization, and fund management modules to further improve the robustness and profitability of the strategy.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|20|Length|
|v_input_float_1|2.0|Multiplier|
|v_input_int_2|14|RSI Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-03-01 00:00:00
end: 2024-03-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Enhanced Bollinger Bands RSI Trading Strategy", overlay=true)
source = close
length = input.int(20, minval=1, title="Length")
mult = input.float(2.0, minval=0.001, maxval=50, title="Multiplier")
basis = ta.sma(source, length)
dev = mult * ta.stdev(source, length)
upper = basis + dev
lower = basis - dev
plot(basis, title="Base Line", color=color.blue)
plot(upper, title="Upper Band", color=color.green)
plot(lower, title="Lower Band", color=color.red)

// RSI indicator addition
rsiLength = input.int(14, title="RSI Length")
rsiSource = source
rsi = ta.rsi(rsiSource, rsiLength)
plot(rsi, title="Relative Strength Index (RSI)", color=color.orange)
```