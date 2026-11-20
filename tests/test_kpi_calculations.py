"""
Test Suite: KPI Mathematical Formulas and Zero-Division Safeguards
"""

import pytest
import pandas as pd
import numpy as np
from src.analysis import (
    safe_divide, calculate_executive_kpis, calculate_funnel_stages,
    calculate_source_performance, calculate_campaign_performance
)

def test_safe_divide():
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(10, 0) == 0.0
    assert safe_divide(None, 10) == 0.0
    assert safe_divide(10, None) == 0.0
    assert safe_divide(np.nan, 5) == 0.0
    assert safe_divide(5, np.nan) == 0.0
    assert safe_divide(10, 2, multiplier=100.0) == 500.0

def test_executive_kpis_empty_df():
    empty_df = pd.DataFrame(columns=[
        "lead_id", "funnel_stage", "is_converted", "deal_value_inr",
        "conversion_time_days", "response_time_days"
    ])
    kpis = calculate_executive_kpis(empty_df)
    assert kpis["total_leads"] == 0
    assert kpis["overall_conversion_rate"] == 0.0
    assert kpis["lead_qualification_rate"] == 0.0
    assert kpis["total_revenue_inr"] == 0.0
    assert kpis["avg_deal_value_inr"] == 0.0

def test_executive_kpis_normal():
    data = [
        {"lead_id": "L1", "funnel_stage": "Lead Acquisition", "is_converted": 0, "deal_value_inr": None, "conversion_time_days": None, "response_time_days": None},
        {"lead_id": "L2", "funnel_stage": "Contacted", "is_converted": 0, "deal_value_inr": None, "conversion_time_days": None, "response_time_days": 2.0},
        {"lead_id": "L3", "funnel_stage": "Qualified", "is_converted": 0, "deal_value_inr": None, "conversion_time_days": None, "response_time_days": 1.0},
        {"lead_id": "L4", "funnel_stage": "Converted", "is_converted": 1, "deal_value_inr": 200000.0, "conversion_time_days": 25.0, "response_time_days": 1.0},
    ]
    df = pd.DataFrame(data)
    kpis = calculate_executive_kpis(df)
    
    assert kpis["total_leads"] == 4
    assert kpis["converted_leads"] == 1
    assert kpis["overall_conversion_rate"] == 25.0 # 1 / 4 * 100
    assert kpis["qualified_leads"] == 2 # L3 (Qualified) + L4 (Converted)
    assert kpis["lead_qualification_rate"] == 50.0 # 2 / 4 * 100
    assert kpis["total_revenue_inr"] == 200000.0
    assert kpis["avg_deal_value_inr"] == 200000.0
    assert kpis["avg_conversion_time_days"] == 25.0

def test_funnel_stages_math():
    data = [
        {"funnel_stage": "Lead Acquisition"},
        {"funnel_stage": "Contacted"},
        {"funnel_stage": "Qualified"},
        {"funnel_stage": "Proposal"},
        {"funnel_stage": "Negotiation"},
        {"funnel_stage": "Converted"},
    ]
    df = pd.DataFrame(data)
    stages = calculate_funnel_stages(df)
    
    assert len(stages) == 6
    # Stage 0: Lead Acquisition -> all 6 leads reached
    assert stages.iloc[0]["lead_count"] == 6
    assert stages.iloc[0]["overall_retention_pct"] == 100.0
    
    # Stage 5: Converted -> 1 lead
    assert stages.iloc[5]["lead_count"] == 1
    assert round(stages.iloc[5]["overall_retention_pct"], 1) == round(1/6*100, 1)

def test_campaign_roi_formula():
    df_leads = pd.DataFrame([
        {"campaign_id": "C1", "is_converted": 1, "deal_value_inr": 300000.0},
        {"campaign_id": "C1", "is_converted": 0, "deal_value_inr": None},
    ])
    df_camps = pd.DataFrame([
        {"campaign_id": "C1", "campaign_name": "Camp 1", "budget_inr": 100000.0}
    ])
    
    res = calculate_campaign_performance(df_leads, df_camps)
    assert len(res) == 1
    row = res.iloc[0]
    assert row["total_leads"] == 2
    assert row["converted_leads"] == 1
    assert row["conversion_rate_pct"] == 50.0
    assert row["cpl_inr"] == 50000.0 # 100,000 / 2
    assert row["cpa_inr"] == 100000.0 # 100,000 / 1
    assert row["roi_pct"] == 200.0 # (300,000 - 100,000) / 100,000 * 100
