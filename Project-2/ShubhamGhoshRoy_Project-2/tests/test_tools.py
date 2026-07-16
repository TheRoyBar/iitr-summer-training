import json
from tools.router_tools import classify_request
from tools.analyst_tools import suggest_kpis, check_sql_query
from tools.scientist_tools import detect_problem_type, recommend_metrics


def test_classify_request_analyst():
    result = json.loads(classify_request("can you build me a sales dashboard"))
    assert result["route"] == "analyst"


def test_classify_request_scientist():
    result = json.loads(classify_request("predict which customers will churn"))
    assert result["route"] == "scientist"


def test_suggest_kpis_known_area():
    result = json.loads(suggest_kpis("retail"))
    assert "Inventory turnover" in result["kpis"]


def test_check_sql_query_blocks_write():
    result = json.loads(check_sql_query("DROP TABLE customers"))
    assert result["ok"] is False


def test_check_sql_query_allows_select():
    result = json.loads(check_sql_query("SELECT store_id FROM events LIMIT 10"))
    assert result["ok"] is True


def test_detect_problem_type_classification():
    result = json.loads(detect_problem_type("predict which customers will churn next month"))
    assert result["problem_type"] == "classification"


def test_recommend_metrics_regression():
    result = json.loads(recommend_metrics("regression"))
    assert "RMSE" in result["metrics"]
