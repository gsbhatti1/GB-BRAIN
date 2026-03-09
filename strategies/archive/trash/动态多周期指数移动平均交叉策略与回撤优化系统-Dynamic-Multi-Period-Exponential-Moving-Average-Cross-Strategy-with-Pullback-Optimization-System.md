``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-12-25 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Strategy with Price & EMA5 & EMA8 < EMA50 Condition", overlay=true, margin_long=100, initial_capital=10000, commission_type=strategy.commission.percent, commission_value=0.1)

// ==============================
// INPUTS
// ==============================
lengthEMA5 = input.int(5, "EMA5 Length")
lengthEMA8 = input.int(8, "EMA8 Length")
lengthEMA13 = input.int(13, "EMA13 Length")
lengthEMA21 = input.int(21, "EMA21 Length")
lengthEMA50 = input.int(50, "EMA50 Length")

// Position size (e.g., 100 units)
full_position = 100.0 
qty20 = full_position * 0.2
qty40 = full_position * 0.4

// ==============================
// EMA CALCULATIONS
// ==============================
ema5 = ta.ema(close, lengthEMA5)
ema8 = ta.ema(close, lengthEMA8)
ema13 = ta.ema(close, lengthEMA13)
ema21 = ta.ema(close, lengthEMA21)
ema50 = ta.ema(close, lengthEMA50)

// ==============================
// CROSS DETECTION FUNCTIONS
// ==============================
crossUp(src1, src2) => ta.crossover(src1, src2)
crossDown(src1, src2) => ta.crossunder(src2, src1)

// ==============================
// STRATEGY CONDITIONS
// ==============================

// Step 1: Buy 20% when EMA5 crosses above EMA8
step1_condition = crossUp(ema5, ema8)
```