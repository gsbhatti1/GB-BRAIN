> Name

OkEX-Advanced-API-Function-V110-Futures-Batch-Order-Spot-TBD-Python2-3

> Author

FawkesPan

> Strategy Description

# OkEX Advanced API Function (FMZ.com)

### Initialization
This library integrates some advanced OkEX API functions. Before use, initialization is required.
#### OkEX Futures
```
# OkEX Futures
# future parameter can be 'this_week', 'next_week', or 'quarter'. If not provided, defaults to 'this_week'.
OkEXFuture = ext.OkEXFuturePlus(exchange, future=str)    # Create a new interface object 
# Multiple exchanges
OkEXFuture = ext.OkEXFuturePlus(exchanges[0], future=str)    # exchanges[the position of your added exchange]
```
#### OkEX Spot
# Still writing

### Order Operations - Futures
#### Batch Orders
##### BulkAdd() Add New Orders to Local Order List
```
side, price, and amount are required parameters.
symbol and future can be omitted if using default trading pair settings.
matchPrice is False by default; set it to True for counterparty price trading.
OkEXFuture.BulkAdd(side=str, price=float, amount=int, matchPrice=False, symbol=str, future=str)
```
##### BulkClear() Clear Unsubmitted Local Orders
```
Specify the symbol to clear orders of a specific trading pair. If not specified, all orders will be cleared.
notify is True by default; set it to False if no log display is needed.
OkEXFuture.BulkClear(symbol=str, notify=True)
```
##### BulkPost() Submit Unsubmitted Local Orders
```
Specify the symbol to submit only orders of a specific trading pair. If not specified, all orders will be submitted.
future must be specified along with the symbol for this function. It only submits orders of specific contracts within the specific trading pair.
OkEXFuture.BulkPost(symbol=str, future=str)
```
##### BulkOrders() View Unsubmitted Local Orders
```
Specify the symbol to view orders of a specific trading pair. If not specified, all orders will be viewed.
future must be specified along with the symbol for this function. It only views orders of specific contracts within the specific trading pair.
OkEXFuture.BulkOrders(symbol=str, future=str)
```

### Contact Me
Email: i@fawkex.me
Telegram: [FawkesPan](https://telegram.me/FawkesPan)

Custom strategy requests accepted.

### About This Library
[OkEX API Documentation](https://github.com/okcoin-okex/API-docs-OKEx.com/)

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
# OkEX Advanced API Interface for FMZ.com.
#
# Copyright 2018 FawkesPan
# Contact : i@fawkex.me / Telegram@FawkesPan
#
# GNU General Public License v3.0
#

import json
import time

QUOTES = {}
QUOTES['ZH'] = {
    'GREET' : '[OkEX Interface Initialized]  Currency: %s Contract: %s. %s',
    'INITF' : 'Incorrect exchange used, current exchange: %s',
    'PARAMERR' : '***Parameters incorrect, check your code*** %s',
    'NEWORDER' : '[Add Order]  Currency: %s Contract: %s Direction: %s Price: %.4f Amount: %d Pairs. %s',
    'ORDCOUNT' : '[Batch Orders Sent]  Total: %d orders. %s',
    'THISBATCH' : '[Information]  Processing Currency: %s Contract: %s Count: %d. %s',
    'ORDSENT' : '[Order Sent]  Currency: %s Contract: %s Count: %d. %s',
    'NEEDSPLIT' : '[Information]  Due to single contract amount greater than 5, splitting required. %s',
    'CLEARALL' : '[Information]  All local orders cleared. %s',
    'CLEARS' : '[Information]  All %s local orders cleared. %s',
    'CLEAR' : '[Information]  All %s %s local orders cleared. %s'
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


class OkEXFuture:

    def __init__(self, exchange, future='this_week'):
        self.QUOTES = {}
        exchange.GetCurrency()
        if isinstance(exchange.GetCurrency(), bytes):
            self.symbol = str(exchange.GetCurrency(), "utf-8").lower()
            name = str(exchange.GetName(), "utf-8")
        else:
            self.symbol = exchange.GetCurrency()
            name = exchange.GetName()
        self.IO = exchange.IO
        self.future = future
        self.bulks = {}
        self.bulks[self.symbol] = {}
        self.bulks[self.symbol][self.future] = []
        if 'OKCoin' in str(name):
            Log(QUOTES[LANG]['GREET'] % (self.symbol.upper(),self.future.upper(),COLORS['LAPIS']))
        else:
            Log(QUOTES[LANG]['INITF'] % (name))

    def BulkAdd(self, side=None, price=None, amount=None, matchPrice=False, symbol=None, future=None):
        if type is None or price is None or amount is None:
            Log(QUOTES[LANG]['PARAMERR'] % (COLORS['RED']))
            return False
        side = side.lower()
        if side == 'buy':
            tp = 1
            cl = COLORS['DEEPGREEN']
        if side == 'sell':
            tp = 2
            cl = COLORS['DEEPRED']
        if side == 'closebuy':
            tp = 3
            cl = COLORS['LIGHTRED']
        if side == 'closesell':
            tp = 4
            cl = COLORS['LIGHTGREEN']
        if symbol is None:
            symbol = self.symbol
        if future is None:
            future = self.future

        order = {}
        order['price'] = price
        order['amount'] = amount
        order['type'] = tp

        if matchPrice:
            order['matchPrice'] = 1

        try:
            self.bulks[symbol]
        except KeyError:
            self.bulks[symbol] = {}
        try:
            self.bulks[symbol][future]
        except KeyError:
            self.bulks[symbol][future] = []

        self.bulks[symbol][future].append(order)

        Log(QUOTES[LANG]['NEWORDER'] % (symbol.upper(),future.upper(),side.upper(),price,amount,cl))

        return True

    def BulkOrders(self, symbol=None, future=None):
        if symbol is None:
            return self.bulks
        else:
            if future is None:
                return self.bulks[symbol]
            else:
                return self.bulks[symbol][future]

    def BulkClear(self, symbol=None, future=None, notify=True):
        if symbol is None:
            self.bulks = {}
            if notify:
                Log(QUOTES[LANG]['CLEARALL'] % (COLORS['RED']))
        else:
            if future is None:
                self.bulks[symbol] = {}
                if notify:
                     Log(QUOTES[LANG]['CLEARS'] % (symbol.encode().upper(), COLORS['RED']))
            else:
                self.bulks[symbol][future] = []
                if notify:
                    Log(QUOTES[LANG]['CLEAR'] % (symbol.encode().upper(), future.encode().upper(), COLORS['RED']))
        return True

    #exchange.IO("api", "POST", "/api/v1/future_batch_trade.do", "symbol=etc_usd&contract_type=this_week&orders_data="+json.dumps(orders))
    def __post(self, symbol='', future=''):
        co
```