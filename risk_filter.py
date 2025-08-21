import json
from pathlib import Path

LOG_FILE = Path(__file__).parent / "risk_log.json"

def risk_check(prediction: int, probability: float, features: dict, rsi_limit=80, min_proba=0.6):
    issues = []
    if probability < min_proba:
        issues.append(f"Prob below threshold: {probability:.2f}")
    if features.get("rsi14", 0) > rsi_limit:
        issues.append(f"RSI overbought: {features.get('rsi14', 0)}")
    return issues

def log_flag(input_data, issues):
    entry = {
        "input": input_data,
        "issues": issues
    }
    try:
        if LOG_FILE.exists():
            with open(LOG_FILE) as f:
                data = json.load(f)
        else:
            data = []
        data.append(entry)
        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def filter_and_log(prediction: int, probability: float, features: dict):
    issues = risk_check(prediction, probability, features)
    if issues:
        log_flag({"prediction": prediction, "probability": probability, "features": features}, issues)
    return issues

if __name__ == "__main__":
    test = {'rsi14': 85, 'returns': 0.04, 'vol_avg20': 2e6, 'volatility90': 2.5, 'ma50': 11, 'ma200': 12}
    prediction = 1
    proba = 0.62
    flagged = filter_and_log(prediction, proba, test)
    print(f"Risk issues: {flagged}")
