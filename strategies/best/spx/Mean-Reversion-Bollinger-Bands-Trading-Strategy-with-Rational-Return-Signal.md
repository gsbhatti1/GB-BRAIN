> Name

Mean-Reversion-Bollinger-Bands-Trading-Strategy-with-Rational-Return-Signal

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1efe4c5d9655f94dee3.png)

#### Overview
This strategy is a quantitative trading system based on Bollinger Bands and price mean reversion principles. It monitors the deviation of prices from moving averages, combined with breakout signals from Bollinger Bands upper and lower bounds, to trade when expecting price regression after market overbought/oversold conditions. The strategy uses percentage thresholds to measure price deviations and sets reasonable trigger conditions to filter out false signals, thereby improving trading accuracy.

#### Strategy Principles
The core logic of the strategy is based on the following key elements:
1. Uses a 20-day moving average as the middle band, paired with 2 standard deviations to construct Bollinger Bands.
2. Introduces a 3.5% price deviation threshold to identify significant divergence.
3. Tracks the status of price deviation through an `is_outside` variable.
4. Triggers trading signals when prices return within the Bollinger Bands range.
5. Specific trading rules:
   - Long position is initiated when the price returns from a deviated state and breaks above the upper band.
   - Short position is initiated when the price returns from a deviated state and breaks below the lower band.

#### Strategy Advantages
1. Robust Mean Reversion Logic
   - Based on the statistical principle that prices will eventually revert to their mean.
   - Ensures significant trading opportunities through deviation thresholds.
2. Comprehensive Risk Control
   - Bollinger Bands provide a clear reference for volatility ranges.
   - Tracking of deviation status avoids trading during extreme volatility periods.
3. Strong Parameter Adjustability
   - Bollinger Bands parameters can be adjusted according to the characteristics of different instruments.
   - Deviation thresholds can be set based on risk preferences.

#### Strategy Risks
1. Trend Market Ineffectiveness Risk
   - May generate frequent false signals in strong trend markets.
   - It is recommended to add a trend filter to identify market conditions.
2. Parameter Sensitivity Risk
   - Improper parameter settings may affect the performance of the strategy.
   - Requires optimization through historical data backtesting.
3. Slippage Cost Risk
   - Frequent trading may incur high transaction costs.
   - It is recommended to add position time limits and cost controls.

#### Strategy Optimization Directions
1. Add Market Environment Recognition
   - Introduce trend strength indicators like ADX for dynamic parameter adjustments based on market conditions.
2. Improve Stop-Loss and Take-Profit Mechanisms
   - Set dynamic stops based on ATR (Average True Range).
   - Introduce trailing stops to protect profits.
3. Optimize Trading Frequency
   - Add minimum position holding time limits.
   - Set trading intervals to control costs.

#### Summary
This strategy captures market overbought/oversold opportunities through Bollinger Bands and mean reversion principles, effectively controlling trading risks with reasonable deviation thresholds and status tracking mechanisms. The strategy framework is scalable and can adapt to different market environments through parameter optimization and functional enhancements. It is recommended to focus on risk control in live trading and adjust parameters based on specific instrument characteristics.

#### Source (PineScript)

```pinescript
/*backtest
start: 2024-12-06 00:00:00
end: 2025-01-04 08:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Mean-Reversion-Bollinger-Bands-Trading-Strategy-with-Rational-Return-Signal", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=200)

// Bollinger Bands configuration
length = input.int(20, title="Moving Average Period")
mult = input.float(2.0, title="Standard Deviation Multiplier")
bbBasis = ta.sma(close, length)
bbUpper = bbBasis + mult * ta.stdev(close, length)
bbLower = bbBasis - mult * ta.stdev(close, length)

// Distance from mean configuration
percent_threshold = input.float(3.5, title="Distance from Mean (%)") / 100

dist_from_mean = 0.0
trigger_condition = false
if not na(bbBasis)
    dist_from_mean := math.abs(close - bbBasis) / bbBasis
    trigger_condition := dist_from_mean >= percent_threshold

// Variables to identify the deviation state
var bool is_outside = false
var color candle_color = color.new(color.white, 0)

if trigger_condition
    is_outside := true

if is_outside and close <= bbUpper and close >= bbLower
    is_outside := false
    candle_color := color.new(color.blue, 0) // Assign a valid color
else
    candle_color := color.new(color.white, 0)

// Apply color to candles
barcolor(candle_color)

// Plot Bollinger Bands
plot(bbBasis, color=color.yellow, title="Middle Band")
plot(bbUpper, color=color.red, title="Upper Band")
plot(bbLower, color=color.green, title="Lower Band")

// Entry and Exit Logic
longCondition = not is_outside and close > bbUpper
if (longCondition)
    strategy.entry("Buy", strategy.long)
```

(Note: The code snippet was cut off at the end. You can continue from where it left off.)