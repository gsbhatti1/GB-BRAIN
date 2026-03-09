> Name

Triple-Moving-Average-Quantitative-Trading-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/107bc45e949b3e2cf23.png)
 [trans]

This strategy generates trading signals by calculating three moving averages of different periods and combining price breakthroughs. It belongs to a typical trend-following strategy. The strategy aims to follow medium-term trends in the market and can be adapted to different products and trading environments by dynamically adjusting parameters.

#### Principle

The strategy contains three moving averages: MA1, MA2, and MA3. MA1 and MA2 form a trading channel, and their crossover generates trading signals; MA3 is used to filter signals.

When the fast moving average MA1 crosses above the medium-term moving average MA2, it indicates the strengthening of the short-term trend. At this time, if the price is above the long-term moving average MA3, a long signal is generated; conversely, if MA1 crosses below MA2 and the price is below MA3, a short signal is generated.

The role of MA3 is to filter out short-term market noise and only generate signals after determining that the trend has entered the medium and long term stage. By dynamically adjusting the parameters of the three moving averages, the strategy can find the optimal parameter combination in different markets.

#### Advantages

- Capture trends of different cycles through multiple moving averages
- MA3 filters signals to avoid whipsaws
- Customizable moving average types and parameters, high adaptability
- Visualize crosses to identify signal points

#### Risks

- Moving averages may lag when major trend reverses 
- Potentially high trading frequency, increasing trading costs and slippage risks
- Improper parameters may cause overtrading or lagging signals

Can optimize MA periods for different products; optimize stop loss to control single loss; combine other technical indicators to confirm signal validity and reduce false signals.

#### Optimization Directions

- Add other indicators to determine trends, e.g. MACD, Bollinger Bands, etc.
- Add stop loss/take profit strategies
- Dynamically adjust parameters to find optimal combinations
- Parameter optimization for different products  
- Consider trading costs, optimize trade frequency

#### Summary

This strategy generates trading signals by calculating three moving averages and observing their crosses. Using the idea of combining fast, medium, and slow lines to determine trends, it is a typical trend-following strategy. The strategy can be adapted to different products through parameter optimization, but risks whipsaws and missing turnings. Future improvements could introduce other technical indicators to judge signal validity, develop dynamic parameter optimization mechanisms, etc., to make the strategy more flexible.

[/trans]

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1|13|MA1 Period|
|v_input_2|0|MA1 Type: SMA|RMA|EMA|WMA|HMA|DEMA|TEMA|
|v_input_3_close|0|MA1 Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_4|true|MA1 Visible|
|v_input_5|50|MA2 Period|
|v_input_6|0|MA2 Type: SMA|RMA|EMA|WMA|HMA|DEMA|TEMA|
|v_input_7_close|0|MA2 Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_8|true|MA2 Visible|
|v_input_9|200|MA3 Period|
|v_input_10|0|MA3 Type: SMA|RMA|EMA|WMA|HMA|DEMA|TEMA|
|v_input_11_close|0|MA3 Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_12|true|MA3 Visible|
|v_input_13|true|Show Crosses|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-01-16 00:00:00
end: 2024-01-22 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Meesemoo

//@version=4
strategy("Custom MA Strategy Tester", overlay = true)
MA1Period = input(13, title="MA1 Period")
MA1Type = input(title="MA1 Type", defval="SMA", options=["RMA", "SMA", "EMA", "WMA", "HMA", "DEMA", "TEMA"])
MA1Source = input(title="MA1 Source", type=input.source, defval=close)
MA1Visible = input(title="MA1 Visible", type=input.bool, defval=true)
MA2Period = input(50, title="MA2 Period")
MA2Type = input(title="MA2 Type", defval="SMA", options=["RMA", "SMA", "EMA", "WMA", "HMA", "DEMA", "TEMA"])
MA2Source = input(title="MA2 Source", type=input.source, defval=close)
MA2Visible = input(title="MA2 Visible", type=input.bool, defval=true) 
MA3Period = input(200, title="MA3 Period")
MA3Type = input(title="MA3 Type", defval="SMA", options=["RMA", "SMA", "EMA", "WMA", "HMA", "DEMA", "TEMA"])
MA3Source = input(title="MA3 Source", type=input.source, defval=close)
MA3Visible = input(title="MA3 Visible", type=input.bool, defval=true)
ShowCrosses = input(title="Show Crosses", type=input.bool, defval=true)

MA1 = if MA1Type == "SMA"
    sma(MA1Source, MA1Period)
else
    if MA1Type == "EMA"
        ema(MA1Source, MA1Period)
    else
        if MA1Type == "WMA"
            wma(MA1Source, MA1Period)
        else
            if MA1Type == "RMA"
                rma(MA1Source, MA1Period)
            else
                // Add other types as needed
```