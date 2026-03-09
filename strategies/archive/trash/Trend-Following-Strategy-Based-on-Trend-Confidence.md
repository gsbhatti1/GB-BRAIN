``` pinescript
/*backtest
start: 2022-11-15 00:00:00
end: 2023-11-21 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © carefulCamel61097

// ################################################################################################

// "This is a trend following strategy that performed very well on the past 5 years"
// "Intended to be used on BTC-USDT, 4hr timeframe"

// "A factor 2 Leverage can be added by changing Order Size to 200% of equity"
// "Higher leverage is not recommended due to big drawdowns"

// "Also seems to work on 1D timeframe, although ideal parameters may be different"
// "Also seems to work on ETH-USDT and some other altcoins, although ideal parameters are different"

// ################################################################################################

//@version=5
strategy("Trend Following based on Trend Confidence", overlay=false )

// Inputs

source      = input(close)

since       = input(timestamp('2000-01-01'), title='Start trading interval')
till        = input(timestamp('2030-01-01'), title='End trading interval')

length      = input(30, title='Length')

longs_on    = input.bool(true, title='Longs')
shorts_on   = input.bool(true, title='Shorts')

// Parameters for best performance 2018 - 2022
// long_entry  = input.float(0.26, step=0.01, title='Long entry threshold')
// long_exit   = input.float(-0.10, step=0.01, title='Long exit threshold')
// short_entry = input.float(-0.24, step=0.01, title='Short entry threshold')
// short_exit  = input.float(-0.04, step=0.01, title='Short exit threshold')

long_entry  = input.float(0.25, step=0.01, title='Long entry threshold')
long_exit   = input.float(-0.1, step=0.01, title='Long exit threshold')
short_entry = input.float(-0.25, step=0.01, title='Short entry threshold')
short_exit  = input.float(-0.05, step=0.01, title='Short exit threshold')

stop_loss   = input.float(10, title='Stop loss (percentage)')

// Strategy logic

var float trend_confidence = na

// Calculate trend confidence
if bar_index > length
    var float k = na
    var float sigma = na
    k := linreg(source, length, 1)[0]
    sigma := ta.stdev(source, length)
    trend_confidence := k / sigma

// Enter long position
if longs_on and trend_confidence > long_entry and strategy.opentrades == 0
    strategy.entry("Long", strategy.long)

// Exit long position
if strategy.position_size > 0 and trend_confidence < long_exit
    strategy.close("Long")

// Enter short position
if shorts_on and trend_confidence < short_entry and strategy.opentrades == 0
    strategy.entry("Short", strategy.short)

// Exit short position
if strategy.position_size < 0 and trend_confidence > short_exit
    strategy.close("Short")

// Stop loss
if strategy.position_size > 0 and source < strategy.position_avg_price * (1 - stop_loss / 100)
    strategy.close("Long")
    
if strategy.position_size < 0 and source > strategy.position_avg_price * (1 + stop_loss / 100)
    strategy.close("Short")
```

```