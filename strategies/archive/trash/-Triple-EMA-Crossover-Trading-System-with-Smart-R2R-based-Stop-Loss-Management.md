``` pinescript
/*backtest
start: 2024-12-06 00:00:00
end: 2025-01-04 08:00:00
period: 4h
basePeriod: 4h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Crossover with SL to BE", shorttitle="OmegaGalsky", overlay=true)

// Input parameters
ema8_period = input.int(8, title="EMA 8 Period")
ema21_period = input.int(21, title="EMA 21 Period")
ema89_period = input.int(89, title="EMA 89 Period")
fixed_risk_reward = input.float(1.0, title="Risk/Reward Ratio (R2R)")
sl_percentage = input.float(0.001, title="Stop Loss Percentage", step=0.0001)
tp_percentage = input.float(0.0025, title="Take Profit Percentage", step=0.0001)

// Calculate EMA
ema8 = ta.ema(close, ema8_period)
ema21 = ta.ema(close, ema21_period)
ema89 = ta.ema(close, ema89_period)

// Buy condition
buy_condition = ta.crossover(ema8, ema21) and close > ema89 and close > open

// Sell condition
sell_condition = ta.crossunder(ema8, ema21) and close < ema89 and close < open

// Enter BUY position
if (buy_condition)
    stop_loss = close * (1 - sl_percentage)
    take_profit = close * (1 + tp_percentage)
    strategy.entry("BUY", strategy.long)
    strategy.exit("TP/SL", from_entry="BUY", stop=stop_loss, limit=take_profit)

// Enter SELL position
if (sell_condition)
    stop_loss = close * (1 + sl_percentage)
    take_profit = close * (1 - tp_percentage)
    strategy.entry("SELL", strategy.short)
    strategy.exit("TP/SL", from_entry="SELL", stop=stop_loss, limit=take_profit)

// Logic for moving SL to BE
if (strategy.position_size > 0)
    entry_price = strategy.position_avg_price
    // For LONG position
    if (strategy.position_size > 0 and high >= entry_price + (entry_price * sl_percentage))
        strategy.exit("SL to BE", from_entry="BUY")
    // For SHORT position
    if (strategy.position_size < 0 and low <= entry_price - (entry_price * sl_percentage))
        strategy.exit("SL to BE", from_entry="SELL")

// Plotting EMA lines on the chart
plot(ema8, title="EMA 8", color=color.blue)
plot(ema21, title="EMA 21", color=color.red)
plot(ema89, title="EMA 89", color=color.green)
```

This Pine Script code implements a trading strategy based on EMA crossovers with intelligent stop-loss management. It includes the calculation of three EMAs (EMA8, EMA21, and EMA89), entry conditions for both buy and sell positions, risk management logic to move stop-losses to break-even points when the risk-reward ratio is reached, and visualization of the EMA lines on the chart.