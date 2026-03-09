> Name

Dual EMA and Relative Strength Adaptive Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/8b3c76d6650fd37427.png)

#### Overview
This strategy is a comprehensive trading system that combines a dual EMA system, Relative Strength Index (RSI), and Relative Strength (RS) analysis. The strategy confirms trends through the crossover of 13-day and 21-day Exponential Moving Averages (EMA) while utilizing RSI and RS values relative to a benchmark index for signal confirmation, implementing a multi-dimensional trading decision mechanism. It also includes risk control mechanisms based on 52-week highs and re-entry condition judgments.

#### Strategy Principles
The strategy employs a multiple signal confirmation mechanism:
1. Entry signals require the following conditions:
   - EMA13 crosses above EMA21 or price above EMA13
   - RSI above 60
   - Positive Relative Strength (RS)
2. Exit conditions include:
   - Price falls below EMA21
   - RSI below 50
   - RS turns negative
3. Re-entry conditions:
   - Price crosses above EMA13 and EMA13 above EMA21
   - RS remains positive
   - Or price breaks above last week's high

#### Strategy Advantages
1. Multiple signal confirmation reduces false breakout risks
2. Integration of relative strength analysis effectively filters strong performers
3. Adopts adaptive timeframe adjustment mechanism
4. Comprehensive risk control system
5. Intelligent re-entry mechanism
6. Real-time trade status visualization

#### Strategy Risks
1. Potential frequent trading in choppy markets
2. Multiple indicators may lead to lagging signals
3. Fixed RSI thresholds may not suit all market conditions
4. RS calculation depends on benchmark index accuracy
5. 52-week high stop-loss might be too loose

#### Strategy Optimization Directions
1. Introduction of adaptive RSI thresholds
2. Optimization of re-entry condition logic
3. Addition of volume analysis dimension
4. Enhancement of profit-taking and stop-loss mechanisms
5. Implementation of volatility filters
6. Optimization of relative strength calculation periods

#### Summary
The strategy builds a comprehensive trading system by combining technical analysis and relative strength analysis. Its multiple signal confirmation mechanism and risk control system make it highly practical. Through the suggested optimization directions, there is room for further improvement. Successful implementation requires traders to have a deep understanding of the market and make appropriate parameter adjustments based on specific trading instrument characteristics.

#### Source (PineScript)

```pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-03 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA 13 & 21 Entry Exit", overlay=true)

// Define the EMAs
ema13 = ta.ema(close, 13)
ema21 = ta.ema(close, 21)

// Define the RSI
rsi = ta.rsi(close, 14)

// Calculate the closing price relative to Nifty 50
nifty50 = request.security("swap", "D", close)
rs = ta.ema(close / nifty50, 55)

// Define the previous 2-week low and last week's high
twoWeekLow = ta.lowest(low, 10)  // 10 trading days roughly equal to 2 weeks
lastWeekHigh = ta.highest(high, 5)  // 5 trading days roughly equal to 1 week
fiftytwoWeekhigh = ta.highest(high, 52*5)  // 252 trading days roughly equal to 52 weeks.

// Long condition: EMA 21 crossing above EMA 55, price above EMA 21, RSI > 50, and RS > 0
longCondition = ta.crossover(ema13, ema21) or close > ema13 and rsi > 60 and rs > 0

// Exit condition: Price closing below EMA 55 or below the previous 2-week low
exitCondition = close < ema21 or rsi < 50 or rs < 0 //or close < fiftytwoWeekhigh*0.80

// Re-entry condition: Price crossing above EMA 21 after an exit, EMA 21 > EMA 55, and RS > 0
reEntryCondition = ta.crossover(close, ema13) and ema13 > ema21 and rs > 0

// Re-entry condition if trailing stop loss is hit: Price crossing above last week's high
reEntryAfterSL = ta.crossover(close, lastWeekHigh)

// Plot the EMAs
plot(ema13 ,color=color.green, title="EMA 13",linewidth = 2)
plot(ema21, color=color.red, title="EMA 21",linewidth = 2)

// Plot buy and sell signals
plotshape(series=longCondition, location=location.abovebar, color=color.rgb(50, 243, 130), style=shape.flag, title="Buy Signal")
plotshape(series=exitCondition, location=location.belowbar, color=color.red, style=shape.xcross, title="Sell Signal")
plotshape(series=reEntryCondition or reEntryAfterSL, location=location.belowbar, color=color.rgb(255, 0, 0), style=shape.triangleup, title="Re-Entry Signal")
```