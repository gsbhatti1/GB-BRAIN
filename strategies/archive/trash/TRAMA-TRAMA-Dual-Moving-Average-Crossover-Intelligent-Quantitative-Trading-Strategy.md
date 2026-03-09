```markdown
---

#### Overview
This is an intelligent quantitative trading strategy based on TRAMA (Triangular Moving Average) and Simple Moving Average (SMA). The strategy combines two moving average systems for generating trading signals and implements a stop-loss/take-profit mechanism for risk control. It uses 4-period and 28-period SMA crossovers along with the TRAMA indicator to confirm trading signals, improving accuracy through multiple signal confirmation.

#### Strategy Principles
The strategy employs two core components for generating trading signals. First is the crossover system based on 4-period and 28-period SMAs, generating long signals when the short-term MA crosses above the long-term MA, and short signals when it crosses below. Second, the strategy incorporates the TRAMA indicator as an auxiliary confirmation system. TRAMA is an improved moving average with faster response time and less lag. Additional trading signals are generated when price breaks through the TRAMA. The strategy also includes percentage-based take-profit and stop-loss mechanisms set at 2% and 1% respectively.

#### Strategy Advantages
1. Dual signal confirmation mechanism significantly improves trading reliability
2. TRAMA indicator enables faster capture of market trend changes
3. Clear risk control mechanism through stop-loss and take-profit levels
4. Clear and easy-to-maintain strategy logic
5. Enables both long and short trading, increasing profit opportunities

#### Strategy Risks
1. May generate excessive trading signals in ranging markets
2. Fixed stop-loss and take-profit percentages may not suit all market conditions
3. Short-term moving average may be sensitive to price noise
4. Potential slippage risks in volatile markets
5. Need to consider the impact of trading costs on strategy performance

#### Strategy Optimization Directions
1. Introduce volatility-adaptive stop-loss and take-profit mechanisms
2. Add market environment filters to adjust strategy parameters under different conditions
3. Optimize TRAMA parameter selection method, consider using adaptive periods
4. Add volume confirmation indicators to improve signal reliability
5. Consider adding trend strength filters to avoid trading in weak trends

#### Summary
This is a strategy that combines traditional technical analysis with modern quantitative trading concepts. Through multiple signal confirmation and strict risk control, the strategy demonstrates good practicality. While there are areas for optimization, the overall framework design is reasonable with good application prospects. Traders are advised to conduct thorough historical data backtesting and parameter optimization before live trading.

---

#### Source (PineScript)

```pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-27 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © ivanvallejoc

//@version=5
strategy("MANCOS2.0", overlay=true, margin_long=80, margin_short=80)

longCondition = ta.crossover(ta.sma(close, 4), ta.sma(close, 28))
if (longCondition)
    strategy.entry("My Long Entry Id", strategy.long)

shortCondition = ta.crossunder(ta.sma(close, 4), ta.sma(close, 28))
if (shortCondition)
    strategy.entry("My Short Entry Id", strategy.short)

// TRAMA parameters
length = input(1.5, title="TRAMA Length")
src = close
filt = 2 / (length + 1)
trama = 0.0
var tramaPrev = na(trama[1]) ? close : trama[1]
trama := (src - tramaPrev) * filt + tramaPrev

// Plot the TRAMA
plot(trama, color=color.blue, linewidth=2, title="TRAMA")

// Buy and sell signals based on TRAMA
buySignal = ta.crossover(close, trama)
sellSignal = ta.crossunder(close, trama)

// Take Profit and Stop Loss configuration
takeProfitPerc = input(2, title="Take Profit (%)") / 100
stopLossPerc = input(1, title="Stop Loss (%)") / 100

// TP/SL prices
takeProfitPrice = strategy.position_avg_price * (1 + takeProfitPerc)
stopLossPrice = strategy.position_avg_price * (1 - stopLossPerc)

// Long entry conditions
if (buySignal)
    strategy.entry("Long", strategy.long)

// Exit long position for TP/SL
if (strategy.position_size > 0)
    strategy.exit("TP/SL", "Long", limit=takeProfitPrice, stop=stopLossPrice)

// Short entry based on TRAMA
if (sellSignal)
    strategy.entry("Short", strategy.short)

// TP/SL prices for short positions
takeProfitPriceShort = strategy.position_avg_price * (1 - takeProfitPerc)
stopLossPriceShort = strategy.position_avg_price * (1 + stopLossPerc)

if (strategy.position_size < 0)
    strategy.exit("TP/SL", "Short", limit=takeProfitPriceShort, stop=stopLossPriceShort)
```

---

#### Detail

https
```