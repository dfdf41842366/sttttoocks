import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler

RAW_DIR = Path(__file__).parent.parent / "data" / "raw" / "market_data"
OUT_DIR = Path(__file__).parent.parent / "data" / "features"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_raw(ticker):
    file = RAW_DIR / f"{ticker}.csv"
    return pd.read_csv(file, index_col=0, parse_dates=True)

def clean(df):
    df = df.ffill().dropna()
    return df

def engineer_features(df):
    feats = pd.DataFrame(index=df.index)
    feats['close'] = df['Close']
    feats['returns'] = df['Close'].pct_change().fillna(0)
    feats['vol_avg20'] = df['Volume'].rolling(20).mean().fillna(method="bfill")
    feats['volatility90'] = df['Close'].rolling(90).std().fillna(method="bfill")
    feats['ma50'] = df['Close'].rolling(50).mean().fillna(method="bfill")
    feats['ma200'] = df['Close'].rolling(200).mean().fillna(method="bfill")
    feats['rsi14'] = calc_rsi(df['Close'], 14)
    feats = feats.dropna().copy()
    return feats

def calc_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

def scale(feats):
    scaled = pd.DataFrame(
        StandardScaler().fit_transform(feats),
        columns=feats.columns,
        index=feats.index
    )
    return scaled

def process_all():
    tickers = [
        f.split(".csv")[0]
        for f in os.listdir(RAW_DIR)
        if f.endswith(".csv")
    ]
    for ticker in tickers:
        df = load_raw(ticker)
        df = clean(df)
        feats = engineer_features(df)
        scaled = scale(feats)
        scaled.to_csv(OUT_DIR / f"{ticker}_features.csv")
        print(f"[{ticker}] Features saved: {OUT_DIR / f'{ticker}_features.csv'}")

if __name__ == "__main__":
    process_all()
