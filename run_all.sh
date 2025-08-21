#!/bin/bash
set -e
python ingestion/ingest_market_data.py
python ingestion/ingest_fundamentals.py
python ingestion/ingest_news.py
python preprocessing/feature_engineering.py
python training/train_model.py
nohup python inference/api_service.py &
sleep 10
python tests/test_inference.py
python orchestration/pipeline_runner.py
echo "Full Pipeline Completed"
