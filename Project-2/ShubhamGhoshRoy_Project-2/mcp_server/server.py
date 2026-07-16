from mcp.server.fastmcp import FastMCP
import pandas as pd
import duckdb
import json

mcp = FastMCP("retail_analytics_mcp")


@mcp.tool()
def run_query(query: str, csv_path: str) -> str:
    """Run a read only SQL query against a local csv using DuckDB."""
    blocked = ["DELETE", "UPDATE", "DROP", "ALTER", "INSERT", "TRUNCATE", "CREATE", "MERGE"]
    if any(word in query.upper() for word in blocked):
        return json.dumps({"error": "only SELECT queries are allowed"})
    try:
        con = duckdb.connect(database=":memory:")
        con.execute(f"CREATE TABLE events AS SELECT * FROM read_csv_auto('{csv_path}')")
        out = con.execute(query).df()
        return out.to_json(orient="records")
    except Exception as err:
        return json.dumps({"error": str(err)})


@mcp.tool()
def profile_csv(csv_path: str) -> str:
    """Return row count, column names, dtypes, nulls and dupes for a csv."""
    try:
        df = pd.read_csv(csv_path)
        return json.dumps({
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "nulls": df.isnull().sum().to_dict(),
            "dupes": int(df.duplicated().sum()),
        })
    except Exception as err:
        return json.dumps({"error": str(err)})


@mcp.tool()
def check_query_safety(query: str) -> str:
    """Static check on a SQL query before it is run anywhere."""
    q = query.strip().upper()
    if not q.startswith("SELECT"):
        return json.dumps({"status": "blocked", "reason": "not read only"})
    if "LIMIT" not in q:
        return json.dumps({"status": "warning", "reason": "no LIMIT clause"})
    return json.dumps({"status": "ok"})


@mcp.tool()
def data_quality_report(csv_path: str) -> str:
    """Flag columns that look like data quality problems."""
    try:
        df = pd.read_csv(csv_path)
        constant_cols = [c for c in df.columns if df[c].nunique() <= 1]
        return json.dumps({
            "total_nulls": int(df.isnull().sum().sum()),
            "dupes": int(df.duplicated().sum()),
            "constant_columns": constant_cols,
        })
    except Exception as err:
        return json.dumps({"error": str(err)})


if __name__ == "__main__":
    mcp.run()
