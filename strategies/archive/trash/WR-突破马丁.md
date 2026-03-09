> Name

WR-Breakthrough Martin

> Author

TigerQuant


> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|period|15|K-line period|
|marginLevel|20|Magnification multiple|
|baseAmount|10|Initial U opening position|
|WRperiod|14|WR period|
|zhiy|100|Profit-taking percentage|
|zhis|100|Stop-loss percentage|
|autoMoveStocks|false|Automatically move out 100U when available assets are greater than *U|
|maxBuc|10|Maximum number of doublings|



|Button|Default|Description|
|----|----|----|
|Clear Position and Stop|__button__|Clear position and stop|


> Source (python)

``` python
'''backtest
start: 2021-03-19 05:00:00
end: 2021-03-21 00:00:00
period: 15m
basePeriod: 15m
exchanges: [{"eid":"Futures_HuobiDM","currency":"BTC_USD"},{"eid":"Futures_HuobiDM","currency":"ETH_USD","stocks":300},{"eid":"Futures_HuobiDM","currency":"EOS_USD","stocks":5000}]
args: [["openConMode",null]]
'''

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import talib
import math
import urllib.request

ChartCfg = {
    '__isStock': True,
    'title': {
        'text': 'WR'
    },
    'yAxis': [{
        'title': {'text': 'WR'},
        'style': {'color': '#4572A7'},
        'opposite': False # right axis
    }],
    'series': [{
        'type': 'line',
        'id': 'wr',
        'name': 'wr',
        'data': []
    }]
}

def MyLog(str1, ktime, price=''):
    if (_G('str') != str1 or _G('ktime') != ktime) and not (_G('str2') == str1 and ktime == _G('ktime2')):
        _G('str2', _G('str'))
        _G('ktime2', _G('ktime'))

        _G('str', str1)
        _G('ktime', ktime)
        Log(str1 + str(price)) 

def moveStocks(_moveStocks):
    global todayProfit
    if exchanges[0].GetName().find('Binance') >= 0: # Futures_Binance only has delivery and shares common capital 2-USD-based to spot 4-BTC-based to spot, returns tranId
        if exchanges[0].GetCurrency().find('USDT') >= 0:
            movecurrency = 'USDT'
            mtype = 2
        else: # BTC-based
            movecurrency = 'BTC'
            mtype = 4
        timestamp = Unix() * 1000       
        params = "type=" + str(mtype) + "&asset=" + movecurrency + "&amount=" + str(_moveStocks) + "&timestamp=" + str(timestamp)
        exchanges[0].SetBase('https://api.binance.com')
        moveid = exchange.IO("api", "POST", "/sapi/v1/futures/transfer", params)   
        exchanges[0].SetBase('https://fapi.binance.com')
        if moveid is not None:
            Log('Capital transfer successful', moveid)
            _G('moveStocks', _G('moveStocks') + _moveStocks)
            todayProfit["initStocks"] = todayProfit["initStocks"] - _moveStocks
            _G('todayProfit', todayProfit)
            
        else:
            Log('Capital transfer failed')
    else:
        Log('Currently not supported for this exchange')

def cancelOD(i):
    orders = _C(exchanges[i].GetOrders)
    for order in orders:
        exchanges[i].CancelOrder(order.Id)
        Sleep(100)

def coverAll(i):
    position = _C(exchanges[i].GetPosition)
    cancelOD(i)
    Sleep(200)
    for j in range(len(position)):
        pamount = position[j]["Amount"] #-position[0]["FrozenAmount"]
        if position[j]["Type"] == 0:     # holding long
            Deal(-1, pamount, "closebuy", exchanges[i].GetCurrency() + ' Manual market price liquidation', i)
        elif position[j]["Type"] == 1:     # holding short
            Deal(-1, pamount, "closesell", exchanges[i].GetCurrency() + ' Manual market price liquidation', i)

def getOpenPrice(position):
    if hasattr(position[0], 'Info') and hasattr(position[0].Info, 'cost_open'):  # huobi
        return position[0].Info.cost_open
    elif hasattr(position[0], 'Info') and hasattr(position[0].Info, 'avg_cost'):  # ok
        return position[0].Info.avg_cost
    elif hasattr(position[0], 'Info') and hasattr(position[0].Info, 'entryPrice'):  # binance
        return position[0].Info.entryPrice
    else:
        return position[0]["Price"] 

def UpdateAccout():
    accout = _C(exchanges[0].GetAccount)
    acc1 = accout.FrozenBalance    # other coin's frozen balance, does it share?
    acc2 = accout.Balance
    
    _G("ableAccount", acc2)  # current available U
    _G("allAccount", acc1 + acc2 + GetMargin())  # not calculated floating profit

    if acc2 < 1:
        Log("Insufficient margin balance in the account")
        Sleep(8000)

def GetMargin():
    allMargin = 0
    for i in range(len(exchanges)):
        allMargin += _G("margin")[i]
    return _N(allMargin, 2)


def GetHighest(records, i, period):
    high = 0
    for j in range(i - period + 1, i + 1):
        if records[j].High > high:
            high = records[j].High
    return high

def GetLowest(records, i, period):
    low = 1000000
    for j in range(i - period + 1, i + 1):
        if records[j].Low < low:
            low = records[j].Low
    return low
    
def SetType(type):
    if type == 0:
        _G("contractType", "swap")
    elif type == 1:
        _G("contractType", "this_week")
    elif type == 2:
        _G("contractType", "next_week")
    elif type == 3:
        _G("contractType", "quarter")
    elif type == 4:
        _G("contractType", "next_quarter")

def Deal(price, num, btype, beizhu='', i=0):
    Sleep(50)
    # if beizhu != '':
    # Log(beizhu)
    exchanges[i].SetDirection(btype)
    if btype == "closebuy" or btype == "sell":
        exchanges[i].Sell(price, num, beizhu)
        # Log('Short entry', price)
    else:
        exchanges[i].Buy(price, num, beizhu)
        # Log('Long entry', price)


def myProfit():
    LogProfit(_G("allAccount") - _G("initStocks"))


def initData():
    SetErrorFilter("502:|503:|tcp|character|unexpected|network|timeout|WSARecv|Connect|GetAddr|no such|reset|http|received|EOF|No need to change|reused")
    global allCoinData
    Log("Initializing...")

    if exchanges[0].GetName().find('Binance') >= 0: # Futures_Binance
        getBinanceAllCoinData()
        Sleep(3000)
        Log("Finished getting exchange information")
    else:
        Log('Currently not supported for this exchange')
        return
    
    if _G("moveStocks") is None:
        _G("moveStocks", 0)
    if _G("moveInStocks") is None:
        _G("moveInStocks", 0)
        
    for i in range(len(exchanges)): # Initialize exchange
        symbol = exchanges[i].GetCurrency().split('_')[0]
        exchanges[i].SetContractType("swap")
        exchanges[i].SetPrecision(allCoinData[symbol]['tick_size'], allCoinData[symbol]['size_increment'])
        exchanges[i].SetMarginLevel(marginLevel)
        timestamp = Unix() * 1000      
```