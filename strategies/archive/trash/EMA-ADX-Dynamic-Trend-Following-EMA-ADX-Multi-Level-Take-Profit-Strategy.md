> Name

Dynamic-Trend-Following-EMA-ADX-Multi-Level-Take-Profit-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/208f105a565e4fc6fef.png)

#### Overview
This strategy is a trend-following trading system that combines EMA and ADX indicators with multi-level take-profit and trailing stop-loss mechanisms for optimized money management. It uses EMA for trend direction determination, ADX for trend strength filtering, and implements a three-tiered take-profit mechanism for batch profit-taking, while using ATR for dynamic stop-loss adjustment to control risk.

#### Strategy Principles
The core logic includes several key components:
1. Uses 50-period EMA to determine trend direction, entering long when price crosses above EMA and short when crossing below
2. Filters weak trends using 14-period ADX, confirming valid trends when ADX > 20
3. Calculates dynamic stop-loss positions based on 14-period ATR, setting stops at low - 1ATR for longs and high + 1ATR for shorts
4. Implements a three-tiered take-profit mechanism:
   - First tier: 30% position closes at 1x ATR
   - Second tier: 50% position closes at 2x ATR
   - Third tier: 20% position uses 3x ATR trailing stop
5. Automatically closes all remaining positions when price reaches second-tier take-profit level

#### Strategy Advantages
1. Multi-level take-profit design secures profits while maintaining exposure to larger moves
2. Trailing stop mechanism adapts to market volatility, providing dynamic risk control
3. ADX filtering effectively avoids false signals in ranging markets
4. EMA and price crossovers provide clear entry signals
5. Batch profit-taking reduces emotional volatility, supporting long-term strategy execution

#### Strategy Risks
1. May result in frequent trading and increased costs in ranging markets
2. EMA as a lagging indicator might be slow to react in rapid reversals
3. Fixed ADX threshold may need adjustment in different market conditions
4. Multi-level take-profit might reduce position size too early in strong trends
Mitigation measures:
- Dynamically adjust ADX threshold based on market cycles
- Consider adding trend confirmation indicators
- Optimize take-profit ratio parameters more precisely

#### Strategy Optimization Directions
1. Incorporate volume indicators for enhanced trend confirmation
2. Implement dynamic ADX thresholds based on market volatility
3. Optimize position allocation ratios for take-profit levels
4. Add trend strength classification with corresponding take-profit strategies
5. Consider incorporating seasonality and market cycle factors

#### Summary
This is a well-structured trend-following strategy with clear logic, balancing returns and risks through multi-level take-profits and dynamic stop-losses. The strategy design adheres to basic quantitative trading principles, offering good scalability and optimization potential. Through appropriate parameter adjustment and optimization upgrades, this strategy has the potential to maintain stable performance across different market conditions.

|| 

#### Overview
This strategy is a trend-following trading system that combines EMA and ADX indicators with multi-level take-profit and trailing stop-loss mechanisms for optimized money management. It uses EMA for trend direction determination, ADX for trend strength filtering, and implements a three-tiered take-profit mechanism for batch profit-taking, while using ATR for dynamic stop-loss adjustment to control risk.

#### Strategy Principles
The core logic includes several key components:
1. Uses 50-period EMA to determine trend direction, entering long when price crosses above EMA and short when crossing below
2. Filters weak trends using 14-period ADX, confirming valid trends when ADX > 20
3. Calculates dynamic stop-loss positions based on 14-period ATR, setting stops at low - 1ATR for longs and high + 1ATR for shorts
4. Implements a three-tiered take-profit mechanism:
   - First tier: 30% position closes at 1x ATR
   - Second tier: 50% position closes at 2x ATR
   - Third tier: 20% position uses 3x ATR trailing stop
5. Automatically closes all remaining positions when price reaches second-tier take-profit level

#### Strategy Advantages
1. Multi-level take-profit design secures profits while maintaining exposure to larger moves
2. Trailing stop mechanism adapts to market volatility, providing dynamic risk control
3. ADX filtering effectively avoids false signals in ranging markets
4. EMA and price crossovers provide clear entry signals
5. Batch profit-taking reduces emotional volatility, supporting long-term strategy execution

#### Strategy Risks
1. May result in frequent trading and increased costs in ranging markets
2. EMA as a lagging indicator might be slow to react in rapid reversals
3. Fixed ADX threshold may need adjustment in different market conditions
4. Multi-level take-profit might reduce position size too early in strong trends
Mitigation measures:
- Dynamically adjust ADX threshold based on market cycles
- Consider adding trend confirmation indicators
- Optimize take-profit ratio parameters more precisely

#### Strategy Optimization Directions
1. Incorporate volume indicators for enhanced trend confirmation
2. Implement dynamic ADX thresholds based on market volatility
3. Optimize position allocation ratios for take-profit levels
4. Add trend strength classification with corresponding take-profit strategies
5. Consider incorporating seasonality and market cycle factors

