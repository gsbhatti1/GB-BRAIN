```javascript
var client = null
var deribitAcc = {} // You can set a global object to save token

function WS_GetAccount() { // Get the asset information of a certain currency in the account
    var msg = {
        "jsonrpc": "2.0",
        "id": 2515,
        "method": "private/get_account_summary",
        "params": {
            "currency": "ETH",
            "extended": true
        }
    }

    client.write(JSON.stringify(msg))
    var ret = client.read()
    Log(ret, "#FF0000")
}

function WS_GetToken() { // Authentication and get token
    var msg = {
        "jsonrpc": "2.0",
        "id": 9929,
        "method": "public/auth",
        "params": {
            "grant_type": "client_credentials",
            "client_id": "XXXXXXX", // Obtained when applying for API KEY
            "client_secret": "XXXXXXXXXXXXXXXXXXXXXXXXXX" // Obtained when applying for API KEY
        }
    }
    while (1) {
        client.write(JSON.stringify(msg))
        var ret = client.read()
        try {
            var jsonObj = JSON.parse(ret)
            if (jsonObj) {
                deribitAcc.accessToken = jsonObj.result.access_token
                deribitAcc.refToken = jsonObj.result.refresh_token
                break
            }
        } catch (e) {
            Log("error:", e)
        }
    }
    Log("Update deribitAcc accessToken, refToken:", deribitAcc)
}

function WS_Depth() { //Access the get_order_book public channel to obtain order book depth data
    var msg = {
        "jsonrpc": "2.0",
        "id": 8772,
        "method": "public/get_order_book",
        "params": {
            "instrument_name": "BTC-PERPETUAL", // Specify to obtain the depth data of BTC perpetual contract
            "depth": 5
        }
    }

    client.write(JSON.stringify(msg))
    var ret = client.read()
    Log("depth : ", ret)
}

function main() {
    client = Dial("wss://www.deribit.com/ws/api/v2")
    WS_GetToken()

    WS_GetAccount()
    WS_Depth()

}

function onexit() {
    Log("Close ws connection")
    client.close()
}
```

---

**Name**

Deribit-websocket-example

**Author**

Inventor Quantification-Little Dream

**Source (javascript)**

```javascript
var client = null
var deribitAcc = {} // You can set a global object to save token

function WS_GetAccount() { // Get the asset information of a certain currency in the account
    var msg = {
        "jsonrpc": "2.0",
        "id": 2515,
        "method": "private/get_account_summary",
        "params": {
            "currency": "ETH",
            "extended": true
        }
    }

    client.write(JSON.stringify(msg))
    var ret = client.read()
    Log(ret, "#FF0000")
}

function WS_GetToken() { // Authentication and get token
    var msg = {
        "jsonrpc": "2.0",
        "id": 9929,
        "method": "public/auth",
        "params": {
            "grant_type": "client_credentials",
            "client_id": "XXXXXXX", // Obtained when applying for API KEY
            "client_secret": "XXXXXXXXXXXXXXXXXXXXXXXXXX" // Obtained when applying for API KEY
        }
    }
    while (1) {
        client.write(JSON.stringify(msg))
        var ret = client.read()
        try {
            var jsonObj = JSON.parse(ret)
            if (jsonObj) {
                deribitAcc.accessToken = jsonObj.result.access_token
                deribitAcc.refToken = jsonObj.result.refresh_token
                break
            }
        } catch (e) {
            Log("error:", e)
        }
    }
    Log("Update deribitAcc accessToken, refToken:", deribitAcc)
}

function WS_Depth() { //Access the get_order_book public channel to obtain order book depth data
    var msg = {
        "jsonrpc": "2.0",
        "id": 8772,
        "method": "public/get_order_book",
        "params": {
            "instrument_name": "BTC-PERPETUAL", // Specify to obtain the depth data of BTC perpetual contract
            "depth": 5
        }
    }

    client.write(JSON.stringify(msg))
    var ret = client.read()
    Log("depth : ", ret)
}

function main() {
    client = Dial("wss://www.deribit.com/ws/api/v2")
    WS_GetToken()

    WS_GetAccount()
    WS_Depth()

}

function onexit() {
    Log("Close ws connection")
    client.close()
}
```

**Detail**

https://www.fmz.com/strategy/147765

**Last Modified**

2019-05-15 18:37:40