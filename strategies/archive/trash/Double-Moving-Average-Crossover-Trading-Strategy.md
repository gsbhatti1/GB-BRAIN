> Name

Double-Moving-Average-Crossover-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/170922912c9402bfcb6.png)
[trans]
# 

## Overview
This strategy generates buy and sell signals based on the golden cross and death cross of moving averages. Specifically, it uses a 5-day exponential moving average (EMA) and a 34-day double exponential moving average (DEMA). When the short-term 5-day EMA crosses above the long-term 34-day DEMA, a buy signal is generated. When the short-term 5-day EMA crosses below the long-term 34-day DEMA, a sell signal is generated.

## Strategy Logic
1. Calculate the 5-day EMA and 34-day DEMA
2. Generate a buy signal when the short-term 5-day EMA crosses above the long-term 34-day DEMA
3. Generate a sell signal when the short-term 5-day EMA crosses below the long-term 34-day DEMA
4. Option to trade only during specific trading sessions
5. Option to use trailing stop loss

This strategy combines both trend following and moving average crossover factors for stable performance. Moving averages as a trend following indicator can effectively identify market trends; The EMA and DEMA combination can effectively smooth price data to generate trading signals; The crossovers between short-term and long-term moving averages can provide early trading signals when major trend changes.

## Advantage Analysis
1. Simple and clear strategy logic, easy to understand and implement
2. Combination use of moving averages considers both trend judgment and price data smoothing
3. Crossovers between short-term and long-term moving averages can provide early signals at major turning points
4. Parameters can be optimized to adjust moving average lengths for different products and timeframes
5. Integrating two factors can improve strategy stability

## Risk Analysis
1. More false signals may occur in ranging markets
2. Inappropriate moving average lengths may cause signal lagging
3. Improper trading hours and stop loss settings may affect strategy profitability

These risks can be reduced by adjusting moving average lengths, optimizing trading hours, and setting reasonable stop loss.

## Optimization Directions
1. Adjust moving average length parameters for different trading products and timeframes
2. Optimize trading session parameters to trade during most active periods
3. Compare fixed stop loss vs trailing stop loss
4. Test impact of different price source options on strategy

## Conclusion
This strategy generates trading signals through double moving average crossovers, combined with trend following and data smoothing techniques. It is a simple and practical trend following strategy. Through parameter tuning and logic refinement, it can adapt to different products and timeframes, provide early signals at major trend changes, and avoid false signals. Worth recommending and applying.

||

## Overview
This strategy generates buy and sell signals based on the golden cross and death cross of moving averages. Specifically, it uses a 5-day exponential moving average (EMA) and a 34-day double exponential moving average (DEMA). When the short-term 5-day EMA crosses above the long-term 34-day DEMA, a buy signal is generated. When the short-term 5-day EMA crosses below the long-term 34-day DEMA, a sell signal is generated.

## Strategy Logic
1. Calculate the 5-day EMA and 34-day DEMA
2. Generate a buy signal when the short-term 5-day EMA crosses above the long-term 34-day DEMA
3. Generate a sell signal when the short-term 5-day EMA crosses below the long-term 34-day DEMA
4. Option to trade only during specific trading sessions
5. Option to use trailing stop loss

This strategy combines both trend following and moving average crossover factors for stable performance. Moving averages as a trend following indicator can effectively identify market trends; The EMA and DEMA combination can effectively smooth price data to generate trading signals; The crossovers between short-term and long-term moving averages can provide early trading signals when major trend changes.

## Advantage Analysis
1. Simple and clear strategy logic, easy to understand and implement
2. Combination use of moving averages considers both trend judgment and price data smoothing
3. Crossovers between short-term and long-term moving averages can provide early signals at major turning points
4. Parameters can be optimized to adjust moving average lengths for different products and timeframes
5. Integrating two factors can improve strategy stability

## Risk Analysis
1. More false signals may occur in ranging markets
2. Inappropriate moving average lengths may cause signal lagging
3. Improper trading hours and stop loss settings may affect strategy profitability

These risks can be reduced by adjusting moving average lengths, optimizing trading hours, and setting reasonable stop loss.

## Optimization Directions
1. Adjust moving average length parameters for different trading products and timeframes
2. Optimize trading session parameters to trade during most active periods
3. Compare fixed stop loss vs trailing stop loss
4. Test impact of different price source options on strategy

## Conclusion
This strategy generates trading signals through double moving average crossovers, combined with trend following and data smoothing techniques. It is a simple and practical trend following strategy. Through parameter tuning and logic refinement, it can adapt to different products and timeframes, provide early signals at major trend changes, and avoid false signals. Worth recommending and applying.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|Use Trading Session?|
|v_input_2|true|Use Trailing Stop?|
|v_input_3|0400-1500|Trade Session:|
|v_input_4|true|Trade Size:|
|v_input_5|55|Take profit in pips:|
|v_input_6|22|Stop loss in pips:|
|v_input_7|5|EMA length:|
|v_input_8|34|DEMA length:|
|v_input_9_open|0|Price source:: open|high|low|close|hl2|hlc3|hlcc4|ohlc4|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-01 00:00:00
end: 2023-11-30 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
args: [["v_input_1",false]]
*/

//@version=2
strategy(title='[STRATEGY][RS]MicuRobert EMA cross V2', shorttitle='S', overlay=true)
USE_TRADESESSION = input(title='Use Trading Session?', type=bool, defval=true)
USE_TRAILINGSTOP = input(title='Use Trailing Stop?', type=bool, defval=true)
trade_session = input(title='Trade Session:',  defval='0400-1500', confirm=false)
istradingsession = not USE_TRADESESSION ? false : not na(time('1', trade_session))
bgcolor(istradingsession?gray:na)
trade_size = input(title='Trade Size:', type=float, defval=1)
tp = input(title='Take profit in pips:', type=float, defval=55.0) * (syminfo.mintick*10)
sl = input(title='Stop loss in pips:', type=float, defval=22.0) * (syminfo.mintick*10)
ma_length00 = input(title='EMA length:', defval=5)
ma_length01 = input(title='DEMA length:',  defval=34)
price = input(title='Price source:', defval=open)

//  ||--- NO LAG EMA, Credit LazyBear:  ---||
f_LB_zlema(_src, _length)=>
    _ema1=ema(_src, _length)
    _ema2=ema(_ema1, _length)
    _d=_ema1-_ema2
    _zlema=_ema1+_d
//  ||-------------------------------------||

ma00 = f_LB_zlema(price, ma_length00)
ma01 = f_LB_zlema(price, ma_length01)
plot(title='M0', series=ma00, color=black)
plot(title='M1', series=ma01, color=black)

isnewbuy = change(strategy.position_size)>0 and change(strategy.opentrades)>0
isnewsel = change(strategy.position_size)<0 and change(strategy.opentrades)>0

buy_entry_price = isnewbuy ? price : buy_entry_price[1]
sel_entry_price = isnewsel ?