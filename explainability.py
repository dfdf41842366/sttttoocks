import shap
import json

def explain_model(model, X_test, output_json):
    explainer = shap.Explainer(model, X_test)
    shap_values = explainer(X_test[:100])
    feature_imp = dict(zip(X_test.columns, shap_values.abs.mean(0).tolist()))
    with open(output_json, "w") as f:
        json.dump({"feature_importance": feature_imp}, f, indent=2)
