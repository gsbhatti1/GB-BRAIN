``` pinescript
/*backtest
start: 2023-12-31 00:00:00
end: 2024-01-30 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
//study(title="CCI EMA Scalping Strategy", shorttitle="EMA-CCI-Strategy", overlay=true)
strategy("CCI EMA Scalping Strategy", shorttitle="EMA-CCI-Strategy", overlay=true)

exponential = input(true, title="Exponential MA")

// risk management inputs
inpTakeProfit   = input(defval=1000, title="Take Profit", minval=0)
inpStopLoss     = input(defval=200, title="Stop Loss", minval=0)
inpTrailStop    = input(defval=200, title="Trailing Stop Loss", minval=0)
inpTrailOffset  = input(defval=0, title="Trailing Stop Loss Offset", minval=0)

// === RISK MANAGEMENT VALUE PREP ===
// if an input is less than 1, assuming not wanted so we assign 'na' value to disable it.
useTakeProfit   = inpTakeProfit >= 1 ? inpTakeProfit : na
useStopLoss     = inpStopLoss    >= 1 ? inpStopLoss    : na
useTrailStop    = inpTrailStop   >= 1 ? inpTrailStop   : na
useTrailOffset  = inpTrailOffset >= 1 ? inpTrailOffset : na

src = close

ma10 = exponential ? ema(src, 10) : sma(src, 10)
ma21 = exponential ? ema(src, 21) : sma(src, 21)
ma50 = exponential ? ema(src, 50) : sma(src, 50)

xCCI = cci(close, 200)

// buy condition: short-term MA crosses above medium-term and long-term MAs and CCI is positive
buy_cond = ma10 > ma21 and ma10 > ma50 and xCCI > 0

// sell condition: short-term MA crosses below medium-term and long-term MAs and CCI is negative
sell_cond = ma10 < ma21 and ma10 < ma50 and xCCI < 0

// === STRATEGY - LONG POSITION EXECUTION ===
enterLong() => buy_cond
exitLong() => ma10 < ma21
strategy.entry(id="Long", long=true, when=enterLong())
```

This translation preserves the original code blocks and formatting while translating the human-readable text from Chinese to English.