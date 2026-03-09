> Name

Bollinger Waveband Standard Deviation Breakout Strategy Bollinger-Bands-Standard-Deviation-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/18b9dabaeb5e5761cc6.png)

[trans]

### Overview

This strategy is based on the classic Bollinger Bands indicator. It goes long when the price closes above the upper band and goes short when the price closes below the lower band, belonging to a trend-following breakout strategy.

### Strategy Logic   

1. The baseline is 55-day simple moving average.
2. The upper and lower bands are one standard deviation above and below the baseline respectively.
3. A long signal is generated when the price closes above the upper band.
4. A short signal is generated when the price closes below the lower band.
5. Using one standard deviation instead of the classic two standard deviations reduces risk.

### Advantage Analysis   

1. Using standard deviation instead of a fixed value reduces risk.
2. The 55-day moving average can better reflect the medium-term trend.
3. Close breakout filters out false breakouts.
4. Easy to determine trend direction through multi-timeframe analysis.

### Risk Analysis

1. Prone to churning small profits.
2. Need to consider the impact of transaction fees.
3. Breakout signals may be false breakouts.
4. Slippage loss may occur.

Risks can be mitigated by setting stop loss, considering transaction fees, or adding indicator filters.

### Optimization Directions   

1. Optimize baseline parameters to find the best moving average.
2. Optimize the standard deviation size to find the optimal parameters.
3. Add auxiliary volume indicators for judgment.
4. Add a stop loss mechanism.

### Summary   

The overall logic of this strategy is clear. It adjusts risk through the standard deviation band width and avoids false breakouts using close breakout. But it is still necessary to prevent oscillating losses by using stop loss, adding filters etc.

||

### Overview  

This strategy is based on the classic Bollinger Bands indicator. It goes long when the price closes above the upper band and goes short when the price closes below the lower band. It belongs to a trend-following breakout strategy.

### Strategy Logic   

1. The baseline is 55-day simple moving average.
2. The upper and lower bands are one standard deviation above and below the baseline respectively.
3. A long signal is generated when the price closes above the upper band.
4. A short signal is generated when the price closes below the lower band.
5. Using one standard deviation instead of the classic two standard deviations reduces risk.

### Advantage Analysis   

1. Using standard deviation instead of a fixed value reduces risk.
2. The 55-day moving average can better reflect the medium-term trend.
3. Close breakout filters out false breakouts.
4. Easy to determine trend direction through multi-timeframe analysis.

### Risk Analysis

1. Prone to churning small profits.
2. Need to consider the impact of transaction fees.
3. Breakout signals may be false breakouts.
4. Slippage loss may occur.

Risks can be mitigated by setting stop loss, considering transaction fees, or adding indicator filters.

### Optimization Directions   

1. Optimize baseline parameters to find the best moving average.
2. Optimize the standard deviation size to find the optimal parameters.
3. Add auxiliary volume indicators for judgment.
4. Add a stop loss mechanism.

### Summary   

The overall logic of this strategy is clear. It adjusts risk through the standard deviation band width and avoids false breakouts using close breakout. But it is still necessary to prevent oscillating losses by using stop loss, adding filters etc.

||

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_close|0|Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_2|55|SMA length|
|v_input_3|true|Standard Deviation|
|v_input_4|true|Color Bars|
|v_input_5|true|╔═══ Time Range to BackTest ═══╗|
|v_input_6|true|From Month|
|v_input_7|true|From Day|
|v_input_8|2018|From Year|
|v_input_9|true|To Month|
|v_input_10|true|To Day|
|v_input_11|9999|To Year|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-13 00:00:00
end: 2023-11-20 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4

//┌───── •••• ─────┐//
//   TradeChartist  //
//└───── •••• ─────┘//

//Bollinger Bands is a classic indicator that uses a simple moving average of 20 periods along with upper and lower bands that are 2 standard deviations away from the basis line.
//These bands help visualize price volatility and trend based on where the price is in relation to the bands.

//This Bollinger Bands filter plots a long signal when price closes above the upper band and plots a short signal when price closes below the lower band.
//It doesn't take into account any other parameters such as Volume/RSI/fundamentals etc, so user must use discretion based on confirmations from another indicator or based on fundamentals.

//This filter's default is 55 SMA and 1 standard deviation, but can be changed based on asset type

//It is definitely worth reading the 22 rules of Bollinger Bands written by John Bollinger.


strategy(shorttitle="BB Breakout Strategy", title="Bollinger Bands Filter", overlay=true, 
             pyramiding=1, currency=currency.NONE , 
             initial_capital = 10000, default_qty_type = strategy.percent_of_equity, 
             default_qty_value=100, calc_on_every_tick= true, process_orders_on_close=false)

src         = input(close, title = "Source")
length      = input(55, minval=1, title = "SMA length")// 20 for classic Bollinger Bands SMA line (basis)


mult        = input(1., minval=0.236, maxval=2, title="Standard Deviation")//2 for Classic Bollinger Bands //Maxval = 2 as higher the deviation, higher the risk
basis       = sma(src, length)
dev         = mult * stdev(src,length)

CC          = input(true, "Color Bars")


upper       = basis + dev
lower       = basis - dev

//Conditions for Long and Short - Extra filter condition can be used such as RSI or CCI etc.

short       = src<lower// and rsi(close,14)<40
long        = src>upper// and rsi(close,14)>60

L1          = barssince(long)
S1          = barssince(short)

longSignal  = L1<S1 and not (L1<S1)[1]
shortSignal = S1<L1 and not (S1<L1)[1]

//Plots and Fills



////Long/Short shapes with text
// plotshape(S1<L1 and not (S1<L1)[1]?close:na, text = "sᴇʟʟ", textcolor=#ff0100, color=#ff0100, style=shape.triangledown, size=size.small, location=location.abovebar, transp=0, title = "SELL", editable = true)
// plotshape(L1<S1 and not (L1<S1)[1]?close:na, text = "ʙᴜʏ", textcolor = #008000, color=#008000, style=shape.triangleup, size=size.small, location=location.belowbar, transp=0, title = "BUY", editable = true)  


// plotshape(shortSignal?close:na, color=#ff0100, style=shape.triangledown, size=size.small, location=location.abovebar, transp=0, title = "Short Signal", editable = true)
```