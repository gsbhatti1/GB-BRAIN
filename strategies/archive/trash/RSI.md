---
> Name

RSI Arbitrage Strategy

> Author

quant777

> Strategy Description

This strategy is an RSI statistical arbitrage strategy based on the RSI indicator, which has achieved high success rates even during bear markets according to field testing. The strategy will perform RSI data analysis of market trends and execute short-term arbitrage once a predefined candlestick pattern is captured.

RSI Indicator Explanation:
The Relative Strength Index (RSI) was originally used for futures trading but has since been found to be effective in guiding stock market investments as well. People have continuously summarized the characteristics of this indicator, and RSI has become one of the most widely applied technical indicators among investors. The general principle behind investment is that investors' buying and selling actions are the result of a combination of various factors, and changes in the market ultimately depend on supply and demand. Therefore, the RSI indicator measures the percentage by which the upward price movement within a given period exceeds the average magnitude of price change to assess the strength of bulls versus bears, thereby guiding specific operations.

Strategy Features:
Supports trend tracking at any level (minute K, hourly K, daily K, weekly K, etc.)
Supports trading pairs from any exchange (ETH/BTC, BSV/BTC, etc.)
Supports multiple exchanges
Detailed strategy reports including the current status of the strategy and a record of all transactions
Supports up to 10 customizable parameters

Strategy Parameters Explanation:
https://www.pcclean.io/8cut

> Source Code (JavaScript)

