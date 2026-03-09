> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|1.15|Total Stop Loss|
|v_input_2|1.05|Enter Second trade @ what higher 5%?|
|v_input_3|0.95|First Trade Profit % Target|
|v_input_4|0.9|Second Trade Profit % Target|


> Source (PineScript)

```pinescript
/*backtest
start: 2023-11-23 00:00:00
end: 2023-11-28 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//              @version=4
strategy("Dual-Entry Position Averaging Trailing Stop Loss Strategy", "DE-PATSLS", 1, initial_capital=0)


//              DUAL ENTRIES
//              ADDS ON MORE SHARES IF THE PILOT TRADE DOES NOT REACH PROFIT TARGET
//              RED     LINE        == STOP LOSS LINE
//              GREEN   LINE        == FIRST TRADE PROFIT TARGET
//              YELLOW  LINE        == SECOND ENTRY AT 5% HIGHER THAN FIRST ENTRY PRICE
//              WHITE   LINE        == COMBINED PROFIT TARGET FOR BOTH TRADING LEGS


StopLossPerc        = input(1.15, "Total Stop Loss", step=0.01)


T2EntTrgPerc        = input(1.05, "Enter Second trade @ what higher 5%?", step=0.01)    //  BUY STOP LIMIT ONLY WHEN ONE TRADE IS ALREADY OPEN & AIMS TO BUY DOUBLE THE OWNED SHARES AT A HIGHER ENTRY PRICE // YELLOW LINE

T1ProfTrgPerc       = input(0.95, "First Trade Profit % Target", step=0.01)
T2ProfTrgPerc       = input(0.90, "Second Trade Profit % Target", step=0.01)


//              INITIALIZATION
var float pilotEntryPrice = na
var float pilotStopLossLevel = na
var bool firstTradeOpen = false
var float totalAverageEntryPrice = 0


//              ENTRY LOGIC FOR THE FIRST TRADE
if (time >= timestamp("2023-11-23", "HHmm") and time < timestamp("2023-11-24", "HHmm"))
    if close <= sma(close, 200)
        pilotEntryPrice := open
        firstTradeOpen := true
        strategy.entry("First Trade", strategy.long)


//              UPDATE STOP LOSS FOR THE FIRST TRADE
pilotStopLossLevel := max(pilotEntryPrice * (1 - StopLossPerc), low[1])


//              ENTRY LOGIC FOR THE SECOND TRADE
if firstTradeOpen and close > pilotEntryPrice * T2EntTrgPerc
    totalAverageEntryPrice := (totalAverageEntryPrice + open) / 2
    strategy.entry("Second Trade", strategy.long, comment="Adding positions at 5% higher entry price")


//              PROFIT TARGETS FOR THE FIRST AND SECOND TRADES
if firstTradeOpen and close > pilotEntryPrice * T1ProfTrgPerc
    strategy.exit("First Trade Exit", "First Trade", profit_percent=T1ProfTrgPerc, comment="Taking profit on the first trade")

if totalAverageEntryPrice != 0 and close > totalAverageEntryPrice * T2ProfTrgPerc
    strategy.exit("Second Trade Exit", "Second Trade", profit_percent=T2ProfTrgPerc, comment="Taking profit on the second trade")


//              DRAWINGS
plot(pilotStopLossLevel, color=color.red)
plot(sma(close, 200), color=color.green, title="First Trade Profit Target")
plot(open * T2EntTrgPerc, color=color.yellow, title="Second Entry at 5% Higher Price")
plot(totalAverageEntryPrice * (1 + max(T1ProfTrgPerc, T2ProfTrgPerc)), color=color.white, title="Combined Profit Target for Both Trades")
```

This Pine Script implements the described strategy with the necessary logic and visualizations.