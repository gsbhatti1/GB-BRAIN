> Name

This-BIST-stocks-4-stage-quantitative-acquisition-strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/18866ba73b6dadc76fa.png)
 [trans]

## Overview

The four-stage BIST stock quantitative acquisition strategy is based on a four-step buy to track wave movements. It enters the market after manipulation and sells when buyer demand increases. This strategy is suitable for stocks with large fluctuations, achieving better cost control through stage-by-stage purchases.

## Strategy Principles

This strategy first calculates the resistance and support lines. The resistance line is determined by the intersection of the close price and the oscillating moving average of the high price, while the support line is determined by the intersection of the close price and the oscillating moving average of the low price.

When the price breaks below the support line, if the price is within the set buying range from the resistance line, it will buy in 25% of the position in the first stage. Then it will buy another 25% of the position around the first buy price, and so on for 4 times, eventually holding 100% of the position.

When the stock price exceeds twice the opening cost, it will close out all positions.

## Advantages of the Strategy

1. Lower buying costs through four-stage purchases
2. Better entry points by tracking stock fluctuations
3. Reasonable take profit point for decent returns

## Risks and Solutions

1. Continued stock decline without stop loss, leading to large losses

    - Set reasonable stop loss to effectively control losses

2. Improper parameter settings make multiple buy points too close to diversify costs

    - Set appropriate price differences between buying stages  

3. Stop loss point too wide to effectively control losses

    - Set suitable stop distance based on actual trading environment and psychological tolerance

## Optimization Directions   

1. Adjust parameters for different types of stocks to better fit their characteristics
2. Add volatility indicators to buy when volatility rises  
3. Optimize take profit by using trailing stop to achieve higher returns  
4. Add stop loss settings to cut losses when price breaks certain levels

## Summary  

The four-stage BIST stock quantitative acquisition strategy is well suited for popular concept stocks overall. By staging the purchases, it can effectively utilize the volatility of the stocks to get better costs when prices pull back. Also, the reasonable take profit and stop loss settings allow it to perform well in risk control. With continual parameter adjustments and optimizations based on actual market environments, this strategy can reliably deliver alpha.

[/trans]


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|30|Buy_Upper_Line|
|v_input_2|90|Buy_Lower_Line|
|v_input_3|true|Barcolor|
|v_input_4|true|Bgcolor|
|v_input_5|40|Sell_Upper_Line|
|v_input_6|300|Sell_Lower_Line|
|v_input_7|true|Barcolor2|
|v_input_8|true|Bgcolor2|
|v_input_9|25|Buy_Range_%|
|v_input_10|45|Sell_Range_%|
|v_input_11|0.12|Buy_Level_%|
|v_input_12|long entry message|message_long_entry|
|v_input_13|long exit message|message_long_exit|
|v_input_14|2|Profit_Sell_Level|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-12 00:00:00
end: 2023-12-18 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Cantalk

//@version=5
strategy("BİST_100 HİSSELERİ 1_SAAT 4 KADEME ALIM",overlay = true, pyramiding=4, initial_capital=10000, process_orders_on_close=true, commission_type=strategy.commission.percent, commission_value=0.002)



LB2 = input(30, title="Buy_Upper_Line")
LB = input(90, title="Buy_Lower_Line")
Barcolor=input(true,title="Barcolor")
Bgcolor=input(true,title="Bgcolor")
//////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////
RDirenc = ta.valuewhen(ta.cross(ta.hma(close, LB2), close), ta.highest(high, LB2), 1)
SDestek = ta.valuewhen(ta.cross(close, ta.hma(close, LB)), ta.lowest(low, LB), 1)



//plot(RDirenc,title="Resistance", color=#f7d707fc, linewidth =2)
//plot(SDestek,title="Support", color=#064df4, linewidth = 2)

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

LB22 = input(40, title="Sell_Upper_Line")
LB1 = input(300, title="Sell_Lower_Line")

Barcolor2=input(true,title="Barcolor2")
Bgcolor2=input(true,title="Bgcolor2")
//////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////////////
RDirenc2 = ta.valuewhen(ta.cross(ta.hma(close, LB22), close), ta.highest(high, LB22), 1)
SDestek2 = ta.valuewhen(ta.cross(close, ta.hma(close, LB1)), ta.lowest(low, LB1), 1)



//plot(RDirenc2,title="Resistance2", color=#f7d707fc, linewidth =2)
//plot(SDestek2,title="Support2", color=#064df4, linewidth = 2)

```