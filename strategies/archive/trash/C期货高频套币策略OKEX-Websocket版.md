> Name

C Future High-Frequency Arbitrage Strategy OKEX-Websocket Version

> Author

InventorQuantitative - Xiao Xiaomeng

> Strategy Description

## C++ Future High-Frequency Arbitrage Strategy OKEX Websocket Version

### Strategy Principle

The strategy principle is quite simple, involving cross-period hedging on the OKEX futures. The position control design is based on a differential grid hedge.

Two contracts are defined: Contract A and Contract B. Different contract codes can be set for these contracts to perform the hedge.

For example, you can set Contract A as a quarterly contract and Contract B as an upcoming weekly contract (or vice versa).

- **Hedge Operation**: 
  - Shorting Contract A (quarterly) while Longing Contract B (similar to cross-period arbitrage in commodity futures, where one shorts the future contract and longs the nearby contract for positive arbitrage).
  - Longing Contract A, Shorting Contract B (similar to shorting the nearby and longing the future in commodity futures for reverse arbitrage).

### Design Features

- **Programming Language**
  The strategy code is written using C++, which offers performance advantages such as speed.

- **Market Data Source:**
  Market data is sourced via OKEX WebSocket API, ensuring timely access to the latest market information. Real-time tick data is used for analyzing small differential price fluctuations; a K-line generator specifically constructed by the strategy computes and synthesizes K-lines from the acquired tick data. The opening and closing of positions during hedging operations are driven by the generated K-line data.

- **Position Control:**
  Position control utilizes a ratio similar to the Fibonacci sequence, allowing for an increase in arbitrage hedges when the differential is larger, thereby distributing the positions to capture smaller differential price fluctuations with small positions and larger ones with higher risk.

- **Exit Strategy: Stop Loss and Take Profit:**
  Fixed take profit and stop loss prices are set. Positions are closed once they reach the take profit or stop loss levels.

- **Cycle Design for Entering and Exiting Markets:**
  The parameter `NPeriod` controls a dynamic cycle to manage opening and closing positions in strategies.

- **Position Balancing System, Order Monitoring System:**
  The strategy includes a dedicated periodic position balancing system as well as an order monitoring system.

- **Strategy Expansion:**
  The code design is loosely coupled, making it easy to expand for use with commodity futures or further optimization modifications.

- **Strategy Chart Generation:**
  The strategy automatically generates differential K-line charts and marks relevant trading information.

### Backtest

