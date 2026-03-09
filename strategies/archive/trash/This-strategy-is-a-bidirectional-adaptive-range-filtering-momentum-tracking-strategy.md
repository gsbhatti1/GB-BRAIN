``` pinescript
/*backtest
start: 2023-01-17 00:00:00
end: 2024-01-23 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("Range Filter [DW] & Labels", shorttitle="RF [DW] & Labels", overlay=true)


//Conditional Sampling EMA Function 
Cond_EMA(x, cond, n)=>
    var val     = array.new_float(0)
    var ema_val = array.new_float(1)
    if cond
        array.push(val, x)
        if array.size(val) > 1
            array.remove(val, 0)
        if na(array.get(ema_val, 0))
            array.fill(ema_val, array.get(val, 0))
        array.set(ema_val, 0, (array.get(val, 0) - array.get(ema_val, 0))*(2/(n + 1)) + array.get(ema_val, 0))
    EMA = array.get(ema_val, 0)
    EMA

//Conditional Sampling SMA Function
Cond_SMA(x, cond, n)=>
    var vals = array.new_float(0)
    if cond
        array.push(vals, x)
        if array.size(vals) > n
            array.remove(vals, 0)
    SMA = array.avg(vals)
    SMA

//Standard Deviation Function
Stdev(x, n)=>
    sqrt(Cond_SMA(pow(x, 2), 1, n) - pow(Cond_SMA(x, 1, n), 2))

//Range Size Function
rng_size(x, scale, qty, n)=> 
    ATR      = Cond_EMA(tr(true), 1, n)
    AC       = Cond_EMA(abs(x - x[1]), 1, n)
    SD       = Stdev(x, n)
    rng_size = scale=="Pips" ? qty*0.0001 : scale=="Points" ? qty*syminfo.pointvalue : scale=="% of Price" ? close*qty/100 : scale=="ATR" ? qty*ATR :
               scale=="Average Change" ? qty*AC : scale=="Standard Deviation" ? qty*SD : scale=="Ticks" ? qty*syminfo.mintick : qty   

//Two Type Range Filter Function
rng_filt(h, l, rng_, n, type, smooth, sn, av_rf, av_n)=>
    rng_smooth = Cond_EMA(rng_, 1, sn)
    r          = smooth ? rng_smooth : rng_
    var rfilt  = array.new_float(2, (h + l)/2)
    array.set(rfilt, 1, array.get(rfilt, 0))
    if type=="Type 1"
        if h - r > array.get(rfilt, 1)
            array.set(rfilt, 0, h - r)
        if l + r < array.get(rfilt, 1)
            array.set(rfilt, 0, l + r)
    if type=="Type 2"
        i
```