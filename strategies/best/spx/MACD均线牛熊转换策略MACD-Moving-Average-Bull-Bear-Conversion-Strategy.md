``` pinescript
/*backtest
start: 2022-12-01 00:00:00
end: 2023-12-07 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("MACD Moving Average Bull Bear Conversion Strategy", 
          shorttitle="BB Conversion", 
          overlay=true, 
          pyramiding=1, 
          max_bars_back=5000, 
          calc_on_order_fills = false, 
          calc_on_every_tick=true, 
          default_qty_type=strategy.percent_of_equity, 
          default_qty_value=100, 
          commission_type = strategy.commission.percent)
```

This Pine Script code implements the MACD Moving Average Bull Bear Conversion Strategy with a short title of "BB Conversion" to match the translated description. The other parameters remain as specified in the original script.