> Name

One-Point Balance Strategy Ichimoku-Breakout-Strategy

> Author

ChaoZhang

> Strategy Description

### Overview

The One-Point Balance Strategy uses the concept of moving averages and employs one-point lines and price relationships to determine trend direction. It falls under the category of trend-following strategies. When prices break above the lines, a long position is taken; when they break below, a short position is initiated, following the trend.

### Principle Analysis

The core of this strategy is based on the theory of one-point lines. The `donchian()` function calculates the average of the highest high and lowest low over a certain period to form the equilibrium line. It then determines if prices have broken through this line to generate trading signals.

Specifically, the strategy first computes the Tenkan Line (`TS`) using the `Ten` period as a reference line. When prices break above the line, it indicates an upward trend and triggers a long signal. Conversely, when prices break below the line, it suggests a downward trend and triggers a short signal.

Additionally, the strategy calculates the Kijun Line (`KS`) for the `Kij` period. Together with the `TS` line, it acts as a filter to minimize false signals. A long signal is only triggered when the `TS` crosses above the `KS`.

The code also plots the Ichimoku Cloud to assist in trend direction judgment and includes the Chikou Span to determine its relationship with price as an auxiliary condition.

### Advantage Analysis

- Uses moving averages to identify trends, which are simple and easy to understand
- Incorporates the Ichimoku Cloud for additional reference points, enhancing accuracy 
- Adds the Chikou Span as an auxiliary condition to further filter signals
- Flexibility in adjusting parameters with different combinations of moving averages

### Risk Analysis

- Moving average strategies are sensitive to parameters; different periods can produce varying results
- Pure trend following cannot distinguish between trends and ranges, posing a risk of losses
- Poor handling of consolidation phases, prone to issuing incorrect signals
- Cloud judgment is unstable and may be misleading

Consider combining with momentum indicators such as MACD for trend strength. Adopting multiple moving average systems could improve stability. Incorporating stop-loss strategies can help control risks.

### Optimization Directions

- Integrate momentum indicators to assess trend strength 
- Consider a multi-moving average system, like golden cross
- Add channel and volatility indicators to detect consolidation phases
- Optimize parameters to find the best period combinations
- Include stop-loss strategies to limit per-trade losses

### Conclusion

The One-Point Balance Strategy is relatively simple and straightforward, making it suitable for beginners to understand trends through moving averages. It can also be expanded with multiple indicators to enrich system performance. However, its practical performance needs further validation before live trading applications, especially in risk management. The key is to apply it judiciously based on market conditions, avoiding blind adherence to the lines.

|Argument|Default|Description|
|----|----|----|
|v_input_1|18|Tenkan|
|v_input_2|52|Kijun|
|v_input_3|104|Senkou B|
|v_input_4|52|Senkou A|
|v_input_5|52|Span Offset|
|v_input_6|true|Show Tenkan|
|v_input_7|true|Show Kijun|
|v_input_8|true|Show Span A|
|v_input_9|true|Show Span B|

> Source (PineScript)

```pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-10-12 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4

strategy(title="Ichimoku Crypto Breakout", shorttitle="Ichimoku Breakout", overlay=true)

Ten = input(18, minval=1, title="Tenkan")
Kij = input(52, minval=1, title="Kijun")
LeadSpan = input(104, minval=1, title="Senkou B")
Displace = input(52, minval=1, title="Senkou A")
SpanOffset = input(52, minval=1, title="Span Offset")

sts = input(true, title="Show Tenkan")
sks = input(true, title="Show Kijun")
ssa = input(true, title="Show Span A")
ssb = input(true, title="Show Span B")

source = close

// Ichimoku Indicator Script
donchian(len) => avg(lowest(len), highest(len))
TS = donchian(Ten)
KS = donchian(Kij)
SpanA = avg(TS, KS)
SpanB = donchian(LeadSpan)

CloudTop = max(TS, KS)

Chikou = source[Displace]
SpanAA = avg(TS, KS)[SpanOffset]
SpanBB = donchian(LeadSpan)[SpanOffset]

// Kumo Breakout (Long)
SpanA_Top = SpanAA >= SpanBB ? 1 : 0
SpanB_Top = SpanBB >= SpanAA ? 1 : 0

SpanA_Top2 = SpanA >= SpanB ? 1 : 0
SpanB_Top2 = SpanB >= SpanA ? 1 : 0

SpanA1 = SpanA_Top2 ? SpanA : na
SpanA2 = SpanA_Top2 ? SpanB : na

SpanB1 = SpanB_Top2 ? SpanA : na
SpanB2 = SpanB_Top2 ? SpanB : na

// Plot Tenkan and Kijun (Current Timeframe)
p1= plot(sts and TS ? TS : na, title="Tenkan", linewidth = 2, color = gray)
p2 = plot(sks and KS ? KS : na, title="Kijun", linewidth = 2, color = black)
p5 = plot(close, title="Chikou", linewidth = 2, offset=-Displace, color = orange)

// Plot Kumo Cloud (Dynamic Color)
p3 = plot(ssa and SpanA ? SpanA : na, title="SpanA", linewidth=2, offset=0, color=color.new(color.blue, 0))
```