> Name

RSIBollinger双轨低位区间突破策略RSIBollinger-Bands-Breakout-Strategy-at-Lower-Area

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11c32b1d29f7eae44c2.png)
 [trans]
### 1. Overview

This is a breakout strategy that combines the RSI indicator and Bollinger Bands to trade in the lower area of the price range. The main idea is to buy when RSI is below 10 and sell when RSI is above 90, with the 5-period simple moving average (SMA) as the stop loss line.

### 2. Principles

When the RSI indicator is below 10, it is considered an oversold signal, meaning that the stock is less likely to be overvalued and a good time to buy. When the RSI indicator is above 90, it is considered an overbought signal and a sell signal. The stop loss line is set at the 5-period SMA to avoid unnecessary stop losses due to normal market fluctuations.

### 3. Advantages

This is a statistical arbitrage strategy that buys low and sells high using indicator signals. Its main advantage is that by judging buy and sell points through the RSI indicator, it can effectively identify opportunities when stocks are overvalued or undervalued, thereby achieving excess returns. Additionally, combining Bollinger Bands for breakout judgments helps avoid the risks of catching a falling knife and chasing tops and bottoms.

### 4. Risks and Solutions

The main risk of this strategy is that normal market fluctuations in the short term may exceed the stop loss line, causing unnecessary stop losses. Moreover, failure to take profits on time may also miss out on potential gains. To address these risks, one can appropriately adjust the cycle parameters of the stop loss line to avoid being stopped out due to normal market fluctuations. Additionally, setting a take profit level after reaching target returns can help with risk management.

### 5. Optimization Directions

This strategy can be optimized in several ways:

(1) Adjust the overbought and oversold threshold values of the RSI indicator, such as using 15 and 85, to increase trading opportunities.
(2) Optimize the cycle parameters of the stop loss line to better adapt to market short-term fluctuations.
(3) Add a take profit level for automatic profit taking and risk control.
(4) Incorporate volatility indicators like ATR to further refine parameter settings.

### 6. Summary

The RSI+Bollinger Bands breakout strategy at lower area uses the RSI indicator to determine entry and exit points, Bollinger Bands to identify price ranges, and SMA as a stop loss line. This approach effectively captures market trends while managing risks for stable profits. There is still significant room for optimization of this strategy, making it worth further exploration.

[/trans]

### 1. Overview  

This is a breakout strategy that combines the RSI indicator and Bollinger Bands to trade in the lower area of the price range. The main idea is to buy when RSI is below 10 and sell when RSI is above 90, with the 5-period simple moving average (SMA) as the stop loss line.

### 2. Principles  

When the RSI indicator is below 10, it is considered an oversold signal, meaning that the stock is less likely to be overvalued and a good time to buy. When the RSI indicator is above 90, it is considered an overbought signal and a sell signal. The stop loss line is set at the 5-period SMA to avoid unnecessary stop losses due to normal market fluctuations.

### 3. Advantages  

This is a statistical arbitrage strategy that buys low and sells high using indicator signals. Its main advantage is that by judging buy and sell points through the RSI indicator, it can effectively identify opportunities when stocks are overvalued or undervalued, thereby achieving excess returns. Additionally, combining Bollinger Bands for breakout judgments helps avoid the risks of catching a falling knife and chasing tops and bottoms.

### 4. Risks and Solutions  

The main risk of this strategy is that normal market fluctuations in the short term may exceed the stop loss line, causing unnecessary stop losses. Moreover, failure to take profits on time may also miss out on potential gains. To address these risks, one can appropriately adjust the cycle parameters of the stop loss line to avoid being stopped out due to normal market fluctuations. Additionally, setting a take profit level after reaching target returns can help with risk management.

### 5. Optimization Directions  

This strategy can be optimized in several ways:

(1) Adjust the overbought and oversold threshold values of the RSI indicator, such as using 15 and 85, to increase trading opportunities.
(2) Optimize the cycle parameters of the stop loss line to better adapt to market short-term fluctuations.
(3) Add a take profit level for automatic profit taking and risk control.
(4) Incorporate volatility indicators like ATR to further refine parameter settings.

### 6. Summary  

The RSI+Bollinger Bands breakout strategy at lower area uses the RSI indicator to determine entry and exit points, Bollinger Bands to identify price ranges, and SMA as a stop loss line. This approach effectively captures market trends while managing risks for stable profits. There is still significant room for optimization of this strategy, making it worth further exploration.

