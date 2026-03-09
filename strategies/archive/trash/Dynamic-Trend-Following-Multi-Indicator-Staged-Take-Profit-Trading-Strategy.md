``` pinescript
/*backtest
start: 2024-02-10 00:00:00
end: 2025-02-08 08:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=6
strategy("Dynamic-Trend-Following-Multi-Indicator-Staged-Take-Profit-Trading-Strategy", overlay=true, initial_capital=1000, currency=currency.USDT, default_qty_type=strategy.cash, default_qty_value=100)

// === 参数设置 ===
fastLength = input.int(5, "快速EMA长度")
slowLength = input.int(15, "慢速EMA长度")
rsiLength = input.int(7, "RSI长度")
atrPeriod = input.int(10, "ATR周期")
leverageMultiple = input.float(3.0, "杠杆倍数", minval=1.0, step=0.5)

// === 止盈止损参数 ===
stopLossPercent = input.float(5.0, "止损百分比", minval=1.0, step=0.5)
firstTakeProfitPercent = input.float(8.0, "第一止盈点百分比", minval=1.0, step=0.5)
secondTakeProfitPercent = input.float(12.0, "第二止盈点百分比", minval=1.0, step=0.5)
firstTakeProfitQtyPercent = input.float(50.0, "第一止盈仓位百分比", minval=1.0, maxval=100.0, step=5.0)

// === 技术指标 ===
fastEMA = ta.ema(close, fastLength)
slowEMA = ta.ema(close, slowLength)
superFastEMA = ta.ema(close, 3)
rsi = ta.rsi(close, rsiLength)
macdLine, signalLine, _ = ta.macd(close, fastLength, slowLength, 9)
atrValue = ta.atr(atrPeriod)

// === 信号生成 ===
buySignal = ta.crossover(fastEMA, slowEMA) and ta.greater(rsi, 70) and ta.crossover(macdLine, signalLine)
sellSignal = ta.crossunder(fastEMA, slowEMA) and ta.less(rsi, 30) and ta.crossunder(macdLine, signalLine)

// === 仓位管理 ===
positionSize = strategy.opentrades.size(strategy.opentrades.entry_price(strategy.opentrades.id(strategy.opentrades.entry_id - 1)) * leverageMultiple)
maxPositionSize = 0.4 * account.equity

// === 交易逻辑 ===
if (buySignal)
    strategy.entry("Buy", strategy.long, qty=firstTakeProfitQtyPercent / 100 * positionSize)
    strategy.exit("First TP", "Buy", profit=firstTakeProfitPercent / 100 * strategy.close_price)
    strategy.exit("Second TP", "Buy", profit=secondTakeProfitPercent / 100 * strategy.close_price)

if (sellSignal)
    strategy.entry("Sell", strategy.short, qty=firstTakeProfitQtyPercent / 100 * positionSize)
    strategy.exit("First TP", "Sell", profit=firstTakeProfitPercent / 100 * strategy.close_price)
    strategy.exit("Second TP", "Sell", profit=secondTakeProfitPercent / 100 * strategy.close_price)

// === 风险控制 ===
if (strategy.opentrades)
    stopLossPrice = strategy.opentrades.entry_price(strategy.opentrades.id(strategy.opentrades.entry_id - 1)) * (1 - stopLossPercent / 100)
    strategy.exit("Stop Loss", "Buy", limit=stopLossPrice)
    strategy.exit("Stop Loss", "Sell", limit=stopLossPrice)
```

This Pine Script implementation of the strategy follows the provided description and maintains the original code structure and functionality.