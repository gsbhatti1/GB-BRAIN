> Name

Johnys-BOT

> Author

ChaoZhang

> Strategy Description

Hello


This is an updated version of the 60MIN bot. I decided to create this bot for people who are still using the 10BOT. This version is much more profitable and reliable.

THIS IS SO IMPORTANT FOR USERS

As always, this bot is ONLY FOR BINANCE:BTCUSDTPERP.

To make the results as accurate as possible, I decided to use as few indicators as possible, which translates into a higher number of positions. This makes the bot quicker in reacting to any change in trend. Unfortunately, this also means that the quality of opened positions has decreased somewhat (79% profitable trades). It also consists of a fairly high target point and basically a low stop-loss.

**Take Profit (TP): 1.5**
**Stop Loss (SL): 7.2**

The bot uses some of the most efficient and important indicators, such as:

- **ADX**: One of the most powerful and accurate trend indicators. ADX measures how strong a trend is and can provide valuable information on potential trading opportunities.
- **CLOUD**: This is one of the newest indicators I'm using. It helps in identifying the correct market trend. By applying the length of this indicator, I can notice changes in the trend slightly later but more accurately.
- **RANGE FILTER**: This indicator provides a better view of trends and defines trends, which is crucial for avoiding bull/bear traps. The variable nature of trends makes it very useful.
- **FAST MA**: Like previous indicators, it helps in identifying trends correctly and predicting future price action.
- **MACD**: Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. MACD is calculated by subtracting the 26-period Exponential Moving Average (EMA) from the 12-period EMA.
- **VOLUME**: This is the most important indicator for the strategy to avoid opening trades on flat charts. New trades are opened after strong volume bars.
- **RSI**: The RSI value helps in stopping trades at the right time. When RSI is overbought, new long positions are not opened; when RSI is oversold, new short positions are not opened.

Using these indicators, the bot opens about 75-80% of positions.

In addition, I created two independent conditions for opening a position:

- **REVERSALS (based on RSI crossovers)**: This option can add more speed to make the right decisions while trends are changing very fast.
- **BOLLINGER BANDS**: This function has also increased the possibilities of opening and closing new positions. It works such that if the candle closes outside the Bolinger bands, more positions are opened. I focused on this function to maintain a high percentage level as much as possible.

To maintain the high quality of trades, both Bollinger Bands and Reversals depend on the most important indicators.

I think these results from the bot are the most accurate, but let's not forget that backtesting is testing in the past, and it is not known how the bot will behave in the future. However, using non-optimized indicators can bring results very close in the future.

Good luck and enjoy ;)

**Backtesting**

![IMG](https://www.fmz.com/upload/asset/159efe4661da93e1142.png)

> Strategy Arguments

| Argument | Default | Description |
| --- | --- | --- |
| v_input_1_high | 0 | src: high, close, low, open, hl2, hlc3, hlcc4, ohlc4 |
| v_input_26 | 15 | leftBars |
| v_input_27 | 7 | rightBars |
| v_input_2 | 0 | ADX options: MASANAKAMURA, CLASSIC |
| v_input_3 | 13 | ADX options length |
| v_input_4 | 15 | ADX options threshold |
| v_input_5 | 7 | Cloud Length |
| v_input_6 | 0.015 | SAR Start |
| v_input_7 | 0.018 | SAR Increment |
| v_input_8 | 0.1 | SAR Maximum |
| v_input_9 | 10 | Range Filter Period |
| v_input_10 | 1.5 | mult. |
| v_input_11 | 11 | MACD Fast Length |
| v_input_12 | 8 | Slow Length |
| v_input_13 | 17 | Signal Smoothing |
| v_input_14 | 0.8 | Volume mult. |
| v_input_15 | 37 | Volume length |
| v_input_16 | 25 | RSI Lenght |
| v_input_17 | true | Show BB |
| v_input_18 | true | Show MA |
| v_input_19 | Timeframe |
| v_input_20_high | 0 | Source: high, close, low, open, hl2, hlc3, hlcc4, ohlc4 |
| v_input_21 | 10 | Period |
| v_input_22 | 2.1 | Deviation |
| v_input_23 | 66 | Fast MA Length |
| v_input_24 | 2 | AvgType |
| v_input_25 | true | REVERSAL |
| v_input_28 | 64 | REV Rsi Overbought |
| v_input_29 | 34 | REV RSI Oversold |
| v_input_30 | 1.5 | TP Long |
| v_input_31 | 1.5 | TP Short |
| v_input_32 | true | Stop loss? |
| v_input_33 | 7.2 | % Stop loss |
| v_input_34 | true | Longs |
| v_input_35 | true | Shorts |
| v_input_36 | 0.015 | TP/100 |
| v_input_37 | 0.072 | SL/100 |

> Source (PineScript)

``` pinescript
/*backtest
start: 2022-05-01 00:00:00
end: 2022-05-16 23:59:00
period: 4h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4

strategy("Johny's BOT [60MIN]", overlay=true, pyramiding=1, initial_capital = 10000, default_qty_type= strategy.percent_of_equity, default_qty_value = 100, calc_on_order_fills=false, slippage=0, commission_type=strategy.commission.percent, commission_value=0.04)

//SOURCE =============================================================================================================================================================================================================================================================================================================

src                 =                   input(high)

// INPUTS ============================================================================================================================================================================================================================================================================================================

// ADX -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```