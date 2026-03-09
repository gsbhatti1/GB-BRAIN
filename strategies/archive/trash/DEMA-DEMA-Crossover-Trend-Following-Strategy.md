> Name

DEMA Cross Trend Following Strategy DEMA-Crossover-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ad583c41ddf8c8e92d.png)
[trans]
### Overview

This strategy is based on the crossover of double exponential moving average (DEMA) as trading signals and adopts a trend following approach with automated stop loss and take profit setting. The advantages of this strategy are clear trading signals, flexible stop loss/take profit configuration, and effective risk control.

### Strategy Logic  

1. Calculate fast DEMA line (8-day), slow DEMA line (24-day) and auxiliary DEMA line (configurable).

2. When the fast line crosses above the slow line and a golden cross signal is generated, go long. When the fast line crosses below the slow line and a death cross signal is generated, go short.

3. Add a signal filter that only triggers signals when the current value of the auxiliary line is higher than the previous day's value, avoiding false breakouts.  

4. Adopt a trend following stop loss mechanism where the stop loss line keeps adjusting based on price movement to lock in partial profits.

5. At the same time set fixed percentage stop loss and take profit to limit maximum loss and profit per trade.

### Advantages

1. Clear trading signals, easy to determine entry and exit timing.

2. Double DEMA algorithm is smoother, avoids overfitting, more reliable signals.  

3. Auxiliary line filter improves signal accuracy, reducing false signals. 

4. Trend following stop loss locks in partial profits, effectively controlling risks.

5. Fixed percentage stop loss/take profit limits maximum loss per trade, avoiding exceeding risk tolerance.

### Risks  

1. Frequent trading could occur in ranging market, increasing exposure and causing losses.  

2. Overly large fixed stop loss percentage may trigger unwanted big stop loss in extreme price swings.

3. DEMA crossover signals lag and long entries at peak may increase loss risks in fast-moving market.  

4. In live trading slippage affects profitability, parameter tuning needed.

### Enhancement

1. DEMA parameters can be optimized for different market conditions. 

2. Consider widening fixed stop loss in live trading to account for slippage costs.

3. Other indicators like MACD can be added to improve signal quality.

4. Fine tune tracking stop loss stepping value to improve logic.

### Conclusion

This strategy leverages DEMA's trend detection capability and combines it with trend following risk control methodologies. It is a very typical example in the Determine Trend Direction strategy system. In general this is a strategy with clear signals, sensible stop loss/profit taking configuration and controllable risks. When optimized for slippage costs and added with supplemental indicators in live trading, it can achieve good investment returns.

||

### Overview

This strategy is based on the crossover of double exponential moving average (DEMA) as trading signals and adopts a trend following approach with automated stop loss and take profit setting. The advantages of this strategy are clear trading signals, flexible stop loss/take profit configuration, and effective risk control.

### Strategy Logic  

1. Calculate fast DEMA line (8-day), slow DEMA line (24-day) and auxiliary DEMA line (configurable).

2. When the fast line crosses above the slow line and a golden cross signal is generated, go long. When the fast line crosses below the slow line and a death cross signal is generated, go short.

3. Add a signal filter that only triggers signals when the current value of the auxiliary line is higher than the previous day's value, avoiding false breakouts.  

4. Adopt a trend following stop loss mechanism where the stop loss line keeps adjusting based on price movement to lock in partial profits.

5. At the same time set fixed percentage stop loss and take profit to limit maximum loss and profit per trade.

### Advantages

1. Clear trading signals, easy to determine entry and exit timing.

2. Double DEMA algorithm is smoother, avoids overfitting, more reliable signals.  

3. Auxiliary line filter improves signal accuracy, reducing false signals. 

4. Trend following stop loss locks in partial profits, effectively controlling risks.

5. Fixed percentage stop loss/take profit limits maximum loss per trade, avoiding exceeding risk tolerance.

### Risks  

1. Frequent trading could occur in ranging market, increasing exposure and causing losses.  

2. Overly large fixed stop loss percentage may trigger unwanted big stop loss in extreme price swings.

3. DEMA crossover signals lag and long entries at peak may increase loss risks in fast-moving market.  

4. In live trading slippage affects profitability, parameter tuning needed.

### Enhancement

1. DEMA parameters can be optimized for different market conditions. 

2. Consider widening fixed stop loss in live trading to account for slippage costs.

3. Other indicators like MACD can be added to improve signal quality.

4. Fine tune tracking stop loss stepping value to improve logic.

### Conclusion

This strategy leverages DEMA's trend detection capability and combines it with trend following risk control methodologies. It is a very typical example in the Determine Trend Direction strategy system. In general this is a strategy with clear signals, sensible stop loss/profit taking configuration and controllable risks. When optimized for slippage costs and added with supplemental indicators in live trading, it can achieve good investment returns.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|Source Data: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|8|Length DEMA #1|
|v_input_3|24|Length DEMA #2|
|v_input_4|false|Length DEMA #3|
|v_input_5|false|Use Trailing Stop?|
|v_input_6|9|(?Stop Loss & Take Profit Settings)Stop Loss Long %|
|v_input_7|6|Stop Loss Short %|
|v_input_8|25|Take Profit Long % 1|
|v_input_9|6|Take Profit Short % 1|
|v_input_10|true|(?BackTest Period)Start Date|
|v_input_11|true|Start Month|
|v_input_12|2018|Start Year|
|v_input_13|31|End Date|
|v_input_14|12|End Month|
|v_input_15|2031|End Year|


> Source (PineScript)

``` pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © zeguela
//@version=4
strategy(title="ZEGUELA DEMABOT", commission_value=0.063, commission_type=strategy.commission.percent, initial_capital=100, default_qty_value=90, default_qty_type=strategy.percent_of_equity, overlay=true, process_orders_on_close=true)

// Step 1. Script settings

// Input options
srcData = input(title="Source Data", type=input.source, defval=close)

// Length settings
len1 = input(title="Length DEMA #1", type=input.integer, defval=8, minval=1)
len2 = input(title="Length DEMA #2", type=input.integer, defval=24, minval=0)
len3 = input(title="Length DEMA #3", type=input.integer, defval=0, minval=0)

// Step 2. Calculate indicator values
// Function that calculates the DEMA
DEMA(series, length) =>
    if (length > 0)
        emaValue = ema(series, length)
        2 * emaValue - ema(emaValue, length)
    else
        na

// Calculate the DEMA values
demaVal1 = DEMA(srcData, len1)
demaVal2 = DEMA(srcData, len2)
demaVal3 = DEMA(srcData, len3)

// Step 3. Determine indicator signals
// See if there's a DEMA crossover
demaCrossover = if (len2 > 0) and (len3 > 0)
    crossover(demaVal1, demaVal2) and (demaVal3 > demaVal3[1])
else
    if (len2 > 0) and (len3 == 0)
        crossover(demaVal1, demaVal2)
```