> Name

bybit-swap Perpetual Position Reinforcement Strategy

> Author

gulishiduan_高频排序

> Strategy Description

//Recently, some friends have reported a minor bug; hence, we are going to test it on the test network first. The parameters can be adjusted as needed. Essentially, this strategy tracks the offset price of candlesticks to determine long or short positions. Simply put, it identifies signals through the turning points of moving averages and conducts real-time detection.

//Register a new account? Use my referral link: https://www.bytick.com/zh-CN/register/?affiliate_id=7586&language=en&group_id=0&group_type=2
//This link provides access to multiple strategies. 

//Basic principle: Continuously add positions as long as the candlesticks are continuously rising until reaching maximum position.

//If long: not suitable for a bear market, but it won’t continuously increase long positions during a decline.
//If short: not suitable for a bull market, but it won’t continuously add positions during an ascent.

//Note that both long and short positions can be opened in separate accounts.

//For inquiries about other strategies, please contact us via WeChat: ying5737
//You need to connect your own exchange. Start by testing with a demo account. You bear the risks on your own.

//On the daily or weekly level, we use the daily for this example,
//Detect ma5 and ma10; if the candlestick closing price is above both moving averages (MA) and MA5 is rising (judged based on yesterday's closing price being greater than five days ago), place an order at opening time or buy 500u directly every day. As long as it continues to rise, keep adding positions.
//For position reinforcement: If two consecutive bearish candlesticks appear during the ascent, add 500u on the third day. Each pair of consecutive bearish candles is counted separately.

//Sell if there are three consecutive bullish candlesticks and reduce by 1000u (or four consecutive bulls for a reduction of 2000u).
//This cycle continues.
//The strategy runs for 13 days (or 21 days) before automatically stopping, closing positions or orders.

//Maximum position is capped at 5000u; if the current position exceeds this limit, no additional additions are made.

