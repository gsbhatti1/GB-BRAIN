# SOURCE: https://github.com/razielapps/chfjpy_bot
# FILE  : signal_engine.py

# signal_engine.py

import ta
import pandas as pd

def get_signal(df: pd.DataFrame) -> str:
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['ema'] = ta.trend.EMAIndicator(df['close'], window=14).ema_indicator()
    
    latest = df.iloc[-1]
    
    if latest['rsi'] < 30 and latest['close'] > latest['ema']:
        return "🔼 BUY Signal: RSI Oversold + Price above EMA"
    elif latest['rsi'] > 70 and latest['close'] < latest['ema']:
        return "🔽 SELL Signal: RSI Overbought + Price below EMA"
    else:
        return "⚠️ No clear signal at this moment."
