> Name

EMA-SMA Trend Following with Swing Trading Strategy Combined with Volume Filtering and Percentage Take-Profit and Trailing Stop Loss System - EMA-SMA-Trend-Following-with-Swing-Trading-Strategy-Combined-Volume-Filter-and-Percentage-Take-Profit-Stop-Loss-System

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/f82369ecfc33395bad.png)

[trans]
#### Overview
This strategy is a comprehensive trading system that combines trend following with swing trading methods, utilizing EMA and SMA crossovers, swing high/low identification, volume filtering, and percentage-based take-profit and trailing stop-loss mechanisms. The strategy emphasizes multi-dimensional signal confirmation, enhancing trading accuracy through the synergy of technical indicators.

#### Strategy Principles
The strategy employs a multi-layered signal filtering mechanism, starting with EMA(10) and SMA(21) crossovers for basic trend determination, then using 6-bar left/right pivot point breakouts for entry timing, while requiring volume above the 200-period moving average to ensure sufficient liquidity. The system uses 2% take-profit and 1% trailing stop-loss for risk management. Long positions are initiated when price breaks above swing highs with volume confirmation; short positions are taken when price breaks below swing lows with volume confirmation.

#### Strategy Advantages
1. Multiple signal confirmation reduces false signals through trend, price breakout, and volume expansion verification
2. Flexible profit/loss management using percentage-based take-profit with trailing stop-loss
3. Comprehensive visualization system for monitoring trades and signals
4. High customizability with adjustable key parameters
5. Systematic risk management through preset stop-loss and take-profit levels

#### Strategy Risks
1. Potential false breakouts in ranging markets
2. Volume filtering may miss some valid signals
3. Fixed percentage take-profit might exit too early in strong trends
4. Moving average system has inherent lag in quick reversals
5. Need to consider impact of trading costs on strategy returns

#### Optimization Directions
1. Introduce volatility adaptation for dynamic adjustment of take-profit/stop-loss
2. Add trend strength filtering to avoid trading in weak trends
3. Optimize volume filtering algorithm considering relative volume changes
4. Implement time-based filters to avoid unfavorable trading periods
5. Consider market regime classification for parameter adaptation

#### Summary
The strategy builds a complete trading system through moving averages, price breakouts, and volume verification, suitable for medium to long-term trend following. Its strengths lie in multiple signal confirmation and comprehensive risk management, though performance in ranging markets needs attention. Through the suggested optimizations, particularly in adaptability, the strategy has room for improvement in stability and performance.

||

#### Overview
This strategy is a comprehensive trading system that combines trend following with swing trading methods, utilizing EMA and SMA crossovers, swing high/low identification, volume filtering, and percentage-based take-profit and trailing stop-loss mechanisms. The strategy emphasizes multi-dimensional signal confirmation, enhancing trading accuracy through the synergy of technical indicators.

#### Strategy Principles
The strategy employs a multi-layered signal filtering mechanism, starting with EMA(10) and SMA(21) crossovers for basic trend determination, then using 6-bar left/right pivot point breakouts for entry timing, while requiring volume above the 200-period moving average to ensure sufficient liquidity. The system uses 2% take-profit and 1% trailing stop-loss for risk management. Long positions are initiated when price breaks above swing highs with volume confirmation; short positions are taken when price breaks below swing lows with volume confirmation.

#### Strategy Advantages
1. Multiple signal confirmation reduces false signals through trend, price breakout, and volume expansion verification
2. Flexible profit/loss management using percentage-based take-profit with trailing stop-loss
3. Comprehensive visualization system for monitoring trades and signals
4. High customizability with adjustable key parameters
5. Systematic risk management through preset stop-loss and take-profit levels

#### Strategy Risks
1. Potential false breakouts in ranging markets
2. Volume filtering may miss some valid signals
3. Fixed percentage take-profit might exit too early in strong trends
4. Moving average system has inherent lag in quick reversals
5. Need to consider impact of trading costs on strategy returns

#### Optimization Directions
1. Introduce volatility adaptation for dynamic adjustment of take-profit/stop-loss
2. Add trend strength filtering to avoid trading in weak trends
3. Optimize volume filtering algorithm considering relative volume changes
4. Implement time-based filters to avoid unfavorable trading periods
5. Consider market regime classification for parameter adaptation

