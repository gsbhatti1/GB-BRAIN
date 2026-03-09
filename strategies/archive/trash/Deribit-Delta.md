> Name

Deribit Option Delta Dynamic Hedging Strategy Teaching

> Author

InventorQuant - Xiao Xiao Meng

> Strategy Description

## Deribit Option Delta Dynamic Hedging Strategy (Teaching)

Article URL: https://www.fmz.com/bbs-topic/6726

> Strategy Arguments


|Argument|Default|Description|
|----|----|----|
|isTestNet|true|Whether to switch to the test network|
|testNetBase|https://test.deribit.com|Base address for the test network|
|hedgeDeltaStep|true|Delta hedging step size|
|isResetLog|true|Whether to clear logs|


|Button|Default|Description|
|----|----|----|
|setContractType||Set option contract type|
|buyOption||Buy option contract|
|sellOption||Sell option contract|
|setHedgeDeltaStep|true|Set hedging threshold|


> Source (javascript)

``` javascript
// Constructor
function createManager(e, subscribeList, msg) {
	var self = {}
    self.supportList = ["Futures_Binance", "Huobi", "Futures_Deribit"]  // Supported exchanges

    // Object properties
    self.e = e
    self.msg = msg
    self.name = e.GetName()
    self.type = self.name.includes("Futures_") ? "Futures" : "Spot"
    self.label = e.GetLabel()
    self.quoteCurrency = ""  
    self.subscribeList = subscribeList   // subscribeList : [strSymbol1, strSymbol2, ...]
    self.tickers = []                    // All market data obtained from the interface, defined format: {bid1: 123, ask1: 123, symbol: "xxx"}}
    self.subscribeTickers = []           // Required market data, defined format: {bid1: 123, ask1: 123, symbol: "xxx"}}
    self.accData = null 
    self.pos = null 

    // Initialization function
    self.init = function() { 
    	// Determine if the exchange is supported
        if (!_.contains(self.supportList, self.name)) {        
        	throw "not support"
        }
    }

    self.setBase = function(base) {
        // Switch base URL to use the test network
        self.e.SetBase(base)
        Log(self.name, self.label, "Switched to test network:", base)
    }

    // Determine data precision
    self.judgePrecision = function (p) {
        var arr = p.toString().split(".")
        if (arr.length != 2) {
            if (arr.length == 1) {
                return 0
            }
            throw "judgePrecision error, p:" + String(p)
        }
        
        return arr[1].length
    }

    // Update account balance
    self.updateAcc = function(callBackFuncGetAcc) {
        var ret = callBackFuncGetAcc(self)
        if (!ret) {
        	return false 
        }
        self.accData = ret 
        return true 
    }

    // Update position
    self.updatePos = function(httpMethod, url, params) {
        var pos = self.e.IO("api", httpMethod, url, params)
        var ret = []
        if (!pos) {
            return false 
        } else {
            // Organize data
            // {"jsonrpc":"2.0","result":[],"usIn":1616484238870404,"usOut":1616484238870970,"usDiff":566,"testnet":true}
            try {
                _.each(pos.result, function(ele) {
                    ret.push(ele)
                })
            } catch(err) {
                Log("Error:", err)
                return false 
            }
            self.pos = ret
        }
        return true 
    }

    // Update market data
    self.updateTicker = function(url, callBackFuncGetArr, callBackFuncGetTicker) {
    	var tickers = []
    	var subscribeTickers = []
    	var ret = self.httpQuery(url)
    	if (!ret) {
    		return false 
    	}
    	// Log("Test", ret)// Test
    	try {
            _.each(callBackFuncGetArr(ret), function(ele) {
            	var ticker = callBackFuncGetTicker(ele)
            	tickers.push(ticker)
                if (self.subscribeList.length == 0) {
                    subscribeTickers.push(ticker)
                } else {
                	for (var i = 0 ; i < self.subscribeList.length ; i++) {                        
                    	if (self.subscribeList[i] == ticker.symbol) {
                    		subscribeTickers.push(ticker)
                    	}
                	}
                }
            })
        } catch(err) {
        	Log("Error:", err)
        	return false 
        }

        self.tickers = tickers
        self.subscribeTickers = subscribeTickers
        return true 
    }

    self.getTicker = function(symbol) {
    	var ret = null 
    	_.each(self.subscribeTickers, function(ticker) {
    		if (ticker.symbol == symbol) {
    			ret = ticker
    		}
    	})
    	return ret 
    }

    self.httpQuery = function(url) {
    	var ret = null
        try {
            var retHttpQuery = HttpQuery(url)
            ret = JSON.parse(retHttpQuery)
        } catch (err) {
            // Log("Error:", err)
            ret = null
        }
        return ret 
    }

    self.returnTickersTbl = function() {
        var tickersTbl = {
        	type : "table", 
        	title : "tickers",
        	cols : ["symbol", "ask1", "bid1"], 
        	rows : []
        }
        _.each(self.subscribeTickers, function(ticker) {        
        	tickersTbl.rows.push([ticker.symbol, ticker.ask1, ticker.bid1])
        })
        return tickersTbl
    }
    
    // Return position table
    self.returnPosTbl = function() {
        var posTbl = {
            type : "table", 
            title : "pos|" + self.msg,
            cols : ["instrument_name", "mark_price", "direction", "size", "delta", "index_price", "average_price", "settlement_price", "average_price_usd", "total_profit_loss"], 
            rows : []
        }
        /* Interface returns the following position data format
        {
            "mark_price":0.1401105,"maintenance_margin":0,"instrument_name":"BTC-25JUN21-28000-P","direction":"buy",
            "vega":5.66031,"total_profit_loss":0.01226105,"size":0.1,"realized_profit_loss":0,"delta":-0.01166,"kind":"option",
            "initial_margin":0,"index_price":54151.77,"floating_profit_loss_usd":664,"floating_profit_loss":0.000035976,
            "average_price_usd":947.22,"average_price":0.0175,"theta":-7.39514,"settlement_price":0.13975074,"open_orders_margin":0,"gamma":0
        }
        */
        _.each(self.pos, function(ele) {
        	if(ele.direction != "zero") {
                posTbl.rows.push([ele.instrument_name, ele.mark_price, ele.direction, ele.size, ele.delta, ele.index_price, ele.average_price, ele.settlement_price, ele.average_price_usd, ele.total_profit_loss])
            }
        })
        return posTbl
    }

    self.returnOptio