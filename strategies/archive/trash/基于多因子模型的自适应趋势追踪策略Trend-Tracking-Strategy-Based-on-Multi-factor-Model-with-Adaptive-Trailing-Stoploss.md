> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1_hlc3|0|SOURCE: hlc3|high|low|open|hl2|close|hlcc4|ohlc4|
|v_input_2|14|RSI LENGTH|
|v_input_3|52|RSI CENTER LINE|
|v_input_4|7|MACD FAST LENGTH|
|v_input_5|12|MACD SLOW LENGTH|
|v_input_6|12|MACD SIGNAL SMOOTHING|
|v_input_7|10|Key Vaule. 'This changes the sensitivity'|
|v_input_8|3|SmoothK|
|v_input_9|3|SmoothD|
|v_input_10|14|LengthRSI|
|v_input_11|14|LengthStoch|
|v_input_12_close|0|RSISource: close|high|low|open|hl2|hlc3|hlcc4|ohlc4|
|v_input_13|10|ATR Period|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-12 00:00:00
end: 2023-12-18 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=2
strategy(title="TradersAI_UTBot", overlay = true)
// CREDITS to @HPotter for the orginal code. 
// CREDITS to @Yo_adriiiiaan for recently publishing the UT Bot study based on the original code - 
// I just added some simple code to turn it into a strategy so that you all can backtest it to see the results for yourself! 
// Use this strategy on your favorite instrumnet and timeframe, with your favorite settings
// While @Yo_adriiiiaan mentions it works best on a 4-hour timeframe or above, 
// I am happy to share here this working on a 15-minute chart on e-mini S&P 500 Index (using the KeyValue setting at 10)
// I am sure different people would discover different settings that work best for their preferred instrumnet/timeframe etc. 
// Play with it and enjoy! And, don't forget to share any positive results you might get! Good luck with your trading!

SOURCE = input(hlc3)
RSILENGTH = input(14, title = "RSI LENGTH")
RSICENTERLINE = input(52, title = "RSI CENTER LINE")
MACDFASTLENGTH = input(7, title = "MACD FAST LENGTH")
MACDSLOWLENGTH = input(12, title = "MACD SLOW LENGTH")
MACDSIGNALSMOOTHING = input(12, title = "MACD SIGNAL SMOOTHING")
KEYVALUE = input(10, title = "Key Vaule. 'This changes the sensitivity'")
SMOOTHK = input(3, title = "SmoothK")
SMOOTHD = input(3, title = "SmoothD")
LENGTHRSI = input(14, title = "LengthRSI")
LENGTHSTOCH = input(14, title = "LengthStoch")
RSISOURCE = input(close, title = "RSISource: close")
ATRPERIOD = input(10, title = "ATR Period")

// RSI
rsiValue = rsi(SOURCE, RSILENGTH)
rsiCenterLine = rsi(SOURCE, RSICENTERLINE)

// MACD
macdLine = ema(SOURCE, MACDFASTLENGTH) - ema(SOURCE, MACDSLOWLENGTH)
macdSignal = ema(macdLine, MACDSIGNALSMOOTHING)
macdHist = macdLine - macdSignal

// Stochastics
stochK = stoch(SOURCE, LENGTHSTOCH)
stochD = sma(stochK, SMOOTHK)

// ATR
atrValue = atr(ATRPERIOD)

// Buy Signal
buySignal = rsiValue > RSICENTERLINE and macdHist > 0 and stochK > stochD and stochK > KEYVALUE

// Sell Signal
sellSignal = rsiValue < RSICENTERLINE and macdHist < 0 and stochK < stochD and stochK < KEYVALUE

// Stop Loss
stopLoss = atrValue * 2

// Strategy Execution
if (buySignal)
    strategy.entry("Buy", strategy.long)
    strategy.exit("Stop Loss", "Buy", stop = stopLoss)

if (sellSignal)
    strategy.entry("Sell", strategy.short)
    strategy.exit("Stop Loss", "Sell", stop = stopLoss)
```

This translation preserves the original PineScript code and formatting, including the comments and default values for the strategy arguments.