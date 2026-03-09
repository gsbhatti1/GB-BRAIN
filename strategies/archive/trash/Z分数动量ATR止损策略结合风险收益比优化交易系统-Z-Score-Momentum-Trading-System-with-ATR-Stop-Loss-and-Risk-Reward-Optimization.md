```pinescript
/*backtest
start: 2024-10-01 00:00:00
end: 2025-02-18 08:00:00
period: 2h
basePeriod: 2h
exchanges: [{"eid":"Binance","currency":"ETH_USDT"}]
*/

//@version=5
strategy("admbrk | Candle Color & Price Alarm with ATR Stop", overlay=true, initial_capital=50, default_qty_type=strategy.cash, default_qty_value=200, commission_type=strategy.commission.percent, commission_value=0.05, pyramiding=3)

// **Risk/Reward ratio (RR) as input**
rr = input.float(2.0, title="Risk/Reward Ratio (RR)", step=0.1)

// **Z-score calculation function**
f_zscore(src, len) =>
    mean = ta.sma(src, len)     
    std = ta.stdev(src, len)
    (src - mean) / std

// **Z-score calculations**
len = input(20, "Z-Score MA Length")
z1 = input.float(1.5, "Threshold z1", step=0.1)
z2 = input.float(2.5, "Threshold z2", step=0.1)

z_volume = f_zscore(volume, len)
z_body = f_zscore(math.abs(close - open), len)

i_src = input.string("Volume", title="Source", options=["Volume", "Body size", "Any", "All"])

float z = na
if i_src == "Volume"
    z := z_volume
else if i_src == "Body size"
    z := z_body
else if i_src == "Any"
    z := math.max(z_volume, z_body)
else if i_src == "All"
    z := math.min(z_volume, z_body)

// **Determine trend direction**
green = close >= open
red = close < open

// **Long and Short signals**
longSignal = barstate.isconfirmed and red[1] and low < low[1] and green
shortSignal = barstate.isconfirmed and green[1] and high > high[1] and red

long = longSignal and
```