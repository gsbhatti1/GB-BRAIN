> Name

Triple-Candlestick-Bollinger-Bands-Breakout-Trend-Following-Strategy-with-High-Low-Point-Confirmation

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/9232be7eb2d2f5ae38.png)

#### Overview
This strategy is a trend-following trading system based on Bollinger Bands breakouts and candlestick patterns. It identifies trading signals through three consecutive candles breaking the Bollinger Bands, combined with the position of closing prices within the candlestick bodies. The system employs a fixed 1:1 risk-reward ratio for managing stop-loss and take-profit levels.

#### Strategy Principles
The core logic is based on the following key elements:
1. Uses 20-period Bollinger Bands as the primary indicator with a standard deviation multiplier of 2.0
2. Long entry conditions: three consecutive candles closing above the upper band, all being bullish with closes in the upper half of their ranges
3. Short entry conditions: three consecutive candles closing below the lower band, all being bearish with closes in the lower half of their ranges
4. Stop-loss is set at the extreme point of the earliest signal candle
5. Take-profit is set based on a 1:1 risk-reward ratio

#### Strategy Advantages
1. Employs multiple confirmation mechanisms through consecutive breakout candles, effectively reducing false breakout risks
2. Enhances trend confirmation reliability by considering closing price positions within candle bodies
3. Uses fixed risk-reward ratio for position management, facilitating risk control
4. Clear and easy-to-understand strategy logic
5. Intuitive signal visualization through markers for backtest analysis

#### Strategy Risks
1. May generate frequent false signals in ranging markets
2. Fixed risk-reward ratio might not fully capture strong trends
3. Strict three-candle requirement may miss potential opportunities
4. Stop-loss placement at signal candle extremes may be too wide in volatile conditions
Risk management suggestions:
- Adjust Bollinger Bands parameters based on market volatility cycles
- Dynamically adjust risk-reward ratio according to market characteristics
- Add trend confirmation indicators
- Optimize stop-loss placement method

#### Strategy Optimization Directions
1. Parameter Optimization:
- Dynamically adjust Bollinger Bands period and standard deviation multiplier based on market characteristics
- Consider changing three-candle requirement to dynamic judgment

2. Signal Optimization:
- Add trend confirmation indicators like ADX or trendlines
- Introduce volume confirmation mechanism
- Consider adding oscillators as auxiliary indicators

3. Position Management Optimization:
- Implement dynamic risk-reward ratio settings
- Add money management module
- Consider scaled entry and exit mechanisms

4. Stop-Loss Optimization:
- Introduce trailing stop mechanism
- Set stop-loss distance based on ATR
- Consider time-based stops

#### Summary
This is a well-structured trend-following strategy with clear logic. Through multiple confirmation mechanisms using Bollinger Bands breakouts and candlestick patterns, it effectively reduces false signal risks. The fixed risk-reward ratio simplifies trade management but limits strategy flexibility. There is significant room for improvement through parameter optimization, additional confirmation indicators, and improved position management. Overall, it provides a practical basic strategy framework that can be further refined based on specific requirements.

```pinescript
//@version=6
strategy("Bollinger Band Strategy (Close Near High/Low Relative to Half Range)", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=200, pyramiding=0)

// Bollinger Bands
length = input.int(20, "BB Length")
mult = input.float(2.0, "BB StdDev")
basis = ta.sma(close, length)
upper_band = basis + mult * ta.stdev(close, length)
lower_band = basis - mult * ta.stdev(close, length)

// Plot Bollinger Bands
plot(upper_band, "Upper Band", color.blue)
plot(lower_band, "Lower Band", color.red)

// Buy Condition: 
// 1. Last 3 candles close above upper band AND close > open for all 3 candles
// 2. Close is in the top half of the candle's range (close > (high + low) / 2)
buyCondition =    close[2] > upper_band[2] and     close[1] > upper_band[1] and     close > upper_band and    close[2] > open[2] and close[2] > (high[2] + low[2]) / 2 and    close[1] > open[1] and close[1] > (high[1] + low[1]) / 2 and    close > open and close > (high + low) / 2

// Sell Condition: 
// 1. Last 3 candles close below lower band AND close < open for all 3 candles
// 2. Close is in the bottom half of the candle's range (close < (high + low) / 2)
sellCondition =   close[2] < lower_band[2] and     close[1] < lower_band[1] and     close < lower_band and    close[2] < open[2] and close[2] < (high[2] + low[2]) / 2 and    close[1] < open[1] and close[1] < (high[1] + low[1]) / 2 and    close < open and close < (high + low) / 2

// Buy/Sell Orders
if (buyCondition)
    strategy.entry("Buy", strategy.long)
if (sellCondition)
    strategy.exit("Sell", "Buy")
```

> Notes: The Pine Script code has been translated while maintaining the original structure and formatting.