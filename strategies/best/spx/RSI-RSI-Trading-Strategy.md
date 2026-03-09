``` pinescript
/*backtest
start: 2022-12-13 00:00:00
end: 2023-12-19 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("RSI Trading Strategy for BTC/USDT", overlay=true)

// Strategy Parameters
length = input(14, title="RSI Length")
oversold_level = input(30, title="OverSell Level")
oversold_level = input(70, title="OverBuy Level")
initial_capital = input(20, title="Initial Capital (USDT)")
```