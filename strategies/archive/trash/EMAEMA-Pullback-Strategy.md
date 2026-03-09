``` pinescript
/*backtest
start: 2023-11-20 00:00:00
end: 2023-12-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// created by Space Jellyfish
//@version=4

strategy("EMA pullback strategy", overlay = true, initial_capital=10000, commission_value = 0.075)

target_stop_ratio = input(title="Take Profit Stop Loss ratio", type=input.float, defval=2.06, minval=0.5, maxval=100)
riskLimit_low =  input(title="lowest risk per trade", type=input.float, defval=0.008, minval=0, maxval=100)
riskLimit_high =  input(title="highest risk per trade", type=input.float, defval=0.02, minval=0, maxval=100)
// Adjust position size if the risk is smaller than limit and give up the trade if risk is bigger than limit

ema_pullbackLevel_period = input(title="EMA1 for pullback level Period", type=input.integer, defval=33, minval=1, maxval=10000)
ema_pullbackLimiit_period = input(title="EMA2 for pullback limit Period", type=input.integer, defval=165, minval=1, maxval=10000)
ema_trend_period = input(title="EMA3 for trend Period", type=input.integer, defval=365, minval=1, maxval=10000)

startDate = input(title="Start Date", type=input.integer, defval=1, minval=1, maxval=31)
startMonth = input(title="Start Month", type=input.integer, defval=1, minval=1, maxval=12)
startYear = input(title="Start Year", type=input.integer, defval=2018, minval=1900)

// Calculate EMA values
ema1 = ema(close, ema_pullbackLevel_period)
ema2 = ema(close, ema_pullbackLimiit_period)
ema3 = ema(close, ema_trend_period)

// Determine entry signals
longCondition = crossover(close, ema1) and (low[1] < ema2) and (low < ema2)
shortCondition = crossunder(close, ema1) and (high[1] > ema2) and (high > ema2)

// Risk management parameters
maxRisk = riskLimit_high - riskLimit_low

// Place orders based on signals
if (longCondition)
    strategy.entry("Long", strategy.long)
    if ((bar_index - startDate * 365 + startMonth * 30 + startYear) >= 1461)
        strategy.exit("Take Profit Long", from_entry="Long", limit=target_stop_ratio * maxRisk + close)

if (shortCondition)
    strategy.entry("Short", strategy.short)
    if ((bar_index - startDate * 365 + startMonth * 30 + startYear) >= 1461)
        strategy.exit("Take Profit Short", from_entry="Short", limit=close / target_stop_ratio - maxRisk)

// Print EMA values for debugging
plot(ema1, title="EMA1", color=color.blue)
plot(ema2, title="EMA2", color=color.red)
plot(ema3, title="EMA3", color=color.green)
```

This Pine Script implements the EMA pullback strategy as described. It uses three EMAs to generate trading signals and incorporates risk management based on specified stop loss and take profit ratios. The script also includes start date parameters for filtering trades.