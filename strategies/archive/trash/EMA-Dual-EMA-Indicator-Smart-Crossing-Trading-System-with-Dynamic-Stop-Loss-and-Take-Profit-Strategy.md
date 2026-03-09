``` pinescript
/*backtest
start: 2019-12-23 08:00:00
end: 2024-11-28 00:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//@version=5
strategy("EMA Cross Strategy", overlay=true, initial_capital=10000, default_qty_type=strategy.percent_of_equity, default_qty_value=100)

// 添加策略参数设置
var showLabels = input.bool(true, "显示标签")
var stopLossPercent = input.float(5.0, "止损百分比", minval=0.1, maxval=20.0, step=0.1)
var takeProfitPercent = input.float(10.0, "止盈百分比", minval=0.1, maxval=50.0, step=0.1)

// 计算EMA
ema9 = ta.ema(close, 9)
ema21 = ta.ema(close, 21)

// 绘制EMA线
plot(ema9, "EMA9", color=color.blue, linewidth=2)
plot(ema21, "EMA21", color=color.red, linewidth=2)

// 检测交叉
crossOver = ta.crossover(ema9, ema21)  
crossUnder = ta.crossunder(ema9, ema21)

// 格式化时间显示 (UTC+8)
utc8Time = time + 8 * 60 * 60 * 1000
timeStr = str.format("{0,date,MM-dd HH:mm}", utc8Time)

// 计算止损止盈价格
longStopLoss = strategy.position_avg_price * (1 - stopLossPercent / 100)
longTakeProfit = strategy.position_avg_price * (1 + takeProfitPercent / 100)
shortStopLoss = strategy.position_avg_price * (1 + stopLossPercent / 100)
shortTakeProfit = strategy.position_avg_price * (1 - takeProfitPercent / 100)

// 交易逻辑
if crossOver
    if strategy.position_size < 0  // 如果持有空仓
        strategy.close("Short", when=not na(shortStopLoss))
        strategy.entry("Long", strategy.long, comment="Buy Signal")
        
if crossUnder
    if strategy.position_size > 0  // 如果持有长仓
        strategy.close("Long", when=not na(longStopLoss))
        strategy.entry("Short", strategy.short, comment="Sell Signal")
```

This Pine Script represents the trading strategy using EMA crossovers with dynamic stop-loss and take-profit levels. The code ensures that when the 9-period EMA crosses above the 21-period EMA, it identifies a buy signal, and when it crosses below, it identifies a sell signal. The stop-loss and take-profit levels are dynamically adjusted based on the percentage inputs provided.