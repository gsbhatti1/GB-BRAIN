``` pinescript
/*backtest
start: 2024-02-22 00:00:00
end: 2025-02-19 08:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Binance","currency":"SOL_USDT"}]
*/

//@version=5
strategy("15m - Rebound 50SMA with Dynamic Lots & Trailing Stop, RRR 2:1, Date Filter (Closed Bars Only)", 
     overlay=true, 
     initial_capital=50000, 
     default_qty_type=strategy.fixed, 
     default_qty_value=1, 
     pyramiding=0, 
     calc_on_order_fills=true)

// ===== INPUTS =====
sma50Period  = input.int(50, "50 SMA Period", minval=1)
sma200Period = input.int(200, "200 SMA Period", minval=1)

// ===== CALCULATE SMAs =====
sma50  = ta.sma(close, sma50Period)
sma200 = ta.sma(close, sma200Period)

// ===== PLOT SMAs =====
plot(sma50, color=color.red, title="50 SMA")
plot(sma200, color=color.blue, title="200 SMA")

// ===== DEFINE TRADING SESSIONS =====
// Trading is allowed 15 minutes after market open:
//   - New York: 09:45–16:00 (America/New_York)
//   - London:   08:15–16:00 (Europe/London)
nySession     = not na(time("15", "0945-1600", "America/New_York"))
londonSession = not na(time("15", "0815-1600", "Europe/London"))
inSession     = nySession or londonSession

// ===== DEFINE DATE RANGE =====
// Only allow orders on or after January 1, 2024.
// (We include seconds in the timestamp for proper parsing.)
startDate   = timestamp("UTC", 2024, 1, 1, 0, 0, 0)
inDateRange = time >= startDate

// ===== DEFINE ENTRY CONDITIONS =====
// ----- LONG ENTRY CONDITION -----
// A long entry is triggered when:
//   - The previous candle closed below the 50 SMA and the current candle closes above it,
//   - And the 50 SMA is above the 200 SMA.
longCondition = (close[1] < sma50) and (close >= sma50) and (sma50 > sma200)

// ----- SHORT ENTRY CONDITION -----
// A short entry is triggered when:
//   - The previous candle closed above the 50 SMA and the current candle closes below it,
//   - And the 50 SMA is below the 200 SMA.
shortCondition = (close[1] > sma50) and (close <= sma50) and (sma50 < sma200)

// ===== POSITION SIZING AND TRAILING STOP MECHANISM =====
profitTarget = strategy.net profit + 4000

if (inSession and inDateRange)
    if (longCondition)
        strategy.entry("Long", strategy.long, comment="Long Entry")
        
    elif shortCondition
        strategy.entry("Short", strategy.short, comment="Short Entry")

// Dynamic position sizing: increase position size by one lot when net profit exceeds 4000 units.
if (strategy.netprofit > 4000)
    strategy.close_all()
    strategy.entry("Long", strategy.long, qty=2)  // Example of increasing position to two lots

// Trailing stop mechanism
trailAmount = 1.25 * syminfo.mintick
stopPrice   = na(strategy.position_avg_price)

if (strategy.position_size > 0)
    if not na(stopPrice)
        strategy.exit("Long Exit", "Long", trail=True, trail_offset=trailAmount)

if (strategy.position_size < 0)
    if not na(stopPrice)
        strategy.exit("Short Exit", "Short", trail=True, trail_offset=trailAmount)

```

This updated Pine Script includes the missing conditions for both long and short entries, as well as the logic to dynamically adjust position size and implement a trailing stop mechanism.