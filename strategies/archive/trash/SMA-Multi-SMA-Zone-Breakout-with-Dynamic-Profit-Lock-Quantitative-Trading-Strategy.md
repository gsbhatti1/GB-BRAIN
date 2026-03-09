> Name

Multi-SMA Zone Breakout with Dynamic Profit Lock Quantitative Trading Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/6e247c4ff859e0db22.png)

#### Overview
This is a dynamic trend-following trading strategy based on SMA indicators, combining price zones, stochastic indicators, and multiple profit protection mechanisms. The strategy monitors price movements across different zones, integrates short-term and long-term moving average crossover signals, and uses stochastic indicators to determine market conditions and trend strength for efficient trend capture. The strategy incorporates both percentage-based and fixed-point profit-taking mechanisms to effectively balance returns and risks.

#### Strategy Principles
The core logic includes several key components:
1. Uses 19-period and 74-period SMAs to build trend framework
2. Employs 60-period stochastic indicator to judge market conditions, categorizing SMA colors into yellow, green, red, and orange states
3. Divides price zones into 5 important levels for determining price strength
4. Entry conditions require:
   - SMA in green or yellow state
   - Price breakout above orange zone
   - Closing price above short-term SMA
5. Implements two profit-taking mechanisms:
   - Percentage-based drawdown protection from highest price
   - Fixed-point profit lock

#### Strategy Advantages
1. Multiple confirmation mechanisms reduce false signals
2. Dynamic zone division adapts to different market environments
3. Dual profit-taking mechanisms provide better risk control
4. Clear market state classification helps capture market rhythm
5. Real-time trade status monitoring facilitates strategy debugging
6. Combines technical indicators with price action analysis

#### Strategy Risks
1. May generate excessive trades in ranging markets
2. Fixed-point profit taking might miss larger trends
3. Parameter optimization can lead to overfitting
4. Potential profit loss during rapid market reversals
5. Multiple confirmation conditions might miss some trading opportunities
Solutions:
- Add volatility filters
- Dynamically adjust profit-taking parameters
- Enhance market environment recognition
- Optimize exit timing decisions

#### Strategy Optimization Directions
1. Introduce volatility indicators for dynamic parameter adjustment
2. Adapt profit-taking conditions based on market state
3. Add volume confirmation mechanism
4. Incorporate trend strength filters
5. Optimize zone division method considering market characteristics
6. Enhance risk management mechanisms, including:
   - Daily stop loss
   - Maximum drawdown control
   - Position holding time limits

#### Summary
The strategy constructs a comprehensive trading system through the integrated use of multiple technical indicators and price action analysis methods. Its strengths lie in multiple confirmation mechanisms and flexible profit-taking systems, while attention must be paid to the impact of market environment on strategy performance. Through continuous optimization and improved risk management, the strategy shows potential for maintaining stable performance across different market conditions.

#### Source (PineScript)

```pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-18 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy(title="SMA Color Strategy", 
     overlay=true, 
     initial_capital=10000,
     max_bars_back=5000,
     max_labels_count=500,
     max_boxes_count=500,
     default_qty_type=strategy.fixed,
     default_qty_value=1,
     currency=currency.NONE,
     process_orders_on_close=true)

// === INPUTS ===
zoneLength = input.int(20, "Price Zone Length", minval=5)
profitLockPct = input.float(50, "Profit Lock Percentage", minval=1, maxval=100, step=5) / 100
ticksToLock = input.int(12, "Ticks to Activate Lock", minval=1, tooltip="Number of ticks price must move up to activate tick-based lock")
ticksToSecure = input.int(10, "Ticks to Secure", minval=1, tooltip="Number of ticks to lock in once activated")

// Calculate tick values
tickSize = syminfo.mintick
ticksToLockPoints = ticksToLock * tickSize
ticksToSecurePoints = ticksToSecure * tickSize

// Calculate price zones
h = ta.highest(high, zoneLength)
l = ta.lowest(low, zoneLength)
priceRange = h - l
lvl5 = h
lvl4 = l + (priceRange * 0.75)  // Orange line
lvl3 = l + (priceRange * 0.50)  // Yellow line
lvl2 = l + (priceRange * 0.25)  // Green line
lvl1 = l

// Calculate SMAs
sma19 = ta.sma(close, 19)
sma74 = ta.sma(close, 74)

// Stochastic calculation for color logic
k = ta.stoch(close, high, low, 60)
d = ta.sma(k, 10)

// SMA Color Logic with state tracking
var color currentSMAColor = color.orange
var color previousSMAColor = color.orange
var string currentColorName = "ORANGE"
var string previousColorName = "ORANGE"

smaColor = if d >= 80 or d <= 20
    color.
```