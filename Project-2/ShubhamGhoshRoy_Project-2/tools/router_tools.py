import json
from crewai.tools import tool

ANALYST_WORDS = ["sql", "dashboard", "kpi", "report", "eda", "excel", "revenue", "sales trend"]
SCIENTIST_WORDS = ["predict", "forecast", "churn", "model", "classification", "regression", "ml", "machine learning"]


@tool("Classify Retail Request")
def classify_request(request: str) -> str:
    """Guess whether a request is analyst work, scientist work, or both."""
    text = request.lower()
    hit_analyst = any(w in text for w in ANALYST_WORDS)
    hit_scientist = any(w in text for w in SCIENTIST_WORDS)

    if hit_analyst and hit_scientist:
        route = "both"
    elif hit_scientist:
        route = "scientist"
    elif hit_analyst:
        route = "analyst"
    else:
        route = "analyst"

    return json.dumps({"route": route})


@tool("Estimate Tokens")
def estimate_tokens(text: str) -> str:
    """Rough token count estimate, about 4 characters per token."""
    if not text:
        count = 0
    else:
        count = max(1, len(text) // 4)
    return json.dumps({"chars": len(text or ""), "approx_tokens": count})
