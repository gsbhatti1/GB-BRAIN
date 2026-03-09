```markdown
<!-- AUTO-TRANSLATE FAILED: the JSON object must be str, bytes or bytearray, not NoneType -->


## Overview

DAKELAX-XRPUSDT is a trading bot strategy for XRPUSDT on Binance. It is a simple reverse to mean strategy using Bollinger Bands and performs well in backtesting from May to August 2019, as well as running live.

## Strategy Logic

The strategy first calculates the 20-period Simple Moving Average (SMA) and upper/lower Bollinger Bands. The upper band is calculated as SMA + 1.5 times the standard deviation, and the lower band as SMA - 2.2 times the standard deviation. It then calculates the contraction rate of the bands; if it's greater than 1.3, the bands are filled black. If less than 0.1, they are filled yellow; otherwise, red.

When the close price is below the lower Bollinger Band, a long position with 20 coins is initiated. When the close is above the upper Bollinger Band, all positions are closed.

The strategy also calculates a 7-period Exponential Moving Average (EMA) fast line and an 18-period EMA slow line. A crossover of the fast line over the slow line is considered a buy signal, while a crossover under the slow line is considered a sell signal.

## Advantage Analysis

- Bollinger Bands and their contraction rate intuitively identify trends and volatility.
- Combining with EMA crossovers adds strength to signals.
- Backtest results are good, and it performs relatively stably in live trading.

## Risk Analysis

- High probability of failure when the bands contract but do not break out.
- Fixed quantity buying without position sizing risks overtrading.
- Too many crossovers in ranging markets can lead to losses.
- Only considers daily factors; may miss larger timeframe trends.

Consider dynamically adjusting buy amounts or setting stop-losses to control risk. Optimize EMA crossover strategies to avoid whipsaws in ranging markets. Integrate higher timeframe trend indicators to identify larger moves.

## Optimization Directions

- Adjust the buy amount based on the band width, fewer buys when contracted and more during expansion.
- Consider accumulating positions before a contraction triggers a signal.
- Add longer timeframe trend indicators to determine overall direction; pause strategy if unclear.
- Incorporate stop-losses to control risk, setting them near recent low points of the bands.
- Optimize EMA crossover parameters like period lengths to avoid getting trapped.

## Summary

DAKELAX-XRPUSDT is a trading bot strategy using Bollinger Bands contraction with EMA crossovers. It provides intuitive and good backtest results but contains some risks. These can be mitigated through position sizing, stopping the strategy, adding stop-losses, and optimizing the crossover logic. Overall, it offers a clear example of a Bollinger Band strategy, although specific optimizations are needed for stable live profits.

---

## Source (PineScript)

```pinescript
//@version=3
//study(title="Tradebotler DAKELAX Binance:XRPUSDT Study-strategy", overlay=true)
strategy(title="Tradebotler DAKELAX Binance:XRPUSDT Strategy", overlay=true)

buyAmount = input(20, minval=1)

// SMA20
len2 = input(20, minval=1)
src2 = input(close)
out2 = sma(src2, len2)

// BB contraction value (medium tight)
contraction_value = 1.3
// BB contraction value (very tight)
contraction_value2 = 0.1

// 2xSTDEV BB calculation
dev = stdev(src2, len2)
upper_BB = out2  + 1.5*dev
lower_BB = out2  - 2.2*dev
x1 = plot(upper_BB, color=blue, linewidth = 2)
x2 = plot(lower_BB, color=blue, linewidth = 2)

contraction = (upper_BB-lower_BB)/out2

//fills the BBands according to the contraction value (threshold)

// Calculate values
fastMA  = ema(close, 7)
slowMA  = ema(close, 18)

// Determine alert setups
crossUp   = crossover(fastMA, slowMA)
crossDown = crossunder(fastMA, slowMA)

buySignal   = (crossUp or crossUp[1]) and (low > slowMA)
shortSignal = (crossDown or crossDown[1]) and (high < slowMA)

// Highlight alerts on the chart
bgColour =
     (buySignal and barstate.isrealtime) ? green :
     (shortSignal and barstate.isrealtime) ? red :
     na

signalBuy = (buySignal ) ? true : false
signalSell = (shortSignal ) ? true : false

test = true

test := not test[1]

closesBelowLowerBB = close < lower_BB
closesAboveUpperBB = close > upper_BB

tmptext = "blah"

// Plot values
plot(series=fastMA, color=teal)
plot(series=slowMA, color=orange)

plot(out2, color=black, linewidth = 1)
fill(x1, x2, color = contraction > contraction_value ? black : contraction < contraction_value2 ? yellow: red)

isInRed = contraction < contraction_value and contraction >= contraction_value2
isInYellow = contraction < contraction_value and contraction < contraction_value2

if ( closesBelowLowerBB )
    strategy.order('Buy', strategy.long, buyAmount)

if ( closesAboveUpperBB )
    strategy.close_all()
```

## Detail

https://www.fmz.com/strategy/4308
```