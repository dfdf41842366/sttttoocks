import os
import json
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "../config/data_sources.json")) as fp:
    CONFIG = json.load(fp)
OUTPUT_DIR = os.path.join(BASE, "../data/raw/fundamentals/")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ingest():
    for ticker in CONFIG["tickers"]:
        url = (
            f"https://financialmodelingprep.com/api/v3/profile/{ticker}"
            f"?apikey={CONFIG['fmp_api_key']}"
        )
        r = requests.get(url)
        r.raise_for_status()
        outpath = os.path.join(OUTPUT_DIR, f"{ticker}_fundamentals.json")
        with open(outpath, "w") as f:
            json.dump(r.json(), f, indent=2)
        print(f"Saved: {outpath}")

if __name__ == "__main__":
    ingest()
