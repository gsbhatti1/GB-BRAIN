```pinescript
/*backtest
start: 2023-09-06 00:00:00
end: 2023-09-13 00:00:00
period: 15m
basePeriod: 5m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy("NNFX ft. ATR, Kijun-Sen, %R","NNFX-2",true,pyramiding=1,calc_on_order_fills=true,calc_on_every_tick=true,initial_capital = 50000, currency="USD",slippage=5,commission_type=strategy.commission.cash_per_contract,commission_value=0.000035)
//INDICATOR---------------------------------------------------------------------
    //Average True Range (1. RISK)
atr_period = input(14, "Average True Range Period")
atr = atr(atr_period)

    //Ichimoku Cloud - Kijun Sen (2. BASELINE)
ks_period = input(20, "Kijun Sen Period")
kijun_sen = (highest(high, ks_period) + lowest(low, ks_period)) / 2
base_long = open < kijun_sen and close > kijun_sen
base_short = open > kijun_sen and close < kijun_sen

    //Williams Percent Range (3. Confirmation#1)
use_wpr = input(true, "Use W%R?")
wpr_len = input(1, "Williams % Range Period")
wpr = -100 * (highest(high, wpr_len) - close) / (highest(high, wpr_len) - lowest(low, wpr_len))
wpr_up = input(-25, "%R Upper Level")
wpr_low = input(-75, "%R Lower Level")
conf1_long = wpr >= wpr_up
conf1_short = wpr <= wpr_low
if(use_wpr == false)
    conf1_long := true
    conf1_short := true
//TRADE LOGIC-------------------------------------------------------------------
    //Long Entry
    //if -> Kijun Sen crosses below and recovers back above AND Williams %R is above -25
l_en = base_long and conf1_long
    //Long Exit
    //if -> Price closes below Kijun Sen
l_ex = close < kijun_sen
    //Short Entry
    //if -> Kijun Sen crosses above and falls below AND Williams %R is below -75
s_en = base_short and conf1_short
    //Short Exit
    //if -> Price closes above Kijun Sen
s_ex = close > kijun_sen
    
//MONEY MANAGEMENT--------------------------------------------------------------
balance = strategy.netprofit + strategy.initial_capital //current balance
floating = strategy.openprofit          //floating profit/loss
isTwoDigit = input(false, "Is this a 2 digit pair? (JPY, XAU, XPD...)")
risk = input(5, "Risk %") / 100           //risk % per trade
equity_protector = input(30, "Equity Protection %") / 100  //equity protection %
stop = atr * 100000 * input(1.5, "Average True Range multiplier")    //Stop level
if(isTwoDigit)
    stop := stop / 100
target = input(150, "Target TP in Points")  //TP level
    //Calculate current DD and determine if stopout is necessary
```