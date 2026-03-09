---
### Overview
This strategy is a dynamic trend-following trading system based on the Ichimoku Cloud indicator. The core concept is to identify market trend changes by monitoring the crossover between the Conversion Line (Tenkan-sen) and Base Line (Kijun-sen), executing position switches between long and short at appropriate times. The strategy combines the reliability of traditional Ichimoku indicators with the flexibility of modern quantitative trading.

#### Strategy Principle
The strategy operates based on the following key elements:
1. Calculates Conversion and Base Lines using 9-period and 26-period high-low averages.
2. Determines market trends through the direction of Conversion and Base Line crossovers.
3. Generates golden cross signals for long entries or position switches when the Conversion Line crosses above the Base Line.
4. Generates dead cross signals for short entries or position switches when the Conversion Line crosses below the Base Line.
5. Automatically determines position switching needs based on current position status.

#### Strategy Advantages
1. Stable and reliable signal system: The Ichimoku indicator shows good reliability in trending markets.
2. Dynamic position management: The strategy automatically adjusts position direction based on market conditions.
3. Reasonable risk control: Confirms trends through moving average crossovers, reducing false breakout losses.
4. Clear operational logic: Well-defined entry and exit signals, suitable for backtesting and live trading.
5. High adaptability: Strategy parameters can be optimized for different market characteristics.

#### Strategy Risks
1. Choppy market risk: May generate frequent false signals in sideways markets.
2. Slippage risk: May face significant slippage losses in fast-moving markets.
3. Trend delay risk: Moving average crossover signals have inherent lag.
4. Money management risk: Requires proper control of position sizing.
5. Market environment risk: Strategy performance may vary under different market conditions.

#### Strategy Optimization Directions
1. Incorporate volume indicators: Confirm signal reliability using volume data.
2. Add trend filters: Filter false signals by combining other technical indicators.
3. Optimize parameter selection: Dynamically adjust moving average periods based on market characteristics.
4. Improve stop-loss mechanism: Implement dynamic stop-losses for risk control.
5. Enhanced market condition assessment: Adjust strategy parameters based on volatility metrics.

#### Summary
This strategy captures market trend transitions through Ichimoku indicator's Conversion and Base Line crossovers, featuring clear logic and easy implementation. Its strength lies in automatically adapting to market changes and timely adjusting position direction. While inherent risks exist, the strategy can achieve stable returns in trending markets through proper optimization and risk control measures. Investors are advised to optimize strategy parameters based on market characteristics and individual risk preferences in practical applications.

#### Source (PineScript)

```pinescript
// backtest
// start: 2024-02-19 00:00:00
// end: 2025-02-16 08:00:00
// period: 4h
// basePeriod: 4h
// exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © pyoungil0842

//@version=6
strategy("Ichimoku Crossover Strategy with Switching", overlay=true)

// Calculation of Ichimoku Cloud elements
tenkanLength = input(9, title="Conversion Line Period")
kijunLength = input(26, title="Base Line Period")

tenkan = ta.sma(ta.highest(high, tenkanLength) + ta.lowest(low, tenkanLength), 2)
kijun = ta.sma(ta.highest(high, kijunLength) + ta.lowest(low, kijunLength), 2)

// Check for crossover signals at the current candle
goldenCross = (tenkan > kijun) and (tenkan[1] <= kijun[1]) // Conversion Line crosses above Base Line
deadCross = (tenkan < kijun) and (tenkan[1] >= kijun[1])   // Conversion Line crosses below Base Line

// Current position status
isLong = strategy.position_size > 0  // Long position status
isShort = strategy.position_size < 0 // Short position status

// Strategy buy/sell conditions
if (goldenCross)
    if (isShort)  // Switch from short to long when a short position exists
        strategy.close("Short")
        strategy.entry("Long", strategy.long)
    else if (strategy.position_size == 0)  // Enter new position if no current position
        strategy.entry("Long", strategy.long)

if (deadCross)
    if (isLong)  // Switch from long to short when a long position exists
        strategy.close("Long")
        strategy.entry("Short", strategy.short)
    else if (strategy.position_size == 0)  // Enter new position if no current position
        strategy.entry("Short", strategy.short)

// Plot Conversion and Base Lines on the chart
plot(tenkan, color=color.blue, title="Conversion Line")
plot(kijun, color=color.red, title="Base Line")

```

#### Detail

https://www.fmz.com/strategy/482445

#### Last Modified

2025-02-18 14:51:56