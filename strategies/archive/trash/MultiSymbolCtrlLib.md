> Name

MultiSymbolCtrlLib

> Author

InventorQuant- Xiao Xiaomeng

> Strategy Description

## Description

This template is used in the article at https://www.fmz.com/digest-topic/7373.
The code provided here is for reference and learning purposes only; use with caution in live trading.


> Source (javascript)

``` javascript
// Implementation of exchange API calls
// OKEX V3 Futures
function funcConfigure_Futures_OKCoin(self) {
    // Built-in functions can be freely customized according to needs
    var formatSymbol = function(originalSymbol) {
        // originalSymbol : LINK-USD-210423
        var arr = originalSymbol.split("-")
        var baseCurrency = arr[0]
        var quoteCurrency = arr[1]
        return [(baseCurrency + "_" + quoteCurrency).toUpperCase(), baseCurrency.toUpperCase(), quoteCurrency.toUpperCase()]    // Return data: [currency, baseCurrency, quoteCurrency]
    }

    self.interfaceGetTickers = function interfaceGetTickers() {
        // Can identify whether perpetual futures price is needed based on the symbols subscribed by self.subscribeSymbols
        var url = "https://www.okex.com/api/futures/v3/instruments/ticker"
        self.routineGetTicker = HttpQuery_Go(url)
    }

    self.waitTickers = function waitTickers() {
        var ret = []
        var arr = JSON.parse(self.routineGetTicker.wait())
        _.each(arr, function(ele) {
            ret.push({
            	bid1: parseFloat(ele.best_bid), 
            	bid1Vol: parseFloat(ele.best_bid_size), 
            	ask1: parseFloat(ele.best_ask), 
            	ask1Vol: parseFloat(ele.best_ask_size), 
            	symbol: formatSymbol(ele.instrument_id)[0], 
            	type: "Futures", 
            	originalSymbol: ele.instrument_id
            })
        })
        return ret 
    }

    self.interfaceGetAcc = function interfaceGetAcc(symbol, updateTS) {
        // Can recognize whether the symbol is a perpetual futures based on the symbol
        var arr = formatSymbol(symbol)
        var url = "/api/futures/v3/accounts/" + arr[1].toLowerCase() + "-" + arr[2].toLowerCase()
        self.routineGetAcc = self.e.Go("IO", "api", "GET", url)
    }

    self.waitAcc = function waitAcc(symbol, updateTS) {
        var acc = null 
        var ret = self.routineGetAcc.wait()
        // Check if it is a cross-margin account
        if (ret.margin_mode != "crossed") {
            Log(self.name, "Position mode is not crossed!")
            return 
        }
        var balance = parseFloat(ret.equity) - parseFloat(ret.margin)
        var frozenBalance = parseFloat(ret.margin_for_unfilled)
        if (ret.currency == "USDT") {
            acc = {symbol: symbol, Stocks: 0, FrozenStocks: 0, Balance: balance, FrozenBalance: frozenBalance, originalInfo: ret}
        } else if (ret.currency == "USD") {
            acc = {symbol: symbol, Stocks: balance, FrozenStocks: frozenBalance, Balance: 0, FrozenBalance: 0, originalInfo: ret}
        }
        return acc
    }

    self.interfaceGetPos = function interfaceGetPos(symbol, updateTS) {
    	var symbolInfo = self.getSymbolInfo(symbol)
    	var url = "/api/futures/v3/" + symbol + "/position"
    	if (symbol.includes("SWAP")) {
    		url = "/api/swap/v3/" + symbol + "/position"
    	}
    	var ret = self.e.IO("api", "GET", url)
    	var positions = []
    	_.each(ret.holding, function(ele) {
    		if (ele.instrument_id == symbol && parseFloat(ele.short_qty) > 0) {   // Holding short position
    			positions.push({symbol: symbol, amount: -parseFloat(ele.short_qty) * symbolInfo.multiplier, price: parseFloat(ele.short_avg_cost), marginLevel: parseFloat(ele.leverage), originalInfo: ele})
    		}
    		if (ele.instrument_id == symbol && parseFloat(ele.long_qty) > 0) {    // Holding long position
    			positions.push({symbol: symbol, amount: parseFloat(ele.long_qty) * symbolInfo.multiplier, price: parseFloat(ele.long_avg_cost), marginLevel: parseFloat(ele.leverage), originalInfo: ele})
    		}
    	})
        return positions
    }

    self.interfaceTrade = function interfaceTrade(symbol, type, price, amount) {
        // Determine whether the contract is settled or perpetual
        var url = "/api/futures/v3/order"
        if (symbol.includes("SWAP")) {
            url = "/api/swap/v3/order"
        }
        var tradeType = ""
        switch(type) {
        case self.OPEN_LONG:
            tradeType = "1"
            break
        case self.OPEN_SHORT:
            tradeType = "2"
            break
        case self.COVER_LONG:
            tradeType = "3"
            break
        case self.COVER_SHORT:
            tradeType = "4"
            break
        default:
            throw "type error, type:" + type
        }
        var params = {
            "instrument_id": symbol, 
            "type": tradeType,
            "order_type": "4",
            "size": String(amount)
        }
        self.routineTrade = self.e.Go("IO", "api", "POST", url, self.encodeParams(params))
    }

    self.waitTrade = function waitTrade() {
        return self.routineTrade.wait()
    }

    self.calcAmount = function calcAmount(symbol, type, price, amount) {
        // Process order quantity
        var symbolInfo = self.getSymbolInfo(symbol)
        if (!symbolInfo) {
            throw symbol + " trading pair information not found"
        }
        var tradeAmount = _N(amount / symbolInfo.multiplier, 0)
        // Check minimum order size
        if (tradeAmount < parseFloat(symbolInfo.min)) {
            Log(self.name, " tradeAmount:", tradeAmount, "is less than", parseFloat(symbolInfo.min))
            return false 
        }
        return [tradeAmount, tradeAmount * symbolInfo.multiplier]
    }

    self.interfaceSetMarginLevel = function interfaceSetMarginLevel(symbol, marginLevel) {
        var arr = formatSymbol(symbol)
        var underlying = arr[1] + "-" + arr[2]
        var url = "/api/futures/v3/accounts/" + underlying + "/leverage"
        var params = {
        	"leverage" : String(marginLevel)
        }
        if (symbol.includes("SWAP")) {
        	url = "/api/futures/v3/accounts/" + symbol + "/leverage"
        	params = {
        		"instrument_id" : symbol,
        		"leverage" : String(marginLevel), 
        		"side" : "3"
        	}
        } else {
            var ret  = self.e.IO("api", "GET", "/api/futures/v3/accounts/" + underlying + "/leverage")
            // If not a perpetual contract, switch to cross-margin mode first. Ensure the account is in crossed margin mode before setting.
```