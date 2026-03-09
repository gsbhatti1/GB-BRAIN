```pinescript
/*backtest
start: 2024-01-02 00:00:00
end: 2024-02-01 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
//This is a simple strategy based on Doji star candlestick
//It places two orders: buy stop at doji star high or previous candle high and sell stop at doji star low or previous candle low.
//This strategy works very well with high time frames like Weekly TF because it eliminates the noise in doji formation.
//

strategy("Doji strategy W", overlay=true, calc_on_every_tick=true, pyramiding=0,default_qty_type=strategy.percent_of_equity,default_qty_value=100,currency=currency.USD)

//INPUTS
Use_SL_TP=input(true,'Use stop loss and take profit?')
TP=input(200,'Take Profit in ticks')
SL=input(200,'Stop Loss in tiks')
DojiSize=input(0.05,'Doji size')

//Doji pattern detection
body = close - open
range = high - low
abody = abs(body)
ratio = abody / range
data = (abs(open - close) <= (high - low) * DojiSize)

if data and barstate.islast
    if (high > high[1] and body[1] < (high - low) * DojiSize)
        longDist = math.max(high, high[1])
    else
        longDist = high

    if (low < low[1] and body[1] < (high - low) * DojiSize)
        shortDist = math.min(low, low[1])
    else
        shortDist = low

//Place orders
if not na(longDist)
    strategy.entry("buy", strategy.long, when=barstate.islast, comment="Buy order")
    strategy.order("buy stop", strategy.stop, stop=longDist)

if not na(shortDist)
    strategy.entry("sell", strategy.short, when=barstate.islast, comment="Sell order")
    strategy.order("sell stop", strategy.stop, stop=shortDist)

//Exit rules
exitRule1 = false
if Use_SL_TP and strategy.opentrades > 0
    exitRule1 := strategy.exit("exit buy", "buy stop", loss=SL, profit=TP, when=Use_SL_TP)

if not Use_SL_TP and close < shortDist
    strategy.close("buy stop")

```