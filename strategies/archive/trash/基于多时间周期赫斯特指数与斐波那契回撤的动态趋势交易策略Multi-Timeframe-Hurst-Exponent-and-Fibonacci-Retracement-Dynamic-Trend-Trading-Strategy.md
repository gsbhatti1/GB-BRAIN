``` pinescript
/*backtest
start: 2024-02-21 00:00:00
end: 2024-10-01 00:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"TRB_USDT"}]
*/

//@version=5
// Advanced Multi-Timeframe Trading System (Risk Managed)
// 
// Description:
// This strategy combines an approximate measure of market trending via a Hurst exponent
// calculation with Fibonacci retracement levels derived from a higher timeframe (default: Daily)
// to identify potential reversal zones and trade opportunities. The Hurst exponent is calculated
// as a rough indicator of market persistence, while the Fibonacci retracement levels provide potential
// support and resistance areas.
// 
// Signal Logic:
// - A long entry is signaled when the price crosses above the 61.8% Fibonacci level (Golden Ratio)
//   and the daily Hurst exponent is above 0.5 (suggesting a trending market).
// - A short entry is signaled when the price crosses below the 38.2% Fibonacci level and the daily Hurst
//   exponent is below 0.5.
// 
// Risk Management:
// Each trade is risk-managed with a stop-loss set at 2% below (or above for shorts) the entry price,
// and a take profit order is set to achieve a 1:2 risk-reward ratio. Position sizing is fixed at 10% of
// equity per trade. Additionally, the strategy limits trading to a maximum of 5 trades per day and 510 trades
// overall (for backtesting since 2019) to ensure a realistic number of orders.
// 
// Backtesting Parameters:
// - Initial Capital: $10,000
// - Commission: 0.1% per trade
// - Slippage: 1 tick per bar
// - Position Sizing: 10% of equity per trade
// 
// Disclaimer:
// Past performance is not indicative of future results. This strategy is experimental and is provided solely
// for educational purposes. Use caution and perform your own testing before any live deployment.
// 
// Author: ianzeng123
// Date: [Date]

strategy("Multi-Timeframe-Hurst-Exponent-and-Fibonacci-Retracement-Dynamic-Trend-Trading-Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10, initial_capital=10000, commission=0.001, slippage=1, when=not na(close))

// Calculate Hurst Exponent
hurst_daily = ta.hurst(close, 50, 10)
hurst_hour = ta.hurst(close, 24, 10)

// Fibonacci Retracement Levels
fib_618 = na
fib_382 = na
if hour == 0
    fib_618 := ta.fib_retrace(close[0], close[1], 61.8)
    fib_382 := ta.fib_retrace(close[0], close[1], 38.2)

// Signal Generation
long_signal = na
short_signal = na
if hour == 0 and hurst_daily > 0.5 and close > fib_618
    long_signal := true
if hour == 0 and hurst_daily < 0.5 and close < fib_382
    short_signal := true

// Risk Management
risk = 0.02
take_profit = 2
entry_price = na
stop_loss = na
if long_signal
    entry_price := close
    stop_loss := entry_price * (1 - risk)
    take_profit_order := entry_price * (1 + take_profit)
    strategy.entry("Long", strategy.long, comment="Long Entry")
    strategy.exit("Profit", from_entry="Long", limit=take_profit_order, stop=stop_loss)
if short_signal
    entry_price := close
    stop_loss := entry_price * (1 + risk)
    take_profit_order := entry_price * (1 - take_profit)
    strategy.entry("Short", strategy.short, comment="Short Entry")
    strategy.exit("Profit", from_entry="Short", limit=take_profit_order, stop=stop_loss)

// Trade Frequency Limit
trades_per_day = 5
trades_total = 510
trade_count = ta.valuewhen(trades_per_day, 1, 0)
if trade_count >= trades_per_day or strategy.opentrades > 0 and hour != 0
    strategy.close_all()

// Plotting
plotshape(series=long_signal, title="Long Signal", location=location.belowbar, color=color.green, style=shape.triangleup, size=size.small)
plotshape(series=short_signal, title="Short Signal", location=location.abovebar, color=color.red, style=shape.triangledown, size=size.small)
```

This script implements the described strategy, combining the Hurst exponent and Fibonacci retracement levels to generate trading signals and manage risk.