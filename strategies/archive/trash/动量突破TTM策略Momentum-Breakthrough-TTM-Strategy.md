``` pinescript
lengthttm = input(title="TTM Length", type=input.integer, defval=50, minval=1)
multFactor = input(title="Multiplier Factor", type=input.float, defval=0.2, minval=0.01)
alertLevel = input(title="Alert Level", type=input.float, defval=0.1, minval=0.01)
impulseLevel = input(title="Impulse Level", type=input.float, defval=0.75, minval=0.01)
showRange = input(title="Show Range", type=input.bool, defval=false)

// Load RSI and Bollinger Bands
rsiLength = input(30, title="RSI Length")
rsiSrc = close
rsi = rsi(rsiSrc, rsiLength)

len = input(20, title="BB Length")
src = close
mult = input(2.0, title="BB Multiplier")
basis = sma(src, len)
dev = mult * stdev(src, len)
lower = basis - dev
upper = basis + dev

// TTM Squeeze code
lengthttm = input(50, title="TTM Length", type=input.integer, minval=1)
multFactor = input(0.2, title="Multiplier Factor", type=input.float, minval=0.01)
alertLevel = input(0.1, title="Alert Level", type=input.float, minval=0.01)
impulseLevel = input(0.75, title="Impulse Level", type=input.float, minval=0.01)
showRange = input(false, title="Show Range", type=input.bool)

// TTM Squeeze code
var float ttmLow = na
var float ttmHigh = na
var int ttmCount = 0
var float ttmLevel = na

ttmLow := lowest(low, lengthttm)
ttmHigh := highest(high, lengthttm)
ttmLevel := (ttmHigh + ttmLow) / 2

ttmSqueeze = ttmLow > ttmLevel * (1 - alertLevel) and ttmHigh < ttmLevel * (1 + alertLevel)

// Strategy Conditions
if ttmSqueeze
    if rsi > 30 and rsi < 70 and close > upper * impulseLevel and open[1] < close[1]
        strategy.entry("Buy", strategy.long)
    if rsi > 30 and rsi < 70 and close < lower * impulseLevel and open[1] > close[1]
        strategy.entry("Sell", strategy.short)

// Plot
plot(ttmLow, color=color.red, title="TTM Low")
plot(ttmHigh, color=color.green, title="TTM High")
plot(ttmLevel, color=color.blue, title="TTM Level")
plot(upper, color=color.orange, title="Upper BB")
plot(lower, color=color.orange, title="Lower BB")

if showRange
    hline(ttmLevel, "TTM Level")
    hline(ttmLevel * (1 - alertLevel), "Lower Alert Level")
    hline(ttmLevel * (1 + alertLevel), "Upper Alert Level")
```

``` markdown
## Overview

This is a binary option breakthrough trading strategy that utilizes the momentum indicator RSI combined with the Bollinger Bands indicator BB. In terms of timeliness, the TTM indicator is used to determine whether the market is in a consolidation state, thereby improving the reliability of entry.

## Principle

The basic logic of the strategy is to determine the breakthrough direction based on Bollinger Bands and the RSI indicator under the condition that the TTM indicator set forms a breakthrough. Specifically, the strategy uses 20 periods of BB and 30 periods of RSI. When the market breaks through the squeeze, it determines the opening direction when the RSI is within a certain fluctuation range (30-70) and the BB has a large breakthrough (0.15 times the fluctuation range). In addition, the strategy also checks the opening direction of the previous K-line before opening a position to avoid unnecessary repeated opening.

## Advantages

The main advantages of this strategy are:

1. Using the TTM indicator to judge the trading state of the market and avoid meaningless trading in the consolidating market. The compression and expansion of the TTMS indicator can better determine the main trend direction and provide a reference for opening positions.
2. The combination of RSI and BB can make opening positions more reliable. The RSI indicator judges whether prices are overbought or oversold; while the BB indicator judges whether prices have occurred a major breakthrough. The combination of the two makes the strategy profit from strong directional trends.
3. The strategy logic considers certain optimizations such as avoiding repeated opening. This can reduce unnecessary profit and loss switching to some extent.

## Risk Analysis

The main risks of this strategy are:

1. Breakdown failure risk. When the TTM indicator does not accurately judge the trend, RSI and BB may still have false breakouts. At this time, the strategy opens positions based on the indicators, and may eventually be trapped. To control this risk, consider reducing the size of the position.
2. It is easy to lose when the market oscillates. When the market is in an oscillating state, the performance of the TTM indicator is not ideal. RSI and BB indicators may also give multiple false signals. At this time, it is very easy to form losses. To control this risk, avoid using this strategy in obvious oscillating markets.

## Optimization

The strategy can be optimized in the following aspects:

1. Optimize the parameters of the TTM indicator to adjust the length and factors of the indicator. This can improve TTM's judgment on consolidation and breakthrough.
2. Optimize RSI and BB parameters. Appropriately shortening cycle numbers may obtain more timely and precise breakthrough signals. At the same time, the bandwidth of the BB channel can also test different values.
3. Increase stop loss logic. Since the strategy does not set a stop loss, to prevent a single loss from being too large, consider adding a moving stop loss or expected stop loss.
4. Different varieties of parameters can be tested. The current strategy runs on 1 minute charts. For other varieties of parameters (such as 5 minutes), indicator parameters can be retested and optimized to obtain better parameter combinations.

## Conclusion

This strategy utilizes TTM to determine trend accuracy and uses RSI and BB to determine breakthrough directions. Compared with simple breakthrough strategies, its entry timing and indicator parameter optimization are more advantageous, which can increase profitability. But this strategy also poses certain risks of failure and adaptability issues in oscillating markets. This requires us to adjust position sizing during use and avoid using it in oscillating markets. With further parameter and stop loss optimization, this strategy can become a reliable option trading strategy.
```