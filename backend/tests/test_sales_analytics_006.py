"""Pytest suite for ApexSales Revenue Analytics Module 006."""
from backend.app.main import app, get_revenue_summary, get_pipeline_stages

def test_revenue_summary_006():
    res = get_revenue_summary()
    assert res["arr_total_usd"] >= 10_000_000
    assert res["mrr_growth_pct"] > 0

def test_pipeline_stages_006():
    res = get_pipeline_stages()
    assert len(res["stages"]) == 5
    assert res["total_pipeline_value_usd"] > 0
