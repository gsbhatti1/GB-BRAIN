> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_string_1|Geometric (% Fall)|(?GRID)Width Type|
|v_input_float_1|75|Width Parameter|
|v_input_string_2|4W|Pivot Point Resolution|
|v_input_timeframe_1|D|EMA Resolution|
|v_input_int_1|100|MA Length|
|v_input_string_3|Cash / n Buys|(?BUY)Buy Type|
|v_input_float_2|10|Contracts / Cash / % Cash|
|v_input_int_2|4|N Buys over MA|
|v_input_int_3|5|N Buys under MA (Max.)|
|v_input_int_4|2|Buy all in last Trades|
|v_input_string_4|Position / n Sells +|(?SELL)Sell Type|
|v_input_float_3|5|Contracts / Cash / % Position|
|v_input_int_5|20|N Sells over MA (Max.)|
|v_input_int_6|4|N Sells under MA|
|v_input_string_5|Never|Loss Allowed|
|v_input_string_6|Spot|(?TRADING)Trading Type|
|v_input_float_4|10|% Initial Capital 1st Trade|
|v_input_float_5|0.1|% Commission Value|
|v_input_float_6|true|% Margin Rate|
|v_input_1|StartDate|Start of Trading|
|v_input_string_7|Small|(?PLOTTING)Table Size|
|v_input_2|true|Level Grid|
|v_input_3|false|Information Panel|
|v_input_4|false|Liquidation Price|


> Source (PineScript)

```pinescript
//@version=5
indicator("Assassins-Grid-B-A-Dynamic-Grid-Trading-Strategy", shorttitle="Dynamic Grid Trading Strategy", overlay=true)

// Define input parameters
widthType = input.string("Geometric (% Fall)", title="?GRID Width Type")
widthParam = input.float(75, title="Width Parameter")
pivotResolution = input.string("4W", title="?Pivot Point Resolution")
emaRes = input.timeframe("D", title="?EMA Resolution")
maLen = input.int(100, title="?MA Length")
buyType = input.string("Cash / n Buys", title="?BUY Buy Type")
contractsCash = input.float(10, title="Contracts / Cash / % Cash")
nbBuysAboveMa = input.int(4, title="N Buys over MA")
maxBuysBelowMa = input.int(5, title="N Buys under MA (Max.)")
buyAllLastTrades = input.int(2, title="Buy all in last Trades")
sellType = input.string("Position / n Sells +", title="?SELL Sell Type")
contractsPosition = input.float(5, title="Contracts / Cash / % Position")
nbSellsAboveMa = input.int(20, title="N Sells over MA (Max.)")
nbSellsBelowMa = input.int(4, title="N Sells under MA")
lossAllowed = input.string("Never", title="?LOSS Allowed")
tradingType = input.string("Spot", title="?TRADING Trading Type")
initialCap1stTrade = input.float(10, title="% Initial Capital 1st Trade")
commissionValue = input.float(0.1, title="% Commission Value")
marginRate = input.float(true, title="% Margin Rate")
startDate = input.time("2023-02-19 00:00:00", title="Start of Trading")
plotSize = input.string("Small", title="?PLOTTING Table Size")
showGridLevel = input.bool(true, title="Level Grid")
infoPanel = input.bool(false, title="Information Panel")
liquidationPrice = input.bool(false, title="Liquidation Price")

// Backtest start and end dates
var startDateBacktest = timestamp("2023-02-19 00:00:00")
var endDateBacktest = timestamp("2024-02-01 05:20:00")

// Define strategy parameters
var width = na
if (widthType == "Geometric (% Fall)")
    width := close * (1 - widthParam / 100)
else if (widthType == "Arithmetic")
    width := close + (close * widthParam / 100)

ema = ta.ema(close, emaRes)

var maValues = array.new_float(maLen)
maValue = na
if bar_index > maLen - 2
    for i = 0 to array.size(maValues) - 1
        array.set(maValues, i, close[bar_index - i])
    maValue := ta.sma(array.toArray(maValues), 1)

buysAboveMa = na
buysBelowMa = na

if maValue > ema
    buysAboveMa := nbBuysAboveMa
else
    buysBelowMa := maxBuysBelowMa

// Buy logic
if (showGridLevel)
    levelGrid = plot(width, color=color.new(color.gray, 0), title="Grid Levels")

if (bar_index % maLen == 0 and bar_index > 0)
    if (high[1] < close or low[1] > close) // Check for grid entry
        buyCondition = true
    else
        buyCondition = false

    if (buyType == "Cash / n Buys")
        if (buyCondition)
            strategy.entry("Buy", strategy.long, comment="Entering Buy Order")
    else if (buyType == "Position / n Sells +")
        if (buyCondition and maValue > ema)
            strategy.entry("Sell", strategy.short, comment="Entering Sell Order")

// Sell logic
sellCondition = na

if (bar_index % maLen == 0 and bar_index > 0)
    sellCondition := true

if (sellType == "Position / n Sells +")
    if (sellCondition and maValue < ema)
        strategy.close("Buy", comment="Closing Buy Order")

// Plot table size
plotTableSize = plot(0, title="Plot Table Size", style=plot.style_linebr)
plot_table_size = plot(table.new(position.top_right, 1, 2, bgcolor=color.white), "Table")
table.cell(plot_table_size, 0, 0, text=plotSize)

// Other settings
if (infoPanel)
    label.new(x=bar_index - 50, y=yaxis.max + 10, text="Info Panel: On", color=color.green, style=label.style_label_down)
else
    label.new(x=bar_index - 50, y=yaxis.max + 10, text="Info Panel: Off", color=color.red, style=label.style_label_down)

if (liquidationPrice)
    label.new(x=bar_index - 50, y=yaxis.min - 10, text="Liquidation Price: On", color=color.green, style=label.style_label_down)
else
    label.new(x=bar_index - 50, y=yaxis.min - 10, text="Liquidation Price: Off", color=color.red, style=label.style_label_down)

// Backtest and live trading setup
if time >= startDateBacktest and time < endDateBacktest
    strategy.backtest()
else if time >= startDate and time < time[1]
    strategy.entry("Buy", strategy.long)
    strategy.close("Buy")

```

This Pine Script implements the dynamic grid trading strategy as described, with configurable parameters for width type, buy/sell conditions, and trading settings.