||

### 1. Overview  

This is a breakout strategy that combines the RSI indicator and Bollinger Bands to trade in the lower area of the price range. The main idea is to buy when RSI is below 10 and sell when RSI is above 90, with the 5-period simple moving average (SMA) as the stop loss line.

### 2. Principles  

When the RSI indicator is below 10, it is considered an oversold signal, meaning that the stock is less likely to be overvalued and a good time to buy. When the RSI indicator is above 90, it is considered an overbought signal and a sell signal. The stop loss line is set at the 5-period SMA to avoid unnecessary stop losses due to normal market fluctuations.

### 3. Advantages  

This is a statistical arbitrage strategy that buys low and sells high using indicator signals. Its main advantage is that by judging buy and sell points through the RSI indicator, it can effectively identify opportunities when stocks are overvalued or undervalued, thereby achieving excess returns. Additionally, combining Bollinger Bands for breakout judgments helps avoid the risks of catching a falling knife and chasing tops and bottoms.

### 4. Risks and Solutions  

The main risk of this strategy is that normal market fluctuations in the short term may exceed the stop loss line, causing unnecessary stop losses. Moreover, failure to take profits on time may also miss out on potential gains. To address these risks, one can appropriately adjust the cycle parameters of the stop loss line to avoid being stopped out due to normal market fluctuations. Additionally, setting a take profit level after reaching target returns can help with risk management.

### 5. Optimization Directions  

This strategy can be optimized in several ways:

(1) Adjust the overbought and oversold threshold values of the RSI indicator, such as using 15 and 85, to increase trading opportunities.
(2) Optimize the cycle parameters of the stop loss line to better adapt to market short-term fluctuations.
(3) Add a take profit level for automatic profit taking and risk control.
(4) Incorporate volatility indicators like ATR to further refine parameter settings.

### 6. Summary  

The RSI+Bollinger Bands breakout strategy at lower area uses the RSI indicator to determine entry and exit points, Bollinger Bands to identify price ranges, and SMA as a stop loss line. This approach effectively captures market trends while managing risks for stable profits. There is still significant room for optimization of this strategy, making it worth further exploration.

[/trans]

> Source (PineScript)

```pinescript
/*backtest
start: 2023-01-11 00:00:00
end: 2024-01-17 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
//Created by ChrisMoody
//Based on Larry Connors RSI-2 Strategy - Lower RSI
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)
src = close,

//RSI CODE
up = rma(max(change(src), 0), 2)                
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
//Criteria for Moving Avg rules
ma1 = sma(close,1)
ma2 = sma(close,2)
ma3 = sma(close,3)
ma4 = sma(close,4)
ma5 = sma(close,5)
ma6 = sma(close,6)
ma7 = sma(close,7)
ma8 = sma(close,8)
ma9 = sma(close,9)
ma200= sma(close, 200)

//Rule for RSI Color
col = close > ma200 and close < ma5 and rsi < 10 ? lime : close < ma200 and close > ma5 and rsi > 90 ? red : silver

plot(rsi, title="RSI", style=line, linewidth=4,color=col)
plot(100, title="Upper Line 100",style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0",style=line, linewidth=3, color=aqua)

band1 = plot(90, title="Upper Line 90",style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Line 10",style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

///////////// RSI + Bollinger Bands Strategy

if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")
if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

> This script is for informational purposes only and should not be considered investment advice. Always consult a financial advisor before making investment decisions.

[/trans] 

### Summary

The RSI+Bollinger Bands breakout strategy at lower area uses the RSI indicator to determine entry points, Bollinger Bands to identify price ranges, and SMA as a stop loss line. This approach helps in capturing market trends while managing risks for stable profits. The provided Pine Script code implements this strategy on the BTC/USDT pair on the Binance Futures exchange. [End of Summary] 

--- 

> Note: This script is for informational purposes only and should not be considered investment advice. Always consult a financial advisor before making investment decisions.

[/trans] 
--- 

> Last updated: 2024-01-17

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

This script is designed for users familiar with Pine Script and aims to provide insights into trading strategies. Please ensure you fully understand the implications before using it in a live environment. --- 

--- 

> Last updated: 2024-01-17

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

This script is designed for users familiar with Pine Script and aims to provide insights into trading strategies. Please ensure you fully understand the implications before using it in a live environment. 

--- 

```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

