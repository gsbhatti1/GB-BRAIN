> Name

Renko Reversal Tracking Strategy Renko-Reversal-Tracking-Strategy

> Author

ChaoZhang

> Strategy Description


[trans]

### Strategy Overview

The Renko reversal tracking strategy is a short-term trading approach that utilizes Renko charts to identify market reversals. It captures short-term reversal opportunities by monitoring color changes between adjacent Renko bricks. Trading signals are generated when the current brick color flips after consecutive same-colored bricks.

### Strategy Logic

1. Use traditional non-repainting Renko bricks.

2. Monitor color changes between neighboring Renko bricks.

3. Signals emerge when the current brick color flips while previous two bricks share the same color.

4. Long signal: Bullish brick appears after two bearish bricks, indicating a bullish trend.

5. Short signal: Bearish brick appears after two bullish bricks, indicating a bearish trend.

6. Entry options include market orders or stop orders.

7. Set stop loss and take profit levels as multiples of the Renko brick size.

The core of this strategy is to capitalize on short-term pullbacks caused by color flips in Renko bricks. Consecutive same-colored bricks represent trend formation, while a subsequent flip indicates potential reversals.

Renko brick size and stop loss/take profit coefficients can be adjusted for optimization.

### Advantages of the Strategy

- Bricks directly display reversal information.

- Simple and clear logic, easy to implement.

- Symmetrical long and short opportunities.

- Flexible Renko brick size adjustment.

- Strict risk control with stop loss/take profit.

### Risk Warnings

- Requires a certain number of consecutive bricks to form signals.

- Renko brick size directly impacts profitability and drawdowns.

- Hard to determine trend duration.

- Consecutive stop losses may occur.

### Conclusion

The Renko reversal tracking strategy innovatively applies traditional technical indicators by using direct color flips in Renko bricks to identify short-term reversals. Simple and practical, this strategy can achieve stable returns through parameter tuning and is worth backtesting and applying after live optimization.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Brick size multiplier: use high value to avoid stop loss and take profit|
|v_input_2|true|Use stop orders instead of market orders|


> Source (PineScript)

```pinescript
//@version=3
// Simple Renko strategy, very profitable. Thanks to vacalo69 for the idea.
// Rules when the strategy opens order at market as follows:
//- Buy when previous brick (-1) was bearish and previous brick (-2) was bearish too and actual brick close is bullish
//- Sell when previous brick (-1) was bullish and previous brick (-2) was bullish too and actual brick close is bearish
// Rules when the strategy sends stop order are the same but this time a stop buy or stop sell is placed (better overall results).
// Note that strategy opens an order only after that condition is met, at the beginning of next candle, so the actual close is not the actual price.
// Only input is the brick size multiplier for stop loss and take profit: SL and TP are placed at (brick size)x(multiplier) Or put it very high if you want strategy to close order on opposite signal.
// Adjust brick size considering:
//- Strategy works well if there are three or more consecutive bricks of same "color"
//- Expected Profit
//- Drawdown
//- Time on trade

// Study with alerts, MT4 expert advisor and jforex automatic strategy are available at request.

strategy("Renko Strategy Open_Close", overlay=true, calc_on_every_tick=true, pyramiding=0,default_qty_type=strategy.percent_of_equity,default_qty_value=100,currency=currency.USD)

// INPUTS
Multiplier=input(1,minval=0, title='Brick size multiplier: use high value to avoid SL and TP')
UseStopOrders=input(true,title='Use stop orders instead of market orders')

// CALCULATIONS
BrickSize=abs(open[1]-close[1])
targetProfit = 0
targetSL = 0

// STRATEGY CONDITIONS
longCondition = open[1]>close[1] and close>open and open[1]<open[2]
shortCondition = open[1]<close[1] and close<open and open[1]>open[2]

// STRATEGY
if (longCondition and not UseStopOrders)
    strategy.entry("LongBrick", strategy.long)
    targetProfit=close+BrickSize*Multiplier
    targetSL=close-BrickSize
    strategy.exit("CloseLong","LongBrick", limit=targetProfit, stop=targetSL)
    
if (shortCondition and not UseStopOrders)
    strategy.entry("ShortBrick", strategy.short)
    targetProfit = close-BrickSize*Multiplier
    targetSL = close+BrickSize
    strategy.exit("CloseShort","ShortBrick", limit=targetProfit, stop=targetSL)

if (longCondition and UseStopOrders)
    strategy.entry("LongBrick_Stop", strategy.long, stop=open[2])
    targetProfit=close+BrickSize*Multiplier
    targetSL=close-BrickSize
    strategy.exit("CloseLong","LongBrick_Stop", limit=targetProfit, stop=targetSL)
    
if (shortCondition and UseStopOrders)
    strategy.entry("ShortBrick_Stop", strategy.short, stop=open[2])
    targetProfit = close-BrickSize*Multiplier
    targetSL = close+BrickSize
    strategy.exit("CloseShort","ShortBrick_Stop", limit=targetProfit, stop=targetSL)
```

> Detail

https://www.fmz.com/strategy/426927

> Last Modified

2023-09-1