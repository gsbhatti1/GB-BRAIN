<!-- AUTO-TRANSLATE FAILED: the JSON object must be str, bytes or bytearray, not NoneType -->


> Name

RSIBollinger双轨低位区间突破策略RSIBollinger-Bands-Breakout-Strategy-at-Lower-Area

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/11c32b1d29f7eae44c2.png)
 [trans]
### 1. Overview  

This is a breakout strategy that combines the RSI indicator and Bollinger Bands. The main idea is to buy when RSI is below 10 and sell when RSI is above 90, with the 5-period simple moving average (SMA) as the stop loss line.

### 2. Principles  

When RSI is below 10, it is considered an oversold signal, indicating that the stock is less likely to be overvalued, making it a good time to buy. When RSI is above 90, it is considered an overbought signal and a sell signal. The stop loss line is set at the 5-period SMA to prevent unnecessary stop losses due to normal market fluctuations in the short term.

### 3. Advantages  

This is a statistical arbitrage strategy that buys low and sells high based on indicator signals. Its main advantage is effectively capturing the timing of stock overvaluation and undervaluation through RSI, achieving excess returns. At the same time, by combining Bollinger Bands for breakout judgments, it avoids risks such as catching a falling knife and chasing tops and bottoms.

### 4. Risks and Solutions  

The primary risk of this strategy is that normal market fluctuations in the short term might exceed the stop loss line, causing unnecessary stop losses. Additionally, failure to take profits in time could result in missed opportunities for gains. Solutions include appropriately adjusting the cycle parameters of the stop loss line to prevent normal fluctuations from triggering a stop loss and setting up a take profit line to proactively lock in profits upon reaching target returns.

### 5. Optimization Directions  

This strategy can be optimized through the following aspects:

(1) Adjusting the overbought and oversold thresholds of the RSI indicator, such as changing them to 15 and 85, to capture more trading opportunities.
(2) Optimizing the cycle parameters of the stop loss line to better adapt to short-term market fluctuations.
(3) Adding a take profit line for automatic profit-taking and risk management.
(4) Incorporating volatility indicators like ATR to further optimize parameters.

### 6. Summary  

The RSI + Bollinger Bands breakout strategy at lower area uses RSI to determine entry and exit points, Bollinger Bands to identify the trading range, and a 5-period SMA as the stop loss line. This approach effectively captures market trends while controlling risks to achieve stable profits. There is significant room for optimization of this strategy, making it worthy of further research.

[/trans]

---

### 1. Overview  

This is a breakout strategy that combines the RSI indicator and Bollinger Bands. The main idea is to buy when RSI is below 10 and sell when RSI is above 90, with the 5-period SMA as the stop loss line.  

### 2. Principles  

When RSI is below 10, it is considered an oversold signal, indicating that the stock is less likely to be overvalued, making it a good time to buy. When RSI is above 90, it is considered an overbought signal and a sell signal. The stop loss line is set at the 5-period simple moving average to prevent unnecessary stop losses due to normal market fluctuations in the short term.   

### 3. Advantages  

This is a statistical arbitrage strategy that buys low and sells high based on indicator signals. Its main advantage is effectively capturing the timing of stock overvaluation and undervaluation through RSI, achieving excess returns. At the same time, by combining Bollinger Bands for breakout judgments, it avoids risks such as catching a falling knife and chasing tops and bottoms.

### 4. Risks and Solutions  

The primary risk of this strategy is that normal market fluctuations in the short term might exceed the stop loss line, causing unnecessary stop losses. Additionally, failure to take profits in time could result in missed opportunities for gains. Solutions include appropriately adjusting the cycle parameters of the stop loss line to prevent normal fluctuations from triggering a stop loss and setting up a take profit line to proactively lock in profits upon reaching target returns.

### 5. Optimization Directions  

This strategy can be optimized through the following aspects:

(1) Adjusting the overbought and oversold threshold values of the RSI indicator, such as changing them to 15 and 85, to obtain more trading opportunities.
(2) Optimizing the cycle parameters of the stop loss line to better adapt to short-term market fluctuations.
(3) Adding a take profit line for automatic profit-taking and risk management.
(4) Incorporating volatility indicators like ATR to further optimize parameters.

### 6. Summary  

The RSI + Bollinger Bands breakout strategy at lower area uses RSI to determine entry and exit points, Bollinger Bands to identify the trading range, and a 5-period SMA as the stop loss line. This approach effectively captures market trends while controlling risks to achieve stable profits. There is significant room for optimization of this strategy, making it worthy of further research.

---

### Source (PineScript)

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
    strategy.entry("RSI_2_S", strategy.short, comment="Bearish")

strategy.close("RSI_2_L", when = close > ma5)
strategy.close("RSI_2_S", when = close < ma5)
```

---

### Detail

https://www.fmz.com/strategy/439194

### Last Modified

2024-01-18 11:43:03