``` pinescript
/*backtest
start: 2023-12-03 00:00:00
end: 2024-01-02 00:00:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
// Any timeFrame ok but good on 15 minute & 60 minute, Ichimoku + Daily-Candle_cross(DT) + HULL-MA_cross + MacD combination 420 special blend
strategy("Trade Signal", shorttitle="Trade Alert", overlay=true )
keh=input(title="Double HullMA",defval=14, minval=1)
dt = input(defval=0.0010, title="Decision Threshold (0.001)", type=float, step=0.0001)
SL = input(defval=-10.00, title="Stop Loss in $", type=float, step=1)
TP = input(defval=100.00, title="Target Point in $", type=float, step=1)
ot=1
n2ma=2*wma(close, keh) - wma(2*close-wma(close,keh), keh)

// Calculate Fast and Slow Moving Averages
fastMA = hullma(close, v_input_5)
slowMA = hullma(close, v_input_6)

// Determine Trend Direction
trendDirection = crossover(fastMA, slowMA) ? 1 : (crossunder(fastMA, slowMA) ? -1 : 0)

// Decision Logic based on Threshold and Confidence
decisionLogic = abs(n2ma - close) > dt

if(decisionLogic)
    if(trendDirection == 1)
        strategy.entry("Long", strategy.long)
    else if(trendDirection == -1)
        strategy.entry("Short", strategy.short)

// Stop Loss and Take Profit
stopLossLevel = SL * strategy.position_avg_price
takeProfitLevel = TP * strategy.position_avg_price

strategy.exit("Stop Loss Exit", "Long", stop=stopLossLevel)
strategy.exit("Take Profit Exit", "Long", limit=takeProfitLevel)
strategy.exit("Stop Loss Exit", "Short", stop=-stopLossLevel)
strategy.exit("Take Profit Exit", "Short", limit=-takeProfitLevel)

// Plotting
plot(trendDirection, color=trendDirection==1 ? green : trendDirection==-1 ? red : black, title="Trend Direction")
plot(n2ma, color=black, title="N2MA")
```