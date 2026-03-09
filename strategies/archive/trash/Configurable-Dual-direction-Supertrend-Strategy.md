> Name

Configurable Dual-direction Supertrend Strategy

> Author

ChaoZhang

> Strategy Description


This strategy is named “Configurable Dual-direction Supertrend Strategy”. It uses the Supertrend trailing stop mechanism to identify price trends, and allows separate parameter configuration for long and short trades, enabling precise trend following. 

The Supertrend calculation is: using ATR multiplied by a coefficient to build price channels. The upper band is the long stop loss and the lower band is the short stop loss. Price breaking the channel generates trade signals.

The innovation is the independent parameter configuration for long and short:

1. Supertrend parameters like ATR period and coefficient can be set separately.
2. Maximum holding period can also be configured independently to adjust profit targets.
3. Stop loss methods (fixed percentage or ATR trailing) can also be set differently.

This allows only-long, only-short or dual-direction trading to better fit specific market conditions.

The advantages are the intuitive Supertrend mechanism and abundant configurable combinations. But Supertrend alone is prone to breaches and needs confirmation. Parameter optimization is also crucial.

In summary, the configurable dual Supertrend strategy improves trend trading precision, while keeping the core idea simple for practical application.


> Strategy Arguments


|Argument|Default|Description|
|---|---|---|
|v_input_1|false|════════ Test Period ═══════|
|v_input_2|2017|Backtest Start Year|
|v_input_3|true|Backtest Start Month|
|v_input_4|true|Backtest Start Day|
|v_input_5|2019|Backtest Stop Year|
|v_input_6|12|Backtest Stop Month|
|v_input_7|31|Backtest Stop Day|
|v_input_8|false|═════ Super Trend L ═════|
|v_input_9|2|ATR Period|
|v_input_10|1.5|ATR Multiplier|
|v_input_11|false|═════ Super Trend S ═════|
|v_input_12|3|ATR Period|
|v_input_13|1.3|ATR Multiplier|
|v_input_14|false|═════ Rate of Change L ═════|
|v_input_15|30|ROC Length|
|v_input_16|6|ROC % Change|
|v_input_17|false|═════ Rate of Change S ═════|
|v_input_18|76|ROC Length|
|v_input_19|6|ROC % Change|
|v_input_20|false|═══════ Stop Loss L ══════|
|v_input_21|0|Stop Loss Type: Fixed|ATR Derived|
|v_input_22|6|Fixed Stop Loss %|
|v_input_23|20|ATR Stop Period|
|v_input_24|1.5|ATR Stop Multiplier|
|v_input_25|false|═══════ Stop Loss S ══════|
|v_input_26|0|Stop Loss Type: Fixed|ATR Derived|
|v_input_27|6|Fixed Stop Loss %|
|v_input_28|20|ATR Stop Period|
|v_input_29|1.5|ATR Stop Multiplier|
|v_input_30|false|══════ Longs or Shorts ═════|
|v_input_31|true|Use Longs|
|v_input_32|true|Use Shorts|


> Source (PineScript)


```pinescript
/*backtest
start: 2023-01-01 00:00:00
end: 2023-09-12 00:00:00
period: 3h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
args: [["v_input_8",true],["v_input_11",true]]
*/

//@version=4
strategy("Super Trend Daily 2.0 BF ?", overlay=true, precision=2, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100, commission_type=strategy.commission.percent, commission_value=0.075)

/////////////// Time Frame ///////////////
_0 = input(false,  "════════ Test Period ═══════")
testStartYear = input(2017, "Backtest Start Year") 
testStartMonth = input(1, "Backtest Start Month")
testStartDay = input(1, "Backtest Start Day")
testPeriodStart = timestamp(testStartYear,testStartMonth,testStartDay, 0, 0)

testStopYear = input(2019, "Backtest Stop Year")
testStopMonth = input(12, "Backtest Stop Month")
testStopDay = input(31, "Backtest Stop Day")
testPeriodStop = timestamp(testStopYear,testStopMonth,testStopDay, 0, 0)

testPeriod() => true

///////////// Super Trend Long /////////////
_1 = input(false,  "═════ Super Trend L ═════")
lengthl = input(title="ATR Period", type=input.integer, defval=2)
multl = input(title="ATR Multiplier", type=input.float, step=0.1, defval=1.5)

atrl = multl * atr(lengthl)

longStopl = hl2 - atrl
longStopPrevl = nz(longStopl[1], longStopl)
longStopl :=  close[1] > longStopPrevl ? max(longStopl, longStopPrevl) : longStopl

shortStopl = hl2 + atrl
shortStopPrevl = nz(shortStopl[1], shortStopl)
shortStopl := close[1] < shortStopPrevl ? min(shortStopl, shortStopPrevl) : shortStopl

dirl = 1
dirl := nz(dirl[1], dirl)
dirl := dirl == -1 and close > shortStopPrevl ? 1 : dirl == 1 and close < longStopPrevl ? -1 : dirl

///////////// Super Trend Short /////////////
_2 = input(false,  "═════ Super Trend S ═════")
lengths = input(title="ATR Period", type=input.integer, defval=3)
mults = input(title="ATR Multiplier", type=input.float, step=0.1, defval=1.3)

atrs = mults * atr(lengths)

longStops = hl2 - atrs
longStopPrevs = nz(longStops[1], longStops)
longStops :=  close[1] > longStopPrevs ? max(longStops, longStopPrevs) : longStops

shortStops = hl2 + atrs
shortStopPrevs = nz(shortStops[1], shortStops)
shortStops := close[1] < shortStopPrevs ? min(shortStops, shortStopPrevs) : shortStops

dirs = 1
dirs := nz(dirs[1], dirs)
dirs := dirs == -1 and close > shortStopPrevs ? 1 : dirs == 1 and close < longStopPrevs ? -1 : dirs

///////////// Rate Of Change Long ///////////// 
_3 = input(false,  "═════ Rate of Change L ═════")
sourcel = close
roclengthl = input(30, "ROC Length",  minval=1)
pcntChangel = input(6, "ROC % Change", minval=1)
rocl = 100 * (sourcel - sourcel[roclengthl]) / sourcel[roclengthl]
emarocl = ema(rocl, roclengthl / 2)
isMovingl() => emarocl > (pcntChangel / 2) or emarocl < (0