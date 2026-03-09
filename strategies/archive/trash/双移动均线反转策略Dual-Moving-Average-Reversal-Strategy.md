> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_int_1|14|(?●═════ 2/20 EMA ═════●)Length|
|v_input_int_2|5|(?●═════ Average True Range Reversed  ═════●)nATRPeriod|
|v_input_float_1|3.5|nATRMultip|
|v_input_bool_1|false|(?●═════ MISC ═════●)Trade reverse|
|v_input_int_3|true|(?●═════ Time Start ═════●)From Day|
|v_input_int_4|true|From Month|
|v_input_int_5|2005|From Year|


> Source (PineScript)

```pinescript
/*backtest
start: 2022-10-27 00:00:00
end: 2023-11-02 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
////////////////////////////////////////////////////////////
//  Copyright by HPotter v1.0 05/04/2022
// This is a dual-moving-average-reversal strategy.
//
// First, it uses the 2/20 Exponential Moving Average (EMA) to identify potential trend reversals.
// When the price crosses above or below the EMA, it generates a trading signal.
//
// Second, it uses the ATR Reversal Indicator with a multiple of 3.5 to determine stop loss levels,
// which are triggered when the price breaks through these levels, generating opposing signals.
//
// The strategy combines both indicators and executes trades based on their combined signals:
// - If the EMA generates a long signal while ATR reverses to short, it goes short.
// - If the EMA generates a short signal while ATR reverses to long, it goes long.
//
//
// Advantages:
// 1. The EMA can identify mid-term trends and avoid false signals from market noise.
// 2. The ATR Reversal Indicator captures short-term price movements and reversals.
// 3. Combining both signals allows for early identification of trend reversals, potentially improving profitability.
// 4. Reasonable stop loss levels help control risk.
// 5. Customizable parameters allow adaptation to different market conditions.
//
// Risks:
// 1. The EMA may miss short-term opportunities due to its slower nature.
// 2. Stop loss levels can be easily broken, requiring wider stops.
// 3. Single indicators can generate false signals; multiple filters are needed.
// 4. Frequent trading should be monitored and managed carefully.
//
// Optimization Directions:
// 1. Tune EMA parameters for better performance.
// 2. Optimize ATR multiplier settings.
// 3. Add additional filtering conditions such as volume, volatility, etc.
// 4. Implement advanced capital management techniques to dynamically adjust positions.
// 5. Integrate alternative stop loss strategies like Chandelier Exit.
// 6. Test the strategy across different markets and adjust parameters accordingly.
// 7. Incorporate machine learning models for improved performance.
// 8. Combine multiple sub-strategies to explore additional alpha.
//
// Conclusion:
// This dual-moving-average-reversal strategy aims to capture price reversals by combining trend-following and short-term reversal ideas, but requires careful parameter tuning and risk management to optimize its performance.
////////////////////////////////////////////////////////////
EMA20(Length) =>
    pos = 0.0
    xPrice = close
    xXA = ta.ema(xPrice, Length)
    nHH = math.max(high, high[1])
    nLL = math.min(low, low[1])
    nXS = nLL > xXA or nHH < xXA ? nLL : nHH
    iff_1 = nXS < close[1] ? 1 : nz(pos[1], 0)
    pos := nXS > close[1] ? -1 : iff_1
    pos

ATRR(nATRPeriod, nATRMultip) =>
    pos = 0.0
    xATR = ta.atr(nATRPeriod)
    nLoss = nATRMultip * xATR
    xATRTrailingStop = 0.0
    xATRTrailingStop := close > nz(xATRTrailingStop[1], 0) and close[1] > nz(xATRTrailingStop[1], 0) ? math.max(nz(xATRTrailingStop[1]), close - nLoss) :
                          close < nz(xATRTrailingStop[1], 0) and close[1] < nz(xATRTrailingStop[1], 0) ? math.min(nz(xATRTrailingStop[1]), close + nLoss) : 
                          close > nz(xATRTrailingStop[1], 0) ? close - nLoss : close + nLoss
    pos := close[1] < nz(
```