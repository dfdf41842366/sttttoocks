import os
import json
import requests
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "../config/data_sources.json")) as fp:
    CONFIG = json.load(fp)
OUTPUT_DIR = os.path.join(BASE, "../data/raw/news/")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ingest():
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    for ticker in CONFIG["tickers"]:
        url = f"https://newsapi.org/v2/everything"
        params = {
            "q": ticker,
            "from": seven_days_ago,
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": CONFIG["newsapi_key"]
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        articles = r.json().get("articles", [])
        outpath = os.path.join(OUTPUT_DIR, f"{ticker}_news.json")
        with open(outpath, "w") as f:
            json.dump(articles, f, indent=2)
        print(f"Saved news for {ticker}: {outpath}")

if __name__ == "__main__":
    ingest()
