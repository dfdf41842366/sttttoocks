import subprocess
from pathlib import Path
import logging

BASE = Path(__file__).parent.parent
LOG_DIR = BASE / "monitoring"
LOG_DIR.mkdir(exist_ok=True)
logfile = LOG_DIR / "pipeline.log"
logging.basicConfig(filename=logfile, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def run_step(description, cmd):
    try:
        logging.info(f"Start: {description}")
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logging.info(f"Success: {description} | Output: {res.stdout.strip()}")
        print(f"\033[92m[SUCCESS]\033[0m {description}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Fail: {description} | Out: {e.output} | Err: {e.stderr}")
        print(f"\033[91m[FAILED]\033[0m {description} | {e}")
        raise

def main():
    steps = [
        ("Ingest market data", ["python", "ingestion/ingest_market_data.py"]),
        ("Ingest fundamentals", ["python", "ingestion/ingest_fundamentals.py"]),
        ("Ingest news", ["python", "ingestion/ingest_news.py"]),
        ("Feature engineering", ["python", "preprocessing/feature_engineering.py"]),
        ("Train model", ["python", "training/train_model.py"]),
        ("API smoke test", ["pytest", "tests/test_inference.py"])
    ]
    for desc, cmd in steps:
        run_step(desc, cmd)
    logging.info("Pipeline complete.")

if __name__ == "__main__":
    main()
