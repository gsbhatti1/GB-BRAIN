``` pinescript
/*backtest
start: 2022-04-24 00:00:00
end: 2022-05-23 23:59:00
period: 30m
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=4
//@author=Daveatt

StrategyName = "BEST Engulfing + MA"
ShortStrategyName = "BEST Engulfing + MA"

strategy(title=StrategyName, shorttitle=ShortStrategyName, overlay=true, 
 pyramiding=2, default_qty_value=500, precision=7, currency=currency.USD,
 commission_value=0.2,commission_type=strategy.commission.percent, initial_capital=10000)

includeEngulfing = true

includeMA = true
source_ma = input(title="Source Price vs MA", type=input.source, defval=close)
typeofMA = input(title="Type of MA", defval="SMA", options=["RMA", "SMA", "EMA", "WMA", "VWMA", "SMMA", "KMA", "TMA", "HullMA", "DEMA", "TEMA"])
length_ma = input(32, title = "MA Length", type=input.integer)

// ---------- Candle components and states
GreenCandle = close > open
RedCandle = close < open
NoBody = close==open
Body = abs(close-open)


// bullish conditions
isBullishEngulfing1 = max(close[1],open[1]) < max(close,open) and min(close[1],open[1]) > min(close,open) and Body > Body[1] and GreenCandle and RedCandle[1]
isBullishEngulfing2 = max(close[1],open[1]) < max(close,open) and min(close[1],open[1]) <= min(close,open) and Body > Body[1] and GreenCandle and RedCandle[1]

// bearish conditions
isBearishEngulfing1 = max(close[1],open[1]) < max(close,open) and min(close[1],open[1]) > min(close,open) and Body > Body[1] and RedCandle and GreenCandle[1]
isBearishEngulfing2 = max(close[1],open[1]) >= max(close,open) and min(close[1],open[1]) > min(close,open) and Body > Body[1] and RedCandle and GreenCandle[1]

// consolidation of conditions
isBullishEngulfing = isBullishEngulfing1 or isBullishEngulfing2
isBearishEngulfing = isBearishEngulfing1 or isBearishEngulfing2

//isBullishEngulfing = max(close[1],open[1]) < max(close,open) and min(close[1],open[1]) > min(close,open) and Body > Body[1] and GreenCandle and RedCandle[1]
//isBearishEngulfing = max(close[1],open[1]) < max(close,open) and min(close[1],open[1]) > min(close,open) and Body > Body[1] and RedCandle and GreenCandle[1]

Engulf_curr = 0 - barssince(isBearishEngulfing) + barssince(isBullishEngulfing)
Engulf_Buy = Engulf_curr < 0 ? 1 : 0
Engulf_Sell = Engulf_curr > 0 ? 1 : 0


// Price vs MA

smma(src, len) =>
    smma = 0.0
    smma := na(smma[1]) ? sma(src, len) : (smma[1] * (len - 1) + src) / len
    smma

ma(smoothing, src, length) => 
    if smoothing == "RMA"
        rma(src, length)
    else
        if smoothing == "SMA"
            sma(src, length)
        else 
            if smoothing == "EMA"
                ema(src, length)
            else 
                if smoothing == "WMA"
                    wma(src, length)
                else
                    if smoothing == "VWMA"
                        vwma(src, length)
                    else
                        if smoothing == "SMMA"
                            smma(src, length)
                        else
                            if smoothing == "HullMA"
                                wma(2 * wma(src, length / 2) - wma(src, length), round(sqrt(length)))
                            else
                                if smoothing == "LSMA"
                                    src
                                else
                                    if smoothing == "KMA"
                                        xPrice = src
                                        xvnoise = abs(xPrice - xPrice[1])
                                        nfastend = 0.666
                                        nslowend = 0.0645
                                        nsignal = abs(xPrice - xPrice[length])
                                        nnoise = sum(xvnoise, length)
                                        nefratio = iff(nnoise != 0, nsignal / nnoise, 0)
                                        nsmooth = pow(nefratio * (nfastend - nslowend) + nslowend, 2) 
                                        nAMA = 0.0
                                        nAMA :=

```