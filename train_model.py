import os
import glob
import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from training.explainability import explain_model

BASE = Path(__file__).parent.parent
FEAT_DIR = BASE / "data" / "features"
REGISTRY_DIR = BASE / "registry"
REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_F = BASE / "config" / "model_config.json"

def load_data():
    dfs = []
    for file in glob.glob(str(FEAT_DIR / "*_features.csv")):
        df = pd.read_csv(file, index_col=0)
        df["ticker"] = os.path.basename(file).replace("_features.csv", "")
        dfs.append(df)
    return pd.concat(dfs, axis=0)

def build_target(df):
    df = df.copy()
    df["target"] = (df["close"].shift(-10) >= df["close"] * 1.05).astype(int)
    df = df.dropna()
    drop_cols = [c for c in ["close", "ticker"] if c in df.columns]
    X = df.drop(['target'] + drop_cols, axis=1)
    y = df["target"]
    return X, y

def train():
    cfg = json.load(open(CONFIG_F))
    df = load_data()
    X, y = build_target(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = LGBMClassifier(**cfg["params"])
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print(f"Test accuracy: {score:.3f}")
    joblib.dump(clf, REGISTRY_DIR / "lightgbm_model.pkl")
    registry = {
        "model_file": "lightgbm_model.pkl",
        "accuracy": float(score),
        "algo": cfg["algo"],
        "params": cfg["params"]
    }
    json.dump(registry, open(REGISTRY_DIR / "registry.json", "w"), indent=2)
    explain_model(clf, X_test, REGISTRY_DIR / "explainability.json")
    print(f"Model, registry, and explainability saved in {REGISTRY_DIR}")

if __name__ == "__main__":
    train()