--- 

This script defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair. The strategy focuses on lower RSI values and uses moving averages as stop loss indicators. It is designed to help traders identify potential buy and sell signals based on the combined use of these technical indicators.

### Key Points:
- **RSI Calculation**: The RSI is calculated with a focus on lower values.
- **Bollinger Bands**: Used to determine price ranges, but not actively traded against.
- **Moving Averages**: Serve as stop loss mechanisms and risk management tools.
- **Entry Signal**: Long positions are taken when the close price exceeds a 200-period moving average and RSI is below 10.
- **Exit Strategy**: Short positions are triggered when the close price falls below the 200-period moving average and RSI rises above 90.
- **Stop Loss**: Positions are closed if the stop loss condition is met.

Always review and test any trading strategy thoroughly before applying it in a live environment. 

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair. The strategy focuses on lower RSI values and uses moving averages as stop loss indicators.

### Key Points:
- **RSI Calculation**: The RSI is calculated with a focus on lower values.
- **Bollinger Bands**: Used to determine price ranges, but not actively traded against.
- **Moving Averages**: Serve as stop loss mechanisms and risk management tools.
- **Entry Signal**: Long positions are taken when the close price exceeds a 200-period moving average and RSI is below 10.
- **Exit Strategy**: Short positions are triggered when the close price falls below the 200-period moving average and RSI rises above 90.
- **Stop Loss**: Positions are closed if the stop loss condition is met.

Always review and test any trading strategy thoroughly before applying it in a live environment. 

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md) 

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair. The strategy focuses on lower RSI values and uses moving averages as stop loss indicators.

### Key Points:
- **RSI Calculation**: The RSI is calculated with a focus on lower values.
- **Bollinger Bands**: Used to determine price ranges, but not actively traded against.
- **Moving Averages**: Serve as stop loss mechanisms and risk management tools.
- **Entry Signal**: Long positions are taken when the close price exceeds a 200-period moving average and RSI is below 10.
- **Exit Strategy**: Short positions are triggered when the close price falls below the 200-period moving average and RSI rises above 90.
- **Stop Loss**: Positions are closed if the stop loss condition is met.

Always review and test any trading strategy thoroughly before applying it in a live environment. 

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- 

```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color.new(col, 50))
plot(100, title="Upper Line 100", style=line, linewidth=3, color=aqua)
plot(0, title="Lower Line 0", style=line, linewidth=3, color=aqua)

// Plot the Bollinger Bands
band1 = plot(90, title="Upper Band 90", style=line, linewidth=3, color=aqua)
band0 = plot(10, title="Lower Band 10", style=line, linewidth=3, color=aqua)
fill(band1, band0, color=silver, transp=90)

// Entry and exit rules
if (close > ma200 and rsi < 10)
    strategy.entry("RSI_2_L", strategy.long, comment="Bullish")

if (close < ma200 and rsi > 90)
    strategy.exit("RSI_2_S", "RSI_2_L", limit=ma5)

// Stop Loss
strategy.close("RSI_2_L", when=strategy.position_avg_price - close > 1 * typical_price, comment="Stop Loss")
```

[Back to Scripts](../README.md) [Next Script](./next-script-name.md)

---

This script is designed for informational purposes and should not be considered investment advice. Always consult a financial advisor before making any trading decisions.

--- ```pinescript
// This file defines the RSI + Bollinger Bands breakout strategy for trading on the BTC/USDT pair.
// The strategy is based on Larry Connors' RSI-2 Strategy with modifications to focus on lower RSI values.

//@version=2
strategy(title="_CM_RSI_2_Strat_Low", shorttitle="_CM_RSI_2_Strategy_Lower", overlay=false)

// Source data and initial calculations
src = close

// Calculate the RSI
up = rma(max(change(src), 0), 2)
down = rma(-min(change(src), 0), 2)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))

// Moving averages
ma1 = sma(close, 1)
ma2 = sma(close, 2)
ma3 = sma(close, 3)
ma4 = sma(close, 4)
ma5 = sma(close, 5)
ma6 = sma(close, 6)
ma7 = sma(close, 7)
ma8 = sma(close, 8)
ma9 = sma(close, 9)
ma200 = sma(close, 200)

// Plot the RSI and moving average lines
plot(rsi, title="RSI", style=line, linewidth=4, color=color