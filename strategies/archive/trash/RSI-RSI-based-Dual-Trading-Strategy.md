> Strategy Arguments


|Argument|Default Value|Description|
|---|---|---|
|rsi_length|14|The length of the RSI calculation period.|
|overbought_threshold|70|The threshold for selling signals when RSI is overbought.|
|oversold_threshold|30|The threshold for buying signals when RSI is oversold.|


> Strategy Source Code


```python
using System;
using QuantConnect.Algorithm;
using QuantConnect.Data.Market;
using QuantConnect.Strategy;

namespace QCAlgorithmExamples
{
    public class RSIDualTradingStrategy : QCAlgorithm
    {
        private const int RsiLength = 14;
        private const double OverboughtThreshold = 70;
        private const double OversoldThreshold = 30;

        public override void Initialize()
        {
            SetStartDate(2020, 1, 1);  // Set Start Date
            SetEndDate(DateTime.Now.Year, DateTime.Now.Month, DateTime.Now.Day);   // Set End Date
            SetCash(100000);  // Set Strategy Cash

            AddEquity("SPY", Resolution.Daily);
        }

        public override void OnData(Slice data)
        {
            if (!data.Bars.Contains("SPY"))
                return;

            var rsi = RSI("SPY", RsiLength, Resolution.Daily);

            // Generate buy signal when RSI is below the oversold threshold
            if (rsi < OversoldThreshold && Portfolio["SPY"].Weight == 0)
            {
                SetHoldings("SPY", 1);
            }

            // Generate sell signal when RSI is above the overbought threshold
            if (rsi > OverboughtThreshold && Portfolio["SPY"].Weight != 0)
            {
                Liquidate("SPY");
            }
        }
    }
}
```

This code defines a simple dual trading strategy based on the Relative Strength Index (RSI). The algorithm checks for buy and sell signals based on RSI values relative to predefined thresholds. When the RSI is below the oversold threshold, it buys an equal weight of SPY; when the RSI is above the overbought threshold, it sells all holdings in SPY.