> Source (PineScript)

``` pinescript
/*backtest
start: 2024-04-01 00:00:00
end: 2024-04-30 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © muratatilay

//@version=5
strategy(
     "Kumo Trade Concept", 
     overlay=true,
     initial_capital=10000,
     currency=currency.USDT,
     default_qty_type=strategy.percent_of_equity, 
     default_qty_value=30,
     commission_type=strategy.commission.percent,
     commission_value=0.1,
     margin_long=10, 
     margin_short=10)


// ICHIMOKU Lines 
//  INPUTS
tenkanSenPeriods = input.int(9, minval=1, title="Tenkan-sen")
kijunSenPeriods = input.int(26, minval=1, title="Kijun-sen")
senkouBPeriod = input.int(52, minval=1, title="Senkou span B")
displacement = input.int(26, minval=1, title="Chikou span")

donchian(len) => math.avg(ta.lowest(len), ta.highest(len))
tenkanSen = donchian(tenkanSenPeriods)
kijunSen = donchian(kijunSenPeriods)
senkouA = math.avg(tenkanSen, kijunSen)
senkouB = donchian(senkouBPeriod)

// Other Indicators
float   atrValue    = ta.atr(5)

// Calculate Senkou Span A 25 bars back
senkouA_current = math.avg(tenkanSen[25], kijunSen[25])
// Calculate Senkou Span B 25 bars back
senkouB_current = math.avg(ta.highest(senkouBPeriod)[25], ta.lowest(senkouBPeriod)[25])

// Kumo top bottom 
senkou_max = (senkouA_current >= senkouB_current) ? senkouA_current : senkouB_current
senkou_min = (senkouB_current >= senkouA_current) ? senkouA_current : senkouB_current

// Trade Setups
long_setup = (kijunSen > senkou_max) and (close < senkou_min) 
short_setup = (kijunSen < senkou_min ) and (
```

This PineScript code snippet continues to define the strategy for going short. Here is the continuation:

``` pinescript
// Trade Setups
long_setup = (kijunSen > senkou_max) and (close < senkou_min) 
short_setup = (kijunSen < senkou_min ) and (
    close > kijunSen and
    atrValue * 3 + highest(close, 5)[25] >= high[0]
)

// Stop Loss Calculation
stop_loss_long = lowest(low, 5)[25] - atrValue * 3
stop_loss_short = highest(high, 5)[25] + atrValue * 3

// Trading Logic
when long_setup
    strategy.entry("Long", strategy.long)
    strategy.exit("Exit Long", "Long", stop=stop_loss_long)

when short_setup
    strategy.entry("Short", strategy.short)
    strategy.exit("Exit Short", "Short", stop=stop_loss_short)
```

This completes the PineScript for the Ichimoku-Kumo trading strategy.