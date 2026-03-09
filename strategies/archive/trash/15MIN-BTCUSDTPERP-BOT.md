> Name

15MIN-BTCUSDTPERP-BOT

> Author

ChaoZhang

> Strategy Description

This is my BTCUSDTPERP 15 min bot.
Best results are on BTCUSDTPERP at binancefutures.
Results depend on specific volume indicators that work best at binancefutures.

15-min bots are really fast. It's hard to find a good configuration because of the 15-min backtesting, which is least around 3-4 months.

This bot is specifically designed for high % profitable trades. The net profit is also quite good. However, 15-min bots are extremely difficult to use in the long term, so I made the default settings as flexible as possible.

So,
This bot uses 11 different indicators:
1) ADX
2) RANGE FILTER
3) SAR
4) RSI
5) TWAP
6) JMA
7) MACD
8) VOLUME DELTA
9) VOLUME WEIGHT
10) MA
and the last one for better results on quick charts (15min), I decided to add:
11) STOCH

1) ADX - provides a solid view of trends without any scam wick: Long only on green bars, Shorts only on red bars. This helps my strategy define the right trend; there is also an orange option for unidentified trends.
2) RANGE FILTER - this indicator offers a better view of trends and defines them, which is important for identifying bull/bear traps that help a lot because of the very variable trends.
3) SAR - The parabolic SAR is a technical indicator used to determine the price direction of an asset, as well as draw attention to when the price direction is changing. SAR supports the bot by not opening new trades when the trend is slowly changing.
4) RSI - the value helps the strategy stop trading at the right time. When RSI is overbought, the strategy does not open new long positions; also, when RSI is oversold, the strategy does not open new short positions.
5) TWAP - has the same task as Range Filter, only for a better view of trends and defining them.
6) JMA - The Jurik Moving Average indicator is one of the surest ways to smooth price curves within a minimum time lag. The indicator offers currency traders one of the best price filters during strong price moves. In this time, when Bitcoin's price action is so strong, this indicator is necessary.
7) MACD - Moving average convergence divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. The MACD is calculated by subtracting the 26-period exponential moving average (EMA) from the 12-period EMA.
Today, macd just like JMA is necessary to make profitable bots.
8) Volume Delta - A Cumulative Volume Delta approach based on the Bull and Bear Balance Indicator by Vadim Gimelfarb published in the October 2003 issue of the S&C Magazine. Adjust the length of the moving average according to your needs (Symbol, Timeframe, etc.)
9) Volume Weight - is the most important indicator for the strategy, to avoid opening trades on flat charts; new trades are opened after strong volume bars.
10) MA 5-10-30 - like previous ones, this is for a better view of trends and correctly defining them. Also, Speed_MA are used for predicting future price action.
11) Stochastic - stoch is useful for predicting trend reversals. It also focuses on price momentum and can be used to identify overbought and oversold levels.

Enjoy ;)

**Backtest**
![IMG](https://www.fmz.com/upload/asset/16ed324d9172131e373.png)

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|v_input_1_ohlc4|0|src: ohlc4|high|low|open|hl2|hlc3|hlcc4|close|
|v_input_2|true|AVERAGE DIRECTIONAL INDEX|
|v_input_3|0|ADX OPTION: MASANAKAMURA|CLASSIC|
|v_input_4|11|ADX LENGTH|
|v_input_5|12|ADX THRESHOLD|
|v_input_6|13|Range Filter length|
|v_input_7|true|Range Filter mult|
|v_input_8|false|SAR Start|
|v_input_9|0.006|SAR Increment|
|v_input_10|true|SAR Maximum|
|v_input_11|true|SAR Point Width|
|v_input_12|70|RSI length|
|v_input_13_close|0|RSI Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_14|10|TWAP Smoothing|
|v_input_15|0|TWAP Timeframe|
|v_input_16_close|0|JMA Source: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_17||JMA Resolution|
|v_input_18|false|JMA Allow Repainting?|
|v_input_19|4|JMA Length|
|v_input_20|25|MACD Fast Length|
|v_input_21|50|MACD Slow Length|
|v_input_22|9|MACD Signal Smoothing|
|v_input_23|45|Delta Length|
|v_input_24|100|Volume Weight Length|
|v_input_25|0|Volume Weight Type: SMA|EMA|HMA|WMA|DEMA|
|v_input_26|1.5|Volume To Trigger Signal|
|v_input_27|51|MA Length|
|v_input_28|5|AvgType|
|v_input_29|45|Momentum Length|
|v_input_30|12|Momentum Calc length|
|v_input_31|9|Momentum Smooth length|
|v_input_32|true|BACKTEST|
|v_input_33|180|BACKTEST DAYS|
|v_input_34|0|ENTRY TYPE: % EQUITY|CASH|CONTRACTS|
|v_input_35|3.6|Stop Loss % [plotshape]|
|v_input_36|0.8|Take Profit % [plotshape]|
|v_input_37|3.6|stop loss [BT]|
|v_input_38|100|qty percent|
|v_input_39|0.8|Take profit [BT]|

> Source (PineScript)

```pinescript
//@version=4
strategy("15MIN BTCUSDTPERP BOT", overlay=true, pyramiding=1, initial_capital = 10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0)

// SOURCE ==================================================================================================================================================================================================================================================================

src = input(ohlc4)

// INPUTS ==================================================================================================================================================================================================================================================================

// ADX ----------------------------------------------------------------------------------------------------------------------
```