``` pinescript
/*backtest
start: 2024-11-12 00:00:00
end: 2024-12-11 08:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © tobiashartemink2

//@version=5
strategy("High 5 Trading Technique", overlay=true)

// --- Input parameters ---
sma89Length = input.int(title="SMA 89 Length", defval=89)
sma21Length = input.int(title="SMA 21 Length", defval=21)
ema5HighLength = input.int(title="EMA 5 High Length", defval=5)
ema5LowLength = input.int(title="EMA 5 Low Length", defval=5)
contracts = input.int(title="Number of Contracts", defval=1)
stopLossPoints = input.int(title="Stop Loss Points per Contract", defval=25)
takeProfitPoints = input.int(title="Take Profit Points per Contract", defval=25)

// --- Calculate moving averages ---
sma89 = ta.sma(close, sma89Length)
sma21 = ta.sma(close, sma21Length)
ema5High = ta.ema(high, ema5HighLength)
ema5Low = ta.ema(low, ema5LowLength)

// --- Identify trend and order of moving averages ---
longSetup = close > sma89 and close > sma21 and ema5High > sma21 and sma21 > sma89
shortSetup = close < sma89 and close < sma21 and ema5Low < sma21 and sma21 < sma89

// --- Entry signals ---
longTrigger = longSetup and close <= ema5Low
shortTrigger = shortSetup and close >= ema5High

// --- Position management ---
if (longTrigger)
    strategy.entry("Long", strategy.long, size=contracts)
    strategy.exit("Long Exit", "Long", stop=sma89 - stopLossPoints, limit=sma89 + takeProfitPoints)

if (shortTrigger)
    strategy.entry("Short", strategy.short, size=contracts)
    strategy.exit("Short Exit", "Short", stop=sma89 + stopLossPoints, limit=sma89 - takeProfitPoints)
```

The provided Pine Script is a continuation of the strategy description, ensuring all code blocks, numbers, and formatting remain unchanged.