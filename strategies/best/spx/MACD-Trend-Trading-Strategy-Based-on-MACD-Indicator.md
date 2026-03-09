``` pinescript
/*backtest
start: 2023-01-26 00:00:00
end: 2024-02-01 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © melihtuna

//@version=1
strategy("Trend Trading Strategy Based on MACD Indicator", overlay=true)

// === Strategy Parameters ===
Length = input(21)
Multiplier = input(3, minval=1)
MacdControl = input(true, title="Control 'MACD Histogram is positive?' when Buy condition")
FromMonth = input(true)
FromDay = input(true)
FromYear = input(2020)
ToMonth = input(true)
ToDay = input(true)
ToYear = input(9999)

// === Trend Determination ===
avgTR      = wma(atr(1), Length)
highestC   = highest(Length)
lowestC    = lowest(Length)
hiLimit = highestC[1]-(avgTR[1] * Multiplier)
loLimit = lowestC[1]+(avgTR[1] * Multiplier)
ret = iff(close > hiLimit and close > loLimit, hiLimit,
        iff(close < loLimit and close < hiLimit, loLimit, nz(ret[1], 0)))
pos =	iff(close > ret, 1,
	    iff(close < ret, -1, nz(pos[1], 0))) 
barcolor(pos == -1 ? red: pos == 1 ? green : blue )
plot(ret, color= blue , title="Trend Trading Strategy Based on MACD Indicator")

// === MACD Filtering ===
if (MacdControl and macd > 0)
    strategy.entry("Buy", strategy.long)
```