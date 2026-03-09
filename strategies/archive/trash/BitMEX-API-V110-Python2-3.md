> Name

BitMEX-Advanced-API-Function-V110-Batch-Order-Edition-Iceberg-Order-One-Click-Cancel-Timed-Cancel-Python2-3

> Author

FawkesPan

> Strategy Description

# BitMEX Advanced API Function (FMZ.com)

### Initialization
This library integrates some advanced BitMEX API functions. Initialization is required before use.
```
# Single exchange
BitMEX = ext.BitMEXPlus(exchange)    # Create a new interface object
# Multiple exchanges
BitMEX = ext.BitMEXPlus(exchanges[0]) # exchanges[where the exchange is added]
```

### Order Operations
#### Batch Orders
##### BulkAdd() Add new orders to the local order list.
```
side, price, and amount are required parameters.
symbol can be omitted to use the default trading pair setting.
displayQty is used for iceberg orders. Set the size of the displayed portion; set to 0 to fully hide it.
orderType and execInst are optional parameters please refer to source code comments.
BitMEX.BulkAdd(side=string, price=float, amount=integer, symbol=string, displayQty=integer, ordType='Limit', clOrdID='', execInst='')
```
##### BulkClear() Clear local unsubmitted orders.
```
symbol can be specified to clear orders of a specific trading pair. If not specified, all orders will be cleared.
notify controls whether to show logs; defaults to True.
BitMEX.BulkClear(symbol=string, notify=True)
```
##### BulkPost() Submit local unconfirmed orders.
```
symbol can be specified to only submit orders of a specific trading pair. If unspecified, it submits all orders.
BitMEX.BulkPost(symbol=string)
```
##### BulkOrders() View all local unconfirmed orders.
```
BitMEX.BulkOrders()
```
#### Cancel Orders
##### CancelAllOrders() Cancel current unfinished orders.
```
symbol can be specified to only cancel orders of a specific trading pair. If unspecified, it cancels all orders.
filter allows custom order filtering; only cancel orders that match the conditions. For example: filter={'side': 'Buy'} cancels all buy orders.
BitMEX.CancelAllOrders(symbol=string, filter=dict)
```
##### CancelAllAfter() Cancel all unfinished orders after a certain time period.
Further requests can reset the counter.
```
timeout specifies the number of milliseconds after which to cancel the order; set to 0 to delete the counter.
BitMEX.CancelAllAfter(timeout=int)
```
#### Edit Orders
##### Amend() Modify an order.
```
symbol can be specified for the trading pair. If not specified, use the default trading pair setting.
orderID or clOrdID is required for specifying the order; if both are provided, only orderID will be used.
price and amount set the new price and quantity of the order respectively; at least one must be modified.
BitMEX.Amend(symbol=string, orderID=string, clOrdID=string, price=float, amount=integer)
```
#### Batch Edit Orders
##### AmendAdd() Add an order to be modified to the local pending modification list.
```
symbol can be specified for the trading pair. If not specified, use the default trading pair setting.
orderID or clOrdID is required for specifying the order; if both are provided, only orderID will be used.
price and amount set the new price and quantity of the order respectively; at least one must be modified.
BitMEX.AmendAdd(symbol=string, orderID=string, clOrdID=string, price=float, amount=integer)
```
##### AmendClear() Clear local unconfirmed pending modification orders.
```
symbol can be specified to clear orders of a specific trading pair. If not specified, it clears all orders.
notify controls whether to show logs; defaults to True.
BitMEX.AmendClear(symbol=string, notify=True)
```
##### AmendPost() Submit local unconfirmed pending modification orders.
```
symbol can be specified to only submit modification requests for orders of a specific trading pair. If unspecified, it submits the default trading pair's order modifications.
BitMEX.AmendPost(symbol=string)
```
##### AmendOrders() View all local unconfirmed pending modification orders.
```
BitMEX.AmendOrders()
```

### Contact Me
Email: i@fawkex.me
Telegram: [FawkesPan](https://telegram.me/FawkesPan)

Custom strategy requests are accepted.

### About this Library
[BitMEX API Documentation](https://www.bitmex.com/app/apiOverview)

[Licensed under GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

> Strategy Arguments



|Argument|Default|Description|
|----|----|----|
|LANG|ZH|Language / Language|


> Source (python)

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
    'GREET' : '[BitMEX 接口已初始化] 合约: %s. %s',
    'INITF' : '使用的交易所不正确，当前交易所: %s',
    'PARAMERR' : '***传的参数不对 检查你的代码*** %s',
    'NEWORDER' : '[添加订单] 合约: %s 方向: %s 价格: %.8f 数量: %d 张. %s',
    'MODORDER' : '[修改订单] orderID/clOrdID: %s 新价格: %.8f 新数量: %d. %s',
    'MODORDERP' : '[修改订单] orderID/clOrdID: %s 新价格: %.8f. %s',
    'MODORDERA' : '[修改订单] orderID/clOrdID: %s 新数量: %d. %s',
    'ORDCOUNT' : '[本次批量发送订单] 总计: %d 条. %s',
    'THISBATCH' : '[信息] 正在处理 合约: %s 条数: %d. %s',
    'CLEARALL' : '[信息] 已清除所有本地订单. %s',
    'CLEAR' : '[信息] 已清除所有 %s 本地订单. %s',
    'CA' : '[订单计划取消] 所有订单都将在 %d 毫秒 后取消. %s'
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
            self.Log(QUOTES[LANG]['INITF'] % (name))
            
    def Log(self, *args):
        if self.silent:
            return 
        self.IO.Log(*args)

    def BulkAdd(self, side=None, price=None, amount=None, symbol=None, ordType='Limit', displayQty=None, clOrdID=None, execInst=None):
        if type is None or price is None or amount is None:
            self.Log(QUOTES[LANG]['PARAMERR'] % (COLORS['RED']))
            return False
        side = side.lower()
        if side not in ['buy', 'sell']:
            self.Log(QUOTES[LANG]['PARAMERR'] % (COLORS['RED']))
            return False

        orderQty = int(amount)
        order = {
            'price': price,
            'side': side,
            'orderQty': orderQty
        }

        # Valid order types
        valid_types = ['Market', 'Limit', 'Stop', 'StopLimit', 'MarketIfTouched', 'LimitIfTouched', 'MarketWithLeftOverAsLimit', 'Pegged']
        if ordType not in valid_types:
            self.Log(QUOTES[LANG]['PARAMERR'] % (COLORS['RED']))
            return False

        order['ordType'] = ordType
        # Additional logic for setting up the order can be added here based on the provided parameters.
```