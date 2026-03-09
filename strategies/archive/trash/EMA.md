> Name

EMA Trend Tracking for Weekly, Next Week, and Quarterly

> Author

crypto_future

> Strategy Description

This strategy is based on EMA (Exponential Moving Average) mean line trend tracking. It opens a position when an EMA golden cross occurs and closes it when an EMA death cross happens. Profits are earned from the trends. The strategy supports双向开仓做多做空on OKEX contracts.

Additional Note: EMA, or Exponential Moving Average, is an exponentially weighted moving average indicator. It is also called EXPMA and is a trend-following indicator that weights recent prices more heavily than older ones in its calculation.

The EMA trend tracking method was developed based on the trading philosophy of cutting losses short while letting profits run. Trend following believes that market trends persist due to human greed, fear, and economic cycles, leading to continuous upward or downward movements. By capturing the main trend, this strategy aims to achieve average or above-average profits in the market.

Note: This strategy is for learning and debugging purposes only. Use at your own risk in live trading.

Usage Instructions:
https://www.pcclean.io/number-exchange-ema-trading-strategy-okex-version/

> Source (javascript)

```javascript
var strategy_version="1.62.EMA"; //test

/*
Usage instructions:
- Set the OKEX account to 10x leverage.
- Use Full Margin mode.
- Use API v1.
*/

/********************************************Strategy Parameters**********************************/
var price_n={Futures_OKCoin_BSV_USD:2}; // Price precision settings
var num_n={Futures_OKCoin_BSV_USD:0}; // Quantity precision settings
var minestbuy={Futures_OKCoin_BSV_USD:1}; // Minimum buy quantity
var price_step={Futures_OKCoin_BSV_USD:0.2}; // Price step adjustment for orders
var contract_min={Futures_OKCoin_BSV_USD:10}; // Minimum contract amount
var wait_ms=3000; // Retry wait time (ms)
var max_wait_order=6000; // Order wait time (ms)
var margin_lv=10; // Leverage multiple
var ok_future_target='bsv'; // Target contract
var keep_risk_rate=2; // Risk margin rate  (Total equity / Available funds)
var trade_unit_div=4; // Percentage of trading unit per transaction
var push_notification=true; // Enable WeChat notifications for trading opportunities
var N_mult=3; // Multiple of N used to calculate stop loss levels
var k_type=PERIOD_M15; // K-line type
var N_knumber=50; // Number of bars (60) used in EMA calculation
/********************************************Strategy Parameters**********************************/


// Global variables
var total_loop=0;
var tw_sell1_lowest=100000;
var tw_buy1_highest=0;
var nw_sell1_lowest=100000;
var nw_buy1_highest=0;
var qt_sell1_lowest=100000;
var qt_buy1_highest=0;
var total_trade_num=0;
var success_trade_num=0;
var failed_trade_num=0;

// Main function
function main(){
    Log("strategy_version=" + strategy_version);
    $.set_params(price_n, num_n, minestbuy, price_step, wait_ms, max_wait_order);
    
    if (push_notification){
        Log("Strategy is running! Notifications enabled. @");
    }
    
    // Restore data
    total_trade_num = Number(_G("total_trade_num"));
    success_trade_num = Number(_G("success_trade_num"));
    failed_trade_num = Number(_G("failed_trade_num"));
    
    while(true){
        
        try{
            exchange.SetMarginLevel(margin_lv);
            var exname = exchange.GetName();
            var currency = exchange.GetCurrency();
            var account = $.retry_get_account(exchange);
            var f_orders = _C(exchange.GetOrders);
            
            exchange.SetContractType("this_week");
            var tw_depth = _C(exchange.GetDepth);
            var tw_sell1 = tw_depth.Asks[0].Price;
            var tw_buy1 = tw_depth.Bids[0].Price;
            var tw_records = _C(exchange.GetRecords, k_type);
            if (tw_records.length <= 60){
                Log("tw_records.length invalid, skipping this execution...");
                Sleep(wait_ms);
                continue;
            }
            
            exchange.SetContractType("next_week");
            var nw_depth = _C(exchange.GetDepth);
            var nw_sell1 = nw_depth.Asks[0].Price;
            var nw_buy1 = nw_depth.Bids[0].Price;
            var nw_records = _C(exchange.GetRecords, k_type);
            if (nw_records.length <= 60){
                Log("nw_records.length invalid, skipping this execution...");
                Sleep(wait_ms);
                continue;
            }
            
            exchange.SetContractType("quarter");
            var qt_depth = _C(exchange.GetDepth);
            var qt_sell1 = qt_depth.Asks[0].Price;
            var qt_buy1 = qt_depth.Bids[0].Price;
            var qt_records = _C(exchange.GetRecords, k_type);
            if (qt_records.length <= 60){
                Log("qt_records.length invalid, skipping this execution...");
                Sleep(wait_ms);
                continue;
            }
            
            var position = _C(exchange.GetPosition);
            
            var tw_zuoduo_zhangshu = 0;
            var tw_zuoduo_avg_price = 0;
            var tw_zuoduo_amount = 0;
            var tw_zuokong_zhangshu = 0;
            var tw_zuokong_avg_price = 0;    
            var tw_zuokong_amount = 0;
            
            var nw_zuoduo_zhangshu = 0;
            var nw_zuoduo_avg_price = 0;
            var nw_zuoduo_amount = 0;
            var nw_zuokong_zhangshu = 0;
            var nw_zuokong_avg_price = 0;
            var nw_zuokong_amount = 0;
            
            var qt_zuoduo_zhangshu = 0;
            var qt_zuoduo_avg_price = 0;
            var qt_zuoduo_amount = 0;
            var qt_zuokong_zhangshu = 0;
            var qt_zuokong_avg_price = 0;
            var qt_zuokong_amount = 0;

            for (var i=0; i < position.length; i++){
                if (position[i].ContractType === "this_week"){
                    if (position[i].Type === PD_LONG){
                        tw_zuoduo_zhangshu = position[i].Amount;
                        tw_zuoduo_avg_price = position[i].Price;
                        tw_zuoduo_amount = tw_zuoduo_zhangshu * contract_min[$.get_exchange_id(exchange)] * (1/tw_zuoduo_avg_price - 1/tw_buy1 + 1/tw_zuoduo_avg_price);
                    }
                    if (position[i].Type === PD_SHORT){
                        tw_zuokong_zhangshu = position[i].Amount;
                        tw_zuokong_avg_price = position[i].Price;
                        tw_zuokong_amount = tw_zuokong_zhangshu * contract_min[$.get_exchange_id(exchange)] * (1/tw_sell1 - 1/tw_zuokong_avg_price + 1/tw_zuokong_avg_price);
                    }
                }
                if (position[i].ContractType === "next_week"){
                    if (position[i].Type === PD_LONG){
                        nw_zuoduo_zhangshu = position[i].Amount;
                        nw_zuoduo_avg_price = position[i].Price;
                        nw_zuoduo_amount = nw_zuoduo_zhangshu * contract_min[$.get_exchange_id(exchange)] * (1/nw_zuoduo_avg_price - 1/nw_buy1 + 1/nw_zuoduo_avg_price);
                    }
                    if (position[i].Type === PD_SHORT){
                        nw_zuokong_zhangshu = position[i].Amount;
                        nw_zuokong_avg_price = position[i].Price;
                        nw_zuokong_amount = nw_zuokong_zhangshu * contract_min[$.get_exchange_id(exchange)] * (1/nw_sell1 - 1/nw_zuokong_avg_price + 1/nw_zuokong_avg_price);
                    }
                }
                if (position[i].ContractType === "quarter"){
                    if (position[i].Type === PD_LONG){
                        qt_zuoduo_zhangshu = position[i].Amount;
                        qt_zuoduo_avg_price = position[i].Price;
                        qt_zuoduo_amount = qt_zuoduo_zhangshu * contract_min[$.get_exchange_id(exchange)] * (1/qt_sell1 - 1/qt_buy1 + 1/qt_zuoduo_avg_price);
                    }
                    if (position[i].Type === PD_SHORT){
                        qt_zuokong_zhangshu = position[i].Amount;
                        qt_zuokong_avg_price = position[i].Price;
                        qt_zuokong_amount = qt_zuokong_zhangshu * contract_min[$.get_exchange_id(exchange)] * (1/qt_sell1 - 1/qt_zuokong_avg_price + 1/qt_zuokong_avg_price);
                    }
                }
            }
            
            var account_rights = account.Info.info[ok_future_target].account_rights; // Account rights
            var keep_deposit = account.Info.info[ok_future_target].keep_deposit; // Margin kept
            var profit_real = account.Info.inf