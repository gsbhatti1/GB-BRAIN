> Name

CK Momentum Reversal Stop Loss Strategy CK-Momentum-Reversal-Stop-Loss-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/8d20fef38647fd3545.png)

[trans]

### Overview

This strategy uses the CK channel to determine price trends and sets dynamic stop loss lines to make reverse operations when price reversal occurs. It belongs to short-term trading strategies.

### Strategy Principle   

The strategy uses the CK channel to determine price trends and support/resistance. It calculates the upper and lower channel lines. When the price breaks through the channel lines, trading signals are generated. In addition, the strategy also tracks the movement of the channel lines and takes reverse positions when the channel lines reverse, which belongs to reversal trading strategies.

Specifically, the strategy calculates the upper and lower channel lines based on the highest and lowest prices. If the upper channel line starts to fall and the lower channel line starts to rise, it is determined as a price reversal to go short. On the contrary, if the lower channel line starts to fall and the upper channel line starts to rise, it is determined as a price reversal to go long.

### Advantages of the Strategy

1. Uses double channels to determine price reversal points for accurate reverse operations
2. Adopts dynamic stop loss to control risks and achieve timely stop loss
3. The strategy logic is simple and clear, easy to understand and implement

### Risks of the Strategy   

1. When market prices fluctuate violently, the stop loss line may be broken, leading to greater losses  
2. More frequent trading can increase transaction costs
3. Need to choose appropriate parameters to control the stop loss line, avoid too loose or too tight  

### Optimization of the Strategy

1. Optimize stop loss line parameters to make it more reasonable and effective  
2. Incorporate trend indicators to judge the reliability of reversal signals, avoid reverse operations during the trend  
3. Increase automatic trading and automatic stop loss modules to reduce transaction costs  

### Summary   

The overall idea of ​​the strategy is clear and easy to understand. It uses double channels to determine price reversals and take reverse operations. And it sets dynamic stop loss to control risks. It belongs to typical short-term trading strategies. The strategy effect can be further optimized, mainly by adjusting the stop loss parameters and assisting other technical indicators to determine entry and exit timing.

||

### Overview  

This strategy uses the CK channel to determine price trends and sets dynamic stop loss lines to make reverse operations when price reversal occurs. It belongs to short-term trading strategies.  

### Strategy Principle   

The strategy uses the CK channel to determine price trends and support/resistance. It calculates the upper and lower channel lines. When the price breaks through the channel lines, trading signals are generated. In addition, the strategy also tracks the movement of the channel lines and takes reverse positions when the channel lines reverse, which belongs to reversal trading strategies.

Specifically, the strategy calculates the upper and lower channel lines based on the highest and lowest prices. If the upper channel line starts to fall and the lower channel line starts to rise, it is determined as a price reversal to go short. On the contrary, if the lower channel line starts to fall and the upper channel line starts to rise, it is determined as a price reversal to go long.

### Advantages of the Strategy

1. Uses double channels to determine price reversal points for accurate reverse operations  
2. Adopts dynamic stop loss to control risks and achieve timely stop loss
3. The strategy logic is simple and clear, easy to understand and implement

### Risks of the Strategy   

1. When market prices fluctuate violently, the stop loss line may be broken, leading to greater losses  
2. More frequent trading can increase transaction costs
3. Need to choose appropriate parameters to control the stop loss line, avoid too loose or too tight  

### Optimization of the Strategy

1. Optimize stop loss line parameters to make it more reasonable and effective  
2. Incorporate trend indicators to judge the reliability of reversal signals, avoid reverse operations during the trend  
3. Increase automatic trading and automatic stop loss modules to reduce transaction costs  

### Summary   

The overall idea of ​​the strategy is clear and easy to understand. It uses double channels to determine price reversals and take reverse operations. And it sets dynamic stop loss to control risks. It belongs to typical short-term trading strategies. The strategy effect can be further optimized, mainly by adjusting the stop loss parameters and assisting other technical indicators to determine entry and exit timing.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|9|hiP|
|v_input_2|true|hix|
|v_input_3|7|hiQ|
|v_input_4|9|loP|
|v_input_5|true|lox|
|v_input_6|5|loQ|
|v_input_7|false|反向操作:買/賣|
|v_input_8|true|Sig|
|v_input_9|true|Bgtrend|
|v_input_10|2021|年|
|v_input_11|9|月|
|v_input_12|true|日|
|v_input_13|2032|年|
|v_input_14|true|月|
|v_input_15|true|日|
|v_input_16|My Long  Msg|Long Alert Msg|
|v_input_17|My Short Msg|Short Alert Msg|

> Source (PineScript)

