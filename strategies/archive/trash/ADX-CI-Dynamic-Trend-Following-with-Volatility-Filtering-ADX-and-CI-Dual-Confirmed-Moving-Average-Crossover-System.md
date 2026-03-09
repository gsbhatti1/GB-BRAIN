> Name

Dynamic Trend Following with Volatility Filtering Strategy Based on ADX and CI Dual Confirmation - Dynamic-Trend-Following-with-Volatility-Filtering-ADX-and-CI-Dual-Confirmed-Moving-Average-Crossover-System

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d90197a831ab876063b4.png)
![IMG](https://www.fmz.com/upload/asset/2d91683d2eb8d7978acdd.png)


#### Overview
This strategy combines moving average crossover signals with market state filtering. It captures market trends through the intersection of 9-period and 21-period Simple Moving Averages (SMA) while utilizing the Average Directional Index (ADX) and Choppiness Index (CI) to filter market conditions, ensuring trades are only executed in clear trending markets with favorable volatility characteristics. This approach effectively combines traditional trend-following strategies with modern technical indicators to provide a more robust trading framework.

#### Strategy Principles
The core logic consists of three key components:
1. Trend Signal Generation: Uses 9-period and 21-period SMA crossovers to determine trend direction and generate basic trading signals.
2. Trend Strength Confirmation: Validates trend strength through the ADX indicator (threshold set at 20) to ensure trading only in clear trending market conditions.
3. Market Volatility Filtering: Incorporates the Choppiness Index (threshold at 50) to identify market volatility characteristics and avoid trading in highly choppy markets.

The strategy employs optimized technical indicator calculations, including custom sum functions, highest value and lowest value calculations, and standardized True Range (TR) calculations, ensuring signal accuracy and computational efficiency.

#### Strategy Advantages
1. Multiple Confirmation Mechanism: Combines MA crossover, ADX, and CI triple filtering to significantly improve trading signal reliability.
2. High Adaptability: Strategy parameters can be adjusted for different market environments, providing good adaptability.
3. Comprehensive Risk Control: Effectively reduces false breakout risks by filtering out high volatility periods using the CI index.
4. High Computational Efficiency: Employs optimized calculation methods, particularly excelling in historical data processing.

#### Strategy Risks
1. Parameter Sensitivity: Strategy effectiveness highly depends on ADX and CI threshold settings, different market environments may require different parameter configurations.
2. Lag Issues: Multiple moving average indicators may result in delayed signals.
3. Sideways Market Performance: May miss some short-term trading opportunities in range-bound markets.
4. Computational Complexity: Multiple indicator calculations increase strategy complexity, potentially affecting real-time trading execution efficiency.

#### Strategy Optimization Directions
1. Dynamic Parameter Adjustment: Introduce adaptive parameter adjustment mechanisms to dynamically modify ADX and CI thresholds based on market conditions.
2. Stop Loss Optimization: Add dynamic stop-loss mechanisms, potentially designing more flexible stop-loss strategies based on ATR or Volatility Bands.
3. Signal Confirmation Enhancement: Consider adding volume confirmation mechanisms to further improve signal reliability.
4. Computational Efficiency Improvement: Optimize indicator calculation methods, especially performance in handling long-period data.

#### Summary
This strategy constructs a complete trading system by combining classical moving average crossover strategies with modern technical indicators. It focuses not only on trend capture but also pays special attention to market environment suitability, enhancing trading stability through multiple filtering mechanisms. While there are some parameter sensitivity and lag issues, there is significant room for improvement through the proposed optimization directions. Overall, this is a logically complete and highly practical trading strategy.

||

#### Source (PineScript)

```pinescript
/*backtest
start: 2024-02-22 00:00:00
end: 2024-12-06 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=6
strategy("MA9/MA21 Cross with ADX & CHOP Filter", overlay=true, initial_capital=10000, currency=currency.USD)

// ─── CUSTOM FUNCTIONS ──────────────────────────────────────────────────────
// Custom function to compute the sum over the last 'len' bars.
f_sum(src, len) =>
    s = 0.0
    for i = 0 to len - 1
        s += src[i]
    s

// Custom function to compute the highest value over the last 'len' bars.
f_highest(src, len) =>
    h = src[0]
    for i = 1 to len - 1
        h := math.max(h, src[i])
    h

// Custom function to compute the lowest value over the last 'len' bars.
f_lowest(src, len) =>
    l = src[0]
    for i = 1