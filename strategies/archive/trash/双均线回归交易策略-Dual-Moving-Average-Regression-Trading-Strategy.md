> Name

Dual-Moving-Average-Regression-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/128f1faff075c31350f.png)

[trans]
#### Overview
This strategy uses two different-length linear regression lines as trading signals, combined with ATR for stop loss and partial profit-taking. When the shorter-period linear regression line crosses above the longer-period linear regression line from below, it generates a long signal; conversely, when the shorter-period linear regression line crosses below the longer-period linear regression line from above, it generates a short signal. After opening a position, the strategy uses ATR as a trailing stop loss, while employing a partial profit-taking method to maximize profits.

#### Strategy Principles
1. Calculate two linear regression lines with different periods (default 20 and 40) as trading signals
2. When the shorter-period linear regression line crosses above the longer-period linear regression line, open a long position if there is no current position
3. When the shorter-period linear regression line crosses below the longer-period linear regression line, open a short position if there is no current position
4. Once a position is opened, use ATR to calculate the trailing stop loss price, and close all positions when the price reaches the stop loss level
5. The strategy also employs a partial profit-taking method, calculating 16 different percentage take-profit levels (from 5% to 80%) based on the entry price, and closing a corresponding amount of positions at each take-profit level according to the input percentage
6. Until all positions are closed

#### Advantage Analysis
1. Using linear regression as a trend judgment and trading signal can better capture trends
2. Combining two linear regressions with different periods forms a more reliable signal confirmation
3. Using ATR as a stop loss can better control risks and keep in sync with price fluctuations
4. The partial profit-taking method can obtain more profits when the trend continues, while also taking risk control into account
5. The code is highly modularized with many input parameters, making the strategy highly customizable

#### Risk Analysis
1. Linear regression signals may generate false signals, leading to losses
2. Partial profit-taking may lead to longer holding periods, facing drawdown risks
3. Improper parameter settings may lead to poor strategy performance
4. In extreme market conditions, the strategy may face significant drawdowns

#### Optimization Directions
1. Consider introducing more indicators or filtering conditions to improve signal accuracy, such as trend confirmation indicators, volatility indicators, etc.
2. Optimize the position and strategy of take-profit and stop-loss, consider dynamic take-profit and stop-loss
3. Optimize parameters to find the best parameter combination
4. Add position management to adjust position size according to market volatility conditions

#### Summary
This dual moving average regression strategy combines trend-following and take-profit/stop-loss strategies, which can effectively capture trending markets while controlling drawdowns. However, the strategy may underperform in ranging markets and faces the problem of parameter optimization. Overall, this strategy is a typical representative of a trend-following strategy and can be used as a base strategy for optimization and improvement.

||

#### Source (PineScript)

```pinescript
//@version=5
strategy(title="RPK_V4.3(1K$)_Shared", shorttitle="RPK_V4.3(1K$)_Shared", overlay=true)

regresyonUzunluk = input.int(20, minval=1, step=20, group="Strategy Condition")
off = 0
sapma = 2
cc1 = close
lreg1 = ta.linreg(cc1, regresyonUzunluk, off)
lreg_x1 = ta.linreg(cc1, regresyonUzunluk, off + 1)
b1 = bar_index
s1 = lreg1 - lreg_x1
intr1 = lreg1 - b1 * s1
dS1 = 0.0
for i1 = 0 to regresyonUzunluk - 1 by 1
    dS1 += math.pow(cc1[i1] - (s1 * (b1 - i1) + intr1), 2)
de1 = math.sqrt(dS1 / regresyonUzunluk)
up1 = -de1 * sapma + lreg1
down1 = de1 * sapma + lreg1
t1 = 0
x11 = bar_index - regresyonUzunluk
x21 = bar_index
kirmizi = s1 * (bar_index - regresyonUzunluk) + intr1
yesil = lreg1

regresyonUzunlukUst = input.int(40, minval=1, step=20, group="Strategy Condition")
cc1Ust = close
lreg1Ust = ta.linreg(cc1Ust, regresyonUzunlukUst, off)
lreg_x1Ust = ta.linreg(cc1Ust, regresyonUzunlukUst, off + 1)
b1Ust = bar_index
s1Ust = lreg1Ust - lreg_x1Ust
intr1Ust = lreg1Ust - b1Ust * s1Ust
dS1Ust = 0.0
for i1Ust = 0 to regresyonUzunlukUst - 1 by 1
    dS1Ust += math.pow(cc1Ust[i1Ust] - (s1Ust * (b1Ust - i1Ust) + intr1Ust), 2)
de1Ust = math.sqrt(dS1Ust / regresyonUzunlukUst)
up1Ust = -de1Ust * sapma + lreg1Ust
down1Ust = de1Ust * sapma + lreg1Ust
```

Note: The PineScript code snippet provided was not fully completed, so it was truncated at the point of clarity.