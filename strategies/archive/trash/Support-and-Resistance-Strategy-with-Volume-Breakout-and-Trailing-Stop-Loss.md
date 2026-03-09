> Name

Support-and-Resistance-Strategy-with-Volume-Breakout-and-Trailing-Stop-Loss

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/177c5bdb71e581a2b8a.png)
[trans]

## Overview

The main idea of this strategy is to combine support and resistance levels with volume breakouts to determine entry opportunities, and use the ATR indicator to dynamically adjust stop loss for profit taking, in order to capture more potential profits.

## Strategy Logic

The strategy consists of the following main logics:

1. Use `ta.pivothigh` and `ta.pivotlow` functions to calculate the highest price of previous L_Bars candles and the lowest price of previous R_Bars candles as resistance and support levels.
2. When the close price crosses above the resistance level and volume breaks above the volumeRange threshold, go long; when the close price crosses below the support level and volume breaks above the volumeRange threshold, go short.
3. After a long entry, set stop loss at `close-ATR_LO`. After a short entry, set stop loss at `close+ATR_SH`, achieving dynamic trailing stop loss adjustment.
4. Only take the first signal within trading hours (0915-1445) each day. No new orders after reaching the daily risk limit defined by the `risk` input.

## Advantage Analysis

1. Use support and resistance theory combined with volume indicators to improve entry accuracy.
2. Trailing stop loss based on ATR can flexibly adjust stop levels based on market volatility, reducing the chance of profit retracement.
3. Appropriate control over daily trade times and per trade risk helps to catch trends and avoid excessive stop losses.

## Risk Analysis

1. Support and resistance levels may fail and provide ineffective entry signals.
2. An ATR multiplier set too high may result in a stop loss that is too far away, increasing the risk of loss.
3. Volume threshold set too low may miss opportunities; set too high may cause false signals.

**Solutions:**

- Adjust support and resistance parameters based on different product characteristics.
- Optimize ATR multipliers and volume thresholds.
- Add other indicators to confirm entry signals.

## Optimization Directions

1. Incorporate additional indicators like moving averages to assist in determining entry signals.
2. Optimize parameters such as ATR multipliers and volume thresholds.
3. Use machine learning algorithms to achieve dynamic parameter optimization.
4. Expand the strategy to other products to find parameter patterns.

## Summary

The strategy integrates various analytical tools, applying support and resistance levels, volume analysis, and stop loss methods, achieving good backtest results. However, uncertainties may exist in live trading, requiring further enhancements such as parameter optimization and additional entry confirmation indicators to improve real-world performance. Overall, the strategy is clear in logic and easy to understand, providing a good reference case for quantitative trading strategies.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|10|L_Bars|
|v_input_int_2|15|R_Bars|
|v_input_int_3|20|Volume Break [threshold]|
|v_input_int_4|150|PRICE CROSS EMA|
|v_input_float_1|3.2|_ATR LONG|
|v_input_float_2|3.2|_ATR SHORT|
|v_input_float_3|200|RISK|

> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-03 00:00:00
end: 2024-01-10 00:00:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//   ____________                _________                      _____________
//  |____________|             ||________|                      ||__________|
//       ||            ____    ||        ||                     ||                    ______ ________    _____ ________
//       ||    |   || ||       ||________|| |   || ||    ||     ||     |   ||   /\\   |   // |______| || ||    |______|
//       ||    |===|| |===     ||__________ |   || ||    ||     ||     |===||  /__\\  |===      ||    ||   \\     ||
//       ||    |   || ||___    ||        || |___|| ||___ ||___  ||     |   || /    \\ |   \\    ||    || ___||    ||
//       ||                    ||________||                     ||__________
//       ||                    ||________|                      ||__________|
  
//@version=5
strategy("Support and Resistance Strategy [5MIN TF]", overlay=true)
L_Bars = input.int(defval=10, minval=1, maxval=50, step=1)
R_Bars = input.int(defval=15, minval=1, maxval=50, step=1)
volumeRange = input.int(20, title='Volume Break [threshold]', minval=1)

// ═══════════════════════════ //
// ——————————> INPUT <——————— //
// ═══════════════════════════ //

EMA1 = input.int(title='PRICE CROSS EMA', defval=150, minval=10, maxval=400)
factor1 = input.float(title='_ATR LONG', defval=3.2, minval=1, maxval=5, step=0.1, tooltip="ATR TRAIL LONG")
factor2 = input.float(title='_ATR SHORT', defval=3.2, minval=1, maxval=5, step=0.1, tooltip="ATR TRAIL SHORT")
risk = input.float(title='RISK', defval=200)
```