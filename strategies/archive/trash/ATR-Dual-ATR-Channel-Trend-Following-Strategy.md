``` pinescript
/*backtest
start: 2023-10-24 00:00:00
end: 2023-10-27 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title="Dual ATR Channel Trend Following", overlay=true, default_qty_value=100000, initial_capital=100)

//////////////////////
////// BASELINE //////
//////////////////////
ma_slow_type = input(title="Baseline Type", type=input.string, defval="Kijun", options=["ALMA", "EMA", "DEMA", "TEMA", "WMA", "VWMA", "SMA", "SMMA", "HMA", "LSMA", "Kijun", "McGinley"])
ma_slow_src = close //input(title="MA Source", type=input.source, defval=close)
ma_slow_len = input(title="Baseline Length", type=input.integer, defval=20)
ma_slow_len_fast = input(title="Baseline Length Fast", type=input.integer, defval=12)

lsma_offset  = input(defval=0, title="* Least Squares (LSMA) Only - Offset Value", minval=0)
alma_offset  = input(defval=0.85, title="* Arnaud Legoux (ALMA) Only - Offset Value", minval=0, step=0.01)
alma_sigma   = input(defval=6, title="* Arnaud Legoux (ALMA) Only - Sigma Value", minval=0)

ma(type, src, len) =>
    float result = 0
    if type=="SMA" // Simple
        result := sma(src, len)
    if type=="EMA" // Exponential
        result := ema(src, len)
    if type=="DEMA" // Double Exponential
        result := dema(src, len)
    if type=="TEMA" // Triple Exponential
        result := tema(src, len)
    if type=="WMA" // Weighted
        result := wma(src, len)
    if type=="VWMA" // Volume Weighted
        result := vwma(src, len)
    if type=="HMA" // Hull
        result := hma(src, len)
    if type=="LSMA" // Least Squares
        result := lsma(src, len, lsma_offset)
    if type=="ALMA" // Arnaud Legoux
        result := alma(src, len, alma_offset, alma_sigma)
    result

kijun_line = ma(ma_slow_type, ma_slow_src, ma_slow_len)

//////////////////////
////// ATR CHANNEL //////
//////////////////////
atr_len = input(title="ATR Length", type=input.integer, defval=14)
atr = atr(atr_len)

upper_band = kijun_line + 0.5 * atr
lower_band = kijun_line - 0.5 * atr

donttradeoutside_atrcave = input(title="donttradeoutside_atrcave", type=input.bool, defval=true)

//////////////////////
////// CONFIRMATION //////
//////////////////////
aroon_length = input(title="Length Aroon", type=input.integer, defval=8)
aroon = aroon(aroon_length)

rsi_length = input(title="RSI Length", type=input.integer, defval=14)
rsi = rsi(close, rsi_length)

macd_fast = input(title="Fast Length", type=input.integer, defval=13)
macd_slow = input(title="Slow Length", type=input.integer, defval=26)
macd_signal = input(title="Signal Smoothing", type=input.integer, defval=9)
[...]
```