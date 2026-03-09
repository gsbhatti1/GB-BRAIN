``` pinescript
/*backtest
start: 2023-11-15 00:00:00
end: 2023-11-22 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
//@version=4

// Dynamic Price Swing Oscillator Strategy for identifying price trends.
// It combines moving averages, price channels and Fibonacci retracements to implement dynamic entry and exit.

// ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗██████╗     ██████╗ ██╗   ██╗    
//██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗    ██╔══██╗╚██╗ ██╔╝                       
//██║     ██████╔╝█████╗  ███████║   ██║   █████╗  ██║  ██║    ██████╔╝ ╚████╔╝                        
//██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝  ██║  ██║    ██╔═══╝   ╚██╔╝                          
//╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗██████╔╝    ██║        ██║                           
// ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═════╝     ╚═╝        ╚═╝                          

strategy("Dynamic-Price-Swing-Oscillator-Strategy", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=10)

// Strategy Arguments
var float start_time = timestamp("2021.6.22 00:00 -5")
var float end_time = timestamp("2021.12.31 00:00 -6")
input bool mixed_market_long_short = true, title="Long/Short for Mixed Market"
input bool long_only = false, title="Long Only"
input bool short_only = false, title="Short Only"
input float stop_loss_percent = 10, title="Stop Loss %"
input float target_profit_percent = 20, title="Target Profit %"
input int max_losing_days = 2, title="Stop Trading After This Many Losing Days"
input float equity_loss_threshold = 10, title="Maximum % of Equity Lost to Halt Trading"
input int lookback_bars = 2, title="Number of bars to look back on to calculate price swings."
input int max_lookback_period = 5, title="Max Lookback Period"
input string high_source = "high", title="High Source"
input string low_source = "low", title="Low Source"
input bool trend_fast_slow_ema = true, title="Trend uses Fast and Slow EMA to prevent going the wrong direction"
input int rsi_length = 14, title="RSI Length"
input int fast_ema_length = 12, title="EMA Fast Length"
input int slow_ema_length = 26, title="EMA Slow Length"
input bool avg_price_channel_only = false, title="Use Average Price Channel Only"
input bool price_moving_average_only = false, title="Use Price Moving Average Only"
input bool price_fibonacci_average_only = false, title="Use Price Fibonacci Average Only"

// Calculation of Price Swings
price_high = security(syminfo.tickerid, "1m", high_source == "high" ? high : low_source == "low" ? low : close)
price_low = security(syminfo.tickerid, "1m", high_source == "high" ? high : low_source == "low" ? low : close)

// EMA Calculation
ema_fast = ema(close, fast_ema_length)
ema_slow = ema(close, slow_ema_length)

// RSI Calculation
rsi = rsi(close, rsi_length)

// Average Price Channel Calculation
avg_price_channel_high = highest(high, lookback_bars) + (highest(low, lookback_bars) - lowest(low, lookback_bars)) / 2
avg_price_channel_low = lowest(low, lookback_bars) + (highest(high, lookback_bars) - lowest(low, lookback_bars)) / 2

// Conditions for Entry and Exit
long_condition = avg_price_channel_only ? price_high > avg_price_channel_high : trend_fast_slow_ema ? ema_fast > ema_slow : rsi < 30
short_condition = avg_price_channel_only ? price_low < avg_price_channel_low : trend_fast_slow_ema ? ema_fast < ema_slow : rsi > 70

// Strategy Execution
if (long_condition and not short_only)
    strategy.entry("Long", strategy.long)

if (short_condition and not long_only)
    strategy.entry("Short", strategy.short)

// Stop Loss and Take Profit
stop_loss = stop_price(close, stop_loss_percent / 100)
take_profit = take_profit(close, target_profit_percent / 100)

strategy.exit("StopLoss/Profit", "Long", stop=stop_loss, limit=take_profit)
strategy.exit("StopLoss/Profit", "Short", stop=stop_loss, limit=take_profit)

// Risk Management
if (not trend_fast_slow_ema and not avg_price_channel_only and not price_moving_average_only and not price_fibonacci_average_only)
    strategy.cancel_all()

// Plotting Indicators
plot(price_high, title="Price High Source", color=color.red)
plot(avg_price_channel_high, title="Average Price Channel High", color=color.blue)
plot(ema_fast, title="Fast EMA", color=color.green)
plot(ema_slow, title="Slow EMA", color=color.orange)
```