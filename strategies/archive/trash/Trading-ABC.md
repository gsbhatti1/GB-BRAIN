``` pinescript
/*backtest
start: 2022-04-22 00:00:00
end: 2022-05-21 23:59:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © LonesomeTheBlue

//@version=4
study("Trading ABC", overlay = true, max_bars_back = 500, max_lines_count = 500, max_labels_count = 500)
prd = input(defval = 8, title="ZigZag Period", minval = 2, maxval = 50, group = "Setup")
fiboup = input(defval = 0.618, title = "Fibonacci Max", group = "Setup")
fibodn = input(defval = 0.382, title = "Fibonacci Min", group = "Setup")
errorrate = input(defval = 5.0, title = "Error Rate", minval = 0, maxval = 30, group = "Setup") / 100
showabc = input(defval = true, title = "Show ABC", group = "Extras")
keepabc = input(defval = true, title = "Keep Old ABCs", group = "Extras")
showcloud = input(defval = true, title = "Show Cloud", group = "Extras", inline = "cloud")
c_upcol = input(defval = color.new(color.lime, 75), title = "", group = "Extras", inline = "cloud")
c_dncol = input(defval = color.new(color.red, 75), title = "", group = "Extras", inline = "cloud")
showzigzag = input(defval = true, title = "Show Zig Zag & Fibo", group = "Extras", inline = "zigzag")
upcol = input(defval = color.lime, title = "", group = "Extras", inline = "zigzag")
dncol = input(defval = color.red, title = "", group = "Extras", inline = "zigzag")
srcma = input(defval = close, title = "Source for Moving Averages", group = "Trend Cloud")
malen1 = input(defval = 50, title = "SMA 1 Length", minval = 1, group = "Trend Cloud")
malen2 = input(defval = 100, title = "SMA 2 Length", minval = 1, group = "Trend Cloud")
malen3 = input(defval = 150, title = "SMA 3 Length", minval = 1, group = "Trend Cloud")
malen4 = input(defval = 200, title = "SMA 4 Length", minval = 1, group = "Trend Cloud")
malen5 = input(defval = 20, title = "EMA 1 Length", minval = 1, group = "Trend Cloud")
malen6 = input(defval = 40, title = "EMA 2 Length", minval = 1, group = "Trend Cloud")

ma_array = array.new_float(6)
array.set(ma_array, 0, sma(srcma, malen1))
array.set(ma_array, 1, sma(srcma, malen2))
array.set(ma_array, 2, sma(srcma, malen3))
array.set(ma_array, 3, sma(srcma, malen4))
array.set(ma_array, 4, ema(srcma, malen5))
array.set(ma_array, 5, ema(srcma, malen6))

float umax = na
float umin = na
float lmax = na
float lmin = na
int upper = 0
int lower = 0
for x = 1 to 6
    ma = array.get(ma_array, x -1)
    if ma >= max(open, close)
        upper := upper + 1
        if na(umax)
            umax := ma
            umin := ma
        else
            umax := max(umax, ma)
            umin := min(umin, ma)
    else if ma <= min(open, close)
        lower := lower + 1
        if na(lmax)
            lmax := ma
            lmin := ma
        else
            lmax := max(lmax, ma)
            lmin := min(lmin, ma)

var int trend = 0
trend := lower > 0 and upper == 0 and lower[1] > 0 and upper[1] == 0 ? 1 :
         lower == 0 and upper > 0 and lower[1] == 0 and upper[1] > 0 ? -1 :
         trend
         
tucolor = trend ==  1 ? c_upcol: na
tdcolor = trend == -1 ? c_dncol : na
fill(plot(umax, color = na), plot(umin, color = na), color = showcloud ? tdcolor : na)
fill(plot(lmax, color = na), plot(lmin, color = na), color = showcloud ? tucolor : na)

//===================================================================

// ZigZag part
get_ph_pl_dir(len)=>
    float ph = highestbars(high, len) == 0 ? high : na
    float pl = lowestbars(low, len) == 0 ? low : na
    var dir = 0
    dir := iff(ph and na(pl), 1, iff(pl and na(ph), -1, dir))
    [ph, pl, dir]

[ph, pl, dir] = get_ph_pl_dir(prd)

var max_array_size = 10
var zigzag = array.new_float(0)

add_to_zigzag(value, bindex)=>
    array.unshift(zigzag, bindex)
    array.unshift(zigzag, value)
    if array.size(zigzag) > max_array_size
        array.pop(zigzag)
        array.pop(zigzag)
    
update_zigzag(value, bindex)=>
    if array.size(zigzag) == 0
        add_to_zigzag(value, bindex)
    else
        if (dir == 1 and value > array.get(zigzag, 0)) or (dir == -1
```