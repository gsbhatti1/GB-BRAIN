``` pinescript
/*backtest
start: 2023-08-28 00:00:00
end: 2023-09-27 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 03/03/2017
// The related article is copyrighted material from Stocks & Commodities Aug 2009 
//
// You can change long to short in the Input Settings
// Please, use it only for learning or paper trading. Do not for real trading.
////////////////////////////////////////////////////////////
strategy(title="Combining DMI And Moving Average For A Trading Strategy")
Length_MA = input(30, minval=1)
Length_DMI = input(14, minval=1)
reverse = input(false, title="Trade reverse")

xMA = sma(close, Length_MA)
up = change(high)
down = -change(low)
trur = rma(tr, Length_DMI)
xPDI = fixnan(100 * rma(up > down and up > 0 ? up : 0, Length
```