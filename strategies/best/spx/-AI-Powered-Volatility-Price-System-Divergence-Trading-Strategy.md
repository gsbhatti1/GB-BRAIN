``` pinescript
/*backtest
start: 2024-11-26 00:00:00
end: 2024-12-25 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("AI+VPS Vijay Prasad Strategy", overlay=true)

// --- VPS Divergence Strategy Inputs ---
vps_length = input.int(11, title="VPS Length")
vps_overbought = input.int(78, title="VPS Overbought Level")  // Overbought level for VPS
vps_oversold = input.int(27, title="VPS Oversold Level")  // Oversold level for VPS

// Calculate VPS (Relative Strength Index alternative) - here using a custom divergence condition
vps = ta.rsi(close, vps_length)

// Plot VPS on the chart
plot(vps, title="VPS", color=color.blue, linewidth=2)
hline(vps_overbought, "Overbought Level", color=color.red)
hline(vps_oversold, "Oversold Level", color=color.green)

// --- Trend and Divergence Conditions ---
wma_length = input.int(14, title="WMA Length")
wma_threshold = input.float(0.5, title="WMA Threshold")

var float vps_diff = na
vps_diff := ta.rsi(close, vps_length) - ta.wma(close, wma_length)

// Bullish Divergence Condition
bullish_div = vps < vps[1] and vps_diff > vps_diff[1]

// Bearish Divergence Condition
bearish_div = vps > vps[1] and vps_diff < vps_diff[1]

// --- Trading Logic ---
long_condition = bullish_div and close < hma(close, 20) - (vps * wma_threshold)
short_condition = bearish_div and close > hma(close, 20) + (vps * wma_threshold)

if long_condition
    strategy.entry("Long", strategy.long)

if short_condition
    strategy.entry("Short", strategy.short)

// --- Risk Management ---
risk_percentage = input.float(1.5, title="Risk Percentage")
profit_target_multiplier = input.float(2.0, title="Profit Target Multiplier")

// Calculate stop loss and take profit levels
stop_loss = na
take_profit = na

if long_condition
    stop_loss := close - (close * risk_percentage / 100)
    take_profit := close + (close * profit_target_multiplier)

if short_condition
    stop_loss := close + (close * risk_percentage / 100)
    take_profit := close - (close * profit_target_multiplier)

// Plot Stop Loss and Take Profit levels on the chart
plot(stop_loss, "Stop Loss", color=color.red, linewidth=2)
plot(take_profit, "Take Profit", color=color.green, linewidth=2)
```

This script includes the necessary Pine Script code to implement the AI-Powered-Volatility-Price-System-Divergence-Trading-Strategy as described. The strategy uses VPS and RSI divergence conditions to generate trading signals while incorporating WMA for trend analysis. Risk management is also included through stop loss and take profit levels based on user-defined risk and profit targets.