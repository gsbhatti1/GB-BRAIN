> Name

72s-Adaptive-Hull-Moving-Average

> Author

ChaoZhang

> Strategy Description

One challenging issue for beginner traders is to differentiate market conditions, whether or not the current market is giving the best opportunity to stack profits as early and in the shortest time possible.

On intraday trading, we've observed that significant movements by large banks can sometimes be defined—more precisely circling around—the HMA 200. I’ve been thinking about making the visuals more aligned with price dynamics (separating major movement from minor noise) to get clearer signals of when such moments start happening. This way, it will be easier to see at a glance when strength really sets in, with less cluttered charts.

This Adaptive HMA uses the new Pine Script feature that now supports Dynamic Length arguments for several Pine functions. (Read: https://www.tradingview.com/blog/en/pine...). It doesn't directly support the built-in HMA(), but thankfully we can use its wma() formula to construct it. (Note: I tweaked the popular HMA formula here by using plain int() instead of round() on its wma's length, since I find it precisely matches TradingView’s built-in HMA).

You can choose which aspect the Adaptive HMA period will adapt to.

In this study, I present two options: Volume and Volatility. It will "move" faster or slower depending on which situation the aspect is currently in. For example, when volume is generally low or volatility readings are not there, prices won't move much, so the adapting MA will slow down by dynamically lengthening the lookback period, and vice versa.

The color markings of the Adaptive HMA resemble the situations described above. Additionally, I also combine it with slope calculation of the MA to help measure trend strength or sideways/choppy conditions.

This way, when we use it as dynamic support/resistance, it will be more visually reliable.

Secondly, and more importantly, it might help traders with better probability information on whether or not a trade is even worth making. For example, if at the same time the market isn't giving much movement, any profit would also only be minimal. In most cases, we might be better off saving our capital for later or placing it elsewhere.

**How to Use:**

Aside from better dynamic support/resistance and clearer breakout confirmation, the MA is colored as follows:
- **YELLOW:**  
  Market is in consolidation or flat. Be it sideways, choppy, or in relatively small movements. If it shows up in a trending market, it may be an earlier sign that the current trend might change direction or confirm a price breakout to another side.
- **LIGHT GREEN or LIGHT RED:**  
  Tells if a trend is forming but still relatively weak (or getting weaker), as it doesn't have volume or volatility to support.
- **DARKER GREEN or DARKER RED:**  
  This is where we can expect some good and strong price movement to ride. If it's strong enough, many times it marks the start of a new long-lasting major trend.

**Settings:**

- **Charger:**  
  Choose which aspect your HMA should plug itself into, thus it will adapt to it.
- **Minimum Period, Maximum Period:**  
  172 - 233 is just my own setting to outmatch the static HMA 200 for intraday. I find it—in my style of trading—best in a 15m timeframe in almost any pair and 15m to 1H for some stocks. It also works nicely with conventional EMA 200, sometimes as if they somewhat work hand-in-hand in defining where the price should go. But you can, of course, experiment with other ranges, broader or narrower. Especially if you already have an established strategy to follow.
- **Consolidation Area Threshold:**  
  This has to do with slope calculation. The bigger the number means your MA needs a larger degree to define the market is out of flat (yellow) area. This can be useful if needed to lighten up the filter or vice-versa.
- **Background Colouring:**  
  Just another coloring to help highlight the difference in market conditions.

**Alerts:**

There are two alerts:
- **Volume Break:** when volume breaks above average,
- **Volatility Meter:** when the market is more likely about to have its moment of big wiggling brush.

**Usage:**
Very very nice BUY entry to catch a big up-movement if:
1. Price is above MA. (It is best when price is also not too far from the MA, or you can also use distance oscillator to help out too)
2. HMA's color is in darker green. Means it’s on the charging plug with your chosen aspect.
3. RSI is above 50. This helps as additional confirmation.

Clear SELL entry signal is same as above, just the opposite.

**Backtest**

![](https://www.fmz.com/upload/asset/c26d83c2b416482e2d.png)

> Strategy Arguments

| Argument | Default | Description |
| -------- | ------- | ----------- |
| v_input_1 | 0       | Choose which charger to adapt to:: Volatility | Volume |
| v_input_2_close | 0        | Source:: close | high | low | open | hl2 | hlc3 | hlcc4 | ohlc4 |
| v_input_3 | 172      | Minimum period: |
| v_input_4 | 233      | Maximum period: |
| v_input_5 | 17       | Consolidation area is when slope below: |
| v_input_6 | true     | (?Minor Adaptive HMA+ Period) Show minor xHMA+ |
| v_input_7 | 89       | Minimum: |
| v_input_8 | 121      | Maximum: |
| v_input_9 | false    | (?DISTANCE ZONE) Show Adaptive HMA+ Distance Zone |
| v_input_10 | 2.7     | Distance (Envelope) Multiplier |
| v_input_11 | true     | (?OTHER) Show Possible Signals |
| v_input_12 | true     | Background color to differentiate movement |

> Source (PineScript)

```pinescript
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// 2020 © io72signals / Antorio Bergasdito

//@version=4
study("72s: Adaptive Hull Moving Average+", shorttitle="72s: Adaptive HMA+", overlay=true)

// Optional Inputs
charger     = input("Volatility", title="Choose which charger to adapt to:", options=["Volatility", "Volume"])
src         = input(close, title="Source:")
minLength   = input(172, title="Minimum period:")
maxLength   = input(233, title="Maximum period:")
adaptPct    = 0.03141
```