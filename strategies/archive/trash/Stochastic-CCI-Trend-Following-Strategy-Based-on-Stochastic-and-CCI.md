``` pinescript
/*backtest
start: 2022-11-15 00:00:00
end: 2023-11-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Stochastic CCI BF ?", overlay=false, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.075)

/////////////// Time Frame ///////////////
testStartYear = input(2017, "Backtest Start Year")
testStartMonth = input(1, "Backtest Start Month")
testStartDay = input(1, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear,testStartMonth,testStartDay, 0, 0)

testStopYear = input(2019, "Backtest Stop Year")
testStopMonth = input(12, "Backtest Stop Month")
testStopDay = input(31, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear,testStopMonth,testStopDay, 0, 0)

testPeriod() => true

///////////// CCI ///////////// 
src = close
ccilength = input(13, minval=1, title="CCI Length")
c = cci(src, ccilength)

///////////// Stochastic ///////////// 
len = input(19, minval=1, title="RSI Length")
lenema = input(12, minval=1, title="RSI-EMA Length")
up = rma(max(change(src), 0), len)
down = rma(-min(change(src), 0), len)
rsi = down == 0 ? 100 : up == 0 ? 0 : 100 - (100 / (1 + up / down))
out = ema(rsi, lenema)

///////////// Rate Of Change ///////////// 
source = close
roclength = input(30, minval=1)
pcntChange = input(7.0, minval=1)
roc = 100 * (source - source[roclength]) / source[roclength]
emaroc = ema(roc, roclength / 2)
isMoving() => emaroc > (pcntChange / 2) or emaroc < (0 - (pcntChange / 2))

/////////////// Strategy ///////////////
long = out > out[1] and isMoving() and c > 0
short = out < out[1] and isMoving() and c < 0

last_long = 0.0
last_short = 0.0
last_long := long ? time : nz(last_long[1])
last_short := short ? time : nz(last_short[1])

long_signal = crossover(last_long, last_short)
short_signal = crossover(last_short, last_long)

// Stop Loss
stop_loss_percent = input(3, "Stop Loss %")
strategy.exit("Exit Long", from_entry="Long Entry", loss=stop_loss_percent / 100)
strategy.exit("Exit Short", from_entry="Short Entry", loss=stop_loss_percent / 100)
```

This Pine Script implements the described trend-following strategy using Stochastic, CCI, and Rate of Change indicators. The stop loss is set to 3% as mentioned in the document.