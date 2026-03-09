> Strategy Arguments



|Argument|Default|Description|
|---|---|---|
|v_input_1|12|Fast Length|
|v_input_2|21|Slow Length|
|v_input_3|9|Signal Length|
|v_input_4|14|RSI of MACD Length|
|v_input_5|10|Risk % of capital|
|v_input_6|3|Stop Loss|
|v_input_7|false|Take Profit|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-07 00:00:00
end: 2024-01-14 00:00:00
period: 3m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © mohanee

//@version=4

strategy(title="RSI of MACD Strategy[Long only]", shorttitle="RSIofMACD", overlay=false, pyramiding=1, default_qty_type=strategy.percent_of_equity, default_qty_value=20, initial_capital=10000, currency=currency.USD)  //default_qty_value=10, default_qty_type=strategy.fixed,

	



/////////////////////////////////////////////////////////////////////////////////



// MACD Inputs ///
fastLen = input(12, title="Fast Length")
slowLen = input(21, title="Slow Length")
sigLen  = input(9, title="Signal Length")

rsiLength  = input(14, title="RSI of MACD Length")




riskCapital = input(title="Risk % of capital", defval=10, minval=1)
stopLoss=input(3,title="Stop Loss",minval=1)

takeProfit=input(false, title="Take Profit")


[macdLine, signalLine, _] = macd(close, fastLen, slowLen, sigLen)

rsiOfMACD = rsi(macdLine, rsiLength)
emaSlow = ema(close, slowLen)



//drawings
/////////////////////////////////////////////////////////////////////////////////


obLevelPlot = hline(80, title="Overbought / Profit taking line",  color=color.blue , linestyle=hline.style_dashed)
osLevelPlot = hline(30, title="Oversold / entry line", color=color.green, linestyle=hline.style_dashed)

exitLinePlot = hline(15, title="Exit line", color=color.red, linestyle=hline.style_dashed)




plot(rsiOfMACD, title = "rsiOfMACD" ,  color=color.purple)


//drawings
/////////////////////////////////////////////////////////////////////////////////




//Strategy Logic 
/////////////////////////////////////////////////////////////////////////////////

//Entry--
//Calculate the number of units that can be purchased based on risk management and stop loss
qty1 = (strategy.equity * riskCapital / 100) / (close * stopLoss / 100)

//Check if sufficient cash is available to buy qty1, use available capital only if not enough
if (qty1 > strategy.opaque)
    qty1 := strategy.opaque

longCondition = rsiOfMACD >= 30 and macdLine < signalLine
if (longCondition)
    strategy.entry("Long", strategy.long, size=qty1)

//Exit--
shortCondition = rsiOfMACD <= 15 and macdLine > signalLine
if (shortCondition)
    strategy.close("Long")

//Take Profit
if (takeProfit and rsiOfMACD >= 80)
    strategy.exit("Take Profit", "Long")



plotshape(series=longCondition, location=location.belowbar, color=color.green, style=shape.labeldown, title="Buy Signal")
plotshape(series=shortCondition, location=location.abovebar, color=color.red, style=shape.labelup, title="Sell Signal")

```

This Pine Script defines the RSI of MACD strategy with detailed inputs and logic to manage entries, exits, stop losses, and take profits.