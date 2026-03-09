``` pinescript
/*backtest
start: 2024-01-29 00:00:00
end: 2024-02-28 00:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// © Julien_Eche

//@version=5
strategy("MA ADX Strategy", overlay=true, default_qty_type=strategy.percent_of_equity)

start_date = input(timestamp("1975-01-01T00:00:00"), title="Start Date")
end_date = input(timestamp("2099-01-01T00:00:00"), title="End Date")

// Indicator Inputs
group1 = "MA Parameters"
lengthMA = input.int(50, title="MA Length", minval=1, group=group1)
sourceMA = input(close, title="MA Source", group=group1)

group2 = "ADX Parameters"
diLength = input.int(14, title="DI Length", minval=1, group=group2)
adxSmoothing = input.int(14, title="ADX Smoothing", minval=1, maxval=50, group=group2)
adxMAActive = input.int(15, title="ADX MA Active", minval=1, group=group2)

// Directional Movement calculations
upwardMovement = ta.change(high)
downwardMovement = -ta.change(low)
trueRangeSmoothed = ta.rma(ta.atr(diLength), diLength)
positiveDM = fixnan(100 * ta.rma(upwardMovement > downwardMovement and upwardMovement > 0 ? upwardMovement : 0, diLength) / trueRangeSmoothed)
negativeDM = fixnan(100 * ta.rma(downwardMovement > upwardMovement and downwardMovement > 0 ? downwardMovement : 0, diLength) / trueRangeSmoothed)
dmSum = positiveDM + negativeDM 

// Average Directional Index (ADX) calculation
averageDX = 100 * ta.rma(math.abs(positiveDM - negativeDM) / math.max(dmSum, 1), adxSmoothing)

// Line color determination
lineColor = averageDX > adxMAActive and positiveDM > negativeDM ? na : green

// Plotting MA
plot(close, title="Close Price", color=color.blue)
ma = ta.wma(sourceMA, lengthMA)
plot(ma, title="Weighted Moving Average (WMA)", color=lineColor)

// Plotting ADX
plot(averageDX, title="Average Directional Index (ADX)", color=blue)

// Trading logic
if (ta.vwap(start_date) > ma and averageDX > adxMAActive)
    strategy.entry("Long", strategy.long)
    
if (averageDX < adxMAActive)
    strategy.close("Long")

```

This Pine Script code defines the "MA ADX Strategy" as described in the provided Chinese document. The script calculates the Weighted Moving Average (WMA) and the Average Directional Index (ADX), and uses these to generate trading signals for entering and exiting positions based on the defined parameters.