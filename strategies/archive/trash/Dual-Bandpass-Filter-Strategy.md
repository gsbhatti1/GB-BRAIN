> Name

Dual-Bandpass-Filter-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1838a4c0975c83b5dd1.png)

### Overview

The Dual Bandpass Filter strategy is adapted from a strategy published by Broder in the Stocks & Commodities magazine in 2010. This strategy generates trading signals by calculating the value of Broder's bandpass filter to identify price fluctuations in stocks. It goes short when the bandpass filter value is higher than the threshold, and goes long when it is lower, to follow the trend.

### Strategy Logic

The key steps of this strategy are:

1. Initialize parameters including bandpass length `Length`, fluctuation coefficient `Delta`, sell zone threshold `SellZone`, and buy zone threshold `BuyZone`.

2. Calculate the Broder bandpass filter `BP` using a series of trigonometric functions.

3. Determine position direction: go short if `BP` is above `SellZone`; go long if below `BuyZone`; otherwise, maintain current position.

4. Output signals: generate long/short signals based on position direction.

5. Set bar colors based on signal results.

6. Plot the bandpass filter curve.

This strategy captures short-term fluctuations using the Broder bandpass filter and generates trading signals when the fluctuations reach certain magnitude to follow the trend.

### Advantage Analysis

1. More sensitive to market fluctuations based on the Broder bandpass filter, which can catch short-term trends.
2. The sensitivity can be adjusted through parameter tuning to adapt to different market environments.
3. Simple and clear strategy logic, easy to understand and implement.
4. Parameters can be easily optimized to find the best combination.
5. Visual bandpass filter curve intuitively shows market fluctuations.

### Risk Analysis

1. Overly optimized bandpass filter may become too sensitive and generate false signals.
2. Unable to determine fluctuation end points, which may lead to expanding losses.
3. High trading frequency may increase costs and slippage risks.
4. Vulnerable to black swan events that trigger false signals.
5. Parameters need adjusting for different products and markets.
6. Consider setting stop loss to control loss per trade.
7. Extend exit time or add filters to reduce false signals.

### Optimization Directions

1. Optimize parameters to find the best combination, evaluating win rate, profit ratio, Sharpe ratio etc.
2. Add filters like moving average cross, price patterns to avoid trading in non-trending areas.
3. Consider combining parameters across multiple instruments for basket trading to diversify risks.
4. Add stop loss logic to control loss per trade, like dynamic stops or trailing stops.
5. Add profit taking like moving profit stops to lock in gains. Different levels can be set for different trend stages.
6. Optimize entry signals to avoid false signals in ranging markets. Consider longer holding periods or breakout signals.
7. Expand to a cross-asset arbitrage system utilizing price differentials for hedging.
8. Backtest optimization for best asset selection and rebalancing strategies.

### Summary

The Dual Bandpass Filter strategy judges price fluctuations using Broder's bandpass filter and generates signals when the fluctuations reach thresholds, with the advantage of high sensitivity to short-term trends and easy implementation. However, it is sensitive to parameters and trading frequency, requiring optimization to reduce false signals and manage risks. Overall, it provides an option for catching short-term trends but overfitting should be avoided, and other technical tools can be combined for trading.

> Strategy Arguments



| Argument | Default | Description |
| --- | --- | --- |
| v_input_1 | 20 | Length |
| v_input_2 | 0.5 | Delta |
| v_input_3 | 5 | SellZone |
| v_input_4 | -5 | BuyZone |
| v_input_5 | false | Trade reverse |


> Source (PineScript)

```pinescript
//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 18/09/2018
// The related article is copyrighted material from
// Stocks & Commodities Mar 2010
// You can use in the xPrice any series: Open, High, Low, Close, HL2, HLC3, OHLC4 and ect...
//
// You can change long to short in the Input Settings
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
////////////////////////////////////////////////////////////
strategy(title="Bandpass Filter Strategy ver 2.0")
Length = input(20, minval=1)
Delta = input(0.5, minval=0.1) // Add a minimum value constraint for Delta
SellZone = input(5, minval=-100)
BuyZone = input(-5, maxval=100)
TradeReverse = input(false, title="Trade reverse")

// Calculation of the bandpass filter (BP)
var float BP = na

if barstate.islast
    // Add your calculation logic for BP here using trigonometric functions
    BP := 0.0  // Placeholder value; replace with actual calculations
```

Note: The placeholder calculation for `BP` needs to be replaced with the actual trigonometric function implementation based on Broder's method, which is not provided in the original text.