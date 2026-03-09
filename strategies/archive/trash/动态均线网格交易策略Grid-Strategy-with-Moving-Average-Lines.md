``` pinescript
/*backtest
start: 2022-12-13 00:00:00
end: 2023-12-19 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Seungdori_

//@version=5
strategy("Grid Strategy with MA", overlay=true, initial_capital = 100000, default_qty_type = strategy.cash, default_qty_value = 10000, pyramiding = 10, process_orders_on_close = true, commission_type = strategy.commission.percent, commission_value = 0.04)


// Inputs

length = input.int(defval = 100, title = 'MA Length', group = 'MA')
MA_Type = input.string("SMA", title="MA Type", options=['EMA', 'HMA', 'LSMA', 'RMA', 'SMA', 'WMA'],group = 'MA')

logic = input.string(defval='ATR', title ='Grid Logic', options = ['ATR', 'Percent'])

band_mult = input.float(2.5, step = 0.1, title = 'Band Multiplier/Percent', group = 'Parameter')
atr_len = input.int(defval=100, title = 'ATR Length', group ='parameter')

// Variables

var int order_cond = 0
var bool order_1 = false
var bool order_2 = false
var bool order_3 = false
var bool order_4 = false
var bool order_5 = false
var bool order_6 = false
var bool order_7 = false
var bool order_8 = false
var bool order_9 = false
var bool order_10 = false
var bool order_11 = false
var bool order_12 = false
var bool order_13 = false
var bool order_14 = false
var bool order_15 = false


/////////////////////
// Region : Function //
/////////////////////
getMA(source ,ma_type, length) =>
    maPrice = ta.ema(source, length)
    ema = ta.ema(source, length)
    sma = ta.sma(source, length)
    if ma_type == 'SMA'
        maPrice := ta.sma(source, length)
        maPrice
    if ma_type == 'HMA'
        maPrice := ta.hma(source, length)
        maPrice
    if ma_type == 'WMA'
        maPrice := ta.wma(source, length)
        maPrice
    if ma_type == "RMA"
        maPrice := ta.rma(source, length)
    if ma_type == "LSMA"
        maPrice := ta.linreg(source, length, 0)
    maPrice

main_plot = getMA(ohlc4, MA_Type, length)

atr = ta.atr(atr_len)

premium_zone_1 = logic == 'ATR' ? ta.ema(main_plot + atr * (band_mult * 1), 5) : ta.ema((main_plot * (1 + band_mult)), 5)
```