---
### Name

blackcat-L1-MartinGale-Scalping-Strategy

### Author

Zer3192

### Strategy Description

MartinGale (Martingale) strategy is a popular funding management strategy commonly used in trading. It is typically employed by traders to seek recovery through increasing position size after each loss. Hence, MartinGale is not a specific strategy but a general term for strategies that involve adding or scaling up positions.

In the MartinGale strategy, traders increase their position size exponentially after every losing trade. The aim is to eventually hit a winning trade, thereby recovering previous losses and generating profit.

The underlying principle of the MartinGale strategy is based on the law of averages. By increasing the position size after each loss, this strategy assumes that a winning trade will eventually occur, not only to recover the previous losses but also to generate additional profits. This may be particularly appealing to traders seeking rapid recovery from losses.

However, it's important to note that MartinGale strategies carry significant risks. If a trader experiences a prolonged losing streak or lacks sufficient funds, this strategy could result in substantial losses. The strategy relies on the assumption that a winning trade will occur within a certain timeframe, which is dangerous because there is no guarantee of such an occurrence.

Traders considering implementing a MartinGale strategy should carefully evaluate their risk tolerance and fully understand its potential drawbacks. Establishing a robust risk management plan to mitigate potential losses is crucial. Additionally, traders should recognize that this strategy may not be suitable for all market conditions and may need adjustment based on market volatility.

In summary, the MartinGale strategy involves increasing position size after each loss in an attempt to recover from losing phases. While it offers the potential for rapid recovery, significant risks must be considered by traders before implementing this trading method.

Although I do not fully agree with this trading perspective, someone requested me to discuss this topic. Therefore, I wrote a simple 38-line framework for short-term MartinGale scalping.

MartinGale scalp strategy is a trading approach that aims to generate profits through frequent trading, utilizing the crossing of moving averages as entry and exit signals. This strategy is implemented using TradingView's Pine Script language.

The strategy first defines input variables such as take profit and stop loss levels, along with the trading mode (long, short, or both). It then sets a rule that only allows entries when the trading mode is set to "long."

The strategy logic uses crossover signals of simple moving averages (SMA) to define entry and exit. It calculates a short-term SMA (SMA3) and a long-term SMA (SMA8), plotting them on the chart. `crossoverSignal` and `crossunderSignal` variables track when crossovers and crossunders occur, while `crossoverState` and `crossunderState` determine the state of crossover conditions.

Strategy execution is based on current position size. If there are no open positions (no trades), the strategy checks for a crossover or crossunder event. If an entry condition is met with the trading mode allowing long entries, it enters into a long position. Entry and stop loss prices are calculated based on the current close price and SMA8 value. Similarly, if a short entry condition is met, the strategy enters into a short position, with corresponding price calculations.

If there is a long position and the current close price reaches either the take profit or stop loss level due to an event, it closes the long position. Entry, stop loss, take profit prices are reset to zero.

Similarly, if there is a short position and the current close price reaches either the take profit or stop loss level due to an event, it closes the short position, resetting the price variables.

The strategy also uses the `plotshape` function to mark entry and exit points on the chart. It displays an upward triangle for buy entries, a downward triangle for sell entries, a downward triangle for buy exits, and an upward triangle for sell exits.

Overall, the MartinGale scalp strategy aims to capture small profits by leveraging the crossovers of short-term moving averages. It implements risk management through stop loss and take profit levels and allows different trading modes to adapt to varying market conditions.

### Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_1|1.03|Take Profit|
|v_input_2|0.95|Stop Loss|
|v_input_string_1|0|Trading Mode: Long|Short|BiDir|


### Source (PineScript)

```pinescript
//@version=5
strategy('[blackcat] L1 MartinGale Scalping Strategy', overlay=true, pyramiding = 5)
 
 // Define input variables
// martingaleMultiplier = input(2, title="加倍倍数")
 takeProfit = input(1.03, title='Take Profit')
 stopLoss = input(0.95, title='Stop Loss')
 inputTradingMode = input.string(defval='Long', options=['Long', 'Short', 'BiDir'], title='Trading Mode')
 
 // The purpose of this rule is to forbid short entries; only long entries will be placed. The rule affects the following function: 'entry'.
 strategy.risk.allow_entry_in(inputTradingMode == 'Long' ? strategy.direction.long : inputTradingMode == 'Short' ? strategy.direction.short : strategy.direction.all)

// Define strategy logic 
entryPrice = 0.0
stopPrice = 0.0
takeProfitPrice = 0.0
stopLossPrice = 0.0

// Define SMA crossover and crossunder signals
sma3 = ta.sma(close, 3)
sma8 = ta.sma(close, 8)
plot(sma3, color=color.yellow)
plot(sma8, color=color.fuchsia)
crossoverSignal = ta.crossover(sma3, sma8)
crossunderSignal = ta.crossunder(sma3, sma8)
crossoverState = sma3 > sma8
crossunderState = sma3 < sma8

if strategy.position_size == 0
    if crossoverState
       strategy.entry('Buy',strategy.long)
       entryPrice := close
       stopPrice := close - stopLoss * sma8[1]
       takeProfitPrice := close + takeProfit * sma8[1]
       stopLossPrice := stopPrice
       stopLossPrice
    if crossunderState
        strategy.entry('Sell', strategy.short)
        entryPrice := close
        stopPrice := close + stopLoss *  sma8[1]
        takeProfitPrice := close - takeProfit *  sma8[1]
        stopLossPrice := stopPrice
        stopLossPrice

if strategy.position_size > 0
    if (close > takeProfitPrice or close < stopLossPrice) and crossunderState
        strategy.close('Buy')
        entryPrice := 0.0
        stopPrice := 0.0
        takeProfitPrice := 0.0
        stopLossPrice := 0.0
        stopLossPrice
    else
        strategy.entry('Buy', strategy.long)
        entryPrice := close
        stopPrice := close - stopLoss *  sma8[1]
        takeProfitPrice := close + takeProfit *  sma8[1]
        stopLossPrice := stopPrice
        stopLossPrice

if strategy.position_size < 0
    if (close > takeProfitPrice or close < stopLossPrice) and crossoverState
        strategy.close('Sell')
        entryPrice := 0.0
        stopPrice := 0.0
        takeProfitPrice := 0.0
        stopLossPrice := 0.0
        stopLossPrice
    else
        strategy.entry('Sell', strategy.short)
        entryPrice := close
        stopPrice := close + stopLoss *  sma8[1]
        takeProfitPrice := close - takeProfit *  sma8[1]
        stopLossPrice := stopPrice
        stopLossPrice

// Plot entry and exit points
plotshape(strategy.position_size > 0 and crossoverSignal, 'Buy Entry', shape.triangleup, location.belowbar, color.new(color.green, 0), size=size.small)
plotshape(strategy.position_size > 0 and (close >= takeProfitPrice or close <= stopLossPrice), 'Buy Exit', shape.triangledown, location.abovebar, color.new(color.red, 0), size=size.small)
plotshape(strategy.position_size < 0 and crossunderSignal, 'Sell Entry', shape.triangledown, location.abovebar, color.new(color.red, 0), size=size.small)
plotshape(strategy.position_size < 0 and (close >= takeProfitPrice or close <= stopLossPrice), 'Sell Exit', shape.triangleup, location.belowbar, color.new(color.green, 0), size=size.small)
```

### Detail

https://www.fmz.com/strategy/428756

### Last Modified

2023-11-03 17:27:45