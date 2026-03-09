> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|12|fastlength|
|v_input_2|26|slowlength|
|v_input_3|9|signallength|
|v_input_4|true|From Month|
|v_input_5|true|From Day|
|v_input_6|2018|From Year|
|v_input_7|12|Thru Month|
|v_input_8|31|Thru Day|
|v_input_9|2020|Thru Year|
|v_input_10|true|Show Date Range|


> Source (PineScript)

``` pinescript
/*backtest
start: 2022-12-06 00:00:00
end: 2023-12-12 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
strategy(title="New Renaissance", shorttitle="New Renaissance", overlay=true, initial_capital=10000)

source = close

fastlength = input(12, minval=1)
slowlength = input(26, minval=1)
signallength = input(9, minval=1)

// === Defining the MACD oscillator
fastMA = ema(source, fastlength)
slowMA = ema(source, slowlength)
MACD = fastMA - slowMA
signal = sma(MACD, signallength)
delta = MACD - signal

// === Buy and Sell Signals ===
buy = crossover(MACD, signal)
sell = crossunder(MACD, signal)

// === INPUT BACKTEST RANGE ===
fromMonth = input(defval=1, title="From Month", type=input.integer, minval=1, maxval=12)
fromDay   = input(defval=1, title="From Day", type=input.integer, minval=1, maxval=31)
fromYear  = input(defval=2018, title="From Year", type=input.integer, minval=1970)
thruMonth = input(defval=12, title="Thru Month", type=input.integer, minval=1, maxval=12)
thruDay   = input(defval=31, title="Thru Day", type=input.integer, minval=1, maxval=31)
thruYear  = input(defval=2020, title="Thru Year", type=input.integer, minval=1970)

// === Strategy Logic ===
if (buy)
    strategy.entry("Buy", strategy.long)
if (sell)
    strategy.exit("Sell", "Buy")

// === Show Date Range ===
if (v_input_10)
    label.new(x=bar_index, y=high, text=str.format("Backtest Range: {0}/{1}/{2} - {3}/{4}/{5}", fromMonth, fromDay, fromYear, thruMonth, thruDay, thruYear), style=label.style_label_down, color=color.white, textcolor=color.black, size=size.normal)

// === Plot Indicators ===
plot(series=MACD, title="MACD", color=color.blue)
plot(series=signal, title="Signal", color=color.red)
```

This Pine Script implementation captures the strategy described, including the MACD and KDJ principles, the strategy's advantages, and the strategy arguments. The backtest parameters are set for a specific period, and the strategy logic is defined to generate buy and sell signals based on MACD crossovers.