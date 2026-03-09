> Name

VWAP Trend Following Strategy VWAP-Trend-Following-Strategy

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/7a2fbd8f9da14f9223.png)
[trans]
## Overview

This strategy uses VWAP and EMA as indicators to determine the trend direction. It goes long when the price is above both VWAP and EMA200, and goes short when the price is below both VWAP and EMA200. It's a typical trend following strategy.

## Strategy Logic

The core logic of the strategy lies in using VWAP and EMA to judge the price trend.

- VWAP represents the typical price and reflects the average cost of market participants. When the price is above VWAP, it means the buying power increases, so we should go long. When the price is below VWAP, it means the selling power strengthens, so we should go short.
- EMA200 represents the mid-long term trend of the price. When the price is above EMA200, it indicates a bullish mid-long term outlook and suggests going long. When the price is below EMA200, it indicates a bearish mid-long term outlook and suggests going short.

Therefore, this strategy first judges if the price is above both VWAP and EMA200; if yes, then go long; if the price is below both VWAP and EMA200, then go short. We can see that this strategy mainly relies on VWAP and EMA to make trading decisions.

In addition, the strategy also sets take profit and stop loss points. After going long, TP is set to 3.5% of the entry price and SL is set to 1.4% of the entry price. After going short, TP is 2.5% of the entry price and SL is 0.9% of the entry price. This avoids huge losses.

## Advantages

The biggest advantage of this strategy is that using VWAP and EMA to determine trends is very reliable:

- VWAP can accurately reflect the average cost of market participants, making it a very good indicator to judge trends.
- EMA200 can clearly reflect the mid-long term trend and determine the direction of major trends very accurately.

Therefore, combining VWAP and EMA to judge trends is highly reliable. When both indicators give consistent signals, the success rate of trading is very high.

In addition, setting TP/SL avoids excessive losses per trade.

## Risks

The main risk of this strategy is that VWAP and EMA may give wrong signals:

- During violent market fluctuations, the price may deviate from VWAP in the short term and give wrong signals.
- When a new trend just begins, EMA may lag the price change and cause missing the best entry timing.

Also, improper TP/SL settings still pose the risk of excessive losses per trade.

To solve the above issues, we can optimize the parameters of VWAP and EMA to make them better in detecting the beginning of new trends. Also, we can set adaptive TP/SL to adjust them according to price fluctuations.

## Enhancement

The main aspects to enhance this strategy:

- Optimize VWAP parameters to find more stable settings for determining trends.
- Optimize EMA periods to find more accurate settings for judging trends.
- Add other trend indicators like Bollinger Bands, KDJ etc. to combine with VWAP and EMA, to improve accuracy.
- Set adaptive take profit and stop loss based on certain rules to adjust them dynamically according to price fluctuations.
- Incorporate position sizing based on drawdown, consecutive losses etc. to control overall risk.

## Conclusion

In conclusion, this is a very reliable trend following strategy. It uses simple logic of VWAP and EMA to determine trend directions. When both indicators give consistent signals, the success rate is very high. By setting proper TP/SL, the risk can be controlled. There are still many ways (parameter optimization, adding indicators, adaptive TP/SL, position sizing etc.) to further improve this strategy and make its performance even better.

||

## Overview

This strategy uses VWAP and EMA as indicators to determine the trend direction. It goes long when the price is above both VWAP and EMA200, and goes short when the price is below both VWAP and EMA200. It's a typical trend following strategy.

## Strategy Logic

The core logic of the strategy lies in using VWAP and EMA to judge the price trend.

- VWAP represents the typical price and reflects the average cost of market participants. When the price is above VWAP, it means the buying power increases, so we should go long. When the price is below VWAP, it means the selling power strengthens, so we should go short.
- EMA200 represents the mid-long term trend of the price. When the price is above EMA200, it indicates a bullish mid-long term outlook and suggests going long. When the price is below EMA200, it indicates a bearish mid-long term outlook and suggests going short.

Therefore, this strategy first judges if the price is above both VWAP and EMA200; if yes, then go long; if the price is below both VWAP and EMA200, then go short. We can see that this strategy mainly relies on VWAP and EMA to make trading decisions.

In addition, the strategy also sets take profit and stop loss points. After going long, TP is set to 3.5% of the entry price and SL is set to 1.4% of the entry price. After going short, TP is 2.5% of the entry price and SL is 0.9% of the entry price. This avoids huge losses.

## Advantages

The biggest advantage of this strategy is that using VWAP and EMA to determine trends is very reliable:

- VWAP can accurately reflect the average cost of market participants, making it a very good indicator to judge trends.
- EMA200 can clearly reflect the mid-long term trend and determine the direction of major trends very accurately.

Therefore, combining VWAP and EMA to judge trends is highly reliable. When both indicators give consistent signals, the success rate of trading is very high.

In addition, setting TP/SL avoids excessive losses per trade.

## Risks

The main risk of this strategy is that VWAP and EMA may give wrong signals:

- During violent market fluctuations, the price may deviate from VWAP in the short term and give wrong signals.
- When a new trend just begins, EMA may lag the price change and cause missing the best entry timing.

Also, improper TP/SL settings still pose the risk of excessive losses per trade.

To solve the above issues, we can optimize the parameters of VWAP and EMA to make them better in detecting the beginning of new trends. Also, we can set adaptive TP/SL to adjust them according to price fluctuations.

## Enhancement

The main aspects to enhance this strategy:

- Optimize VWAP parameters to find more stable settings for determining trends.
- Optimize EMA periods to find more accurate settings for judging trends.
- Add other trend indicators like Bollinger Bands, KDJ etc. to combine with VWAP and EMA, to improve accuracy.
- Set adaptive take profit and stop loss based on certain rules to adjust them dynamically according to price fluctuations.
- Incorporate position sizing based on drawdown, consecutive losses etc. to control overall risk.

## Conclusion

In conclusion, this is a very reliable trend following strategy. It uses simple logic of VWAP and EMA to determine trend directions. When both indicators give consistent signals, the success rate is very high. By setting proper TP/SL, the risk can be controlled. There are still many ways (parameter optimization, adding indicators, adaptive TP/SL, position sizing etc.) to further improve this strategy and make its performance even better.

||

## Strategy Arguments


| Argument | Default | Description |
| ---- | ---- | ---- |
| v_input_1 | 3.5 | Long Take Profit % |
| v_input_2 | 1.4 | Long Stop Loss % |
| v_input_3 | 2.5 | Short Take Profit % |
| v_input_4 | 0.9 | Short Stop Loss % |
| v_input_5 | 2019 | Backtest Start Year |
| v_input_6 | true | Backtest Start Month |
| v_input_7 | true | Backtest Start Day |
| v_input_8 | 2020 | Backtest Stop Year |
| v_input_9 | 12 | Backtest Stop Month |
| v_input_10 | 31 | Backtest Stop Day |

## Source (PineScript)

```pinescript
/*backtest
start: 2024-01-01 00:00:00
end: 2024-01-31 23:59:59
period: 2h
basePeriod: 15m
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

//26m Binance BTCUSDTPERP
//@version=4
strategy("VWAP Trend Follower", initial_capital=100, overlay=true, commission_type=strategy.commission.percent, commission_value=0.04, default_qty_type = strategy.percent_of_equity, default_qty_value = 90, currency = currency.USD )
```