![IMG](https://www.fmz.com/upload/asset/165549c612d8ba5ae550.png)

![IMG](https://www.fmz.com/upload/asset/168d0e671a56094b28c3.png)

![IMG](https://www.fmz.com/upload/asset/170dcc772a1925d46885.png)

> Strategy Arguments

|Argument|Default|Description|
|----|----|----|
|InstrumentA|this_week|Recent contract|
|InstrumentB|next_week|Futures contract|
|DPeriod|30|Differential period (seconds)|
|NPeriod|20|Cycle length|
|LeavePeriod|5|Exit cycle|
|AddMax|5|Maximum add times|
|StopLoss|10|Stop loss price difference|
|StopWin|30|Take profit price difference|
|OpenAmount|10|Contract size|
|SlidePrice|true|Slippage handling|
|MaxDelay|500|Maximum market delay (milliseconds)|
|IsSetProxy|false|(?Proxy) Proxy setting?|
|Proxy||Proxy setting|

> Source (cpp)

``` cpp
/*backtest
start: 2019-07-22 00:00:00
end: 2019-08-21 00:00:00
period: 1m
exchanges: [{"eid":"Futures_OKCoin","currency":"BTC_USD","stocks":0.1,"fee":[0.02,0.05]}]
args: [["InstrumentB","quarter"],["NPeriod",200],["LeavePeriod",100],["AddMax",3],["StopLoss",20],["StopWin",50],["OpenAmount",2]]
*/

enum State {
    STATE_NA,
    STATE_IDLE,
    STATE_HOLD_LONG,
    STATE_HOLD_SHORT,
};

string replace(string s, const string from, const string& to) {
    if(!from.empty())
        for(size_t pos = 0; (pos = s.find(from, pos)) != std::string::npos; pos += to.size())
            s.replace(pos, from.size(), to);
    return s;
}

class BarFeeder {
    public:
        BarFeeder(int period) : _period(period) {
            _rs.Valid = true;
        }

        void feed(double price, Chart *c=nullptr, int chartIdx=0) {
            uint64_t epoch = uint64_t(Unix() / _period) * _period * 1000;
            bool newBar = false;
            if (_rs.size() == 0 || _rs[_rs.size()-1].Time < epoch) {
                Record r;
                r.Time = epoch;
                r.Open = r.High = r.Low = r.Close = price;
                _rs.push_back(r);
                if (_rs.size() > 2000) {
                    _rs.erase(_rs.begin());
                }
                newBar = true;
            } else {
                Record &r = _rs[_rs.size() - 1];
                r.High = max(r.High, price);
                r.Low = min(r.Low, price);
                r.Close = price;
            }

            auto bar = _rs[_rs.size()-1];
            json point = {bar.Time, bar.Open, bar.High, bar.Low, bar.Close};
            if (c != nullptr) {
               if (newBar) {
                    c->add(chartIdx, point);
                    c->reset(1000);
                } else {
                    c->add(chartIdx, point, -1);
                }
            }
        }
        Records & get() {
            return _rs;
        }
    private:
        int _period;
        Records _rs;
};

class Hedge {
  public:
    Hedge() {
        _isCover = true;
        _needCheckOrder = true;
        _st = STATE_NA;
        for (int i = 0; i < AddMax + 1; i++) {
            if (_addArr.size() < 2) {
                _addArr.push_back((i+1)*OpenAmount);
            }
            _addArr.push_back(_addArr[_addArr.size()-1] + _addArr[_addArr.size()-2]);
        }

        _cfgStr = R"EOF(
        [{
        "extension": { "layout": "single", "col": 6, "height": "500px"},
        "rangeSelector": {"enabled": false},
        "tooltip": {"xDateFormat": "%Y-%m-%d %H:%M:%S, %A"},
        "plotOptions": {"candlestick": {"color": "#d75442", "upColor": "#6ba583"}},
        "chart":{"type":"line"},
        "title":{"text":"Spread Long"},
        "xAxis":{"title":{"text":"Date"}},
        "series":[
            {"type":"candlestick", "name":"Long Spread","data":[], "id":"dataseriesA"},
            {"type":"flags","data":[], "onSeries": "dataseriesA"}
            ]
        },
        {
        "extension": { "layout": "single", "col": 6, "height": "500px"},
        "rangeSelector": {"enabled": false},
        "tooltip": {"xDateFormat": "%Y-%m-%d %H:%M:%S, %A"},
        "plotOptions": {"candlestick": {"color": "#d75442", "upColor": "#6ba583"}},
        "chart":{"type":"line"},
        "title":{"text":"Spread Short"},
        "xAxis":{"title":{"text":"Date"}},
        "series":[
            {"type":"candlestick", "name":"Long Spread","data":[], "id":"dataseriesA"},
            {"type":"flags","data":[], "onSeries": "dataseriesA"}
            ]
        }
        ]
        )EOF";
        _c.update(_cfgStr);
        _c.reset();
    };
    
    State getState(string &symbolA, Depth &depthA, string &symbolB, Depth &depthB) {
        
        if (!_needCheckOrder && _st != STATE_NA) {
            return _st;
        }

        //Log("sync orders");
        auto orders = exchange.GetOrders();
        if (!orders.Valid) {
            return STATE_NA;
        }

        if (orders.size() > 0) {
            for (auto &order : orders) {
                exchange.CancelOrder(order.Id);
            }
            return STATE_NA;
        }
        
        Sleep(500);

        //Log("sync positions");

        auto positions = exchange.GetPosition();
        if (!positions.Valid) {
            return STATE_NA;
        }
``` 

The rest of the code is omitted for brevity. The provided snippet covers the basic structure and some key parts of the strategy implementation in C++. The full code would continue with further logic to handle positions, orders, and other aspects of trading as needed.