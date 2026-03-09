> Name

Multi-Dynamic-Indicator-Combination-Strategy

> Author

ianzeng123

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/2d8f677d7a2dc747807c9.png)
![IMG](https://www.fmz.com/upload/asset/2d8e3ef393a4613abdc3e.png)


#### Overview

This article introduces a composite trading strategy combining Bollinger Bands and SuperTrend indicators. The strategy aims to provide more precise market entry and exit signals by integrating multiple technical analysis tools while reducing trading risks.

#### Strategy Principle

The strategy's core consists of two main parts: Bollinger Bands and SuperTrend indicators.

1. **Bollinger Bands Calculation:**
   - Uses configurable moving average (MA) to calculate the baseline
   - Generates upper and lower bands based on standard deviation multiplier
   - Supports multiple moving average types: Simple Moving Average (SMA), Exponential Moving Average (EMA), Smoothed Moving Average (SMMA), Weighted Moving Average (WMA), and Volume Weighted Moving Average (VWMA)

2. **SuperTrend Component:**
   - Calculates stop-loss levels using Average True Range (ATR)
   - Dynamically determines market trend direction
   - Generates buy and sell signals based on trend changes

#### Strategy Advantages

1. **Multi-Indicator Combination:** Improves signal accuracy by combining Bollinger Bands and SuperTrend
2. **Flexible Configuration:** Customizable moving average types, parameters, and calculation methods
3. **Dynamic Stop-Loss:** ATR-based stop-loss mechanism effectively controls risk
4. **Visual Enhancement:** Provides trend state filling and signal labels
5. **Risk Management:** Percentage position management and pyramid trading restrictions

#### Strategy Risks

1. **Parameter Sensitivity:** Parameters may require frequent adjustments in different market environments
2. **Backtesting Limitations:** Historical performance does not guarantee future market results
3. **Position Switching Risk:** Frequent position changes may increase trading costs
4. **Indicator Lag:** Technical indicators have inherent signal delays

#### Strategy Optimization Directions

1. **Introduce Machine Learning Algorithms for Dynamic Parameter Optimization**
2. **Add Additional Filtering Conditions, Such as Volume Confirmation**
3. **Develop Multi-Timeframe Verification Mechanisms**
4. **Optimize Risk Management Module with More Precise Position Control Strategies**

#### Summary

This is a trading strategy combining multiple dynamic indicators, providing a relatively comprehensive trading signal system through the combination of Bollinger Bands and SuperTrend. The strategy's core lies in balancing signal accuracy and risk management, but still requires continuous optimization and adjustment according to different market environments.

||

#### Overview

This article introduces a composite trading strategy combining Bollinger Bands and SuperTrend indicators. The strategy aims to provide more precise market entry and exit signals by integrating multiple technical analysis tools while reducing trading risks.

#### Strategy Principle

The strategy's core consists of two main parts: Bollinger Bands and SuperTrend indicators.

1. **Bollinger Bands Calculation:**
   - Uses configurable moving average (MA) to calculate the baseline
   - Generates upper and lower bands based on standard deviation multiplier
   - Supports multiple moving average types: Simple Moving Average (SMA), Exponential Moving Average (EMA), Smoothed Moving Average (SMMA), Weighted Moving Average (WMA), and Volume Weighted Moving Average (VWMA)

2. **SuperTrend Component:**
   - Calculates stop-loss levels using Average True Range (ATR)
   - Dynamically determines market trend direction
   - Generates buy and sell signals based on trend changes

#### Strategy Advantages

1. **Multi-Indicator Combination:** Improves signal accuracy by combining Bollinger Bands and SuperTrend
2. **Flexible Configuration:** Customizable moving average types, parameters, and calculation methods
3. **Dynamic Stop-Loss:** ATR-based stop-loss mechanism effectively controls risk
4. **Visual Enhancement:** Provides trend state filling and signal labels
5. **Risk Management:** Percentage position management and pyramid trading restrictions

#### Strategy Risks

1. **Parameter Sensitivity:** Parameters may require frequent adjustments in different market environments
2. **Backtesting Limitations:** Historical performance does not guarantee future market results
3. **Position Switching Risk:** Frequent position changes may increase trading costs
4. **Indicator Lag:** Technical indicators have inherent signal delays

#### Strategy Optimization Directions

1. **Introduce Machine Learning Algorithms for Dynamic Parameter Optimization**
2. **Add Additional Filtering Conditions, Such as Volume Confirmation**
3. **Develop Multi-Timeframe Verification Mechanisms**
4. **Optimize Risk Management Module with More Precise Position Control Strategies**

#### Summary

This is a trading strategy combining multiple dynamic indicators, providing a relatively comprehensive trading signal system through the combination of Bollinger Bands and SuperTrend. The strategy's core lies in balancing signal accuracy and risk management, but still requires continuous optimization and adjustment according to different market environments.

||

```pinescript
//@version=6
strategy("Combined BB & New SuperTrend Strategy", overlay=true, initial_capital=100000, default_qty_type=strategy.percent_of_equity, default_qty_value=10, pyramiding=0)

//============================
// Bollinger Bands Parameters
//============================
lengthBB   = input.int(20, minval=1, title="BB Length")
maType     = input.string("SMA", "BB Basis MA Type", options=["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"])
srcBB      = input(close, title="BB Source")
multBB     = input.float(2.0, minval=0.001, maxval=50, title="BB StdDev Multiplier")
offsetBB   = input.int(0, title="BB Offset", minval=-500, maxval=500)

// Moving average function based on chosen type
ma(source, length, _type) =>
    switch _type
        "SMA"         => ta.sma(source, length)
        "EMA"         => ta.ema(source, length)
        "SMMA (RMA)"  => ta.rma(source, length)
        "WMA"         => ta.wma(source, length)
        "VWMA"        => ta.vwma(source, length)

// Bollinger Bands calculations
basis   = ma(srcBB, lengthBB, maType)
dev     = multBB * ta.stdev(srcBB, lengthBB)
upperBB = basis + dev
lowerBB = basis - dev

// Plot Bollinger Bands
plot(basis, title="BB Basis", color=color.blue, offset=offsetBB)
p1 = plot(upperBB, title="BB Upper", color=color.red, offset=offsetBB)
p2 = plot(lowerBB, title="BB Lower", color=color.green, offset=offsetBB)
fill(p1, p2, title="BB Fill", color=color.new(color.blue, 90))

//============================
// New SuperTrend Parameters & Calculations
// (Based on the new script you provided)
//============================
st_length         = input.int(title="ATR Period", defval=22)
st_mult           = input.float(title="ATR Multiplier", step=0.1, defval=3)
st_src            = input.source(title="SuperTrend Source", defval=hl2)
st_wicks          = input.bool(title="Take Wicks into Account?", defval=true)
st_showLabels     = input.bool(title="Show Buy/Sell Labels?", defval=true)
st_highlightState = input.bool(title="Highlight State?", defval=true)

// Calculate ATR component for SuperTrend
st_atr = st_mult * ta.atr(st_length)

// Price selection based on whether wicks are taken into account
st_high = st_wicks ? high : max(high, upperBB)
st_low  = st_wicks ? low  : min(low,  lowerBB)

// SuperTrend calculation
super_trend = na
super_trend := ta.crossover(st_atr * st_mult, st_low) ? st_low :
               ta.crossunder(st_atr * st_mult, st_high) ? st_high :
               na

// Plot SuperTrend
plot(super_trend, title="SuperTrend", color=color.orange)
```