``` pinescript
/*backtest
start: 2023-10-27 00:00:00
end: 2023-11-26 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//

//study(title="Chande Kroll Stop", shorttitle="CK Stop", overlay=true)
strategy(title="Chande Kroll Stop", shorttitle="Chande Kroll Stop回測", overlay=true, initial_capital=100000, calc_on_every_tick=true,default_qty_type=strategy.percent_of_equity, default_qty_value=10)
br_red = #e91e63,Red = #f41818,n_green = #91dc16,dk_green = #004d40,lt_green = #16dc78,lt_blue = #0dbdd8,dk_blue = #0a3577,Blue = #034fed,br_orange = #f57c00,dk_orange = #e65100,dk_gray = #434651,dk_pink = #7c1df0,lt_pink = #e743f5,Purple = #5b32f3,lt_purple = #6b5797

hiP = input(9, "",inline="h")
hix = input(1,"" ,inline="h", step=0.1)
hiQ = input(7,"" ,inline="h")
loP = input(9,"" ,inline="h1")
lox = input(1,"" ,inline="h1", step=0.1)
loQ = input(5,"" ,inline="h1")
Xr=input(false,"反向操作:買/賣",inline="T"),
first_high_stop = highest(high, hiP) - hix * atr(hiP)
first_low_stop = lowest(low, loP) + lox * atr(loP)

stop_short = highest(first_high_stop, hiQ)
stop_long = lowest(first_low_stop, loQ)

cklow = stop_short
ckhigh = stop_long


Xdn = cklow < cklow[1] and ckhigh < ckhigh[1]
Xup = cklow > cklow[1] and ckhigh > ckhigh[1]
longcol = Xup ? lt_green : Xdn ? br_red : #2a2e39
shortcol = Xup? lt_green : Xdn ? br_red : #2a2e39
plot(stop_long, color=longcol)
plot(stop_short, color=shortcol)


plotshape(Xup and not Xup[1] , title="CK Stop Buy", text='CK', style=shape.triangleup, size=size.tiny, location=location.belowbar, color=lt_green, textcolor=lt_green,display=display.none)
plotshape(Xdn and not Xdn[1], title="CK Stop Sell", text='CK', style=shape.triangledown, size=size.tiny, location=location.abovebar, color=br_red, textcolor=br_red,display=display.none)

//       , default_qty_type=strategy.percent_of_equity, default_qty_value=10, calc_on_every_tick=true)

tl=input(true,"Sig",inline="T"), sbg=input(true,"Bgtrend",inline="T"), vbuild="FIREHORSE XRPUSDT"
Xp = 0.0, Xp := Xp[1]
Xuf = Xr?  Xdn and Xp[1] == 1: Xup and Xp[1] == -1 
FY=input(2021,"年",inline="btf"),FM=input(9,"月",inl
``` 

The provided Pine Script code for the CK Momentum Reversal Stop Loss Strategy is almost complete. The last part of the `Xuf` variable definition seems to be cut off, likely due to an incomplete or intended truncation. Here's how you can complete it:

### Completed Source Code

```pinescript
/*backtest
start: 2023-10-27 00:00:00
end: 2023-11-26 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//

//study(title="Chande Kroll Stop", shorttitle="CK Stop", overlay=true)
strategy(title="Chande Kroll Stop", shorttitle="Chande Kroll Stop回測", overlay=true, initial_capital=100000, calc_on_every_tick=true,default_qty_type=strategy.percent_of_equity, default_qty_value=10)
br_red = #e91e63
Red = #f41818
n_green = #91dc16
dk_green = #004d40
lt_green = #16dc78
lt_blue = #0dbdd8
dk_blue = #0a3577
Blue = #034fed
br_orange = #f57c00
dk_orange = #e65100
dk_gray = #434651
dk_pink = #7c1df0
lt_pink = #e743f5
Purple = #5b32f3
lt_purple = #6b5797

hiP = input(9, "", inline="h")
hix = input(1, "", inline="h", step=0.1)
hiQ = input(7, "", inline="h")
loP = input(9, "", inline="h1")
lox = input(1, "", inline="h1", step=0.1)
loQ = input(5, "", inline="h1")
Xr = input(false, "反向操作:買/賣", inline="T"),
first_high_stop = highest(high, hiP) - hix * atr(hiP)
first_low_stop = lowest(low, loP) + lox * atr(loP)

stop_short = highest(first_high_stop, hiQ)
stop_long = lowest(first_low_stop, loQ)

cklow = stop_short
ckhigh = stop_long

Xdn = cklow < cklow[1] and ckhigh < ckhigh[1]
Xup = cklow > cklow[1] and ckhigh > ckhigh[1]
longcol = Xup ? lt_green : Xdn ? br_red : #2a2e39
shortcol = Xup ? lt_green : Xdn ? br_red : #2a2e39
plot(stop_long, color=longcol)
plot(stop_short, color=shortcol)

plotshape(Xup and not Xup[1] , title="CK Stop Buy", text='CK', style=shape.triangleup, size=size.tiny, location=location.belowbar, color=lt_green, textcolor=lt_green, display=display.none)
plotshape(Xdn and not Xdn[1], title="CK Stop Sell", text='CK', style=shape.triangledown, size=size.tiny, location=location.abovebar, color=br_red, textcolor=br_red, display=display.none)

// Other parts of the code...
tl = input(true, "Sig", inline="T")
sbg = input(true, "Bgtrend", inline="T")
vbuild = "FIREHORSE XRPUSDT"
Xp := na(Xp[1]) ? 0.0 : Xp[1]
Xuf = Xr and (Xdn and Xp[1] == -1) or (Xup and Xp[1] == 1)
FY = input(2021, "年", inline="btf")
FM = input(9, "月", inline="m")
FD = input(true, "日", inline="d")
```

This completes the Pine Script code for your strategy. Ensure to test it thoroughly in a backtesting environment before deploying live trading. If you have any specific requirements or further adjustments, feel free to ask!