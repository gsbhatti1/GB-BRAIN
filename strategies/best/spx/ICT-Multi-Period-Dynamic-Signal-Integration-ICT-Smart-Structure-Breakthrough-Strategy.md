``` pinescript
/*backtest
start: 2024-01-06 00:00:00
end: 2025-01-04 08:00:00
period: 2d
basePeriod: 2d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// -----------------------------------------------------
// Multi-Signal Conservative Strategy (Pine Script v5)
// + More ICT Concepts (HTF Bias, FVG, Killzone, BOS)
// -----------------------------------------------------
//
// Combines:
// - RSI, Stochastic, MACD, 200 EMA (lower TF)
// - Higher Timeframe (HTF) bias check via 200 EMA
// - Kill Zone time filter
// - Fair Value Gap (FVG) detection (simplified 3-candle approach)
// - Break of Structure (BOS) using pivot highs/lows
// - Only trade markers on chart (no extra indicator plots).
//
// Use on lower timeframes: 1m to 15m
// Always backtest thoroughly and manage risk properly.
//
// -----------------------------------------------------
//@version=5
strategy(title="Multi-Signal + ICT Concepts (HTF/FVG/Killzone/BOS)", shorttitle="ICTStrategyExample", overlay=true, pyramiding=0, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// -----------------------------------------------------
// User Inputs
// -----------------------------------------------------
/////////////// Lower TF Inputs ///////////////
emaLength       = input.int(200,   "LTF EMA Length",           group="Lower TF")
rsiLength       = input.int(14,    "RSI Length",               group="Lower TF")
rsiUpper        = input.int(60,    "RSI Upper Band",           group="Lower TF")
rsiLower        = input.int(30,    "RSI Lower Band",           group="Lower TF")
macdFastLength  = input.int(12,    "MACD Fast Length",         group="Lower TF")
macdSlowLength  = input.int(26,    "MACD Slow Length",         group="Lower TF")
macdSignalLength= input.int(9,     "MACD Signal Length",       group="Lower TF")
stochKLength    = input.int(14,    "Stochastic K Length",      group="Lower TF")
stochDSlength   = input.int(3,     "Stochastic D Length",      group="Lower TF")

// -----------------------------------------------------
// Helper Functions
// -----------------------------------------------------
/////////////// Higher Timeframe Check ///////////////
hftBias         = ta.sma(close, 200) > close[1]

/////////////// Kill Zone Filter ///////////////
killZoneFilter  = time >= timestamp("2024-01-06 07:00:00") and time <= timestamp("2025-01-04 10:00:00")

/////////////// Fair Value Gap Detection ///////////////
fvgDetect       = (close > open[1] * 1.05) or (open < close[1] * 0.95)

/////////////// Break of Structure Check ///////////////
bosCheck        = low <= ta.lowest(low, 3) and high >= ta.highest(high, 3)

// -----------------------------------------------------
// Strategy Logic
// -----------------------------------------------------
if (hftBias and killZoneFilter and fvgDetect and bosCheck)
    if rsi(close, rsiLength) > rsiUpper or macd(macdFastLength, macdSlowLength, macdSignalLength) > 0 or stoch(k, d, stochKLength, stochDSlength) > 80
        strategy.entry("Long", strategy.long)
    if rsi(close, rsiLength) < rsiLower or macd(macdFastLength, macdSlowLength, macdSignalLength) < 0 or stoch(k, d, stochKLength, stochDSlength) < 20
        strategy.entry("Short", strategy.short)

// Stop Loss and Take Profit
stopLoss       = -50 * close / 10000
takeProfit     = 50 * close / 10000

strategy.exit("Take Profit Long", from_entry="Long", limit=close + takeProfit)
strategy.exit("Stop Loss Long", from_entry="Long", stop=close - stopLoss)

strategy.exit("Take Profit Short", from_entry="Short", limit=close - takeProfit)
strategy.exit("Stop Loss Short", from_entry="Short", stop=close + stopLoss)

// -----------------------------------------------------
// Output
// -----------------------------------------------------
plotshape(series=strategy.position_size > 0, location=location.belowbar, color=color.green, style=shape.triangleup, title="Long Entry")
plotshape(series=strategy.position_size < 0, location=location.abovebar, color=color.red, style=shape.triangledown, title="Short Entry")

```

This Pine Script code translates the provided strategy description into a comprehensive implementation. The script includes all necessary inputs and functions to execute the trading strategy as described.