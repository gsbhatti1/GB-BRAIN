> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|Length|
|v_input_2|true|KSmoothing|
|v_input_3|3|DLength|
|v_input_4|50|Level|
|v_input_5|30|SellLevel|
|v_input_6|3|BuyLevel|
|v_input_7|false|Trade reverse|


> Source (PineScript)

``` pinescript
/*backtest
start: 2023-11-13 00:00:00
end: 2023-11-20 00:00:00
period: 10m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 29/05/2019
// This is combo strategies for get 
// a cumulative signal. Result signal will return 1 if two strategies 
// is long, -1 if all strategies is short and 0 if signals of strategies is not equal.
//
// First strategy
// This System was created from the Book "How I Tripled My Money In The 
// Futures Market" by Ulf Jensen, Page 183. This is reverse type of strategies.
// The strategy buys at market, if close price is higher than the previous close 
// during 2 days and the meaning of 9-days Stochastic Slow Oscillator is lower than 50. 
// The strategy sells at market, if close price is lower than the previous close price 
// during 2 days and the meaning of 9-days Stochastic Fast Oscillator is higher than 50.
//
// Second strategy
// Bear Power Indicator
// To get more information please see "Bull And Bear Balance Indicator" 
// by Vadim Gimelfarb. 
//
// WARNING:
// - For purpose educate only
// - This script to change bars colors.
////////////////////////////////////////////////////////////
Reversal123(Length, KSmoothing, DLength, Level) =>
    vFast = sma(stoch(close, high, low, Length), KSmoothing) 
    vSlow = sma(vFast, DLength)
    pos = 0.0
    pos := iff(close[2] < close[1] and close > close[1] and vFast < vSlow and vFast > Level, 1,
             iff(close[2] > close[1] and close < close[1] and vFast > vSlow and vFast < Level, -1, nz(pos[1], 0))) 
    pos

BearPower(SellLevel, BuyLevel) =>
    value =  iff (close < open ,  
              iff (close[1] > open ,  max(close - open, high - low), high - low), 
               iff (close > open, 
                 iff(close[1] > open, max(close[1] - low, high - close), max(open - low, high - close)), 
                  iff(high - close > close - low, 
                   iff (close[1] > open, max(close[1] - open, high - low), high - low), 
                     iff (high - close < close - low, 
                      iff(close > open, max(close - low, high - close),open - low), 
                       iff (close > open, max(close[1] - open, high - close),
                         iff(close[1] < open, max(open - low, high - close), high - low))))))
    pos = 0.0
    pos := iff(value > SellLevel, -1,
           iff(value <= BuyLevel, 1, nz(pos[1], 0))) 

    pos

strategy(title="Combo Backtest 123 Reversal & Bear Power", 
         shorttitle="Combo Reversal & Bear Power",
         overlay=false,
         default_qty_type=strategy.percent_of_equity,
         default_qty_value=50,
         process_orders_on_close=true) 
{
    var int signal = 0
    signal := Reversal123(v_input_1, v_input_2, v_input_3, v_input_4)
    signal := signal + BearPower(v_input_5, v_input_6)

    if (signal == 2)
        strategy.entry("Long", strategy.long)
    else if (signal == -2)
        strategy.exit("Short", "Long")
}
```

This Pine Script defines a trading strategy that combines the 123 Reversal Pattern and Bear Power Indicator. The script includes detailed comments for clarity, as well as the necessary functions to calculate both indicators and the overall signal.