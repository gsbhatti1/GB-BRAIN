# SOURCE: https://github.com/irisx3/attention_drl_trading
# FILE  : data.py

# data.py
from typing import List, Dict
import numpy as np
import pandas as pd
def load_panel_from_csv(csv_path: str, window: int):
    df = pd.read_csv(csv_path, low_memory=False)
    assert {"Date", "ticker", "Close"}.issubset(df.columns), "CSV must include Date, ticker, Close"
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Date","ticker"]).reset_index(drop=True)

    # choose features (add/remove freely)
    default_feats = [
        "Open","High","Low","Close","Volume",
        "macd","macd_signal","macd_hist",
        "macdboll","ubboll","lb","rsi","30cci",
        "plus_di_14","minus_di_14","dx_14","dx30",
        "close30_sma","close60_sma"
    ]
    feature_cols = [c for c in default_feats if c in df.columns]
    tickers = df["ticker"].unique()
    dates = df["Date"].drop_duplicates().sort_values()

    close_mat = df.pivot(index="Date", columns="ticker", values="Close").reindex(index=dates, columns=tickers)
    if "log_return" in df.columns:
        logret_mat = df.pivot(index="Date", columns="ticker", values="log_return").reindex(index=dates, columns=tickers)
    else:
        logret_mat = np.log(close_mat / close_mat.shift(1))
    prices_rel = np.nan_to_num(np.exp(logret_mat.values) - 1.0, nan=0.0, posinf=0.0, neginf=0.0).astype(np.float32)

    if not feature_cols:
        raise ValueError("No feature columns found — include at least one numeric feature.")
    feats = []
    for c in feature_cols:
        mat = df.pivot(index="Date", columns="ticker", values=c).reindex(index=dates, columns=tickers).values
        feats.append(mat)
    features_raw = np.stack(feats, axis=-1).astype(np.float32)  # (T,N,F)
    features = cross_sectional_zscore(features_raw)

    tradable_mask = (~np.isnan(close_mat.values)) & np.isfinite(close_mat.values)

    # sectors kept for signature compatibility (flat policy ignores)
    if "GICS_Sector" in df.columns:
        sector_series = (df.groupby(["ticker","GICS_Sector"]).size().reset_index(name="n")
                           .sort_values(["ticker","n"], ascending=[True, False])
                           .drop_duplicates(subset=["ticker"]).set_index("ticker")["GICS_Sector"]
                           .reindex(tickers))
        sector_ids = pd.Categorical(sector_series).codes
        if (sector_ids < 0).any():
            max_id = sector_ids[sector_ids >= 0].max() if (sector_ids >= 0).any() else -1
            sector_ids = np.where(sector_ids < 0, max_id + 1, sector_ids)
        num_sectors = int(sector_ids.max() + 1) if len(sector_ids) else 1
    else:
        sector_ids = np.zeros(len(tickers), dtype=np.int64)
        num_sectors = 1

    T, N, Fdim = features.shape
    if T <= window:
        raise ValueError(f"Not enough rows for window={window}. Got T={T}.")

    return dict(
        prices_rel=prices_rel, features=features, tradable_mask=tradable_mask.astype(bool),
        sector_ids=sector_ids.astype(np.int64), num_sectors=num_sectors, N=N, Fdim=Fdim, T=T
    )
