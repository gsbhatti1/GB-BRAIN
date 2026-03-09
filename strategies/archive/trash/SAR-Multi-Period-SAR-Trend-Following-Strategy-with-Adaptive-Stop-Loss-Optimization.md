> Name

Multi-Period SAR Trend Following Strategy with Adaptive Stop Loss Optimization

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1d6b2f5012e5925e0fc.png)

#### Overview
This strategy is a deep optimization of the traditional Parabolic SAR (Stop and Reverse) indicator, combining multi-period trend judgment and adaptive stop-loss mechanisms. The strategy employs a dynamic Acceleration Factor (AF) adjustment method, tracking market trends through continuous updates of Extreme Points (EP) to achieve precise capture of upward trends and risk control.

#### Strategy Principles
The core logic of the strategy is based on the following key elements:
1. Dynamic SAR Calculation: Uses three parameters - initial AF, increment value, and maximum value - to dynamically adjust SAR values based on trend strength.
2. Trend Determination Mechanism: Judges trend direction by comparing SAR values with price positions, triggering trend reversal signals when SAR crosses price.
3. Entry Logic: Places entry orders using next period's predicted SAR value as stop-loss when an uptrend is confirmed and no position is held.
4. Stop-Loss Optimization: Uses extremes from the previous 1-2 candles as SAR adjustment benchmark, improving stop-loss accuracy and timeliness.

#### Strategy Advantages
1. Strong Adaptability: Parameters automatically adjust to market volatility through dynamic AF adjustment.
2. Comprehensive Risk Control: Uses predictive SAR values for stop-loss, ensuring forward-looking and effective risk management.
3. Accurate Trend Capture: Multiple trend confirmation mechanisms reduce risks from false breakouts.
4. Rigorous Calculation Logic: Employs variable state maintenance mechanism, ensuring strategy stability in historical backtesting.

#### Strategy Risks
1. Sideways Market Risk: Frequent false signals may trigger consecutive stop-losses in ranging markets.
Solution: Introduce volatility filters to reduce trading frequency in low volatility environments.
2. Slippage Impact: Predictive SAR stops may face slippage risks in highly volatile markets.
Solution: Set reasonable slippage tolerance and adjust parameters based on instrument characteristics.
3. Trend Reversal Delay: Stop-loss may lag in sharp reversal situations.
Solution: Incorporate short-period momentum indicators to improve stop-loss sensitivity.

#### Strategy Optimization Directions
1. Multi-Period Synergy: Add trend confirmation mechanisms across multiple timeframes to improve signal reliability.
2. Dynamic Parameter Optimization: Dynamically adjust AF parameters based on market volatility.
3. Stop-Loss Mechanism Enhancement: Introduce ATR-based dynamic stop-loss bands for improved flexibility.
4. Position Management Optimization: Add volatility-based dynamic position management mechanism.

#### Summary
The strategy effectively combines trend following and risk control through deep optimization of the classic PSAR indicator. Its adaptive features and comprehensive stop-loss mechanism provide strong practical application value. Through the suggested optimization directions, the strategy's stability and profitability can be further enhanced.

#### Source (PineScript)

```pinescript
/*backtest
start: 2024-02-19 00:00:00
end: 2025-02-16 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("A股抛物线策略（仅做多）- 完全移除SAR绘图", overlay=true)

// Parameter settings
start     = input.float(0.02, "起始加速因子")
increment = input.float(0.02, "加速因子增量")
maximum   = input.float(0.2,  "加速因子最大值")

// Define variables (var ensures that the variables maintain state throughout the entire historical data)
var bool   uptrend    = true    // Default initialization as an uptrend
var float  EP         = na      // Extreme Point: highest price in an uptrend, lowest price in a downtrend
var float  SAR        = na      // SAR value of the current bar
var float  AF         = start   // Current acceleration factor
var float  nextBarSAR = na      // Predicted SAR of the next bar

//【1】Initialization: For the first bar (bar_index == 0)
if bar_index == 0
    // Initialize with the first bar's closing price
    SAR        := close
    nextBarSAR := close
    EP         := close
    uptrend    := true

//【2】Calculate SAR starting from the second bar (bar_index >= 1)
if bar_index >= 1
    // First, assign the SAR value from the previous bar to the current SAR
    SAR := nz(nextBarSAR, SAR)
    
    // Initialize the second bar (bar_index == 1), using the high and low prices from the previous bar (bar_index == 0)
    if bar_index == 1
        if close > close[1]
            uptrend := true
            EP      := high
            SAR     := low[1]
        else
            uptrend := false
            EP      := low
            SAR     := high[1]
        AF := start
        nextBarSAR := SAR + AF * (EP - SAR)
    else
        // Record the first bar of trend reversal for subsequent judgment
        var bool firstTrendBar = false
        firstTrendBar := false
        
        // Detect trend reversal:
        // In an uptrend, if the current SAR is above the lowest price, a reversal is considered to have occurred
        if uptrend
            if SAR > low
                firstTrendBar := true
                uptrend     := false
                // During a reversal, SAR takes the higher value between the last extreme and the current highest price, and the extreme is set to the current lowest price
                SAR         := math.max(EP,