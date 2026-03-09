``` pinescript
/*backtest
start: 2023-10-06 00:00:00
end: 2023-11-05 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy(title="[WAI GUA]", shorttitle="[EOS] 1.0", overlay=true)

//study(title="[WAI GUA]", shorttitle="[EOS] 1.0", overlay=true)

//
// Use Alternate Anchor TF for MAs 
uRenko    = input(true, title="IS This a RENKO Chart", type=bool)
uAltfTf   = input(false, title="Alternate TimeFrame Multiplier (0=none)", type=bool)
uColRibbon= input(false, title="Show Coloured MA Ribbons", type=bool)
uColRibbonMedian= input(false, title="Show Ribbon Median MA Lines", type=bool)
uMATypeFast   = input("EMA", title="FAST MA Ribbon Type: EMA|SMA|WMA|VWMA|SMMA|DEMA|TEMA|LAGMA|HullMA|ZEMA|TMA|SSMA", type=string, options=["EMA", "SMA", "WMA", "VWMA", "SMMA", "DEMA", "TEMA", "LAGMA", "HullMA", "ZEMA", "TMA", "SSMA"])
uMAlenFastLow = input(5, title="FAST Ribbon Lower MA Length", type=int)
uMAlenFastHigh= input(25, title="FAST Ribbon Upper Length", type=int)
uMATypeSlow   = input("EMA", title="SLOW MA Ribbon Type: EMA|SMA|WMA|VWMA|SMMA|DEMA|TEMA|LAGMA|HullMA|ZEMA|TMA|SSMA", type=string, options=["EMA", "SMA", "WMA", "VWMA", "SMMA", "DEMA", "TEMA", "LAGMA", "HullMA", "ZEMA", "TMA", "SSMA"])
uMAlenSlowLow = input(28, title="SLOW Ribbon Lower MA Length", type=int)
uMAlenSlowHigh= input(72, title="SLOW Ribbon Upper Length", type=int)
uBacktestStartYear= input(2018, title="Backtest Start Year", type=int)
uBacktestStartMonth= input(true, title="Backtest Start Month", type=bool)
uBacktestStartDay= input(true, title="Backtest Start Day", type=bool)
uInitialCap= input(0.02, title="start", type=float)
uIncrementCap= input(0.02, title="increment", type=float)
uMaxCap= input(0.2, title="maximum", type=float)
uOppTradeClose= input(false, title="Use Opposite Trade as a Close Signal", type=bool)
uColCandles= input(true, title="Colour Candles to Trade Order state", type=bool)
uOrdersType= input(0, title="What type of Orders: Longs+Shorts|LongsOnly|ShortsOnly|Flip", type=int, options=[0, 1, 2, 3])
uTrailingStop= input(true, title="Trailing Stop", type=bool)
uTrailingStopPerc= input(3, title="Trailing Stop (%)", type=float)
uTakeProfit= input(true, title="Take Profit", type=bool)
uTakeProfitPerc= input(3, title="Take Profit (%)", type=float)
uTrailingProfitPerc= input(true, title="Trailing Profit (%)", type=bool)
uStopLoss= input(false, title="Stop Loss", type=bool)
uStopLossPerc= input(3, title="Stop Loss (%)", type=float)

// Main strategy logic
// ...


```