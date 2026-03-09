> Name

Long Reversal Strategy Based on Ultimate Oscillator

> Author

ChaoZhang

> Strategy Description


This strategy is named "Long Reversal Strategy Based on Ultimate Oscillator". It uses the Ultimate Oscillator to judge overbought/oversold levels and enters counter-trend long trades when the indicator reaches oversold levels.

The Ultimate Oscillator incorporates price information across multiple periods to gauge market overbought/oversold conditions. When the indicator crosses below a low point, it signals an oversold market and hints at a possible price bounce.

The trading logic is:

1. When the Ultimate Oscillator crosses below a low level (such as 45), the market is oversold and long trades are considered.

2. Continue holding long positions until the indicator crosses above a middle level (such as 70) for taking profit.

3. Set a stop loss line so positions are stopped out if price breaches the line. If the indicator shows bullish divergence, the stop can be adjusted accordingly.

4. If the indicator crosses below the low point again, adding to long positions can be considered.

The advantage of this strategy is capturing oversold bounce opportunities. But optimization of parameters is needed, and the lagging nature of the indicator calls for combining trend analysis. Stop loss and money management are also critical.

In conclusion, using indicators to determine reversal timing is common. But traders still need discretion and should not purely rely on any single indicator.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|5|length1|
|v_input_2|10|length2|
|v_input_3|15|length3|
|v_input_4|9|Signal length|
|v_input_5|45|Buy Line (UO crossing up oversold at ) |
|v_input_6|70|Exit Line (UO crsossing down overbought at) |
|v_input_7|10|Risk % of capital|
|v_input_8|3|Stop Loss|
|v_input_9|false|Take Profit|
|v_input_10|75|Take Profit at RSIofUO crossing below this value |
|v_input_11|true|show Signal Line|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-09-11 00:00:00
end: 2023-09-12 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © mohanee

//@version=4

strategy(title="Ultimate Oscillator [Long] Strategy",  shorttitle="UO" , overlay=false, pyramiding=2, default_qty_type=strategy.percent_of_equity, default_qty_value=20, initial_capital=10000, currency=currency.USD)  //default_qty_value=10, default_qty_type=strategy.fixed,

	
//Ultimate Oscillator logic copied from  TradingView  built-in indicator
/////////////////////////////////////////////////////////////////////////////////
length1 = input(5, minval=1), length2 = input(10, minval=1), length3 = input(15, minval=1)

//rsiUOLength = input(7, title="RSI UO length", minval=1)

signalLength = input(9, title="Signal length", minval=1)

buyLine = input (45, title="Buy Line (UO crossing up oversold at ) ")       //crossover
exitLine = input (70, title="Exit Line (UO crsossing down overbought at) ")      //crossunder


riskCapital = input(title="Risk % of capital", defval=10, minval=1)
stopLoss=input(3,title="Stop Loss",minval=1)

takeProfit=input(false, title="Take Profit")
profitExitLine = input (75, title="Take Profit at RSIofUO crossing below this value ") //crossunder


showSignalLine=input(true, "show Signal Line")
//showUO=input(false, "show Ultimate Oscialltor")


average(bp, tr_, length) => sum(bp, length) / sum(tr_, length)
high_ = max(high, close[1])
low_ = min(low, close[1])
bp = close - low_
tr_ = high_ - low_
avg7 = average(bp, tr_, length1)
avg14 = average(bp, tr_, length2)
avg28 = average(bp, tr_, length3)
ultOscVal = 100 * (4*avg7 + 2*avg14 + avg28)/7
//Ultimate Oscillator 
/////////////////////////////////////////////////////////////////////////////////

//Willimas Alligator  copied from  TradingView  built-in Indicator
/////////////////////////////////////////////////////////////////////////////////
smma(src, length) =>
	smma =  0.0
	smma := na(smma[1]) ? sma(src, length) : (smma[1] * (length - 1) + src) / length
	smma

//moving averages logic copied from Willimas Alligator -- built-in indicator in TradingView
sma1=smma(hl2,5)
sma2=smma(hl2,20)
sma3=smma(hl2,50)

//Willimas Alligator
/////////////////////////////////////////////////////////////////////////////////

myVwap= vwap(hlc3)

//drawings
/////////////////////////////////////////////////////////////////////////////////
hline(profitExitLine, title="Middle Line 60  [Profit Exit Here]", color=color.purple  , linestyle=hline.style_dashed)

obLevelPlot = hline(exitLine, title="Overbought",  color=color.red , linestyle=hline.style_dashed)
osLevelPlot = hline(buyLine, title="Oversold", color=color.blue, linestyle=hline.style_dashed)

//fill(obLevelPlot, osLevelPlot, title="Background", color=color.blue, transp=90)
//rsiUO = rsi(ultOscVal,rsiUOLength)

rsiUO=ultOscVal

//emaUO = ema(rsiUO, 9)

//signal line
emaUO = ema(ultOscVal , 5)     // ema(ultOscVal / rsiUO, 9)

//ultPlot=plot(showUO==true? ultOscVal : na, color=color.green, title="Oscillator")

plot(rsiUO, title = "rsiUO" ,  color=color.purple)
plot(showSignalLine ? emaUO : na , title = "emaUO [signal line]" ,  color=color.blue)  //emaUO

//drawings
/////////////////////////////////////////////////////////////////////////////////




//Strategy Logic 
///////////////////////////////////////////
```