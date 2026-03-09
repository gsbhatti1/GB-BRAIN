``` pinescript
/*backtest
start: 2024-05-01 00:00:00
end: 2024-05-31 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy('Supertrend Strategy', overlay=true, format=format.price, precision=2)
Periods = input.int(title='ATR Period', defval=10)
src = input.source(hl2, title='Source High-Low')
multiplier = input.float(3.0, title='ATR Multiplier')
factor = input.int(3, title='Factor')

up = ta.sma(src, Periods) + multiplier * ta.atr(Periods)
dn = ta.sma(src, Periods) - multiplier * ta.atr(Periods)

trend = na(trend[1]) ? 1 : trend[1] == -1 and close > dn ? 1 : trend[1] == 1 and close < up ? -1 : trend[1]
buySignal = trend == -1 and trend[1] == 1
sellSignal = trend == 1 and trend[1] == -1

plotshape(series=buySignal, title='Buy Signal', location=location.belowbar, color=color.green, style=shape.labelup, text='Buy')
plotshape(series=sellSignal, title='Sell Signal', location=location.abovebar, color=color.red, style=shape.labeldown, text='Sell')

if (buySignal)
    strategy.entry('Long', strategy.long, stop=dn)
    strategy.exit('Take Profit', 'Long', limit=up)
    
if (sellSignal)
    strategy.entry('Short', strategy.short, stop=up)
    strategy.exit('Take Profit', 'Short', limit=dn)
    
trailVal = input.int(50, title='Trailing Value')
trailStop = na
if (trend == 1 and strategy.opentrades)
    trailStop := strategy.opentrades.entry_price(strategy.opentrades.id(0)) + trailVal * (up - dn)
    strategy.exit('Trailing Stop', 'Long', stop=trailStop)
    
if (trend == -1 and strategy.opentrades)
    trailStop := strategy.opentrades.entry_price(strategy.opentrades.id(0)) - trailVal * (up - dn)
    strategy.exit('Trailing Stop', 'Short', stop=trailStop)
```

This Pine Script defines the dynamic trend following strategy using the Supertrend indicator. It calculates the Supertrend upper and lower bands, generates buy and sell signals, and implements dynamic stop-loss and trailing stop-loss features. The strategy is designed to be adaptable and includes clear signals for trading.