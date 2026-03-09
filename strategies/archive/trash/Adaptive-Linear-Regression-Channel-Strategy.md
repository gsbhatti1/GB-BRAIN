``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy("Stealthy 7 Linear Regression Channel Strategy", overlay=true)
source = open
length = input(100, minval=1)
mult1 = input(1, minval=0.001, maxval=50)
mult2 = input(1, minval=0.001, maxval=50)
DayTrader = input(title="Range Mode", type=bool, defval=false)

// Calculate the first least squares line
sum_x = 0
sum_y = 0
sum_xy = 0
sum_xx = 0
for i = 1 to length
    sum_x := sum_x + i
    sum_y := sum_y + close[i]
    sum_xy := sum_xy + (i * close[i])
    sum_xx := sum_xx + (i * i)
m = (length * sum_xy - sum_x * sum_y) / (length * sum_xx - sum_x * sum_x)
b = sum_y / length - m * sum_x / length

// Find the first standard deviation from the line
difference = 0
for i = 1 to length
    y = i * m + b
    difference := difference + abs(close[i] - y) ^ 2
STDDEV = sqrt(difference / length)

// Create trading zones
dev = mult1 * STDDEV
dev2 = mult2 * STDDEV
upper = b + dev
lower = b - dev2
middle = b

if not DayTrader
    if crossover(source, upper)
        strategy.entry("RGLONG", strategy.long, oca_name="Reg"
```