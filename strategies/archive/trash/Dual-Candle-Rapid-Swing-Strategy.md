```plaintext
Name

Dual-Candle-Rapid-Swing-Strategy

Author

ChaoZhang

Strategy Description


This strategy calculates the combination of daily trading volume changes and NVI indicators to determine the market swings within the very short term for trading.

Specifically, it counts the number of days when daily trading volume decreases from the previous day, and forms an oscillator through changes in the NVI value. Long positions are generated when the indicator turns from negative to positive and the second candle is still positive; short positions are taken when the indicator turns from positive to negative and the second candle is still negative.

The advantage of this strategy is that it captures very short-term gaps and only requires 2 candles to form a trading signal and achieve profits. However, this high-frequency trading method has the risk of over-optimization, and the effect may vary greatly in different market time periods.

In addition, such short-term transactions also have a certain dependence on transaction fees, and parameters need to be adjusted for specific varieties. At the same time, errors in trading decisions within a very small period of time may also cause losses. Only by strictly controlling the capital size of a single transaction can this double candle strategy be applied for a long time.

||

This strategy combines calculations of daily volume change and the NVI indicator to trade short-term market swings.

Specifically, it counts the number of days when volume is lower than the previous day, and uses changes in NVI value to form an oscillator. Long signals are generated when the oscillator flips from negative to positive and remains positive on the second candle. Short signals occur when the oscillator flips from positive to negative and remains negative on the second candle.

The advantage of this strategy is that it capitalizes on short-term gaps within just 2 candles. However, such high-frequency trading risks over-optimization, with performance varying greatly across market time periods.

Also, trading fees can be a concern for such short-term trades, requiring parameter tuning per instrument. And slight errors in decisions within small timeframes could lead to losses. Only by strictly controlling per trade position sizes can this dual candle strategy be applied successfully over the long run.

```

> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_1|true|═════════ DESDE ════════|
|v_input_2|true|Mes|
|v_input_3|true|Dia|
|v_input_4|2018|Año|
|v_input_5|true|═════════ HASTA ════════|
|v_input_6|31|Mes|
|v_input_7|12|Dia|
|v_input_8|9999|Año|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-09-04 00:00:00
end: 2023-09-10 00:00:00
Period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//
//▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