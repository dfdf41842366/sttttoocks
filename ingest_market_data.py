import os
import json
import yfinance as yf

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "../config/data_sources.json")) as fp:
    CONFIG = json.load(fp)
OUTPUT_DIR = os.path.join(BASE, "../data/raw/market_data/")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ingest():
    for ticker in CONFIG["tickers"]:
        print(f"Downloading: {ticker}")
        data = yf.download(ticker, period="1y", interval="1d")
        outcsv = os.path.join(OUTPUT_DIR, f"{ticker}.csv")
        data.to_csv(outcsv)
        print(f"Saved: {outcsv}")

if __name__ == "__main__":
    ingest()