```javascript
/*
RSI Strategy: For learning purposes only. Use at your own risk in real trading.
*/

var ExchangProcessor={
    createNew: function(exc_obj){
        // Strategy Parameters
        var manage_assets=1; //bch
        var max_positions=4; //max=4N
        var price_n={BTC_BCH:8,ETH_BCH:8,XRP_BCH:8,EOS_BCH:8,LTC_BCH:8,DASH_BCH:8,CET_BCH:8}; //price precision
        var num_n={BTC_BCH:8,ETH_BCH:8,XRP_BCH:8,EOS_BCH:8,LTC_BCH:8,DASH_BCH:8,CET_BCH:8}; //quantity precision
        var minest_buy={BTC_BCH:0.001,ETH_BCH:0.01,XRP_BCH:1,EOS_BCH:1,LTC_BCH:0.1,DASH_BCH:0.01,CET_BCH:1};//minimum buy amount
        var minest_sell={BTC_BCH:0.001,ETH_BCH:0.01,XRP_BCH:1,EOS_BCH:1,LTC_BCH:0.1,DASH_BCH:0.01,CET_BCH:1};//minimum sell amount
        var order_wait_secs=120000; //maximum waiting time for orders in milliseconds
        var wait_ms=1000;//default wait time in milliseconds
        var sxf=0.0005;//used to calculate transaction costs

        // Global State Variables
        var positions=[]; //track positions
        var init_asset=0; //initial asset
        var trades=[]; //record all transactions
        var trades_recorder=true;//record all transactions
        var pre_time=null; //record polling interval time
        var approximate_profit=0;//approximate profit/loss
        var add_already=0;//number of times positions have been added
        
        var processor={};
        
        // Retry buy until successful
        processor.retryBuy=function(ex,price,num)
        {
            var currency=ex.GetCurrency();
            var r=ex.Buy(_N(price,price_n[currency]), _N(num,num_n[currency]));
            while (!r){
                Log("Buy failed, retrying.");
                Sleep(wait_ms);
                var account=_C(ex.GetAccount);
                var ticker=_C(ex.GetTicker);
                var last=ticker.Last;
                var fixedAmount=(price===-1?Math.min(account.Balance*0.95,num):Math.min(account.Balance/last*0.95,num));
                r=ex.Buy(_N(price,price_n[currency]), _N(fixedAmount,num_n[currency]));
            }
            return r;
        }
        
        // Retry sell until successful
        processor.retrySell=function(ex,price,num){
            var currency=ex.GetCurrency();
            var r=ex.Sell(_N(price,price_n[currency]), _N(num,num_n[currency]));
            while (!r){
                Log("Sell failed, retrying.");
                Sleep(wait_ms);
                var account=_C(ex.GetAccount);
                var fixedAmount=Math.min(account.Stocks,num);
                r=ex.Sell(_N(price,price_n[currency]), _N(fixedAmount,num_n[currency]));
            }
            return r;
        }

        // Get current time in China timezone
        processor.get_ChinaTimeString=function(){
            var date = new Date(); 
            var now_utc =  Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(),
                    date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds());
            var cdate=new Date(now_utc);
            cdate.setHours(cdate.getHours()+8);
            var localstring=cdate.getFullYear()+'/'+(cdate.getMonth()+1)+'/'+cdate.getDate()+' '+cdate.getHours()+':'+cdate.getMinutes()+':'+cdate.getSeconds();
            return localstring;
        }
        
        // Initialize object
        processor.init_obj=function(){
            _CDelay(wait_ms);
            pre_time = new Date();
            
            // Initialization
            {
                var account=_C(exc_obj.GetAccount);
                var ticker=_C(exc_obj.GetTicker);
                var last=ticker.Last;
                init_asset=(account.Balance+account.FrozenBalance)+(account.Stocks+account.FrozenStocks)*last;
                Sleep(wait_ms);
            }
        }

        // Main function
        processor.work=function(){
            var cur_time = new Date();
            var passedtime=cur_time-pre_time;
            pre_time=cur_time;

            // Calculate n and position size
            var exname=exc_obj.GetName();
            var currency=exc_obj.GetCurrency();
            var account=_C(exc_obj.GetAccount);
            var ticker=_C(exc_obj.GetTicker);
            var depth = _C(exc_obj.GetDepth);
            var last=ticker.Last;
            var ask1=depth.Asks[0].Price;
            var bid1=depth.Bids[0].Price;
            var bestprice=bid1+(Math.abs(ask1-bid1)/2);
            var records = _C(exc_obj.GetRecords);
            if (records.length<=50){
                Log("records.length is not valid.");
                Sleep(wait_ms);
                return;
            }
            var atr = TA.ATR(records, 20);
            if (atr.length<=1){
                Log("atr.length is not valid.");
                Sleep(wait_ms);
                return;
            }
            var N=atr[atr.length-1];
            var position_unit=Math.min(manage_assets*0.01/N,account.Balance/last*0.95);//cet
            //Log("N="+N+",  头寸单位="+position_unit+"CET");
            var highest=TA.Highest(records, 20, 'High');
            var Lowest=TA.Lowest(records, 10, 'Low');
            var cur_asset=(account.Balance+account.FrozenBalance)+(account.Stocks+account.FrozenStocks)*last;
            var rsi6 = TA.RSI(records, 6);
            var rsi12 = TA.RSI(records, 12);
            if (rsi6.length<=5 || rsi12.length<=5){
                Log("rsi is not valid.");
                Sleep(wait_ms);
                return;
            }
            var rsi_in=false;
            if (rsi6[rsi6.length-1]-rsi6[rsi6.length-2]>1 && rsi6[rsi6.length-2]<=65){
                    //Log("rsi_in=true");
                    rsi_in=true;
                }
            var rsi_out=false;
            if (rsi6[rsi6.length-1]>=60){
                //Log("rsi_out=true");
                rsi_out=true;
            }

            // Open position
            if (positions.length==0 && position_unit>minest_buy[currency]){
                if (rsi_in)
                {
                    var buyID = processor.retryBuy(exc_obj,last,position_unit);
                    Sleep(order_wait_secs);
                    var buyOrder=_C(exc_obj.GetOrder,buyID);
                    if (buyOrder.Status!=ORDER_STATE_CLOSED){
                        exc_obj.CancelOrder(buyID);
                    }
                    if (buyOrder.DealAmount>0){
                        var postion = {
                            amount:buyOrder.DealAmount, 
                            buy_price:buyOrder.AvgPrice, 
                            stoploss_price:buyOrder.Price,
                            Memo:""
                            };
                        positions.push(postion);

                        add_already=1;
                    }
                }
            }

            // Add position
            if (positions.length>0 && position_unit>minest_buy[currency]){
                var last_buy_price=positions[positions.length-1].buy_price;
                if (add_already<max_positions){
                    if (last-last_buy_price>=0.5*N){
                        var buyID = processor.retryBu
``` 

Note: The function `processor.retryBuy` is incomplete in the original text and has been left as it was provided, without completion to maintain accuracy. If this part of the code needs further completion or modification, please provide additional details.