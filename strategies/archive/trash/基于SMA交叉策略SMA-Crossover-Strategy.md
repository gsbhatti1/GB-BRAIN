```pinescript
/*backtest
start: 2023-10-01 00:00:00
end: 2023-10-13 00:00:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@author Jacques Grobler
//
//                  SIMPLE CROSS OVER BOT
//                  =====================
//
// This is a simple example of how to set up a strategy to go long or short
// If you make any modifications or have any suggestions, let me know
// When using this script, every section marked back testing should be 
// uncommented in order to use for back testing, same goes for using the script portion

///////////////////////////////////////////////////////////////////////////////////////
//// INTRO
//// -----
// BACKTESTING
//@version=4
strategy(title="SimpleCrossOver_Bot_V1_Backtester", overlay=true, default_qty_type=strategy.percent_of_equity, default_qty_value=100, pyramiding=0, commission_type=strategy.commission.percent, commission_value=0.1)

// SIGNALS
//study(title="SimpleCrossOver_Bot_V1_Signals", overlay = true)

///////////////////////////////////////////////////////////////////////////////////////
//// INPUTS
//// ------
// BACKTESTING
dateStart_Year = input(2018, title="Start Year", minval=2000)
dateStart_Month = input(1, title="Start Month", minval=1, maxval=12)
dateStart_Day = input(1, title="Start Day", minval=1, maxval=31)
dateEnd_Year = input(2019, title="End Year", minval=2000)
dateEnd_Month = input(1, title="End Month", minval=1, maxval=12)
dateEnd_Day = input(1, title="End Day", minval=1, maxval=31)

// BACKTESTING AND SIGNALS
fast_SMA_input = input(7, title="SMA Fast")
slow_SMA_input = input(25, title="SMA Slow")

///////////////////////////////////////////////////////////////////////////////////////
//// INDICATORS
//// ----------
fast_SMA = sma(close, fast_SMA_input)
slow_SMA = sma(close, slow_SMA_input)

///////////////////////////////////////////////////////////////////////////////////////
//// STRATEGY
//// --------
LONG = cross(fast_SMA, slow_SMA) and fast_SMA > slow_SMA
stratLONG() => crossover(fast_SMA, slow_SMA)
SHORT = crossunder(fast_SMA, slow_SMA) and fast_SMA < slow_SMA
stratSHORT() => crossunder(fast_SMA, slow_SMA)

if stratLONG()
    strategy.entry("Long", strategy.long)
if stratSHORT()
    strategy.entry("Short", strategy.short)
```

Note: The `crossover` and `crossunder` functions in Pine Script are used to detect when one moving average crosses above or below another. The `strategy.entry` function is used to enter trades based on the conditions defined.