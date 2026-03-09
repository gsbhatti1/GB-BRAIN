> Name

Seven-Candlestick-Oscillation-Breakthrough-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/14b50815ac56c1445d3.png)
 [trans]

### Overview

The Seven-Candlestick-Oscillation-Breakthrough-Strategy identifies the persistence of upward or downward price movements formed by seven K-lines to determine the market oscillation trend and execute break-even operations at fixed times to achieve profits.

### Strategy Principle

The core logic of this strategy is based on two indicators:

1. sevenReds: Detecting 7 consecutive declining K-lines defines a downward market oscillation trend.
2. sevenGreens: Detecting 7 consecutive rising K-lines defines an upward market oscillation trend.

When sevenReds is detected, go long; when sevenGreens is detected, go short.

Additionally, the strategy closes positions at fixed times (US important data release times) every day to lock in profits.

### Advantage Analysis

The Seven-Candlestick-Oscillation-Breakthrough-Strategy has the following advantages:

1. Captures market oscillation trends. Seven K-lines filter out market noise, improving signal quality.
2. Timed operations avoid system risks associated with large gap moves around major economic data releases.
3. Timely profit-taking locks in gains and reduces drawdown probability.

### Risk Analysis

The Seven-Candlestick-Oscillation-Breakthrough-Strategy also has some risks:

1. Pattern recognition error risk. Seven K-lines cannot completely filter out market noise, which may generate incorrect signals.
2. Inadequate stop-loss measures to limit per-trade losses.
3. Fixed profit-taking times cannot be dynamically adjusted, which may result in missed profit-taking opportunities.

Corresponding solutions:

1. Increase the number of K-lines and raise the persistence threshold.
2. Add moving stop-loss logic.
3. Dynamically adjust profit-taking times based on volatility indicators.

### Optimization Directions

The Seven-Candlestick-Oscillation-Breakthrough-Strategy can be optimized in the following aspects:

1. Add multiple security pools for index or sector rotation.
2. Add machine learning models to aid in market state prediction.
3. Incorporate moving averages for optimized entry signals.
4. Dynamically adjust position sizing based on drawdown to control risk exposure.

### Conclusion

The Seven-Candlestick-Oscillation-Breakthrough-Strategy profits by capturing short-term oscillation trends in the market, while using timed operations to avoid major risks and taking profits to lock in gains. The strategy can be enhanced through multi-asset rotation, machine learning, etc., and is a typical medium-frequency quantitative trading strategy.

||

### Overview

The seven candlestick oscillation breakthrough strategy detects the persistence up and down candlestick patterns formed by seven K-lines to determine market oscillation trends and make breakthrough operations at fixed times to profit.

### Strategy Principle

The core logic of this strategy is based on two indicators:

1. sevenReds: Detecting 7 consecutive declining K-lines defines a downward market oscillation trend.
2. sevenGreens: Detecting 7 consecutive rising K-lines defines an upward market oscillation trend.

When sevenReds is detected, go long; when sevenGreens is detected, go short.

Additionally, the strategy closes positions at fixed times (US important data release times) every day to lock in profits.

### Advantage Analysis

The seven candlestick oscillation breakthrough strategy has the following advantages:

1. Captures market oscillation trends. Seven K-lines filter out market noise, improving signal quality.
2. Timed operations avoid system risks associated with large gap moves around major economic data.
3. Timely profit-taking locks in gains and reduces drawdowns.

### Risk Analysis

The seven candlestick oscillation breakthrough strategy also has some risks:

1. Pattern recognition error risk. Seven K-lines cannot completely filter noise and may generate incorrect signals.
2. Lack of stop loss measures to limit per trade loss.
3. Fixed profit-taking times cannot be dynamically adjusted, risk of failure to take profits in time.

Corresponding solutions:

1. Increase the number of K-lines, raise the persistence threshold.
2. Add moving stop loss logic.
3. Dynamically adjust profit-taking times based on volatility indicators.

### Optimization Directions

The seven candlestick oscillation breakthrough strategy can be optimized in the following aspects:

1. Add multiple security pools for index/sector rotation.
2. Add machine learning models to aid in market regime prediction.
3. Incorporate moving averages for optimized entry signals.
4. Dynamically adjust position sizing based on drawdown to control risk.

### Conclusion

The seven candlestick oscillation breakthrough strategy profits by capturing short-term oscillation trends in the market, while using timed execution to avoid major risks and taking profits to lock in gains. The strategy can be enhanced via multi-asset rotation, machine learning, etc., and is a typical medium-frequency quantitative trading strategy.

||

### Source (PineScript)

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Eliza123123

//@version=5
strategy("Seven-Candlestick-Oscillation-Breakthrough-Strategy", overlay=true)

// Generic signal (not a viable strategy don't use, just some code I wrote quick for demo purposes only)
red = open > close
green = open < close
sevenReds = red and red[1] and red[2] and red[3] and red[4] and red[5] and red[6]
sevenGreens = green and green[1] and green[2] and green[3] and green[4] and green[5] and green[6]
if sevenReds
    strategy.entry('Buy', direction=strategy.long)
if sevenGreens
    strategy.entry('Sell', direction=strategy.short)
if (hour == 5 and minute == 0 ) or (hour == 11 and minute == 0) or (hour == 17 and minute == 0 ) or (hour == 23 and minute == 0) 
    strategy.close_all("Close")

// Breakeven line for visualizing breakeven price on stacked orders.  
var breakEvenLine = 0.0
if strategy.opentrades > 0 
    breakEvenLine := strategy.position_avg_price
else
    breakEvenLine := 0.0
color breakEvenLineColor = na
if strategy.position_size > 0
    breakEvenLineColor := #15FF00
if strategy.position_size < 0
    breakEvenLineColor := #FF000D
plot(breakEvenLine, color = breakEvenLine and breakEvenLine[1] > 0 ? breakEvenLineColor : na, linewidth = 2, style = plot.style_circles)
```

> Detail

https://www.fmz.com/strategy/435514

> Last Modified

2023-12-15 16:14:32