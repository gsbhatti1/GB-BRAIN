> Name

TradingViewWebHook Direct Connect Strategy

> Author

InnovatorQuant - Xiao Xiaomeng

> Strategy Description

Related Article: [https://www.fmz.com/bbs-topic/5969](https://www.fmz.com/bbs-topic/5969)

Due to some issues with HTTPServer, consider using ThreadingHTTPServer instead.
Reference: [https://docs.python.org/3.7/library/http.server.html](https://docs.python.org/3.7/library/http.server.html)
Requires Python 3.7 version.

More information on HTTPServer issues:
[https://www.zybuluo.com/JunQiu/note/1350528](https://www.zybuluo.com/JunQiu/note/1350528)

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|AccessKey|$$$__enc__$$$|AccessKey secret key|
|SecretKey|$$$__enc__$$$|SecretKey secret key|
|ContractType||contract ID|
|Port|80|listening port for the service|
|UseMarketOrderForCTP|true|use market order for commodity futures|
|isDealBodyMsg|false|whether to process Body messages|
|amount|0.0001|order quantity|
|ct|swap|contract code|


> Source (python)

``` python
'''
Request format: http://x.x.x.x:xxxx/data?access_key=xxx&secret_key=yyy&type=buy&amount=0.001
Strategy robot parameters:
- Type: Encrypted string, AccessKey , SecretKey , can be a low-level API KEY from the FMZ platform or your own generated key.
- Type: String, contract ID, ContractType
- Type: Numeric, port number, Port
'''

import re
import _thread
import json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

def url2Dict(url):
    query = urlparse(url).query  
    params = parse_qs(query)  
    result = {key: params[key][0] for key in params}  
    return result

class Executor(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            dictParam = url2Dict(self.path)
            Log("Test", dictParam)
        except Exception as e:
            Log("Provider do_GET error, e:", e)
    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            dictParam = url2Dict(self.path)
            
            # Test POST request Body information
            data = self.rfile.read(200)   # specified read length
            Log("data:", data)            # print the POST request data, and based on the data in the request, let the robot perform corresponding operations
            
            # Validation
            if len(dictParam) == 4 and dictParam["access_key"] == AccessKey and dictParam["secret_key"] == SecretKey:
                del dictParam["access_key"]
                del dictParam["secret_key"]
                Log("Received request", "Parameters:", dictParam, "#FF0000")
                
                isSpot = True
                if exchange.GetName().find("Futures") != -1:
                    if ContractType != "":
                        exchange.SetContractType(ContractType)
                        isSpot = False 
                    else :
                        raise "未设置期货合约"
                                
                q = None
                if exchange.GetName() == "Futures_CTP" and UseMarketOrderForCTP == False:
                    q = ext.NewTaskQueue()
                
                if isSpot and dictParam["type"] == "buy":
                    exchange.Buy(-1, float(dictParam["amount"]))
                    Log(exchange.GetAccount())
                elif isSpot and dictParam["type"] == "sell":
                    exchange.Sell(-1, float(dictParam["amount"]))
                    Log(exchange.GetAccount())
                elif not isSpot and dictParam["type"] == "long":
                    exchange.SetDirection("buy")
                    if not q:
                        exchange.Buy(-1, float(dictParam["amount"]))
                    else :
                        q.pushTask(exchange, ContractType, "buy", float(dictParam["amount"]), lambda task, ret: Log(task["desc"], ret, "#FF0000"))
                    Log("Position:", exchange.GetPosition())
                elif not isSpot and dictParam["type"] == "short":
                    exchange.SetDirection("sell")
                    if not q:
                        exchange.Sell(-1, float(dictParam["amount"]))
                    else :
                        q.pushTask(exchange, ContractType, "sell", float(dictParam["amount"]), lambda task, ret: Log(task["desc"], ret, "#FF0000"))
                    Log("Position:", exchange.GetPosition())
                elif not isSpot and dictParam["type"] == "cover_long":
                    exchange.SetDirection("closebuy")
                    if not q:
                        exchange.Sell(-1, float(dictParam["amount"]))
                    else :
                        q.pushTask(exchange, ContractType, "closebuy", float(dictParam["amount"]), lambda task, ret: Log(task["desc"], ret, "#FF0000"))
                    Log("Position:", exchange.GetPosition())
                elif not isSpot and dictParam["type"] == "cover_short":
                    exchange.SetDirection("closesell")
                    if not q:
                        exchange.Buy(-1, float(dictParam["amount"]))
                    else :
                        q.pushTask(exchange, ContractType, "closesell", float(dictParam["amount"]), lambda task, ret: Log(task["desc"], ret, "#FF0000"))
                    Log("Position:", exchange.GetPosition())
                
                if q is not None:
                    while q.size() > 0:
                        q.poll()
                        Sleep(500)
            
            # Process Body data
            if isDealBodyMsg:
                if exchange.GetName().find("Futures") != -1:
                    Log("data:", data.decode('utf-8'))  # Test
                    if re.search(r'buy', data.decode('utf-8')):
                        Log("Triggered buy")
                        exchange.SetContractType(ct)
                        exchange.SetDirection("buy")
                        exchange.Buy(-1, amount)
                    elif re.search(r'sell', data.decode('utf-8')):
                        Log("Triggered sell")
                        exchange.SetContractType(ct)
                        exchange.SetDirection("sell")
                        exchange.Sell(-1, amount)
            
            # Write response with data
            self.wfile.write(json.dumps({"state": "ok"}).encode())
        except Exception as e:
            Log("Provider do_POST error, e:", e)


def create
```