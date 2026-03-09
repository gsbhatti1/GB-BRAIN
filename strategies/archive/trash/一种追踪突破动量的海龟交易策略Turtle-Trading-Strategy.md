``` pinescript
/*backtest
start: 2022-12-24 00:00:00
end: 2023-12-24 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
// originally coded by tmr0, modified by timchep
// original idea from «Way of the Turtle: The Secret Methods that Turned Ordinary People into Legendary Traders» (2007) CURTIS FAITH
strategy("Turtles", shorttitle = "Turtles", overlay=true, pyramiding=1, default_qty_type= strategy.percent_of_equity, default_qty_value = 100)
//////////////////////////////////////////////////////////////////////
// Com
```

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|2011|Backtest Start Year|
|v_input_2|12|Backtest Start Month|
|v_input_3|true|Backtest Start Day|
|v_input_4|2030|Backtest Stop Year|
|v_input_5|12|Backtest Stop Month|
|v_input_6|30|Backtest Stop Day|
|v_input_7|false|Color Background?|
|v_input_8|true|Enable Shorting?|
|v_input_9|20|enter_fast|
|v_input_10|10|exit_fast|
|v_input_11|55|enter_slow|
|v_input_12|20|exit_slow|


> Source (PineScript)

``` pinescript
//@version=2
strategy("Turtles", shorttitle = "Turtles", overlay=true, pyramiding=1, default_qty_type= strategy.percent_of_equity, default_qty_value = 100)

// Calculate high and low prices
slowL = ta.highest(high, v_input_11)
fastL = ta.highest(high, v_input_9)
slowS = ta.lowest(low, v_input_11)
fastS = ta.lowest(low, v_input_10)

// Enter long when price exceeds 55-day high
enterL2 = ta.crossover(close, slowL)
if (enterL2)
    strategy.entry("Enter Long", strategy.long)

// Exit long when price falls below 20-day high
exitL1 = ta.crossunder(close, fastL)
if (exitL1)
    strategy.exit("Exit Long", "Enter Long", stop=fastL)

// Enter short when price falls below 55-day low
enterS2 = ta.crossunder(close, slowS)
if (enterS2)
    strategy.entry("Enter Short", strategy.short)

// Exit short when price exceeds 20-day low
exitS1 = ta.crossover(close, fastS)
if (exitS1)
    strategy.exit("Exit Short", "Enter Short", stop=fastS)
```