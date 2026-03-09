``` pinescript
/*backtest
start: 2024-10-28 00:00:00
end: 2024-11-27 00:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © algostudio
// Code Generated using PineGPT - www.marketcalls.in

//@version=5
strategy("Squeeze Momentum and Ultimate Buy/Sell with Stop Loss", overlay=true, process_orders_on_close = false)

// Input settings
smiLength = input.int(20, title="SMI Length")
smiSmoothing = input.int(5, title="SMI Smoothing")
ultBuyLength = input.int(14, title="Ultimate Buy/Sell Length")
stopLossPerc = input.float(2.5, title="Stop Loss Percentage", step=0.1) / 100

// Define Squeeze Momentum logic
smi = ta.sma(close - ta.lowest(low, smiLength), smiSmoothing) - ta.sma(ta.highest(high, smiLength) - close, smiSmoothing)
squeezeMomentum = ta.sma(smi, smiSmoothing)
smiUp = squeezeMomentum > squeezeMomentum[1]
smiDown = squeezeMomentum < squeezeMomentum[1]

// Define Ultimate Buy/Sell Indicator logic (you can customize the conditions)
ultimateBuy = ta.crossover(close, ta.sma(close, ultBuyLength))
ultimateSell = ta.crossunder(close, ta.sma(close, ultBuyLength))

// Trading logic: Short entry (Squeeze Momentum from green to red and Ultimate Sell signal)
shortCondition = smiDown and ultimateSell
if (shortCondition)
    strategy.entry("Short", strategy.short)

// Set short target (exit when price decreases by 0.4%)
shortTarget = strategy.position_avg_price * 0.996

// Set stop loss for short (2.5% below the entry price)
shortStop = strategy.position_avg_price * (1 - stopLossPerc)

// Exit logic for short
if (strategy.position_avg_price < shortStop or close <= shortTarget)
    strategy.close("Short")

```