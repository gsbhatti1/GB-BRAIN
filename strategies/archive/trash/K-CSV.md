Name

Backtesting saves K-line to local CSV

Author

grass



Source(python)

```python
'''
/*backtest
start: 2017-10-01
end: 2017-11-16
Period: 1440
periodBase: 15
mode: 0
*/
'''

# You need to use the pandas library and perform your own managed backtest to save it locally.
#import numpy as np
import pandas as pd

# Save path
path = 'C:\\Users\\Public\\Documents\\'

def main():
    df = pd.DataFrame()
    while True:
        records = _C(exchange.GetRecords)
        df_new = pd.DataFrame(records) # Convert records to dataframe
        df_new['Time'] = pd.to_datetime(df_new['Time'], unit='ms') + pd.Timedelta('8 h')
        df_new.index = df_new['Time']
        
        if df.empty or df_new['Time'].min() >= df['Time'].max():
            df = df.combine_first(df_new)
            Log(df['Time'].max())
            
        # Determine the last time for saving data
        if df_new['Time'].max() == pd.Timestamp('2017-11-15 23:45:00'):
            Log('save data')
            df = df.combine_first(df_new)
            df.to_csv(path + 'records15.csv', index=False)
            break
        
        # Sleep time is the selection period
        Sleep(15 * 60 * 1000)

```

Detail

https://www.fmz.com/strategy/61867

Last Modified

2017-12-15 13:31:31