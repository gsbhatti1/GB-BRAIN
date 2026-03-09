> Name

Grid-Strategy-with-Moving-Average-Lines

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/181aa589911d945c7af.png)
 [trans]

## Overview  

This is a grid trading strategy that utilizes moving average lines dynamically. It draws multiple buy and sell zones above and below the moving average line based on settings of the MA and volatility range. When price drops into different buy zones, corresponding long orders will be opened. When price goes back into sell zones, opened orders are closed sequentially. Thus forms a dynamic grid trading mechanism.

## Strategy Logic  

1. Users set parameters for determining major moving average line;  
2. Multiple buy and sell zones are divided based on ATR and settings;
3. When price drops into different buying zones, corresponding long orders are triggered;  
4. When price moves back into sell zones, orders are closed sequentially;
5. A dynamic grid trading system is formed eventually.

## Advantages  

1. Using MA line to determine trend direction avoids trading against major trend;
2. ATR parameter considers market volatility, making grid more dynamic;
3. Opening orders in batches controls risks;  
4. Closing orders sequentially avoids cascade stop loss; 
5. Simple parameters, easy to operate.

## Risks  

1. Significant fluctuation may frequently trigger grid losses;
2. In strong trends, stop loss points could be too close leading to quick post-pullback stops;
3. Increased transactions from multiple entries produce higher commission fees;
4. Not suitable for range-bound or trendless markets.

Risks can be reduced by relaxing grid interval, optimizing ATR parameter, reducing order quantities etc. Different parameter sets could also be used for trending and ranging scenarios.  

## Optimization Directions  

1. Spot index indicators can be added to determine bullish/bearish bias;
2. Quantitative indicators can be used to select assets with trend characteristics;
3. ATR parameters or grid intervals can be adjusted dynamically based on volatility; 
4. Profit taking mechanism can be added to follow trends.

These further optimizations will make the strategy more dynamic and locally enhanced.  

## Conclusion  

In conclusion, this is an overall mature and simple trend-following grid strategy. It uses moving averages to determine major trends, and establishes a dynamic grid mechanism for batched trades. Has certain risk control capabilities. With further quant optimizations, it can become a very practical quant tool.

||

## Source (PineScript)

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Seungdori_

//@version=5
strategy("Grid Strategy with MA", overlay=true, initial_capital = 100000, default_qty_type = strategy.cash, default_qty_value = 10000, pyramiding = 10, process_orders_on_close = true, commission_type = strategy.commission.percent, commission_value = 0.04)


// Inputs //

length = input.int(defval=100, title='MA Length', group='MA')
MA_Type = input.string("SMA", title="MA Type", options=['EMA', 'HMA', 'LSMA', 'RMA', 'SMA', 'WMA'], group='MA')

logic = input.string(defval='ATR', title ='Grid Logic', options = ['ATR', 'Percent'])

band_mult = input.float(2.5, step=0.1, title='Band Multiplier/Percent', group='Parameter')
atr_len = input.int(defval=100, title='ATR Length', group='parameter')

// Vars //

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
getMA(source, ma_type, length) =>
    maPrice = ta.ema(source, length)
    ema = ta.ema(source, length)
    sma = ta.sma(source, length)
    
    if ma_type == 'SMA'
        maPrice := ta.sma(source, length)
    else if ma_type == 'HMA'
        maPrice := ta.hma(source, length)
    else if ma_type == 'WMA'
        maPrice := ta.wma(source, length)
    else if ma_type == "RMA"
        maPrice := ta.rma(source, length)
    else if ma_type == "LSMA"
        maPrice := ta.linreg(source, length, 0)
        
    maPrice

main_plot = getMA(ohlc4, MA_Type, length)

atr = ta.atr(atr_len)

premium_zone_1 = logic == 'ATR' ? ta.ema(main_plot + atr * (band_mult * 1), 5) : ta.ema((main_plot * (1 + band_mult)), 5)
```

The provided Pine Script code defines a grid trading strategy that uses moving averages to dynamically determine buy and sell zones based on the ATR value or percentage, and then trades accordingly.