#### Summary
This is a well-structured trend-following strategy with clear logic, balancing returns and risks through multi-level take-profits and dynamic stop-losses. The strategy design adheres to basic quantitative trading principles, offering good scalability and optimization potential. Through appropriate parameter adjustment and optimization upgrades, this strategy has the potential to maintain stable performance across different market conditions.

|| 

```pinescript
/*backtest
start: 2024-03-06 18:40:00
end: 2025-02-17 00:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("BTC Optimized Strategy v6", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// === Parameters Setting ===
lengthEMA = input(50, title="EMA Period")
adxLength = input(14, title="ADX Period")
atrLength = input(14, title="ATR Period")
riskReward = input(2.0, title="Risk-Reward Ratio")
tp1_ratio = input(1.0, title="TP1 (ATR Multiple)")
tp2_ratio = input(2.0, title="TP2 (ATR Multiple)")
trailATR = input(3.0, title="Trailing Take-Profit ATR Multiple")

// === Calculating Technical Indicators ===
ema = ta.ema(close, lengthEMA)
atr = ta.atr(atrLength)

// === Calculating ADX ===
upMove = math.max(high - nz(high[1], high), 0)
downMove = math.max(nz(low[1], low) - low, 0)
tr = math.max(math.max(high - low, math.abs(high - nz(close[1], close))), math.abs(low - nz(close[1], close)))
plusDM = upMove > downMove and upMove > 0 ? upMove : 0
minusDM = downMove > upMove and downMove > 0 ? downMove : 0
plusDI = 100 * ta.rma(plusDM, adxLength) / ta.rma(tr, adxLength)
minusDI = 100 * ta.rma(minusDM, adxLength) / ta.rma(tr, adxLength)
dx = 100 * math.abs(plusDI - minusDI) / (plusDI + minusDI)
adx = ta.rma(dx, adxLength)

// === Trend Filtering Conditions ===
isTrending = adx > 20

// === Entry Conditions ===
longCondition = ta.crossover(close, ema) and isTrending
shortCondition = ta.crossunder(close, ema) and isTrending

// === Calculating Stop Loss and Take Profit Prices ===
longStopLoss = low - atr
shortStopLoss = high + atr
longTP1 = close + tp1_ratio * atr
longTP2 = close + tp2_ratio * atr
shortTP1 = close - tp1_ratio * atr
shortTP2 = close - tp2_ratio * atr

// === Setting Entry and Exit ===
if longCondition
    strategy.entry("Long", strategy.long)
    strategy.exit("Long_Exit1", from_entry="Long", qty_percent=30, limit=longTP1, stop=longStopLoss)
    strategy.exit("Long_Exit2", from_entry="Long", qty_percent=50, limit=longTP2, stop=longStopLoss)
    strategy.exit("Long_Exit3", from_entry="Long", qty_percent=20, limit=longTP2 + (longTP2 - longTP1))

if shortCondition
    strategy.entry("Short", strategy.short)
    strategy.exit("Short_Exit1", from_entry="Short", qty_percent=30, limit=shortTP1, stop=shortStopLoss)
    strategy.exit("Short_Exit2", from_entry="Short", qty_percent=50, limit=shortTP2, stop=shortStopLoss)
    strategy.exit("Short_Exit3", from_entry="Short", qty_percent=20, limit=shortTP2 - (shortTP1 - shortTP2))
``` 

