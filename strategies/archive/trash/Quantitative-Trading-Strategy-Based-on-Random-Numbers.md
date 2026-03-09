> Name

Quantitative Trading Strategy Based on Random Numbers

> Author

ChaoZhang

> Strategy Description

![IMG](https://www.fmz.com/upload/asset/ae1d8e408827795469.png)
[trans]

## Overview

The core idea of this strategy is to simulate probability events such as coin flipping and dice rolling using random numbers to determine long or short positions, thus implementing random trading. This kind of trading strategy can be used for simulation testing and also as a basic framework for more complex strategy development.

## Strategy Principle

1. Use the `flip` variable to simulate random events and determine long or short based on the `coinLabel` random number size.

2. Use `risk` and `ratio` to set stop loss and take profit lines.

3. Trigger the next trading signal randomly according to the set maximum cycle number.

4. Control whether to display the close position box through the `plotBox` variable.

5. `stoppedOut` and `takeProfit` variables are used to detect stop loss or take profit.

6. Provide backtesting capabilities to test strategy performance.

## Advantage Analysis

1. The code structure is clear and easy to understand and can be easily redeveloped.

2. The UI interaction is friendly, and various parameters can be adjusted through the graphical interface.

3. The randomness is strong and is not affected by market fluctuations, with high reliability.

4. Better returns can be obtained through parameter optimization.

5. Can be used as a demonstration or test for other strategies.

## Risk Analysis

1. Random trading cannot judge the market and there is a certain profit risk.

2. Unable to determine the optimal parameter combination, repeated testing is required.

3. There is a risk of super correlation that may result from overly dense random signals.

4. It is recommended to use stop loss and take profit mechanisms to control risks.

5. Risks can be reduced by appropriately extending the trading interval.

## Optimization Directions

1. Incorporate more complex factors to generate random signals.

2. Increase trading varieties to expand test scope.

3. Optimize UI interaction and increase strategy control capabilities.

4. Provide more test tools and indicators for parameter optimization.

5. Can be used as a trading signal or stop loss take profit component added to other strategies.

## Summary

The overall framework of this strategy is complete, generating trading signals based on random events, with high reliability. At the same time, it provides parameter adjustment, backtesting, and charting capabilities. It can be used to test novice strategy development, and also as a basic module for other strategies. Through appropriate optimization, the strategy performance can be further improved.

||

## Overview

The core idea of this strategy is to simulate probability events such as coin flipping and dice rolling using random numbers to determine long or short positions, thus implementing random trading. This kind of trading strategy can be used for simulation testing and also as a basic framework for more complex strategy development.

## Strategy Principle

1. Use the `flip` variable to simulate random events and determine long or short based on the `coinLabel` random number size.

2. Use `risk` and `ratio` to set stop loss and take profit lines.

3. Trigger the next trading signal randomly according to the set maximum cycle number.

4. Control whether to display the close position box through the `plotBox` variable.

5. `stoppedOut` and `takeProfit` variables are used to detect stop loss or take profit.

6. Provide backtesting capabilities to test strategy performance.

## Advantage Analysis

1. The code structure is clear and easy to understand and can be easily redeveloped.

2. The UI interaction is friendly, and various parameters can be adjusted through the graphical interface.

3. The randomness is strong and is not affected by market fluctuations, with high reliability.

4. Better returns can be obtained through parameter optimization.

5. Can be used as a demonstration or test for other strategies.

## Risk Analysis

1. Random trading cannot judge the market and there is a certain profit risk.

2. Unable to determine the optimal parameter combination, repeated testing is required.

3. There is a risk of super correlation that may result from overly dense random signals.

4. It is recommended to use stop loss and take profit mechanisms to control risks.

5. Risks can be reduced by appropriately extending the trading interval.

## Optimization Directions

1. Incorporate more complex factors to generate random signals.

2. Increase trading varieties to expand test scope.

3. Optimize UI interaction and increase strategy control capabilities.

4. Provide more test tools and indicators for parameter optimization.

5. Can be used as a trading signal or stop loss take profit component added to other strategies.

## Summary

The overall framework of this strategy is complete, generating trading signals based on random events, with high reliability. At the same time, it provides parameter adjustment, backtesting, and charting capabilities. It can be used to test novice strategy development, and also as a basic module for other strategies. Through appropriate optimization, the strategy performance can be further improved.

||

## Strategy Arguments

| Argument        | Default  | Description                                    |
|-----------------|----------|------------------------------------------------|
| v_input_1       | false    | ------- Trade Activity -------                |
| v_input_2       | 25       | Max Bars between Coin Filps                    |
| v_input_3       | false    | ------- Position Settings -------             |
| v_input_4       | 5        | Risk in %                                      |
| v_input_5       | 1.5      | Risk to Reward Ratio x:1                       |
| v_input_6       | false    | ------- Plot Options -------                   |
| v_input_7       | true     | Show Position Boxes                            |
| v_input_8       | false    | ------- Back Testing -------                   |
| v_input_9       | true     | Run Strategy Back Test                         |
| v_input_10      | false    | Use Custom Date Range for back test            |
| v_input_11      | 2021     | Test Start Year                                |
| v_input_12      | true     | Test Start Month                               |
| v_input_13      | true     | Test Start Day                                 |
| v_input_14      | 2021     | Test Stop Year                                 |
| v_input_15      | 5        | Test Stop Month                                |
| v_input_16      | true     | Test Stop Day                                  |

## Source (PineScript)

``` pinescript
/*backtest
start: 2022-11-30 00:00:00
end: 2023-12-06 00:00:00
period: 1d
basePeriod: 1h
exchanges: [{"eid":"Futures_Binance","currency":"BTC_USDT"}]
*/

// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © melodicfish

//@version=4
strategy("Coin Flipper Pro",overlay=true,max_bars_back=100)

// ======= User Inputs variables=========

h1=input(title="------- Trade Activity -------",defval=false)
maxBars=input(25.0,title="Max Bars between Coin Filps",step=1.0,minval=4.0)

h2=input(title="------- Position Settings -------",defval=false)
risk=input(defval=5.0,title="Risk in % ",type=input.float, minval=0.001 ,step=0.1)
ratio= input(defval=1.5,title="Risk to Reward Ratio x:1 ",type=input.float, minval=0.001,step=0.1)

h3=input(title="------- Plot Options -------",defval=false)
showBox=input(defval=true, title="Show Position Boxes")

h4=input(title="------- Back Testing -------",defval=false)
runTest=input(defval=true, title="Run Strategy Back Test")
customTime=input(defval=false, title="Use Custom Date Range for back test")


tsYear = input(2021,minval=1000,maxval=9999,title= "Test Start Year")
tsMonth = input(1,minval=1,maxval=12,title= "Test Start Month")
tsDay = input(1,minval=1,maxval=31,title= "Test Start Day")
start = timestamp(tsYear,tsMonth,tsDay,0,0)

teYear = input(2021,minval=1000,maxval=9999,title=  "Test Stop Year")
teMonth = input(5,minval=1,maxval=12,title=  "Test Stop Month")
teDay = input(1,minval=1,maxval=31,title=  "Test Stop Day")
end = timestamp(teYear,teMonth,teDay,0,0)

// ===
```