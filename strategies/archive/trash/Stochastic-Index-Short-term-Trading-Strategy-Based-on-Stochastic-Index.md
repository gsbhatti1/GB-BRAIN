> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_1|5|sm1|
|v_input_2|3|sm2|
|v_input_3|55|Over Bought Level 1|
|v_input_4|35|Over Bought Level 2|
|v_input_5|-55|Over Sold Level 1|
|v_input_6|-35|Over Sold Level 2|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-10 00:00:00
end: 2024-01-17 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy(title="SMIndex Strategy", shorttitle="SMIndex Strategy", overlay=false, pyramiding=0, initial_capital=1000, currency=currency.USD)
//
sm1 = input(5, 'sm1')
sm2 = input(3, 'sm2')
//
Lower = lowest (low, sm1)
Hight = highest (high, sm1)
Downsideup = Hight - Lower
Upsidedown = close - (Hight+Lower)/2
//
ema1 = ema(ema(Upsidedown,sm2),sm2)
ema2 = ema(ema(Downsideup,sm2),sm2)
smi = ema2 != 0 ? (ema1/(ema2/2)*100) : 0
//
obLevel1 = input(55, "Over Bought Level 1")
obLevel2 = input(35, "Over Bought Level 2")
osLevel1 = input(-55, "Over Sold Level 1")
osLevel2 = input(-35, "Over Sold Level 2")
//
// h1=plot(obLevel1, color=red, title='Sell 1s 55 do', style=dashed, linewidth=2)
// h2=plot(obLevel2, color=maroon, title='Sell 2s 35 do', style=circles, linewidth=2)
// h3=plot(osLevel1, color=red, title='Buy 1s -55 up', style=dashed, linewidth=2)
// h4=plot(osLevel2, color=maroon,
```