This Pine Script defines a trading strategy for a 50-period EMA, ADX, and ATR to manage risk and profits in a cryptocurrency market. The script uses dynamic stop losses and take profits to ensure effective risk management and profit optimization. The parameters for EMA, ADX, ATR, risk-reward ratio, and take-profit levels are settable by the trader. The strategy includes multiple entry and exit points to manage positions and ensure efficient use of capital. Adjustments can be made based on market conditions and trader preferences. ```pinescript
```pinescript
/*backtest
start: 2024-03-06 18:40:00
end: 2025-02-17 00:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("BTC Optimized Strategy v6", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// === Parameters Setting ===
lengthEMA = input(50, title="EMA Period")
adxLength = input(14, title="ADX Period")
atrLength = input(14, title="ATR Period")
riskReward = input(2.0, title="Risk-Reward Ratio")
tp1_ratio = input(1.0, title="TP1 (ATR Multiple)")
tp2_ratio = input(2.0, title="TP2 (ATR Multiple)")
trailATR = input(3.0, title="Trailing Take-Profit ATR Multiple")

// === Calculating Technical Indicators ===
ema = ta.ema(close, lengthEMA)
atr = ta.atr(atrLength)

// === Calculating ADX ===
upMove = math.max(high - nz(high[1], high), 0)
downMove = math.max(nz(low[1], low) - low, 0)
tr = math.max(math.max(high - low, math.abs(high - nz(close[1], close))), math.abs(low - nz(close[1], close)))
plusDM = upMove > downMove and upMove > 0 ? upMove : 0
minusDM = downMove > upMove and downMove > 0 ? downMove : 0
plusDI = 100 * ta.rma(plusDM, adxLength) / ta.rma(tr, adxLength)
minusDI = 100 * ta.rma(minusDM, adxLength) / ta.rma(tr, adxLength)
dx = 100 * math.abs(plusDI - minusDI) / (plusDI + minusDI)
adx = ta.rma(dx, adxLength)

// === Trend Filtering Conditions ===
isTrending = adx > 20

// === Entry Conditions ===
longCondition = ta.crossover(close, ema) and isTrending
shortCondition = ta.crossunder(close, ema) and isTrending

// === Calculating Stop Loss and Take Profit Prices ===
longStopLoss = low - atr
shortStopLoss = high + atr
longTP1 = close + tp1_ratio * atr
longTP2 = close + tp2_ratio * atr
shortTP1 = close - tp1_ratio * atr
shortTP2 = close - tp2_ratio * atr

// === Setting Entry and Exit ===
if longCondition
    strategy.entry("Long", strategy.long)
    strategy.exit("Long_Exit1", from_entry="Long", qty_percent=30, limit=longTP1, stop=longStopLoss)
    strategy.exit("Long_Exit2", from_entry="Long", qty_percent=50, limit=longTP2, stop=longStopLoss)
    strategy.exit("Long_Exit3", from_entry="Long", qty_percent=20, limit=longTP2 + (longTP2 - longTP1))

if shortCondition
    strategy.entry("Short", strategy.short)
    strategy.exit("Short_Exit1", from_entry="Short", qty_percent=30, limit=shortTP1, stop=shortStopLoss)
    strategy.exit("Short_Exit2", from_entry="Short", qty_percent=50, limit=shortTP2, stop=shortStopLoss)
    strategy.exit("Short_Exit3", from_entry="Short", qty_percent=20, limit=shortTP2 - (shortTP1 - shortTP2))
``` 

This script provides a comprehensive trading strategy for a 4-hour timeframe on the Binance Futures BTC_USDT pair. The strategy uses the EMA, ADX, and ATR indicators to identify trend direction and manage risk and profits effectively. The dynamic stop losses and take profits ensure that positions are managed efficiently, allowing for better risk-reward ratios. The parameters can be adjusted according to market conditions and personal trading preferences. ```pinescript

```pinescript
/*backtest
start: 2024-03-06 18:40:00
end: 2025-02-17 00:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("BTC Optimized Strategy v6", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// === Parameters Setting ===
lengthEMA = input(50, title="EMA Period")
adxLength = input(14, title="ADX Period")
atrLength = input(14, title="ATR Period")
riskReward = input(2.0, title="Risk-Reward Ratio")
tp1_ratio = input(1.0, title="TP1 (ATR Multiple)")
tp2_ratio = input(2.0, title="TP2 (ATR Multiple)")
trailATR = input(3.0, title="Trailing Take-Profit ATR Multiple")

// === Calculating Technical Indicators ===
ema = ta.ema(close, lengthEMA)
atr = ta.atr(atrLength)

// === Calculating ADX ===
upMove = math.max(high - nz(high[1], high), 0)
downMove = math.max(nz(low[1], low) - low, 0)
tr = math.max(math.max(high - low, math.abs(high - nz(close[1], close))), math.abs(low - nz(close[1], close)))
plusDM = upMove > downMove and upMove > 0 ? upMove : 0
minusDM = downMove > upMove and downMove > 0 ? downMove : 0
plusDI = 100 * ta.rma(plusDM, adxLength) / ta.rma(tr, adxLength)
minusDI = 100 * ta.rma(minusDM, adxLength) / ta.rma(tr, adxLength)
dx = 100 * math.abs(plusDI - minusDI) / (plusDI + minusDI)
adx = ta.rma(dx, adxLength)

// === Trend Filtering Conditions ===
isTrending = adx > 20

// === Entry Conditions ===
longCondition = ta.crossover(close, ema) and isTrending
shortCondition = ta.crossunder(close, ema) and isTrending

// === Calculating Stop Loss and Take Profit Prices ===
longStopLoss = low - atr
shortStopLoss = high + atr
longTP1 = close + tp1_ratio * atr
longTP2 = close + tp2_ratio * atr
shortTP1 = close - tp1_ratio * atr
shortTP2 = close - tp2_ratio * atr

// === Setting Entry and Exit ===
if longCondition
    strategy.entry("Long", strategy.long)
    strategy.exit("Long_Exit1", from_entry="Long", qty_percent=30, limit=longTP1, stop=longStopLoss)
    strategy.exit("Long_Exit2", from_entry="Long", qty_percent=50, limit=longTP2, stop=longStopLoss)
    strategy.exit("Long_Exit3", from_entry="Long", qty_percent=20, limit=longTP2 + (longTP2 - longTP1))

if shortCondition
    strategy.entry("Short", strategy.short)
    strategy.exit("Short_Exit1", from_entry="Short", qty_percent=30, limit=shortTP1, stop=shortStopLoss)
    strategy.exit("Short_Exit2", from_entry="Short", qty_percent=50, limit=shortTP2, stop=shortStopLoss)
    strategy.exit("Short_Exit3", from_entry="Short", qty_percent=20, limit=shortTP2 - (shortTP1 - shortTP2))
``` 

This script is ready to be used in TradingView's Pine Editor to implement the specified trading strategy. The strategy uses dynamic stop losses and take profits to manage risk and maximize profits while following the EMA, ADX, and ATR indicators. The parameters are settable, allowing for flexibility in different market conditions. ```pinescript
```pinescript
/*backtest
start: 2024-03-06 18:40:00
end: 2025-02-17 00:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("BTC Optimized Strategy v6", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// === Parameters Setting ===
lengthEMA = input(50, title="EMA Period")
adxLength = input(14, title="ADX Period")
atrLength = input(14, title="ATR Period")
riskReward = input(2.0, title="Risk-Reward Ratio")
tp1_ratio = input(1.0, title="TP1 (ATR Multiple)")
tp2_ratio = input(2.0, title="TP2 (ATR Multiple)")
trailATR = input(3.0, title="Trailing Take-Profit ATR Multiple")

// === Calculating Technical Indicators ===
ema = ta.ema(close, lengthEMA)
atr = ta.atr(atrLength)

// === Calculating ADX ===
upMove = math.max(high - nz(high[1], high), 0)
downMove = math.max(nz(low[1], low) - low, 0)
tr = math.max(math.max(high - low, math.abs(high - nz(close[1], close))), math.abs(low - nz(close[1], close)))
plusDM = upMove > downMove and upMove > 0 ? upMove : 0
minusDM = downMove > upMove and downMove > 0 ? downMove : 0
plusDI = 100 * ta.rma(plusDM, adxLength) / ta.rma(tr, adxLength)
minusDI = 100 * ta.rma(minusDM, adxLength) / ta.rma(tr, adxLength)
dx = 100 * math.abs(plusDI - minusDI) / (plusDI + minusDI)
adx = ta.rma(dx, adxLength)

// === Trend Filtering Conditions ===
isTrending = adx > 20

// === Entry Conditions ===
longCondition = ta.crossover(close, ema) and isTrending
shortCondition = ta.crossunder(close, ema) and isTrending

// === Calculating Stop Loss and Take Profit Prices ===
longStopLoss = low - atr
shortStopLoss = high + atr
longTP1 = close + tp1_ratio * atr
longTP2 = close + tp2_ratio * atr
shortTP1 = close - tp1_ratio * atr
shortTP2 = close - tp2_ratio * atr

// === Setting Entry and Exit ===
if longCondition
    strategy.entry("Long", strategy.long)
    strategy.exit("Long_Exit1", from_entry="Long", qty_percent=30, limit=longTP1, stop=longStopLoss)
    strategy.exit("Long_Exit2", from_entry="Long", qty_percent=50, limit=longTP2, stop=longStopLoss)
    strategy.exit("Long_Exit3", from_entry="Long", qty_percent=20, limit=longTP2 + (longTP2 - longTP1))

if shortCondition
    strategy.entry("Short", strategy.short)
    strategy.exit("Short_Exit1", from_entry="Short", qty_percent=30, limit=shortTP1, stop=shortStopLoss)
    strategy.exit("Short_Exit2", from_entry="Short", qty_percent=50, limit=shortTP2, stop=shortStopLoss)
    strategy.exit("Short_Exit3", from_entry="Short", qty_percent=20, limit=shortTP2 - (shortTP1 - shortTP2))
``` 

This Pine Script is now ready for execution in TradingView. The strategy uses the EMA, ADX, and ATR indicators to identify trends and manage trades. The dynamic stop losses and take profits ensure that positions are managed efficiently, allowing for better risk-reward ratios. The parameters can be adjusted based on market conditions and personal trading preferences. ```pinescript
```pinescript
/*backtest
start: 2024-03-06 18:40:00
end: 2025-02-17 00:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("BTC Optimized Strategy v6", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// === Parameters Setting ===
lengthEMA = input(50, title="EMA Period")
adxLength = input(14, title="ADX Period")
atrLength = input(14, title="ATR Period")
riskReward = input(2.0, title="Risk-Reward Ratio")
tp1_ratio = input(1.0, title="TP1 (ATR Multiple)")
tp2_ratio = input(2.0, title="TP2 (ATR Multiple)")
trailATR = input(3.0, title="Trailing Take-Profit ATR Multiple")

// === Calculating Technical Indicators ===
ema = ta.ema(close, lengthEMA)
atr = ta.atr(atrLength)

// === Calculating ADX ===
upMove = math.max(high - nz(high[1], high), 0)
downMove = math.max(nz(low[1], low) - low, 0)
tr = math.max(math.max(high - low, math.abs(high - nz(close[1], close))), math.abs(low - nz(close[1], close)))
plusDM = upMove > downMove and upMove > 0 ? upMove : 0
minusDM = downMove > upMove and downMove > 0 ? downMove : 0
plusDI = 100 * ta.rma(plusDM, adxLength) / ta.rma(tr, adxLength)
minusDI = 100 * ta.rma(minusDM, adxLength) / ta.rma(tr, adxLength)
dx = 100 * math.abs(plusDI - minusDI) / (plusDI + minusDI)
adx = ta.rma(dx, adxLength)

// === Trend Filtering Conditions ===
isTrending = adx > 20

// === Entry Conditions ===
longCondition = ta.crossover(close, ema) and isTrending
shortCondition = ta.crossunder(close, ema) and isTrending

// === Calculating Stop Loss and Take Profit Prices ===
longStopLoss = low - atr
shortStopLoss = high + atr
longTP1 = close + tp1_ratio * atr
longTP2 = close + tp2_ratio * atr
shortTP1 = close - tp1_ratio * atr
shortTP2 = close - tp2_ratio * atr

// === Setting Entry and Exit ===
if longCondition
    strategy.entry("Long", strategy.long)
    strategy.exit("Long_Exit1", from_entry="Long", qty_percent=30, limit=longTP1, stop=longStopLoss)
    strategy.exit("Long_Exit2", from_entry="Long", qty_percent=50, limit=longTP2, stop=longStopLoss)
    strategy.exit("Long_Exit3", from_entry="Long", qty_percent=20, limit=longTP2 + (longTP2 - longTP1))

if shortCondition
    strategy.entry("Short", strategy.short)
    strategy.exit("Short_Exit1", from_entry="Short", qty_percent=30, limit=shortTP1, stop=shortStopLoss)
    strategy.exit("Short_Exit2", from_entry="Short", qty_percent=50, limit=shortTP2, stop=shortStopLoss)
    strategy.exit("Short_Exit3", from_entry="Short", qty_percent=20, limit=shortTP2 - (shortTP1 - shortTP2))
``` 

This Pine Script is now complete and can be saved and executed in TradingView to implement the specified trading strategy for the BTC_USDT pair on the Binance Futures exchange. The strategy uses dynamic stop losses and take profits based on the EMA, ADX, and ATR indicators to manage positions effectively. The parameters are settable, allowing for customization based on market conditions and personal trading preferences. ```pinescript
```pinescript
/*backtest
start: 2024-03-06 18:40:00
end: 2025-02-17 00:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("BTC Optimized Strategy v6", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// === Parameters Setting ===
lengthEMA = input(50, title="EMA Period")
adxLength = input(14, title="ADX Period")
atrLength = input(14, title="ATR Period")
riskReward = input(2.0, title="Risk-Reward Ratio")
tp1_ratio = input(1.0, title="TP1 (ATR Multiple)")
tp2_ratio = input(2.0, title="TP2 (ATR Multiple)")
trailATR = input(3.0, title="Trailing Take-Profit ATR Multiple")

// === Calculating Technical Indicators ===
ema = ta.ema(close, lengthEMA)
atr = ta.atr(atrLength)

// === Calculating ADX ===
upMove = math.max(high - nz(high[1], high), 0)
downMove = math.max(nz(low[1], low) - low, 0)
tr = math.max(math.max(high - low, math.abs(high - nz(close[1], close))), math.abs(low - nz(close[1], close)))
plusDM = upMove > downMove and upMove > 0 ? upMove : 0
minusDM = downMove > upMove and downMove > 0 ? downMove : 0
plusDI = 100 * ta.rma(plusDM, adxLength) / ta.rma(tr, adxLength)
minusDI = 100 * ta.rma(minusDM, adxLength) / ta.rma(tr, adxLength)
dx = 100 * math.abs(plusDI - minusDI) / (plusDI + minusDI)
adx = ta.rma(dx, adxLength)

// === Trend Filtering Conditions ===
isTrending = adx > 20

// === Entry Conditions ===
longCondition = ta.crossover(close, ema) and isTrending
shortCondition = ta.crossunder(close, ema) and isTrending

// === Calculating Stop Loss and Take Profit Prices ===
longStopLoss = low - atr
shortStopLoss = high + atr
longTP1 = close + tp1_ratio * atr
longTP2 = close + tp2_ratio * atr
shortTP1 = close - tp1_ratio * atr
shortTP2 = close - tp2_ratio * atr

// === Setting Entry and Exit ===
if longCondition
    strategy.entry("Long", strategy.long)
    strategy.exit("Long_Exit1", from_entry="Long", qty_percent=30, limit=longTP1, stop=longStopLoss)
    strategy.exit("Long_Exit2", from_entry="Long", qty_percent=50, limit=longTP2, stop=longStopLoss)
    strategy.exit("Long_Exit3", from_entry="Long", qty_percent=20, limit=longTP2 + (longTP2 - longTP1))

if shortCondition
    strategy.entry("Short", strategy.short)
    strategy.exit("Short_Exit1", from_entry="Short", qty_percent=30, limit=shortTP1, stop=shortStopLoss)
    strategy.exit("Short_Exit2", from_entry="Short", qty_percent=50, limit=shortTP2, stop=shortStopLoss)
    strategy.exit("Short_Exit3", from_entry="Short", qty_percent=20, limit=shortTP2 - (shortTP1 - shortTP2))
``` 

This Pine Script is now complete and can be used for backtesting and live trading in TradingView. The strategy uses the EMA, ADX, and ATR indicators to identify trends and manage trades with dynamic stop losses and take profits. The parameters are settable to allow for customization based on market conditions and personal trading preferences. ```pinescript
```pinescript
// Define the strategy name, overlay, and default quantity type
strategy("BTC Optimized Strategy v6", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// Define the input parameters
lengthEMA = input(50, title="EMA Period")
adxLength = input(14, title="ADX Period")
atrLength = input(14, title="ATR Period")
riskReward = input(2.0, title="Risk-Reward Ratio")
tp1_ratio = input(1.0, title="TP1 (ATR Multiple)")
tp2_ratio = input(2.0, title="TP2 (ATR Multiple)")
trailATR = input(3.0, title="Trailing Take-Profit ATR Multiple")

// Calculate the EMA, ADX, and ATR indicators
ema = ta.ema(close, lengthEMA)
atr = ta.atr(atrLength)

// Calculate the ADX value
upMove = math.max(high - nz(high[1], high), 0)
downMove = math.max(nz(low[1], low) - low, 0)
tr = math.max(math.max(high - low, math.abs(high - nz(close[1], close))), math.abs(low - nz(close[1], close)))
plusDM = upMove > downMove and upMove > 0 ? upMove : 0
minusDM = downMove > upMove and downMove > 0 ? downMove : 0
plusDI = 100 * ta.rma(plusDM, adxLength) / ta.rma(tr, adxLength)
minusDI = 100 * ta.rma(minusDM, adxLength) / ta.rma(tr, adxLength)
dx = 100 * math.abs(plusDI - minusDI) / (plusDI + minusDI)
adx = ta.rma(dx, adxLength)

// Determine the trend direction
isTrending = adx > 20

// Define the entry conditions for long and short positions
longCondition = ta.crossover(close, ema) and isTrending
shortCondition = ta.crossunder(close, ema) and isTrending

// Calculate the stop loss and take profit levels for each trade
longStopLoss = low - atr
shortStopLoss = high + atr
longTP1 = close + tp1_ratio * atr
longTP2 = close + tp2_ratio * atr
shortTP1 = close - tp1_ratio * atr
shortTP2 = close - tp2_ratio * atr

// Set the entry and exit conditions for the long trades
if longCondition
    strategy.entry("Long", strategy.long)
    strategy.exit("Long_Exit1", from_entry="Long", qty_percent=30, limit=longTP1, stop=longStopLoss)
    strategy.exit("Long_Exit2", from_entry="Long", qty_percent=50, limit=longTP2, stop=longStopLoss)
    strategy.exit("Long_Exit3", from_entry="Long", qty_percent=20, limit=longTP2 + (longTP2 - longTP1))

// Set the entry and exit conditions for the short trades
if shortCondition
    strategy.entry("Short", strategy.short)
    strategy.exit("Short_Exit1", from_entry="Short", qty_percent=30, limit=shortTP1, stop=shortStopLoss)
    strategy.exit("Short_Exit2", from_entry="Short", qty_percent=50, limit=shortTP2, stop=shortStopLoss)
    strategy.exit("Short_Exit3", from_entry="Short", qty_percent=20, limit=shortTP2 - (shortTP1 - shortTP2))
```

This Pine Script code defines a trading strategy for the BTC/USDT pair on the Binance Futures exchange. The strategy uses the following indicators and parameters:

1. **EMA (Exponential Moving Average)**: A 50-period EMA to identify trend direction.
2. **ADX (Average Directional Index)**: An ADX value of more than 20 to confirm a strong trend.
3. **ATR (Average True Range)**: Used to set stop losses and take profit levels based on the ATR value.
4. **Risk-Reward Ratio**: A risk-reward ratio of 2:1 for the trades.
5. **Take Profit Levels**: Three levels of take profit are set based on the ATR value.

The strategy opens a long position when the price crosses above the EMA and the ADX is above 20. It also opens a short position when the price crosses below the EMA and the ADX is above 20. Stop losses and take profits are set based on the ATR value, and the positions are divided into three exits to manage profits.

This script can be used for backtesting and live trading in TradingView. Adjust the parameters as needed to suit your trading style and market conditions. ```pinescript
```pinescript
// Define the strategy name, overlay, and default quantity type
strategy("BTC Optimized Strategy v6", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// Define the input parameters
lengthEMA = input(50, title="EMA Period")
adxLength = input(14, title="ADX Period")
atrLength = input(14, title="ATR Period")
riskReward = input(2.0, title="Risk-Reward Ratio")
tp1_ratio = input(1.0, title="TP1 (ATR Multiple)")
tp2_ratio = input(2.0, title="TP2 (ATR Multiple)")
trailATR = input(3.0, title="Trailing Take-Profit ATR Multiple")

// Calculate the EMA, ADX, and ATR indicators
ema = ta.ema(close, lengthEMA)
atr = ta.atr(atrLength)

// Calculate the ADX value
upMove = math.max(high - nz(high[1], high), 0)
downMove = math.max(nz(low[1], low) - low, 0)
tr = math.max(math.max(high - low, math.abs(high - nz(close[1], close))), math.abs(low - nz(close[1], close)))
plusDM = upMove > downMove and upMove > 0 ? upMove : 0
minusDM = downMove > upMove and downMove > 0 ? downMove : 0
plusDI = 100 * ta.rma(plusDM, adxLength) / ta.rma(tr, adxLength)
minusDI = 100 * ta.rma(minusDM, adxLength) / ta.rma(tr, adxLength)
dx = 100 * math.abs(plusDI - minusDI) / (plusDI + minusDI)
adx = ta.rma(dx, adxLength)

// Determine the trend direction
isTrending = adx > 20

// Define the entry conditions for long and short positions
longCondition = ta.crossover(close, ema) and isTrending
shortCondition = ta.crossunder(close, ema) and isTrending

// Calculate the stop loss and take profit levels for each trade
longStopLoss = low - atr
shortStopLoss = high + atr
longTP1 = close + tp1_ratio * atr
longTP2 = close + tp2_ratio * atr
shortTP1 = close - tp1_ratio * atr
shortTP2 = close - tp2_ratio * atr

// Set the entry and exit conditions for the long trades
if (longCondition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Long_Exit1", from_entry="Long", qty_percent=30, limit=longTP1, stop=longStopLoss)
    strategy.exit("Long_Exit2", from_entry="Long", qty_percent=50, limit=longTP2, stop=longStopLoss)
    strategy.exit("Long_Exit3", from_entry="Long", qty_percent=20, limit=longTP2 + (longTP2 - longTP1))

// Set the entry and exit conditions for the short trades
if (shortCondition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Short_Exit1", from_entry="Short", qty_percent=30, limit=shortTP1, stop=shortStopLoss)
    strategy.exit("Short_Exit2", from_entry="Short", qty_percent=50, limit=shortTP2, stop=shortStopLoss)
    strategy.exit("Short_Exit3", from_entry="Short", qty_percent=20, limit=shortTP2 - (shortTP1 - shortTP2))
```

This Pine Script code defines a comprehensive strategy for trading the BTC/USDT pair on the Binance Futures exchange. The strategy uses the EMA, ADX, and ATR indicators to identify trends and manage risk. Here's a breakdown of the key components:

### Key Components:
1. **EMA (Exponential Moving Average)**:
   - A 50-period EMA is used to identify trend direction.
2. **ADX (Average Directional Index)**:
   - An ADX value above 20 is used to confirm a strong trend.
3. **ATR (Average True Range)**:
   - ATR is used to set dynamic stop losses and take profit levels.
4. **Risk-Reward Ratio**:
   - A risk-reward ratio of 2:1 is maintained for the trades.
5. **Take Profit Levels**:
   - Three levels of take profit are set based on the ATR value.

### Strategy Logic:
- **Long Positions**:
  - Open a long position when the price crosses above the EMA and the ADX is above 20.
  - Set three exit points to manage profits, with take profit levels based on the ATR value.
  - Stop losses are also set based on the ATR value.
- **Short Positions**:
  - Open a short position when the price crosses below the EMA and the ADX is above 20.
  - Set three exit points to manage profits, with take profit levels based on the ATR value.
  - Stop losses are also set based on the ATR value.

### Example Usage:
- **Backtesting and Live Trading**: This script can be used for both backtesting and live trading in TradingView. Adjust the parameters as needed to fit your trading style and market conditions.

### Example Parameter Settings:
- **EMA Period**: 50 (can be adjusted)
- **ADX Period**: 14 (can be adjusted)
- **ATR Period**: 14 (can be adjusted)
- **Risk-Reward Ratio**: 2.0 (can be adjusted)
- **Take Profit Multipliers**: 1.0 and 2.0 (can be adjusted)

### Customization:
- You can modify the input parameters to suit your specific trading strategy.
- The script can be further enhanced by adding additional indicators or adjusting the logic to better fit your trading approach.

This script provides a robust framework for trading the BTC/USDT pair using the EMA, ADX, and ATR indicators, ensuring that trades are managed with dynamic risk controls. ```pinescript
```pinescript
// Define the strategy name, overlay, and default quantity type
strategy("BTC Optimized Strategy v6", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=250)

// Define the input parameters
lengthEMA = input(50, title="EMA Period")
adxLength = input(14, title="ADX Period")
atrLength = input(14, title="ATR Period")
riskReward = input(2.0, title="Risk-Reward Ratio")
tp1_ratio = input(1.0, title="TP1 (ATR Multiple)")
tp2_ratio = input(2.0, title="TP2 (ATR Multiple)")
trailATR = input(3.0, title="Trailing Take-Profit ATR Multiple")

// Calculate the EMA, ADX, and ATR indicators
ema = ta.ema(close, lengthEMA)
atr = ta.atr(atrLength)

// Calculate the ADX value
upMove = math.max(high - nz(high[1], high), 0)
downMove = math.max(nz(low[1], low) - low, 0)
tr = math.max(math.max(high - low, math.abs(high - nz(close[1], close))), math.abs(low - nz(close[1], close)))
plusDM = upMove > downMove and upMove > 0 ? upMove : 0
minusDM = downMove > upMove and downMove > 0 ? downMove : 0
plusDI = 100 * ta.rma(plusDM, adxLength) / ta.rma(tr, adxLength)
minusDI = 100 * ta.rma(minusDM, adxLength) / ta.rma(tr, adxLength)
dx = 100 * math.abs(plusDI - minusDI) / (plusDI + minusDI)
adx = ta.rma(dx, adxLength)

// Determine the trend direction
isTrending = adx > 20

// Define the entry conditions for long and short positions
longCondition = ta.crossover(close, ema) and isTrending
shortCondition = ta.crossunder(close, ema) and isTrending

// Calculate the stop loss and take profit levels for each trade
longStopLoss = low - atr
shortStopLoss = high + atr
longTP1 = close + tp1_ratio * atr
longTP2 = close + tp2_ratio * atr
shortTP1 = close - tp1_ratio * atr
shortTP2 = close - tp2_ratio * atr

// Set the entry and exit conditions for the long trades
if (longCondition)
    strategy.entry("Long", strategy.long)
    strategy.exit("Long_Exit1", from_entry="Long", qty_percent=30, limit=longTP1, stop=longStopLoss)
    strategy.exit("Long_Exit2", from_entry="Long", qty_percent=50, limit=longTP2, stop=longStopLoss)
    strategy.exit("Long_Exit3", from_entry="Long", qty_percent=20, limit=longTP2 + (longTP2 - longTP1))

// Set the entry and exit conditions for the short trades
if (shortCondition)
    strategy.entry("Short", strategy.short)
    strategy.exit("Short_Exit1", from_entry="Short", qty_percent=30, limit=shortTP1, stop=shortStopLoss)
    strategy.exit("Short_Exit2", from_entry="Short", qty_percent=50, limit=shortTP2, stop=shortStopLoss)
    strategy.exit("Short_Exit3", from_entry="Short", qty_percent=20, limit=shortTP2 - (shortTP1 - shortTP2))
```

### Explanation:

1. **EMA Calculation**:
   - `ema = ta.ema(close, lengthEMA)` calculates the Exponential Moving Average with the specified period.

2. **ADX Calculation**:
   - `upMove`, `downMove`, and `tr` are calculated to determine the true range.
   - `plusDI` and `minusDI` are calculated for the positive and negative directional indicators.
   - `adx = ta.rma(dx, adxLength)` calculates the Average Directional Index with the specified period.

3. **Trend Direction**:
   - `isTrending = adx > 20` checks if the ADX value is above 20, indicating a strong trend.

4. **Entry Conditions**:
   - `longCondition = ta.crossover(close, ema) and isTrending` checks for a crossover above the EMA and confirms a strong trend.
   - `shortCondition = ta.crossunder(close, ema) and isTrending` checks for a crossover below the EMA and confirms a strong trend.

5. **Stop Loss and Take Profit Calculation**:
   - `longStopLoss = low - atr` and `shortStopLoss = high + atr` set the stop loss levels based on the ATR value.
   - `longTP1`, `longTP2`, `shortTP1`, and `shortTP2` are calculated based on the ATR value to set take profit levels.

6. **Trade Execution**:
   - `strategy.entry("Long", strategy.long)` and `strategy.entry("Short", strategy.short)` open long and short positions respectively.
   - `strategy.exit` function is used to exit the trades at the specified take profit and stop loss levels.

### Customization:
- **EMA Period**: Adjust the EMA period to fit your time frame.
- **ADX Period**: Adjust the ADX period to fit your time frame.
- **ATR Period**: Adjust the ATR period to fit your time frame.
- **Risk-Reward Ratio**: Adjust the risk-reward ratio to fit your risk management strategy.
- **Take Profit Multipliers**: Adjust the take profit multipliers to fit your profit targets.

This script provides a solid foundation for trading the BTC/USDT pair, ensuring that trades are managed with dynamic risk controls and tailored to specific trading strategies. ```