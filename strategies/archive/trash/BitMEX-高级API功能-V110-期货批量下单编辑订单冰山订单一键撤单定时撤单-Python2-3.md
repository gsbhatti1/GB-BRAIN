> Name

BitMEX-Advanced-API-Function-V110-Batch-Order-Editing-Iceberg-Order-One-Click-Cancel-Timer-Cancel-Python2-3

> Author

FawkesPan

> Strategy Description

# BitMEX Advanced API Function (FMZ.com)

### Initialization
This library integrates some advanced BitMEX API functions and needs to be initialized before use.
```
# Single Exchange
BitMEX = ext.BitMEXPlus(exchange)    # Create a new interface object
# Multiple Exchanges
BitMEX = ext.BitMEXPlus(exchanges[0]) # exchanges[here depends on which exchange you added]
```

### Order Operations
#### Batch Orders
##### BulkAdd() Add new orders to the local order list
```
side, price, and amount are required parameters
symbol can be omitted and uses the default trading pair setting
displayQty is used for iceberg order function, setting the size of the order visible part. Set to 0 to completely hide
orderType and execInst are optional parameters, please see comments in the source code
BitMEX.BulkAdd(side=string, price=float, amount=integer, symbol=string, displayQty=integer, ordType='Limit', clOrdID='', execInst='')
```
##### BulkClear() Clear local unsubmitted orders
```
symbol can be specified to clear orders of a specific trading pair. If not specified, all orders will be cleared
notify controls whether to show logs, default is to show
BitMEX.BulkClear(symbol=string, notify=True)
```
##### BulkPost() Submit local unsubmitted orders
```
symbol can be specified to submit orders of a specific trading pair. If not specified, all orders will be submitted
BitMEX.BulkPost(symbol=string)
```
##### BulkOrders() View all local unsubmitted orders
```
BitMEX.BulkOrders()
```
#### Cancel Orders
##### CancelAllOrders() Cancel all current uncompleted orders
```
symbol can be specified to cancel orders of a specific trading pair. If not specified, all orders will be canceled
filter is a custom order filter to cancel only orders that meet the conditions. For example, filter={'side': 'Buy'} cancels all buy orders
BitMEX.CancelAllOrders(symbol=string, filter=dict)
```
##### CancelAllAfter() Cancel all uncompleted orders after a certain period of time
A new request can reset the timer
```
timeout specifies the number of milliseconds after which orders will be canceled. Set 0 to delete the timer
BitMEX.CancelAllAfter(timeout=integer)
```
#### Edit Orders
##### Amend() Modify an order
```
symbol can be specified for the trading pair. If not specified, the default trading pair is used
orderID and clOrdID are order ID and user-defined order ID, at least one must be specified. Both can be filled, in which case orderID will be used
price and amount are the new price and new quantity of the order, at least one must be modified. Both can be modified
BitMEX.Amend(symbol=string, orderID=string, clOrdID=string, price=float, amount=integer)
```
#### Batch Edit Orders
##### AmendAdd() Add an order to be modified to the local pending modification list
```
symbol can be specified for the trading pair. If not specified, the default trading pair is used
orderID and clOrdID are order ID and user-defined order ID, at least one must be specified. Both can be filled, in which case orderID will be used
price and amount are the new price and new quantity of the order, at least one must be modified. Both can be modified
BitMEX.AmendAdd(symbol=string, orderID=string, clOrdID=string, price=float, amount=integer)
```
##### AmendClear() Clear local unsubmitted pending modification orders
```
symbol can be specified to clear orders of a specific trading pair. If not specified, all orders will be cleared
notify controls whether to show logs, default is to show
BitMEX.AmendClear(symbol=string, notify=True)
```
##### AmendPost() Submit local unsubmitted pending modification orders
```
symbol can be specified to submit modification requests of orders of a specific trading pair. If not specified, the modification request of the default trading pair will be submitted
BitMEX.AmendPost(symbol=string)
```
##### AmendOrders() View all local unsubmitted orders
```
BitMEX.AmendOrders()
```

