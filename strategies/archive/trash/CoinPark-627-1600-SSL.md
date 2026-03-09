```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
CoinPark Universal Protocol using Python2.7
Running Address: http://127.0.0.1:6667, port can be specified
Since the account has no assets, it hasn't been thoroughly tested. Feedback on bugs is welcome.
QQ: 1051804485
Feedback Address: https://www.botvs.com/bbs-topic/1963
Updated June 26, 2018, 15:57 - Bug fixed
This universal protocol can be run as a regular bot on the BotVs simulation platform without any cost.
To use IO functions, you need to override the rpc method in exchange. An example in JS is shown below:
exchange.rpc = function(path, obj) {
    return exchange.IO("api", "POST", path, "obj=" + escape(JSON.stringify(obj)));
}
function main() {
    Log(exchange.rpc("/transfer", {cmd: "transfer/assets", body: {select: 1}}));
}
'''
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import urllib
import urllib2
import time
import hmac
import hashlib
import random
import ssl
ssl._create_default_context = ssl._create_unverified_context

def httpGet(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(url,headers=headers)
    response = urllib2.urlopen(req)
    return json.loads(response.read())

def getsign(data,secret):
    result = hmac.new(secret.encode("utf-8"), data.encode("utf-8"), hashlib.md5).hexdigest()
    return result

def httpPostWithSign(url, cmds, api_key, api_secret):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    s_cmds = json.dumps(cmds)
    sign = getsign(s_cmds,api_secret)
    req = urllib2.Request(url, urllib.urlencode({'cmds': s_cmds, 'apikey': api_key,'sign':sign}), headers=headers)
    response = urllib2.urlopen(req)
    return json.loads(response.read())

class MyExchange:

    market_url = "https://api.coinpark.cc/v1/mdata"
    trade_url = "https://api.coinpark.cc/v1"
    kline_period = {1:'1min', 3:'3min', 5:'5min', 15:'15min', 30:'30min',\
                    60:'1hour', 120:'2hour', 240:'4hour', 360:'6hour', \
                    60*12:'12hour', 60*24:'day', 60*24*7:'week'}
    @staticmethod
    def GetTicker(symbol):
        url = MyExchange.market_url + "?cmd=ticker&pair=" + symbol
        raw_data = httpGet(url)
        if 'error' in raw_data.keys():
            return {'error':json.dumps(raw_data['error'],encoding="utf8", ensure_ascii=False)}
        ret_data = {"data": {"time": raw_data['result']['timestamp'], "buy": raw_data['result']['buy'],\
                    "sell": raw_data['result']['sell'], "last": raw_data['result']['last'],\
                    "high": raw_data['result']['high'], "low": raw_data['result']['low'],\
                    "vol": raw_data['result']['vol']}}
        return ret_data
    @staticmethod
    def GetDepth(symbol):
        url = MyExchange.market_url + "?cmd=depth&size=10&pair=" + symbol
        raw_data = httpGet(url)
        if 'error' in raw_data.keys():
            return {'error':json.dumps(raw_data['error'],encoding="utf8", ensure_ascii=False)}
        ret_data = {"data" : {"time" : raw_data['result']['update_time'], "asks" : [], "bids" : []}}
        for bid in raw_data['result']['bids']:
            ret_data['data']['bids'].append([bid['price'],bid['volume']])
        for ask in raw_data['result']['asks']:
            ret_data['data']['asks'].append([ask['price'],ask['volume']])
        return ret_data
    @staticmethod
    def GetRecords(symbol, period):
        url = MyExchange.market_url + "?cmd=kline&size=200&period=%s&pair="%MyExchange.kline_period[period] + symbol
        raw_data = httpGet(url)
        if 'error' in raw_data.keys():
            return {'error':json.dumps(raw_data['error'],encoding="utf8", ensure_ascii=False)}
        ret_data = {"data": []}
        for kline in raw_data['result']:
            ret_data['data'].append([kline['time'], kline['open'], kline['high'],\
            kline['low'], kline['close'], kline['vol']])
        return ret_data
    @staticmethod
    def GetTrades(symbol):
        url = MyExchange.market_url + "?cmd=deals&size=50&pair=" + symbol
        raw_data = httpGet(url)
        if 'error' in raw_data.keys():
            return {'error':json.dumps(raw_data['error'],encoding="utf8", ensure_ascii=False)}
        ret_data = {"data":[]}
        for trade in raw_data["result"]:
            ret_data["data"].append({"id":trade["id"], "time":trade["time"], \
            "price":trade["price"], "amount":trade["amount"],"type":"buy" if int(trade["side"])==1 else "sell"})
        return ret_data
    @staticmethod
    def GetAccount(api_key, api_secret):
        url = MyExchange.trade_url + "/transfer"
        cmds = [{"cmd": "transfer/assets", "body": {"select":1}}]
        raw_data = httpPostWithSign(url, cmds, api_key, api_secret)
        if 'error' in raw_data.keys():
            return {'error':json.dumps(raw_data['error'],encoding="utf8", ensure_ascii=False)}
        ret_data = {"data": []}
        if "assets_list" in raw_data["result"][0]["result"].keys():
            for asset in raw_data["result"][0]["result"]["assets_list"]:
                ret_data["data"].append({"currency":asset["coin_symbol"], \
                "free":asset["balance"], "frozen":asset["freeze"]})
        ret_data["raw"] = raw_data["result"]
        return ret_data
    @staticmethod
    def Trade(api_key, api_secret, pair, order_type, order_side, price, amount):
        url = MyExchange.trade_url + "/orderpending"
        cmds = [{
                'cmd':"orderpending/trade",
                'index': ra
```