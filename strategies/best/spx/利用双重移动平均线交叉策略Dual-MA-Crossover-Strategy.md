> Name

Dual-MA-Crossover-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ed411263242bbf3084.png)
[trans]

### Overview

This is a simple quantitative strategy that uses double moving average crossover as buy and sell signals. It uses two MA lines with different periods. When the short period MA crosses over the long period MA from the bottom, a buy signal is generated. When the short period MA crosses below the long period MA, a sell signal is generated.

### Strategy Principle

The strategy calculates the 8-period EMA and 72-period EMA of the close price and plots them on the chart. When 8EMA crosses over 72EMA, a buy signal is generated. When 8EMA crosses below 72EMA, a sell signal is generated.

The basic assumption of the strategy is: the short period MA represents recent price trends and momentum, while the long period MA represents long term trends. When the short MA crosses over the long MA, it indicates the short term trend is strengthening, driving prices to break through the long term MA, so we can buy. When the short MA crosses below the long MA, it indicates the short term upward trend has ended, the long term support is broken, so we should consider selling.

The strategy also uses the William %R indicator to determine overbought and oversold areas, and the MACD indicator to determine price momentum direction for reference. In addition, some auxiliary indicators such as Dema and Pivots are set in the strategy to help analyze trends.

### Advantage Analysis

The biggest advantage of the dual MA crossover strategy is that it is simple and easy to understand and implement. It can generate trading signals simply based on the crossover of two MAs, without complex models and parameter optimization.

Another advantage is that MA crossover strategies perform well in trending markets. When stock prices show obvious upward or downward trends, MA crossover strategies can capture the big trends and generate good returns.

### Risk Analysis

The dual MA crossover strategy also has some risks to note. First, in range-bound choppy markets, MA line crossovers occur frequently, which can easily generate false signals and chained losses. Second, MA crossover signals are often lagging, and cannot respond timely to the impact of sudden events. Finally, parameter settings such as MA period lengths need experience to adjust and determine.

Risks can be reduced by combining other indicators to confirm signals, optimizing MA parameters, or operating in obvious trending markets. In addition, setting stop loss, profit taking, position sizing etc. is also very important.

### Optimization Directions

This simple dual MA strategy can be optimized in the following aspects:

1. Test different combinations of MA period parameters to find the optimal parameters;
2. Add other indicators for signal filtering, such as MACD, KDJ etc. to make the strategy more stable;
3. Build a dynamic exit mechanism to track the best stop loss and take profit levels, rather than just using fixed values;
4. Adopt adaptive MA periods according to market conditions to optimize parameters;
5. Incorporate advanced machine learning and deep learning models for prediction to improve signal accuracy.

### Conclusion

As a simple dual MA crossover strategy, although it has some lagging and false signal issues, it is easy to understand and implement. With some optimization and modifications, it can still be a basic and practical quantitative trading strategy.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|190|Return Candels ?|
|v_input_2|false|══════ Pivots ══════|
|v_input_3|4|leftBars|
|v_input_4|4|rightBars|
|v_input_5|false|══════ William R% Mod ══════|
|v_input_6|-7|OverBought Area|
|v_input_7|-93|OverSold Area|
|v_input_8|17|length_William|
|v_input_9|false|═════ Macd ══════════|
|v_input_10|12|Fast Length|
|v_input_11|26|Slow Length|
|v_input_12_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_13|9|Signal Smoothing|
|v_input_14|false|═════ Tsi ══════════|
|v_input_15|72|Long Length|
|v_input_16|17|Short Length|
|v_input_17|17|Signal Length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-18 00:00:00
end: 2023-12-24 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © DalmarSantos
//@version=4
//Entry and Exit points to TRADE ==> Pontos de Entrada e Saida de TRADE
//Functions in use ==> Funções em uso
//(1) DEMA - Double Exponential Moving Average 08/17/34/72 ==> Média Móvel Exponencial Dupla
//(2) ema() - Exponential Moving Averge 72/ochl4 ==> Média Móvel Exponencial
//(3) plot()
//(4) barcolor()
//(5) cross()
//(6) pivot
```