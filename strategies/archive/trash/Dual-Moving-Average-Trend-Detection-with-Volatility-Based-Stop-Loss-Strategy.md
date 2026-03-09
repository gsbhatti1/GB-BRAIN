> Source (PineScript)

``` pinescript
/*backtest
start: 2024-02-20 00:00:00
end: 2024-05-31 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Binance","currency":"TRB_USDT"}]
*/

//@version=5
strategy("EMA 9/21 + ATR SL Strategy", shorttitle="EMA+ATR", overlay=true)

// ===== Input Parameters ===== //
emaFastLen  = input.int(9,  "Fast EMA")
emaSlowLen  = input.int(21, "Slow EMA")
atrLen      = input.int(14, "ATR Length")
atrMult     = input.float(1.5, "ATR Multiplier")

// ===== EMA Calculation ===== //
emaFast = ta.ema(close, emaFastLen)
emaSlow = ta.ema(close, emaSlowLen)

// ===== ATR Calculation ===== //
atrValue = ta.atr(atrLen)

// ===== Conditions for Entry ===== //
longCondition  = ta.crossover(emaFast, emaSlow)   // Long when 9 EMA crosses above 21 EMA
shortCondition = ta.crossunder(emaFast, emaSlow)  // Short when 9 EMA crosses below 21 EMA

// ===== Entry Commands ===== //
if longCondition
    strategy.entry("Long", strategy.long)

if shortCondition
    strategy.entry("Short", strategy.short)

// ===== Set Stop-Loss Using ATR ===== //
stopLossValue = if (strategy.position_size > 0)
                    close - atrValue * atrMult  // Long position stop-loss
                else if (strategy.position_size < 0)
                    close + atrValue * atrMult  // Short position stop-loss

// Apply stop-loss to the strategy
if (strategy.position_size > 0)
    strategy.exit("Stop Loss", from_entry="Long", stop=stopLossValue)

if (strategy.position_size < 0)
    strategy.exit("Stop Loss", from_entry="Short", stop=stopLossValue)
```

This PineScript code implements the "EMA 9/21 + ATR SL Strategy" as described. It uses two Exponential Moving Averages (EMAs) to determine market trends and calculates a stop-loss based on the Average True Range (ATR). The strategy defines conditions for entering long or short positions and sets appropriate stop-loss levels dynamically.