![Image](https://wx1.sinaimg.cn/mw1024/c5775633ly1gbsjvtrgnhj20m80dmmxy.jpg)
![Image](https://wx1.sinaimg.cn/mw1024/c5775633ly1gbsjvty48uj21hc0u077o.jpg)
![Image](https://wx2.sinaimg.cn/mw1024/c5775633ly1gbsjvu4iipj20lr0h775f.jpg)

# Mid-frequency Unidirectional Trend Strategy
## Monitoring Variables
1. Fast MA
2. Slow MA
3. Closing Price

## Configuration Parameters
1. Single-order Volume: Amount
2. Close Position Volume: CloseAmount
3. Maximum Holding Position: MaxPosition

### Going Long
#### Necessary Conditions
1. The closing price of the candlesticks is greater than both the fast and slow MAs.
2. Fast MA is rising (judged based on yesterday's closing price being greater than five days ago).

#### Orders
1. If there are three consecutive bullish candles, reduce by CloseAmount.
2. If two consecutive bearish candles appear during an ascent, add Amount. That means if two consecutive bearish candles occur, place 2*Amount orders.
3. Under normal conditions, open with a single order of Amount.

#### Restrictions
1. Do not open positions if the maximum holding exceeds MaxPosition.

### Exit Conditions
1. After running for N candlesticks, exit automatically.

## Going Short
#### Necessary Conditions
1. The closing price of the candlesticks is less than both the fast and slow MAs.
2. Fast MA is falling (judged based on yesterday's closing price being lower than five days ago).

#### Orders
1. If there are three consecutive bearish candles, reduce by CloseAmount.
2. If two consecutive bullish candles appear during a decline, add Amount. That means if two consecutive bullish candles occur, place 2*Amount orders.
3. Under normal conditions, open with a single order of Amount.

#### Restrictions
1. Do not open positions if the maximum holding exceeds MaxPosition.

### Exit Conditions
1. After running for N candlesticks, exit automatically.

## Notes
1. The program retrieves account position information to set the strategy's holdings.
2. Please bind your fmz WeChat for important push notifications from the program.

## Parameters
1. Fast MA Period
2. Slow MA Period
3. Polling Interval (ms)
4. Long or Short Position Selection
5. Leverage: 0 indicates full margin mode
6. Contract Type: Currently, only supports swap on Fmex; set to 'swap' for backtesting with OKEx and use options like 'this_week', 'this_month', etc.
7. Close Volume: The volume reduced when the reduction condition is met.
8. Maximum Position (u)
9. API Base URL. Can be set to https://api.fmex.com or testnet at https://api.testnet.fmex.com
10. Strategy Exit after N Candlesticks. The strategy will exit normally after running for a certain number of candlesticks.
11. Whether to fully close positions on active exit.
12. Whether interaction is required: if the program meets the exit conditions, it will wait for human intervention or commands; otherwise, it exits immediately.
13. Whether to use market orders: check this box to place market orders; otherwise, limit orders are used with bids placed at level 1 and asks at level 1.
14. Number of consecutive bullish candles (for long positions). This is a signal for reducing positions, such as reducing when multiple consecutive bullish candles appear during the ascent phase.
15. Number of consecutive bearish candles (for long positions). This is the number of consecutive bearish candles.
16. Whether to identify it as an oscillation market: check this box if it is an oscillation.

## Interactions
**Interactions are only available when 'interaction required' is enabled**
**Interaction occurs during normal exit of the strategy**

1. Continue: Reset and re-run with the same parameters.
2. Stop: The program will stop and exit.
3. Continue after changing market conditions: This is an extension of interaction 1, allowing for running in different market modes (oscillation or trend) post-change.

```
////////////////// params ////////////////////////
//var fastMaPeriod = 5
//var slowMaPeriod = 10
//var direction = 'long' | 'short'
//var interval = 1000
//var amount = 500
//var maxHoldAmount = 5000
//var closeAmount = 1000
//var runNBars = 13
//var marginLevel = 0
//var contractType = 'swap'
//var enableCommand = false
//var isTaker = true
//var maxOppositeDirKNum = 2
//var maxSameDirKNum = 3
//var isShock = false
////////////////// variable ////////////////////////
var makeLong = direction == 'long' ? true : false;
var startTime = null;
var holdAmount = 0;
var lastBar = null;
var yinxianCnt = 0;
var yangxianCnt = 0;
var lastClose = 0;
var last5thClose = 0;
var fastMa = [];
var slowMa = [];
var barCnt = 0;
var localIsShock = false;

////////////////////////////////////////////////
var PreBarTime = 0;
var isFirst = true;

function PlotMA_Kline(records) {
    $.PlotRecords(records, 'K');
    
    if (fastMa.length == 0) {
        fastMa = TA.MA(records, fastMaPeriod);
    }
    if (slowMa.length == 0) {
        slowMa = TA.MA(records, slowMaPeriod);
    }

    if (isFirst) {
        $.PlotFlag(records[records.length - 1].Time, 'Start', 'STR');
        
        for (var i = records.length - 1; i >= 0; i--) {
            if (fastMa[i] !== null) {
                $.PlotLine('ma' + fastMaPeriod, fastMa[i], records[i].Time);
            }
            
            if (slowMa[i] !== null) {
                $.PlotLine('ma' + slowMaPeriod, slowMa[i], records[i].Time);
            }
        }
        
        PreBarTime = records[records.length - 1].Time;
        isFirst = false;
    } else {
        if (PreBarTime !== records[records.length - 1].Time) {
            $.PlotLine('ma' + fastMaPeriod, fastMa[fastMa.length - 2], records[fastMa.length - 2].Time);
            $.PlotLine('ma' + slowMaPeriod, slowMa[slowMa.length - 2], records[slowMa.length - 2].Time);
            
            PreBarTime = records[records.length - 1].T;
        }
    }
}
``` 

This translation retains the essential details of the original description and code while ensuring clarity in English. The example images are referenced as URLs, which should be replaced with actual image content when implemented in a trading platform or strategy editor. If you need further customization or specific implementation guidance for these strategies, please let me know!