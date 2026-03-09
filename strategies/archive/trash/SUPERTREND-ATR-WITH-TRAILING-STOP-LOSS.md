```plaintext
Name

SUPERTREND-ATR-WITH-TRAILING-STOP-LOSS

Author

ChaoZhang

Strategy Description

SuperTrend is a moving stop and reversal line based on the volatility (ATR).

The strategy will ride up your stop loss when price moviment 1%.

The strategy will close your operation when the market price crossed the stop loss.

The strategy will close operation when the line based on the volatility will crossed

The strategy has the following parameters:

+ **ATR PERIOD** - To select number of bars back to execute calculation
+ **ATR MULTPLIER** - To add a multplier factor on volatility
+ **INITIAL STOP LOSS** - Where can isert the value to first stop.
+ **POSITION TYPE** - Where can to select trade position.
+ **BACKTEST PERIOD** - To select range.

## DISCLAIMER

1. I am not licensed financial advisors or broker dealers. I do not tell you when or what to buy or sell. I developed this software which enables you execute manual or automated trades multiple trades using TradingView. The software allows you to set the criteria you want for entering and exiting trades.
2. Do not trade with money you cannot afford to lose.
3. I do not guarantee consistent profits or that anyone can make money with no effort. And I am not selling the holy grail.
4. Every system can have winning and losing streaks.
5. Money management plays a large role in the results of your trading. For example: lot size, account size, broker leverage, and broker margin call rules all have an effect on results. Also, your Take Profit and Stop Loss settings for individual pair trades and for overall account equity have a major impact on results. If you are new to trading and do not understand these items, then I recommend you seek education materials to further your knowledge.

**YOU NEED TO FIND AND USE THE TRADING SYSTEM THAT WORKS BEST FOR YOU AND YOUR TRADING TOLERANCE.**

**I HAVE PROVIDED NOTHING MORE THAN A TOOL WITH OPTIONS FOR YOU TO TRADE WITH THIS PROGRAM ON TRADINGVIEW.**

## NOTE

**backtest**
 ![IMG](https://www.fmz.com/upload/asset/1b6e2cd4525c73f55ac.png) 

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|v_input_1|true|═══════════════ FROM ═══════════════|
|v_input_2|true|Month|
|v_input_3|true|Day|
|v_input_4|2019|Year|
|v_input_5|true|════════════════ TO ════════════════|
|v_input_6|31|Month|
|v_input_7|12|Day|
|v_input_8|9999|Year|
|v_input_9|true|═════════════ STRATEGY ═════════════|
|v_input_10|0|Position Type: SHORT|LONG|
|v_input_11|3|Initial Stop Loss|
|v_input_12|true|ATR Period|
|v_input_13|3|ATR multplierFactoriplier|


> Source (PineScript)

```pinescript
//@version=4
//
// ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