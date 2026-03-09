---

### Overview

This strategy uses simple moving average crossovers and the Average True Range (ATR) indicator to generate buy and sell signals. It belongs to trend following strategies. It mainly uses the crossover of a 50-day simple moving average (SMA) and a 100-day SMA to determine trends, setting stop-loss points based on ATR to control risks.

### Strategy Logic

1. Calculate the 50-day simple moving average (SMA1) and the 100-day simple moving average (SMA2).
2. When SMA1 crosses above SMA2, a buy signal is generated.
3. When SMA1 crosses below SMA2, a sell signal is generated.
4. Calculate the 14-day ATR.
5. Multiply the ATR by a set factor to determine stop-loss points.
6. When a buy signal is triggered, use the closing price minus the stop-loss point as the stop-sell point; when a sell signal is triggered, use the closing price plus the stop-loss point as the stop-buy point.

It can be seen that this strategy mainly relies on the trend judging ability of moving averages and the risk control capability of ATR. The logic is simple and easy to understand and implement.

### Advantages

1. Simple logic easy to implement, suitable for beginners.
2. Moving averages can effectively track trends.
3. ATR stop-loss can effectively control losses from individual black swan events.
4. Parameters can be easily adjusted for different market environments.

### Risks

1. Many false signals may be triggered during range-bound markets, missing reversal points.
2. ATR may not react sensitively enough to fast changing markets, leading to larger than expected losses.
3. The parameter settings and ATR multiplier rely on experience; improper settings may affect strategy performance.
4. The dual moving averages themselves have a lagging effect, potentially missing turning points.

Risk Management:

1. Shorten the moving average periods to make the indicator more sensitive.
2. Dynamically adjust the ATR multiplier for more flexible stop-losses.
3. Add other indicators to filter false signals.
4. Operate based on larger time frame structure judgments.

### Optimization Directions

1. Try other types of moving averages, such as Exponential Moving Averages (EMAs) that filter better.
2. Consider dynamic stop losses with Keltner Channels or other methods instead of ATR.
3. Add supporting indicators like volume to filter signals.
4. Identify trend key points using concepts like Elliott Waves, support and resistance levels.

### Summary

This is a typical trend following strategy, utilizing moving averages to determine the direction of trends and setting stop losses based on ATR to control risks. The logic is simple and easy to grasp. However, it has certain lagging and false signal risks. Improvements can be made through parameter tuning, indicator optimization, incorporating more factors, etc., to make the strategy more adaptive. Overall, this strategy is suitable for beginner practice and optimization but needs careful application in actual trading.

---

### Strategy Arguments

| Argument   | Default  | Description                                                                 |
|------------|----------|-----------------------------------------------------------------------------|
| v_input_int_1 | 50       | Length of 50 SMA                                                             |
| v_input_int_2 | 100      | Length of 100 SMA                                                            |
| v_input_int_3 | 14       | ATR length                                                                   |
| v_input_int_4 | 4        | ATR multiplier                                                               |

### Source (PineScript)

```pinescript
// backtest start: 2023-12-27 00:00:00
// backtest end: 2024-01-03 00:00:00
// backtest period: 1m
// basePeriod: 1m
// exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
//@version=5
strategy("SMA and ATR Strategy", overlay=true)

// Step 1. Define strategy settings
lengthSMA1 = input.int(50, title="50 SMA Length")
lengthSMA2 = input.int(100, title="100 SMA Length")
atrLength = input.int(14, title="ATR Length")
atrMultiplier = input.int(4, title="ATR Multiplier")

// Step 2. Calculate strategy values
sma1 = ta.sma(close, lengthSMA1)
sma2 = ta.sma(close, lengthSMA2)
atr = ta.atr(atrLength)

// Step 3. Output strategy data
plot(sma1, color=color.blue, title="50 SMA")
plot(sma2, color=color.red, title="100 SMA")

// Step 4. Determine trading conditions
longCondition = ta.crossover(sma1, sma2)
shortCondition = ta.crossunder(sma1, sma2)

longStopLoss = close - (atr * atrMultiplier)
shortStopLoss = close + (atr * atrMultiplier)

// Step 5. Execute trades based on conditions
if (longCondition)
    strategy.entry("Buy", strategy.long)
    strategy.exit("Sell", "Buy", stop=longStopLoss)

if (shortCondition)
    strategy.entry("Sell", strategy.short)
    strategy.exit("Buy", "Sell", stop=shortStopLoss)
```

### Detail

https://www.fmz.com/strategy/437640

### Last Modified

2024-01-04 15:03:14