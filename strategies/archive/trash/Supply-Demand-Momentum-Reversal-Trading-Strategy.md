``` pinescript
/*backtest
start: 2023-12-01 00:00:00
end: 2023-12-20 23:59:59
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("Supply and Demand Zones with EMA and Trailing Stop", shorttitle="SD Zones", overlay=true)

showBuySignals = input(true, title="Show Buy Signals", group="Signals")
showSellSignals = input(true, title="Show Sell Signals", group="Signals")
showHLZone = input(true, title="Show HL Zone", group="Zones")
showLHZone = input(true, title="Show LH Zone", group="Zones")
showHHZone = input(true, title="Show HH Zone", group="Zones")
showLLZone = input(true, title="Show LL Zone", group="Zones")

emaLength = input(200, title="EMA Length", group="EMA Settings")
atrLength = input(14, title="ATR Length", group="Trailing Stop")
atrMultiplier = input(2, title="ATR Multiplier", group="Trailing Stop")

// Function to identify supply and demand zones
getSupplyDemandZones(kline) =>
    hh = na
    ll = na
    for i = 1 to array.size(kline) - 1
        if (array.get(kline, i).high > array.get(kline, i - 1).high and 
            array.get(kline, i + 1).high < array.get(kline, i).high)
            hh := kline[i].high
            
        if (array.get(kline, i).low < array.get(kline, i - 1).low and 
            array.get(kline, i + 1).low > array.get(kline, i).low)  
            ll := kline[i].low
        
    hh, ll

// EMA Calculation
ema = ta.ema(close, emaLength)

// ATR Calculation
atrValue = ta.atr(atrLength)
stopLossLevel = atrValue * atrMultiplier

// Determine Entry and Exit Conditions
var float entryPrice = na
var int signal = 0

if (barstate.islast)
    if (signal == 0) 
        hlZone, llZone = getSupplyDemandZones(candledata)
        
        if (close > hlZone and prevClose <= prevhlZone)
            strategy.entry("Buy", strategy.long)
            entryPrice := close
            signal := 1
        
        if (close < llZone and prevClose >= prevllZone) 
            strategy.entry("Sell", strategy.short)
            entryPrice := close
            signal := -1
    
    if (signal == 1 and close <= stopLossLevel or close < prevhlZone)
        strategy.exit("Buy Exit", "Buy")
    
    if (signal == -1 and close >= stopLossLevel or close > prevllZone) 
        strategy.exit("Sell Exit", "Sell")

// Plotting
plot(series=ema, title="EMA", color=color.blue, linewidth=2)
plot(series=(hlZone), title="HL Zone", color=color.red, style=plot.style_linebr)
plot(series=(llZone), title="LL Zone", color=color.green, style=plot.style_linebr)

// Indicators
hline(hlZone, "HL Zone Level", na, color=color.red)
hline(llZone, "LL Zone Level", na, color=color.green)

```
```