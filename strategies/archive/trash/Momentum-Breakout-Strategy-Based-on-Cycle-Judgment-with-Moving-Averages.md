> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|2|Key Vaule. 'This changes the sensitivity'|
|v_input_2|7|ATR Period|
|v_input_int_1|25|atr_length|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-15 00:00:00
end: 2024-01-22 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © kgynofomo

//@version=5
strategy(title="[Salavi] | Andy Advance Pro Strategy", overlay = true)

ema_short = ta.ema(close, 5)
ema_middle = ta.ema(close, 20)
ema_long = ta.ema(close, 40)

cycle_1 = ema_short > ema_middle and ema_middle > ema_long
cycle_2 = ema_middle > ema_short and ema_short > ema_long
cycle_3 = ema_middle > ema_long and ema_long > ema_short
cycle_4 = ema_long > ema_middle and ema_middle > ema_short
cycle_5 = ema_long > ema_short and ema_short > ema_middle
cycle_6 = ema_short > ema_long and ema_long > ema_middle

bull_cycle = cycle_1 or cycle_2 or cycle_3
bear_cycle = cycle_4 or cycle_5 or cycle_6

xATR = ta.atr(v_input_2)
nLoss = v_input_1 * xATR

src = request.security(syminfo.tickerid, timeframe.period, close)

xATRTrailingStop = 0.0
iff_1 = src > nz(xATRTrailingStop[1], 0) ? src - nLoss : src + nLoss
iff_2 = src < nz(xATRTrailingStop[1], 0) ? src + nLoss : src - nLoss

if bull_cycle
    strategy.entry("Buy", strategy.long, when = iff_1 > src)
if bear_cycle
    strategy.exit("Sell", "Buy", when = iff_2 < src)

// Additional logic to handle trailing stop updates can be added here
```