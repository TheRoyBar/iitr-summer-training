import json
from crewai.tools import tool


@tool("Detect ML Problem Type")
def detect_problem_type(description: str) -> str:
    """Guess the ML problem type from a plain description."""
    text = description.lower()
    if "churn" in text or "will buy" in text or "fraud" in text:
        return json.dumps({"problem_type": "classification"})
    if "demand" in text or "sales" in text or "revenue" in text or "price" in text:
        return json.dumps({"problem_type": "regression"})
    if "segment" in text or "group" in text:
        return json.dumps({"problem_type": "clustering"})
    return json.dumps({"problem_type": "unclear, ask a follow up question"})


@tool("Suggest Features")
def suggest_features(context: str) -> str:
    """Suggest a handful of features for a retail ML problem."""
    return json.dumps({
        "features": [
            "days since last purchase",
            "average basket value last 90 days",
            "number of store visits last 30 days",
            "discount sensitivity score",
            "category diversity of past purchases",
        ]
    })


@tool("Flag Data Risks")
def flag_data_risks(context: str) -> str:
    """List common data risks to check before training a model."""
    return json.dumps({
        "risks": [
            "class imbalance if churn rate is low",
            "seasonality not captured in a short training window",
            "leakage from features computed after the outcome date",
            "store level differences not accounted for",
        ]
    })


@tool("Recommend Metrics")
def recommend_metrics(problem_type: str) -> str:
    """Recommend evaluation metrics for a given problem type."""
    table = {
        "classification": ["precision", "recall", "F1", "ROC-AUC"],
        "regression": ["RMSE", "MAE", "MAPE"],
        "clustering": ["silhouette score", "inertia"],
    }
    metrics = table.get(problem_type.strip().lower(), ["accuracy"])
    return json.dumps({"problem_type": problem_type, "metrics": metrics})
