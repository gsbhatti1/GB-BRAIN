> Name

RSI2 Strategy之日内反转胜率回测 - RSI2-Strategy-Intraday-Reversal-Win-Rate-Backtest

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/1b7aa933f913a62e3e5.png)

#### Overview
This strategy is based on the oversold signal of the Relative Strength Index (RSI) indicator, buying at the intraday low and then setting fixed percentage take-profit and stop-loss levels to backtest the probability of the strategy hitting these levels. The main idea is to take advantage of the reversal opportunity when the RSI indicator is oversold, enter at the intraday low, and seek short-term profits brought by the reversal. At the same time, it uses a moving average to filter the trend and only goes long when the price is above the moving average.

#### Strategy Principle
1. Calculate the 2-period RSI indicator and the 200-period simple moving average.
2. When the closing price is higher than the moving average and the RSI is lower than the oversold threshold (default 10), buy at the opening of the next trading day.
3. Record the lowest price of the day of buying as the entry price.
4. Calculate a 6% take-profit price and a 3% stop-loss price based on the entry price.
5. On the next trading day, if the take-profit price is hit, close the position for profit; if the stop-loss price is hit, close the position for loss.
6. Count the number of take-profits and stop-losses, and calculate the win rate of the strategy within the set period.

#### Advantage Analysis
1. Buy at intraday low to capture the reversal gains after the RSI indicator oversold.
2. Fixed percentage take-profit and stop-loss to control single transaction risk.
3. Use long-cycle moving average to filter and reduce counter-trend trading.
4. Simple and easy to use, flexible parameter settings, suitable for short-term traders.

#### Risk Analysis
1. RSI oversold does not guarantee a necessary reversal; the market may continue to fall under extreme conditions.
2. Fixed percentage take-profit and stop-loss may not cover transaction costs.
3. The entry point is based on the intraday lowest price, which is difficult to buy precisely at the lowest point in actual operation.
4. Lack of trend judgment; simply relying on overbought and oversold signals, the return ratio may not be high.

#### Optimization Direction
1. Use adaptive take-profit and stop-loss, dynamically adjusting according to indicators such as price volatility.
2. Add trend confirmation indicators, such as MACD, DMI, etc., to avoid counter-trend trading.
3. Optimize entry points, such as using variable distance turtle trading rules.
4. Increase position management to improve capital utilization and return rate.
5. Combine with other short-cycle indicators to improve signal confirmation, such as Bollinger Bands, KDJ, etc.

#### Summary
The RSI2 strategy attempts to capture intraday reversal opportunities after the RSI indicator is oversold, and controls risk by setting fixed percentage take-profit and stop-loss levels while using a long-period moving average to filter counter-trend signals. The strategy is simple and suitable for short-term speculative traders. However, it also has certain limitations, such as lack of trend judgment, difficulty in accurately buying at the lowest point, and fixed take-profit and stop-loss limits the profit potential. In the future, this strategy can be improved from aspects such as dynamic take-profit and stop-loss, combining trend indicators, optimizing entry points, and strengthening position management to enhance systematicness and robustness, better adapting to changing market environments.

||

#### Source (PineScript)

```pinescript
/*backtest
start: 2024-03-01 00:00:00
end: 2024-03-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © rajk1987

//@version=5
strategy("RSI2 Strategy Raj", overlay=true, margin_long=100, margin_short=100)

rsi_len = input.int(2, title="RSI Length", group="Indicators")
rsi_os  = input.float(10, title="RSI Oversold", group="Indicators")
rsi_ob  = input.float(90, title="RSI OverBrought", group="Indicators")
max_los = input.float(3, title="Max Loss Percent", group="Indicators")
tar_per = input.float(6, title="Target Percent", group="Indicators")

// Get the RSI value of the stock
rsi = ta.rsi(close, rsi_len)
sma = ta.sma(close, 200)
var ent_dat = 0
var tar = 0.0
var los = 0.0
var bp = 0.0

if ((close > sma) and (rsi < rsi_os))
    strategy.entry("RSI2 Long Entry", strategy.long, 1)
    ent_dat := time(timeframe.period)

if (ent_dat == time(timeframe.period)) // Add the missing code here
```

Note: The code block is incomplete at the end. It's suggested to complete it according to your trading logic.