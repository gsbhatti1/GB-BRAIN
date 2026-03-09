> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|price: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_int_1|50|EMA 1 Length|
|v_input_int_2|80|EMA 2 Length|
|v_input_int_3|200|EMA 3 Length|
|v_input_2|true|numberOfCandles|
|v_input_3|3.5|slATRFactor|
|v_input_4|3.5|tpATRFactor|
|v_input_5|14|ATRLength|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-21 00:00:00
end: 2024-01-28 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy('Trend Continuation', shorttitle='Trend_Continuation', overlay=true)

// Input
price = input(close)
MA1_Length = input.int(50, step=1, title='EMA 1 Length')
MA2_Length = input.int(80, step=1, title='EMA 2 Length')
MA3_Length = input.int(200, step=1, title='EMA 3 Length')
numberOfCandles = input(1)
slATRFactor = input(3.5)
tpATRFactor = input(3.5)
ATRLength = input(14)
// switch1=input(true, title="Show Bar Color?")
// switch2=input(true, title="Show Moving Averages?")

// Calculation
MA1 = ta.ema(price, MA1_Length)
MA2 = ta.ema(price, MA2_Length)
MA3 = ta.ema(price, MA3_Length)
prev_price = close[numberOfCandles]


// Strategy
allPositive = true
for i = 0 to numberOfCandles - 1 by 1
    if close[i] < close[i + 1] or close[i] < MA1
        allPositive := false
        break


long = MA2 > MA3 and price > MA1 and ta.crossunder(prev_price, MA1) and allPositive
// short = crossover(price, MA3) or ( change(price)>0 and change(MA1)>0 and crossover(price,MA1)  and change(MA2)<0 ) 


if long
    strategy.entry('Long', strategy.long, comment='Long')

bought = strategy.position_size[0] > strategy.position_size[1]
atrAtLong = ta.valuewhen(bought, ta.atr(ATRLength), 0)


// Stop loss and take profit
slPrice = strategy.position_avg_price - slATRFactor * atrAtLong
tpPrice = strategy.position_avg_price + tpATRFactor * atrAtLong

SL = plot(slPrice, title='SL', style=plot.style_linebr, linewidth=1, color=color.new(color.red, 0))

if price >= tpPrice and price < MA1
    strategy.close('Long')

if price < strategy.position_avg_price
    strategy.exit('Stop Loss', 'Long', stop=slPrice)


// Strategy Alert
alertcondition(long, title='Long Alert', message='Go ')
```