### Contact Information
Email: i@fawkex.me
Telegram: [FawkesPan](https://telegram.me/FawkesPan)

Accepts custom strategy requests

### About this Library
[BitMEX API Documentation](https://www.bitmex.com/app/apiOverview)

[Licensed under GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|LANG|ZH|Language / Language|


> Source (Python)

``` python


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8
#
# BitMEX Advanced API Interface for FMZ.com.
#
# Copyright 2018 FawkesPan
# Contact : i@fawkex.me / Telegram@FawkesPan
#
# GNU General Public License v3.0
#

import json
import math
import decimal

def toNearest(num, tickSize):
    tickDec = decimal.Decimal(str(tickSize))
    return float((decimal.Decimal(round(num / tickSize, 0)) * tickDec))

QUOTES = {}
QUOTES['ZH'] = {
    'GREET' : '[BitMEX 接口已初始化]  合约: %s. %s',
    'INITF' : '使用的交易所不正确，当前交易所: %s',
    'PARAMERR' : '***传的参数不对 检查你的代码*** %s',
    'NEWORDER' : '[添加订单]  合约: %s 方向: %s 价格: %.8f 数量: %d 张. %s',
    'MODORDER' : '[修改订单]  orderID/clOrdID: %s 新价格: %.8f 新数量: %d. %s',
    'MODORDERP' : '[修改订单]  orderID/clOrdID: %s 新价格: %.8f. %s',
    'MODORDERA' : '[修改订单]  orderID/clOrdID: %s 新数量: %d. %s',
    'ORDCOUNT' : '[本次批量发送订单]  总计: %d 条. %s',
    'THISBATCH' : '[信息]  正在处理 合约: %s 条数: %d. %s',
    'CLEARALL' : '[信息]  已清除所有本地订单. %s',
    'CLEAR' : '[信息]  已清除所有 %s 本地订单. %s',
    'CA' : '[订单计划取消]  所有订单都将在 %d 毫秒 后取消. %s'
}

COLORS = {
    'DEEPBLUE' : '#1F618D',
    'BLUE' : '#0000FF',
    'LIGHTBLUE' : '#5DADE2',
    'DEEPGREEN' : '#27AE60',
    'GREEN' : '#00FF00',
    'LIGHTGREEN' : '#58D68D',
    'LAPIS' : '#26619C',
    'DEEPRED' : '#CB4335',
    'RED' : '#FF0000',
    'LIGHTRED' : '#EC7063'
}


class BitMEX:

    def __init__(self, exchange, silent=False):
        self.silent = silent
        exchange.GetCurrency()
        if isinstance(exchange.GetCurrency(), bytes):
            self.symbol = str(exchange.GetCurrency(), "utf-8").lower()
            name = str(exchange.GetName(), "utf-8")
        else:
            self.symbol = exchange.GetCurrency()
            name = exchange.GetName()
        self.IO = exchange.IO
        self.bulks = []
        self.amends = []
        if 'BitMEX' in str(name):
            self.Log(QUOTES[LANG]['GREET'] % (self.symbol.upper(),COLORS['LAPIS']))
        else:
            Log(QUOTES[LANG]['INITF'] % (name))
            
    def Log(self, *args):
        if self.silent:
            return 
        Log(*args)

    def BulkAdd(self, side=None, price=None, amount=None, symbol=None, ordType='Limit', displayQty=None, clOrdID='', execInst=''):
        side, price, and amount are required parameters
        symbol can be omitted and uses the default trading pair setting
        displayQty is used for iceberg order function, setting the size of the order visible part. Set to 0 to completely hide
        orderType and execInst are optional parameters, please see comments in the source code
        BitMEX.BulkAdd(side=string, price=float, amount=integer, symbol=string, displayQty=integer, ordType='Limit', clOrdID='', execInst='')
```

The script provided is incomplete and should have a more complete implementation for the `BulkAdd` method, but this should give you the structure and context for the rest of the script. If you need further assistance with completing the method, please provide more details or context.