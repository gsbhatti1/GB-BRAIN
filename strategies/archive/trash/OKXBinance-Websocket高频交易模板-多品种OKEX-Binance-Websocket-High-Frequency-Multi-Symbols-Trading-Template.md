> Name

OKXBinance-Websocket High-Frequency Trading Template - Multi-Symbols-OKEX-Binance-Websocket-High-Frequency-Multi-Symbols-Trading-Template

> Author

Inventor Quant

> Strategy Description

This template implements the following features:

- Public stream subscription for trades and depth synthesis
- Private stream subscription to maintain local order and position information, as well as balance information
- Maintenance of timeout states for canceling orders and support for OKX's amendOrders to modify orders
- Support for multiple varieties for easy high-frequency strategy operations with the lowest possible latency across multiple markets
- The addition of the EventLoop function (which requires the latest docker support) which allows for waiting for any websocket data return in the case of multiple websocket connections to avoid polling.
- Support for OKEX and Binance futures and Binance spot and leverage trading, OKEX spot is not yet supported but can be modified by those interested.
- OKEX private stream subscription requires a Key and password to be included as parameters in the template.
- Automated handling of basic network functions such as reconnection in case of disconnection.
- Support for event callbacks of order and cancellation reports in private streams.
- Unifies the order placement logic for both exchanges and can be viewed in the template source code or examples.
- Support for subscribing to multiple exchange websockets at the same time.
- Order placement modification and deletion can be done in bulk as tasks and will be handled automatically.
- When placing high-frequency orders, the exchange may not return order information promptly (on the private channel) but in such case, market conditions may have already changed. The template maintains a local order status and strategy implementation is included. It automatically recognizes whether it is OKEX or Binance.
- A simple example is provided below and it is strongly recommended to read the source code to better customize your own functionality.

an example: 
```javascript

function onTick(ctx, event) {
    if (event.depth) {
        Log("depth update", event)
    }
    if (event.trades) {
        Log("trades received", event)
    }
    if (event.balance || event.positions) {
        Log("account update", event)
    }
    if (event.orders) {
        Log("private orders update", event)
    }
    
    // include orders, positions, balance for latest
    Log("account", ctx.wsPrivate.account)
    
    // for test only
    if (false) {
        return {
            amendOrders: [{
                instId: event.instId,
                clOrdId: "xxxx*****",
                cxlOnFail: true,
                newSz: "2",
            }],
            newOrders: [{
                instId: event.instId,
                clOrdId: UUID(),
                side: "sell",
                tdMode: "cross",
                ordType: "post_only",
                px: event.depth.asks[0].price.toFixed(4),
                sz: "1",
            }, {
                instId: event.instId,
                clOrdId: UUID(),
                side: "sell",
                tdMode: "cross",
                ordType: "post_only",
                px: event.depth.asks[0].price.toFixed(4),
                sz: "1",
            }],
            cancelOrders: [{
                instId: order.instId,
                clOrdId: order.Id
            }]
        }
    }
}

function main() {
    let instId = exchange.SetContractType("swap").InstrumentID

    let ctx = $.NewWSS(exchange, function(ws) {
        let msg = null
        if (exchange.GetName() === 'Futures_OKCoin') {
            msg = {
                op: "subscribe",
                args: [{
                    channel: "books5",
                    instId: instId,
                }, {
                    channel: "trades",
                    instId: instId,
                }]
            }
        } else {
            let symbol = exchange.GetCurrency().replace('_', '').toLowerCase()
            msg = {
                method: "SUBSCRIBE",
                params: [symbol + "@aggTrade", symbol + "@depth20@100ms"],
                id: "1",
            }
        }
        ws.write(JSON.stringify(msg))
        Log("subscribe", msg, "channel")
        LogStatus("Ready")
    }, onTick, Debug)

    while (true) {
        ctx.poll()
        EventLoop(1000)
    }
}
```

The running status is as follows, you can also subscribe to multiple symbols in the subscribe function
![IMG](https://www.fmz.com/upload/asset/107646c11b93b32c493.png)

The following is the a common market maker robot for OKX and Binance based on this template
![IMG](https://www.fmz.com/upload/asset/73393d2122c1f41a2a.png)

![IMG](https://www.fmz.com/upload/asset/17efd8896a74dc9e271.gif)


> Source (javascript)

```javascript

/* jshint esversion: 6 */
// AccessKey and Phassphrase only need if OKX
$.NewWSS = function(e, onWSSLogin, onWSSTick, Debug, UseMargin, AccessKey, Passphrase) {
    function NewOKXWebSocketPrivate(ctx) {
        let self = {
            ws: null,
            isReadyDic: {},
            lastPing: 0,
            ctx: ctx,
            account: {
                orders: {},
                cancelPending: {},
                ordersCount: 
```