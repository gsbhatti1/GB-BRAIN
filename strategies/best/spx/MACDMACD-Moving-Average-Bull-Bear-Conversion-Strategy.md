```pinescript
/*backtest
start: 2022-12-01 00:00:00
end: 2023-12-07 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=3
strategy("macd_strategy", 
          shorttitle="macd", 
          overlay=true, 
          pyramiding=1, 
          max_bars_back=5000, 
          calc_on_order_fills = false, 
          calc_on_every_tick=true, 
          default_qty_type=strategy.percent_of_equity, 
          default_qty_value=100, 
          commission_type =strategy.commission.percentage,
          initial_capital=10000, 
          marginPercent=5, 
          currency="USD")

// MACD Calculation
src = close
fastLength = 12
slowLength = 26
signalSmoothing = 9

[trans]

## MACD Calculation

```pinescript
macdLine, signalLine, hist = macd(src, fastLength, slowLength, signalSmoothing)
```

## Long and Short Conditions

```pinescript
// Long Condition
if (crossabove(macdLine, signalLine))
    strategy.entry("Long", strategy.long)

// Short Condition
if (crossbelow(macdLine, signalLine))
    strategy.entry("Short", strategy.short)
```

## EMA Filter

```pinescript
emaLength = 200
emaPrice = ema(close, emaLength)

// Long Condition with EMA Filter
if (crossabove(macdLine, signalLine) and close < emaPrice[1])
    strategy.entry("Long", strategy.long)

// Short Condition with EMA Filter
if (crossbelow(macdLine, signalLine) and close > emaPrice[1])
    strategy.exit("Short Exit", "Long")
```

## Risk Management

```pinescript
strategy.close_on_gap = true

// Stop Loss and Take Profit
stopLossPercent = 0.5
takeProfitPercent = 2

if (isLong)
    stopLossLevel = strategy.position_avg_price * (1 - stopLossPercent / 100)
    takeProfitLevel = strategy.position_avg_price * (1 + takeProfitPercent / 100)

    if (close < stopLossLevel or close > takeProfitLevel)
        strategy.close("Stop Loss/Take Profit")
```

## Summary

The MACD Moving Average Bull Bear Conversion Strategy identifies market trend reversals using DIFF and DEA crossovers, with EMA filters to avoid false signals. This approach allows for quick determination of market trend changes suitable for both short-term and mid-term trading. The strategy incorporates basic risk management measures such as stop loss and take profit levels.

[/trans]
```