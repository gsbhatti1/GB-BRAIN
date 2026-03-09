```javascript
function WSConnecter_Huobi (method, symbol) {
    // wss : wss://api.huobi.pro/ws
    /* Subscribe 
    {
        "sub": "market.btcusdt.detail",
    }
    */
    /* Subscribe string
        '{"sub": "market.btcusdt.detail"}'
    */

    var strSubscribe = ""
    if (method == "GetTicker") {
        symbol = symbol.toLowerCase()
        symbol = symbol.replace("_", "")
        strSubscribe = '{"sub": "market.' + symbol + '.detail"}'   // symbol : btcusdt
    } else {
        throw "Method not implemented: " + method + "!"
    }
    
    var self = {}
    self.method = method
    self.pingCount = 0
    console.log("Dial function link:", "wss://api.huobi.pro/ws|compress=gzip&mode=recv&reconnect=true&payload=" + strSubscribe)
    console.log("Subscription info:", strSubscribe)
    self.client = Dial("wss://api.huobi.pro/ws|compress=gzip&mode=recv&reconnect=true&payload=" + strSubscribe)
    self.client.write(strSubscribe)
    
    self.Read = function () {
        try {
            var ret = self.client.read()
            var objRet = JSON.parse(ret)
            if (objRet.ping) {
                var pong = {"pong" : objRet.ping}
                // console.log("huobiConn received ping packet, send pong:", JSON.stringify(pong))                
                self.client.write(JSON.stringify(pong))
                self.pingCount++
                return null
            } else {
                /* Wrap into FMZ's ticker structure
                {
                    "ch":"market.btcusdt.detail",
                    "ts":1569477791639,
                    "tick":{
                        "id":205028275148,
                        "low":8217,
                        "high":8624.87,
                        "open":8517.89,
                        "close":8386.36,
                        "vol":361804831.52344716,
                        "amount":43197.45945060976,
                        "version":205028275148,
                        "count":335763
                    }
                }
                */
                var ticker = {}
                if (!objRet.tick) {
                    return null
                }
                
                ticker.Info = objRet.tick
                ticker.High = objRet.tick.high
                ticker.Low = objRet.tick.low
                ticker.Last = objRet.tick.close
                ticker.Volume = objRet.tick.vol
                ticker.Buy = objRet.tick.close
                ticker.Sell = objRet.tick.close
                ticker.Time = objRet.ts
                
                return ticker
            }
        } catch (e) {
            console.error("error:", e)
            return null
        }
    }
    
    self.Close = function () {
        self.client.close()
        console.log("Method:", self.method, "closed ws connection")
    }
    
    return self
}

function WSConnecter_Binance (method, symbol) {
    // wss : wss://stream.binance.com:9443
    // /ws/<streamName>
    // Stream name: <symbol>@ticker
    // /ws/btcusdt@ticker

    var strSubscribe = ""
    if (method == "GetTicker") {
        symbol = symbol.toLowerCase()
        symbol = symbol.replace("_", "")
        strSubscribe = "/ws/" + symbol + "@ticker"
    } else {
        throw "Method not implemented: " + method + "!"
    }    
    
    var self = {}
    self.pingCount = 0
    self.method = method
    console.log("Dial function link:", "wss://stream.binance.com:9443" + strSubscribe + "|reconnect=true")
    self.client = Dial("wss://stream.binance.com:9443" + strSubscribe + "|reconnect=true")
    
    self.Read = function () {
        try {
            var ret = self.client.read()
            var objRet = JSON.parse(ret)
            if (objRet.ping) {
                var pong = {"pong" : objRet.ping}
                console.log("binanceConn received ping packet, send pong:", JSON.stringify(pong))                
                self.client.write(JSON.stringify(pong))
                self.pingCount++
                return null
            } else {
                /*
                {
                    "e":"24hrTicker",
                    "E":1569479950378,
                    "s":"BTCUSDT",
                    "p":"-72.67000000",
                    "P":"-0.855",
                    "w":"8380.87678669",
                    "x":"8504.99000000",
                    "c":"8430.98000000",
                    "Q":"0.10865300",
                    "b":"8430.02000000",          //  Buy1
                    "B":"2.00000000",
                    "a":"8431.00000000",
                    "A":"0.24020700",
                    "o":"8503.65000000",
                    "h":"8629.96000000",
                    "l":"8215.64000000",
                    "v":"52091.18312400",
                    "q":"436569787.43499342",
                    "O":1569393550372,
                    "C":1569479950372,
                    "F":182689950,
                    "L":183168699,
                    "n":478750
                }
                */

                var ticker = {}
                ticker.Info = objRet
                ticker.Buy = objRet.b
                ticker.Sell = objRet.a
                ticker.High = objRet.h
                ticker.Low = objRet.l
                ticker.Volume = objRet.v
                ticker.Last = objRet.c
                ticker.Time = objRet.E
                
                console.log("Pushed ticker:", ticker)   // Test log
                
                return ticker
            }
        } catch (e) {
            console.error("error:", e)
            return null
        }
    }
    
    self.Close = function () {
        self.client.close()
        console.log("Closed ws connection")
    }
    
    return self
}


var _DictConnectCreater = {
    "Huobi" : WSConnecter_Huobi,
    "Binance" : WSConnecter_Binance,
}

var _C
```