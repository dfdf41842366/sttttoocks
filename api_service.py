import os
import json
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from risk.risk_filter import filter_and_log

REGISTRY_DIR = Path(__file__).parent.parent / "registry"
MODEL_FILE = REGISTRY_DIR / "lightgbm_model.pkl"
META_FILE = REGISTRY_DIR / "registry.json"

class InputFeatures(BaseModel):
    features: dict

app = FastAPI(title="Small Cap Inference API")

def load_model():
    if not MODEL_FILE.exists():
        raise RuntimeError("Model file missing.")
    return joblib.load(MODEL_FILE)

def load_meta():
    if not META_FILE.exists():
        raise RuntimeError("Registry metadata missing.")
    return json.load(open(META_FILE))

model = load_model()
meta = load_meta()

@app.post("/predict")
def predict(input: InputFeatures):
    try:
        X = pd.DataFrame([input.features])
        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0,1]
        issues = filter_and_log(int(pred), float(proba), input.features)
        return {
            "prediction": int(pred),
            "probability": float(proba),
            "risk_issues": issues,
            "model_info": {
                "accuracy": meta["accuracy"],
                "algo": meta["algo"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
