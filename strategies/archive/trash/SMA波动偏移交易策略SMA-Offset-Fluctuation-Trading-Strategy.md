> Strategy Overview

This strategy uses simple moving averages (SMA) and some math calculations to determine buy/sell points. We keep a 100-day SMA line as our basis. If the closing price is below this line, we determine the opening position based on the percentage the price is below the line (low offset), which is configurable. Similarly, we set a high offset percentage above the 100-day SMA before closing long positions. If we try to close too early while the price is still rising, the trailing stop loss will be triggered.

### Strategy Logic

The strategy uses three SMA lines: fast line (default 14 days), slow line (default 100 days), and reference line (default 30 days).

It goes long when the closing price is below the reference line, and the percentage below the slow line (low offset) is greater than the configured value. Additionally, if the fast line is rising while the slow line is falling, an entry point is identified as it's likely that a crossover will occur soon.

It closes long positions when the closing price is above the reference line, with the percentage above the slow line (high offset) greater than the configured value, and the closing price has risen for three consecutive candles. If there are open profits and the fast line is above the slow line, the trailing stop loss will be triggered if the price continues to rise.

The order size is based on a percentage of total equity, which controls our position size.

### Advantage Analysis

1. Utilize the advantage of SMA being able to smooth price fluctuations and filter out market noise.
2. SMA crossovers have some ability to predict trend changes.
3. Setting offsets avoids false breakouts of SMA lines.
4. Combining trend and crossover indicators improves accuracy of trading signals.
5. Trailing stop loss locks in profits and prevents drawdowns.

### Risk Analysis

1. SMA itself has lag and may miss price turning points.
2. Improper offset setting can make the strategy too aggressive or too conservative.
3. Improper stop loss parameter settings may result in stopping out too early or having a large stop loss percentage.
4. Unable to cope with violent price swings.

Corresponding improvements:
1. Add other leading indicators to filter entries.
2. Backtest and optimize offsets.
3. Backtest and find optimal stop loss parameters.
4. Reduce position size during high volatility periods.

### Optimization Directions

1. Test SMAs of different periods to find optimal parameters.
2. Add other indicators to determine market structure and trend.
3. Optimize trailing stop loss parameters to lock in more profits.
4. Adjust position sizing based on market volatility.
5. Apply the strategy simultaneously to multiple products for diversification.

### Conclusion

The SMA Offset Fluctuation Trading Strategy identifies optimal entry points by setting offsets based on different SMA lines. The exit mechanism sets a trailing stop loss to lock in gains. This strategy is simple to understand and implement. By optimizing parameters like SMA periods, offsets, and stop loss levels, better results can be achieved. It suits medium-long term investors seeking steady profits.

|Argument|Default|Description|
|----|----|----|
|v_input_1|14|SMA Fast (days)|
|v_input_2|100|SMA Slow (days)|
|v_input_3|30|SMA Reference (days)|
|v_input_4|0.001|Low Offset (%)|
|v_input_5|0.0164|High Offset (%)|
|v_input_6|0.96|Order Stake (%)|
|v_input_7|1.35|Trailing Stoploss (%)|

```pinescript
// @version=4
// Author: ChaoZhang (Sonny Parlin, highschool dropout)
strategy(shorttitle="SMA Offset Strategy", title="SMA Offset Fluctuation Trading Strategy",
                                     overlay=true,  currency=currency.USD,
                                     initial_capital=10000)

// Inputs and variables
ss = input(14, minval=10, maxval=50, title="SMA Fast (days)")
ff = input(100, minval=55, maxval=200, title="SMA Slow (days)")
ref = input(30, minval=20, maxval=50, title="SMA Reference (days)")
lowOffset = input(0.001, "Low Offset (%)", minval=0, step=0.001)
highOffset = input(0.0164, "High Offset (%)", minval=0, step=0.0001)
orderStake = input(0.96, "Order Stake (%)", minval=0, step=0.01)

// SMA
smaFast = sma(close, ss)
smaSlow = sma(close, ff)
smaRef = sma(close, ref)
distanceLow = (close - smaSlow) / close
distanceHigh = (close - smaSlow) / close

// Set up SMA plot but don't show by default
plot(smaFast, "smaFast", color=#00ff00, display = 0)
plot(smaSlow, "smaSlow", color=#ff0000, display = 0)
plot(smaRef, "smaRef", color=#ffffff, display = 0)

// The buy strategy:
// Guard that the low is under our sma
```