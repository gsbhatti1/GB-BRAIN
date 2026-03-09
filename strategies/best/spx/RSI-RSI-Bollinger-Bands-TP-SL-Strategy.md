``` pinescript
/*backtest
start: 2023-11-20 00:00:00
end: 2023-12-20 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © BigCoinHunter

//@version=5
strategy(title="RSI Bollinger Bands TP/SL Strategy", overlay=true, 
     pyramiding=0, default_qty_type=strategy.percent_of_equity, 
     default_qty_value=100, initial_capital=1000, 
     currency=currency.USD, commission_value=0.05, 
     commission_type=strategy.commission.percent, 
     process_orders_on_close=true)

//----------- get the user inputs --------------

//---------- RSI -------------
price = input(close, title="Source")

RSIlength = input.int(defval=6, title="RSI Length")
RSISellLevel = input.int(defval=50, title="RSI OverSold Level")
RSPurchaseLevel = input.int(defval=50, title="RSI OverBought Level")
BBandsLength = input.int(defval=200, title="Bollinger Bands Period Length")
BBandsStdDev = input.float(defval=2.0, title="Bollinger Bands Standard Deviation")
takeProfit = input.float(title="Take Profit", defval=1.3)
stopLoss = input.float(title="Stop Loss", defval=0.8)
longEntry = input.bool(defval=true, title="Long Entry")
shortEntry = input.bool(defval=true, title="Short Entry")

//--------- RSI Calculation ------------
rsiValue = rsi(price, RSIlength)

//--------- Bollinger Bands Calculation ------------
src = close
basis = sma(src, BBandsLength)
dev = BBandsStdDev * ta.stdev(src, BBandsLength)
upperBB = basis + dev
lowerBB = basis - dev

longCondition = rsiValue < RSISellLevel and close > lowerBB and longEntry
shortCondition = rsiValue > RSPurchaseLevel and close < upperBB and shortEntry

//---------- Place Orders -------------
if (longCondition)
    strategy.entry("Long", strategy.long, when=longCondition)

if (shortCondition) 
    strategy.entry("Short", strategy.short, when=shortCondition)

//--------- Set Take Profit and Stop Loss ------------
if (strategy.opentrades > 0)
    myStop = strategy.position_avg_price * (1 - stopLoss)
    takeProfitPrice = strategy.position_avg_price * (1 + takeProfit)
    
    strategy.exit("Long Exit", "Long", limit=takeProfitPrice, stop=myStop) 
    strategy.exit("Short Exit", "Short", limit=myStop, stop=takeProfitPrice)

//--------- Display Bollinger Bands ------------
plot(basis, color=color.blue, title="Bollinger Bands Basis")
plot(upperBB, color=color.red, title="Upper Bollinger Band")
plot(lowerBB, color=color.green, title="Lower Bollinger Band")
```

This code integrates the RSI and Bollinger Bands indicators as described in your strategy document. It sets up conditions for entering trades based on these two indicators and includes take profit and stop loss settings to manage risk.