#### Summary
The strategy builds a complete trading system through moving averages, price breakouts, and volume verification, suitable for medium to long-term trend following. Its strengths lie in multiple signal confirmation and comprehensive risk management, though performance in ranging markets needs attention. Through the suggested optimizations, particularly in adaptability, the strategy has room for improvement in stability and performance.

||

```pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-09 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
// Strategy combining EMA/SMA Crossover, Swing High/Low, Volume Filtering, and Percentage TP & Trailing Stop
strategy("Swing High/Low Strategy with Volume, EMA/SMA Crossovers, Percentage TP and Trailing Stop", overlay=true)

// --- Inputs ---
source = close
TITLE = input(false, title='Enable Alerts & Background Color for EMA/SMA Crossovers')
turnonAlerts = input(true, title='Turn on Alerts?')
colorbars = input(true, title="Color Bars?")
turnonEMASMA = input(true, title='Turn on EMA1 & SMA2?')
backgroundcolor = input(false, title='Enable Background Color?')

// EMA/SMA Lengths
emaLength = input.int(10, minval=1, title='EMA Length')
smaLength = input.int(21, minval=1, title='SMA Length')
ema1 = ta.ema(source, emaLength)
sma2 = ta.sma(source, smaLength)

// Swing High/Low Lengths
leftBars = input.int(6, title="Left Bars for Swing High/Low", minval=1)
rightBars = input.int(6, title="Right Bars for Swing High/Low", minval=1)

// Volume MA Length
volMaLength = input.int(200, title="Volume Moving Average Length")

// Percentage Take Profit with hundredth place adjustment
takeProfitPercent = input.float(2.00, title="Take Profit Percentage (%)", minval=0.01, step=0.01) / 100

// Trailing Stop Loss Option
useTrailingStop = input.bool(true, title="Enable Trailing Stop Loss?")
trailingStopPercent = input.float(1.00, title="Trailing Stop Loss Percentage (%)", minval=0.01, step=0.01) / 100

// --- Swing High/Low Logic ---
pivotHigh(_leftBars, _rightBars) =>
    ta.pivothigh(_leftBars, _rightBars)

pivotLow(_leftBars, _rightBars) =>
    ta.pivotlow(_leftBars, _rightBars)

ph = fixnan(pivotHigh(leftBars, rightBars))
pl = fixnan(pivotLow(leftBars, rightBars))

// --- Volume Condition ---
volMa = ta.sma(volume, volMaLength)

// Declare exit conditions as 'var' so they are initialized
var bool longExitCondition = na
var bool shortExitCondition = na

// --- Long Entry Condition: Close above Swing High & Volume >= 200 SMA
longCondition = ta.crossover(ema1, sma2) and ta.close > ph and volMa > volMaLength

// --- Short Entry Condition: Close below Swing Low & Volume >= 200 SMA
shortCondition = ta.crossunder(ema1, sma2) and ta.close < pl and volMa > volMaLength

// --- Long Exit Condition: Take Profit and Trailing Stop
if (longCondition)
    strategy.entry("Long", strategy.long)
    longExitCondition := false

    if (close > (ph * (1 + takeProfitPercent)))
        strategy.exit("Take Profit", "Long")
        longExitCondition := true

    if (useTrailingStop)
        if (close < (ph * (1 - trailingStopPercent)))
            strategy.exit("Trailing Stop", "Long")
            longExitCondition := true

// --- Short Exit Condition: Take Profit and Trailing Stop
if (shortCondition)
    strategy.entry("Short", strategy.short)
    shortExitCondition := false

    if (close < (pl * (1 - takeProfitPercent)))
        strategy.exit("Take Profit", "Short")
        shortExitCondition := true

    if (useTrailingStop)
        if (close > (pl * (1 + trailingStopPercent)))
            strategy.exit("Trailing Stop", "Short")
            shortExitCondition := true

// --- Background Color for EMA/SMA Crossovers
if (TITLE)
    line.new(x1=bar_index, y1=ema1, x2=bar_index, y2=ema1, color=color.new(color.blue, 0), width=2, extend=extend.both)
    line.new(x1=bar_index, y1=sma2, x2=bar_index, y2=sma2, color=color.new(color.red, 0), width=2, extend=extend.both)
    if (ta.crossover(ema1, sma2))
        barcolor(color.new(color.green, 50))
    if (ta.crossunder(ema1, sma2))
        barcolor(color.new(color.red, 50))
```

Note: The code block has been completed with the missing logic to handle the long and short exit conditions.