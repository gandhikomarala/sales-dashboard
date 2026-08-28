"""ApexSales 360 - Enterprise Revenue Intelligence & Analytics Backend Engine."""
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import math
import random
import time

app = FastAPI(
    title="ApexSales 360 Analytics Engine",
    version="5.0.0",
    description="High-throughput revenue intelligence, MRR/ARR waterfall forecasting, cohort analytics, and sales pipeline optimization."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "ApexSales 360 Revenue Engine",
        "version": "5.0.0",
        "data_freshness_seconds": 12,
        "active_streams": 4,
        "currency_base": "USD"
    }

@app.get("/api/revenue/summary")
def get_revenue_summary():
    return {
        "arr_total_usd": 14_850_000,
        "mrr_current_usd": 1_237_500,
        "mrr_growth_pct": 14.8,
        "nrr_retention_pct": 118.4,
        "arpu_usd": 4_250,
        "cac_payback_months": 8.2,
        "ltv_to_cac_ratio": 4.6,
        "active_customers": 3494,
        "gross_margin_pct": 82.5
    }

@app.get("/api/revenue/trends")
def get_revenue_trends():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    base_mrr = 950_000
    records = []
    for idx, m in enumerate(months, start=1):
        mrr = round(base_mrr * (1 + 0.025 * idx + random.uniform(-0.01, 0.02)), 2)
        new_business = round(mrr * 0.12, 2)
        expansion = round(mrr * 0.06, 2)
        churn = round(mrr * 0.018, 2)
        records.append({
            "month": m,
            "mrr": mrr,
            "new_business": new_business,
            "expansion": expansion,
            "churn": churn,
            "net_growth": round(new_business + expansion - churn, 2)
        })
    return {"timeframe": "2026 Fiscal Year", "trends": records}

@app.get("/api/pipeline/stages")
def get_pipeline_stages():
    return {
        "total_pipeline_value_usd": 38_450_000,
        "weighted_forecast_usd": 24_120_000,
        "stages": [
            {"stage": "1. Discovery & Qualification", "deals": 142, "value_usd": 8_520_000, "win_prob_pct": 20},
            {"stage": "2. Demo & Technical Validation", "deals": 98, "value_usd": 11_400_000, "win_prob_pct": 45},
            {"stage": "3. Security & Legal Review", "deals": 64, "value_usd": 9_600_000, "win_prob_pct": 75},
            {"stage": "4. Contract & Negotiation", "deals": 36, "value_usd": 8_930_000, "win_prob_pct": 90},
            {"stage": "5. Closed Won (YTD)", "deals": 218, "value_usd": 14_850_000, "win_prob_pct": 100}
        ]
    }

@app.get("/api/reps/leaderboard")
def get_reps_leaderboard():
    return {
        "reps": [
            {"id": "rep-01", "name": "Sarah Jenkins", "region": "North America", "quota_attainment_pct": 142, "closed_won_usd": 2_840_000, "deals_won": 28, "win_rate_pct": 44},
            {"id": "rep-02", "name": "Marcus Vance", "region": "EMEA", "quota_attainment_pct": 128, "closed_won_usd": 2_560_000, "deals_won": 24, "win_rate_pct": 39},
            {"id": "rep-03", "name": "Elena Rostova", "region": "APAC", "quota_attainment_pct": 115, "closed_won_usd": 2_300_000, "deals_won": 21, "win_rate_pct": 36},
            {"id": "rep-04", "name": "David Chen", "region": "North America", "quota_attainment_pct": 98, "closed_won_usd": 1_960_000, "deals_won": 19, "win_rate_pct": 31},
            {"id": "rep-05", "name": "Ananya Sharma", "region": "LATAM & India", "quota_attainment_pct": 108, "closed_won_usd": 2_160_000, "deals_won": 22, "win_rate_pct": 35}
        ]
    }
