``` pinescript
/*backtest
start: 2022-04-24 00:00:00
end: 2022-05-23 23:59:00
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
//

study(title = "Scalping Swing Trading Tool R1-6 by JustUncleL", shorttitle = "SCALPSWING R1-6", overlay = true)

//
// Revision:        1
// Original Author: JustUncleL
//
// Description:
//    This study project is a Scalping Swing trading Tool designed for a two pane TradingView chart layout: 
//    - the first pane set to 15min Time Frame; 
//    - the second pane set to 1min Time Frame(TF).
//    The tools incorporates the majority of the indicators needed to analyse and scalp Trends for Swings,
//    PullBacks, and reversals on 15min charts and 1min charts. The setup optionally utilizes Heikin Ashi 
//    candle charts. 
//
//    NOTE: A Pullback is synonymous to Retracement, generally a Pullback refers to a large Retracement of 100pips
//    or more. In the context of this Tool and any comments related to it, a Pullback will be the same as a Retracement.
//
//    Incorporated within this tool are the following indicators:
//    1. The following EMAs: 
//       - Green = EMA89 (15min TF) = EMA75 (1min TF)
//       - Blue  = EMA200 (15min TF) = EMA180 (1min TF)
//       - Black = EMA633 (15min TF) = EMA540 (1min TF)
//    2. The 10EMA (default) High/Low+Close Price Action Channel (PAC), the PAC channel display is disabled by default.
//    3. Optionally display Fractals and optional Fractal levels
//    4. Optional HH, LH, LL, HL finder to help with drawing Trend lines and mini Trend Lines.
//    5. Colored-coded Bar high lighting based on the PAC:
//       - blue = bar closed above PAC
//       - red  = bar closed below PAC
//       - gray = bar closed inside PAC
//       - lime line = EMA10 of bar close
//    6. Pivot points (disables Fractals automatically when selected) with optional labels.
//    7. EMA5-12 Channel is displayed by default.
//    8. EMA12-36 Ribbon is displayed by default.
//    9. Optionally display EMA36 and PAC instead of EMA12-36 Ribbon.

Set up and hints:
I am unable to provide a full description here, as Pullback Trading incorporates a full trading methodology, there are many articles and books written on the subject.

Set to two pane TradingView chart, set first pane to 15Min and second to 1min.
Set the chart to Heikin Ashi Candles (optional).
I also add a "Sweetspot Gold2" indicator to the chart as well to help with support and resistance finding and shows where the important "00" lines are.
Use the EMA200 on the 15min pane as the anchor. So when prices above EMA200 we only trade long (buy) and when prices below the EMA200 we only trade short (sell).
On the 15min chart draw any obvious Vertical Trend Lines ( VTL ), use Pivots point as a guide.
On the 15min chart look for the price to Pullback into the EMA5-12 Channel or EMA12-36 ribbon, we draw Trendlines utilising the Pivot points or Fractals to guide your TL drawing.
On the 15min chart look for the trend to resume and break through the drawn TL. The bar color needs to change back to the trend direction color to confirm as a break.
Now this break can be traded as a 15min trade or now look to the 1min chart.
On the 1min chart draw any Pullback into any of the EMAs.
On the 1min chart look for the trend to resume and break through the drawn TL. The bar color needs to change back to the trend direction color to confirm as a break.
Now this break can be traded as a 1min trade.
There is also an option to select Pristine (ie Ideal) filtered Fractals, which look like tents or V shape 5-candle patterns. These are actually used to calculate the Pivot points as well.
Other than the "Sweetspot Gold2" indicator, you should not need any other indicators to successfully trade trends for Pullbacks and reversals. If you really want another indicator use the AO (Awesome Oscillator) as it is momentum based.

**Backtest**
![](https://www.fmz.com/upload/asset/11a7ebca21140501d74.png)

> Strategy Arguments


| Argument  | Default   | Description                                                                 |
|-----------|-----------|----------------------------------------------------------------------------|
| v_input_1 | true      | Show Price Action Channel (PAC)                                             |
| v_input_2 | true      | Show colored bars close relative to PAC                                      |
| v_input_3 | 10        | High Low PAC Length                                                         |
| v_input_4 | false     | Show PAC Swing Alerts                                                       |
| v_input_5 | false     | Use Big Arrows for Swing Alerts                                             |
| v_input_6 | true      | Filter PAC Alerts with 200ema                                               |
| v_input_7 | true      | Show EMA12_Channel                                                          |
| v_input_8 | true      | Show EMA36_Ribbon                                                           |
| v_input_9 | true      | Show Pivot points                                                           |
| v_input_10| true      | Show Pivot Labels                                                           |
| v_input_11| false     | Show HH, LH, LL, HL finder                                                   |
| v_input_12| true      | Show Fractals                                                               |
| v_input_13| false     | Show Fractal Levels                                                         |
| v_input_14| false     | Filter for Pristine (Ideal) Fractals                                        |

```