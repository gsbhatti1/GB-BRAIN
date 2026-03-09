> Name

Momentum-Tracking-CCI-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/de605b9043c989a656.png)

[trans]

### Overview

This strategy is based on the Commodity Channel Index (CCI) indicator, aiming to go long in oversold conditions and go short in overbought conditions. It also optionally uses an Exponential Moving Average (EMA) filter to only trade in the direction of the trend. The strategy also provides fixed percentage or Average True Range (ATR) based stop loss and take profit.

### Strategy Logic

1. Use CCI indicator to determine market trend

    - CCI measures momentum by comparing current price to the average price over a period
    
    - CCI above 150 is overbought, below -100 is oversold
    
2. Optionally use EMA filter

    - Only go long when price is above EMA, and short when below EMA 
    
    - Use EMA to determine trend direction, avoid counter-trend trading

3. Provide two types of stop loss and take profit

    - Fixed percentage based stop loss and take profit: Use fixed percentage of entry price
    
    - ATR based stop loss and take profit: Use ATR multiplier for stop loss, calculate take profit based on risk reward ratio
    
4. Entry conditions

    - Go long when CCI crosses above -100
    
    - Go short when CCI crosses below 150 
    
    - If EMA enabled, only enter when price is on the right side of EMA
    
5. Exit conditions

    - Close position when stop loss or take profit is hit
    
    - Close position when CCI re-enters overbought/oversold region
    
6. Plotting

    - Plot CCI indicator, color code regions

### Advantage Analysis

1. Use CCI overbought/oversold for entry, a classic usage of CCI

2. Optional EMA ensures trading with the trend, avoid reversals

3. Provide two types of stop loss/take profit for flexibility

4. Close on CCI signal again locks in reversal profit

5. Plotting highlights CCI signals clearly

6. Simple and clear logic, easy to understand and optimize

### Risk Analysis

1. CCI has a lagging effect, may miss reversals or give false signals

2. Wrong EMA parameters may miss trends or render strategy ineffective

3. Fixed percentage stop loss/take profit less adaptive to market changes

4. ATR stop loss/take profit sensitive to ATR period, should optimize

5. Larger drawdown risk, position sizing should be adjusted

6. Performance varies across market conditions, re-evaluate parameters

### Optimization Directions

1. Evaluate CCI periods to find optimal parameter combinations

2. Test different EMA periods for best trend estimation

3. Adjust stop loss/take profit for optimal risk reward ratio

4. Add other filters like volume to further avoid false signals

5. Combine with trendlines/chart patterns for pattern confirmation

6. Add position sizing rules like fixed size to control drawdown

7. Backtest across different market conditions, dynamically adjust

### Summary

The strategy utilizes the classic CCI overbought/oversold principles for entry. The EMA filter controls trend trading. Two types of stop loss/take profit provided for flexibility. Plotting highlights signals clearly. Simple and clear logic, easy to understand and optimize. Further improvements can be made via parameter tuning, adding filters, risk control etc.

[/trans]

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|14|CCI Length|
|v_input_int_1|150|Overbought|
|v_input_int_2|-140|Oversold|
|v_input_2|true|Use EMA|
|v_input_3|55|EMA Length|
|v_input_4|true|(?TP/SL Method)Percentage TP/SL|
|v_input_5|false|ATR TP/SL|
|v_input_float_1|10|Take Profit (%)|
|v_input_float_2|10|Stop Loss (%)|
|v_input_6|20|ATR Length|
|v_input_7|4|ATR SL Multiplier|
|v_input_8|2|Risk Reward Ratio|


> Source (PineScript)

```pinescript
//@version=5
strategy("CCI+EMA Strategy with Percentage or ATR TP/SL [Alifer]", shorttitle = "CCI_EMA_%/ATR_TP/SL", overlay=false,
      initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=10, commission_type=strategy.commission.percent, commission_value=0.045)

length = input(14, "CCI Length")
overbought = input.int(150, step = 10, title = "Overbought")
oversold = input.int(-140, step = 10, title = "Oversold")
src = hlc3
ma = ta.sma(src, length)
cci = (src - ma) / (0.015 * ta.dev(src, length))
ema = na
if v_input_2
    ema := ta.ema(src, input.int(55, "EMA Length"))
```