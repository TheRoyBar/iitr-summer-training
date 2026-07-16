import json
import pandas as pd
from crewai.tools import tool

KPI_LIBRARY = {
    "retail": ["Sales per store", "Basket size", "Inventory turnover", "Stockout rate", "Return rate"],
    "ecommerce": ["Conversion rate", "Average order value", "Cart abandonment rate", "Repeat purchase rate"],
    "marketing": ["Customer acquisition cost", "Campaign ROI", "Click through rate", "Email open rate"],
}


@tool("Profile Sample Data")
def profile_sample_data(file_path: str) -> str:
    """Load a csv and return a quick profile of it."""
    try:
        df = pd.read_csv(file_path)
        return json.dumps({
            "rows": len(df),
            "columns": list(df.columns),
            "nulls": df.isnull().sum().to_dict(),
            "dupes": int(df.duplicated().sum()),
        })
    except Exception as err:
        return json.dumps({"error": str(err)})


@tool("Suggest KPIs")
def suggest_kpis(area: str) -> str:
    """Suggest KPIs for a retail-related business area."""
    key = area.strip().lower()
    kpis = KPI_LIBRARY.get(key)
    if not kpis:
        kpis = ["Total revenue", "Active customers", "Conversion rate"]
    return json.dumps({"area": key, "kpis": kpis})


@tool("Check SQL Query")
def check_sql_query(query: str) -> str:
    """Basic check that a SQL query is read only before running it anywhere."""
    q = query.upper()
    bad = ["DROP", "DELETE", "UPDATE", "ALTER", "INSERT", "TRUNCATE"]
    if any(b in q for b in bad):
        return json.dumps({"ok": False, "reason": "query modifies data, blocked"})
    if not q.strip().startswith("SELECT"):
        return json.dumps({"ok": False, "reason": "not a select query"})
    warn = "SELECT *" in q
    return json.dumps({"ok": True, "warning": "uses SELECT *, consider naming columns" if warn else None})
