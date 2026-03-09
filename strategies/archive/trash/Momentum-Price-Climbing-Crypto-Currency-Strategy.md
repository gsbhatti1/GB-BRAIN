> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|60|Number of candles|
|v_input_2|14|Length VORTEX|
|v_input_3|0.1|TP Long|
|v_input_4|0.1|SL Long|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-04 00:00:00
end: 2024-02-03 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © exlux99
//@version=4
strategy(title="Crypto Price Scalper", shorttitle="Scalper Crypto", overlay=true)

inputcc = input(60, title="Number of candles")

low9 = lowest(low, inputcc)
high9 = highest(high, inputcc)

plotlow = ((close - low9) / low9) * 100
plothigh = ((close - high9) / high9) * 100
plotg = (plotlow + plothigh) / 2

center = 0.0

period_ = input(14, title="Length VORTEX", minval=2)
VMP = sum(abs(high - low[1]), period_)
VMM = sum(abs(low - high[1]), period_)
STR = sum(atr(1), period_)
VIP = VMP / STR
VIM = VMM / STR

long = crossover(plotg, center) and close > high[2] and crossover(VIP, VIM)
short = crossunder(plotg, center) and crossunder(VIP, VIM)

tpLong = input(0.1, title="TP Long")
slLong = input(0.1, title="SL Long")

strategy.entry("Buy", strategy.long, when=long)
strategy.exit("Take Profit/Stop Loss", "Buy", profit=tpLong * close, loss=slLong * close)

```

This PineScript code defines a trading strategy for cryptocurrencies that uses price oscillation and vortex indicators to identify entry and exit points. It includes settings for the number of candles, length of the VORTEX indicator, take profit (TP) and stop loss (SL) levels. The strategy enters long positions based on certain conditions involving these indicators and exits when those conditions are no longer met or when the TP or SL is reached.