"""
Test Suite: Aggregation Analysis and Insights Generation
"""

import pytest
import pandas as pd
from src.analysis import (
    calculate_source_performance, calculate_sales_rep_performance,
    calculate_time_metrics, generate_business_insights
)

def test_source_performance():
    data = [
        {"source_name": "Website", "channel_type": "Inbound", "is_converted": 1, "deal_value_inr": 200000.0, "lead_score": 80},
        {"source_name": "Website", "channel_type": "Inbound", "is_converted": 0, "deal_value_inr": None, "lead_score": 50},
        {"source_name": "Referrals", "channel_type": "Referral", "is_converted": 1, "deal_value_inr": 300000.0, "lead_score": 90},
    ]
    df = pd.DataFrame(data)
    src_df = calculate_source_performance(df)
    
    assert len(src_df) == 2
    # Referrals: 1/1 = 100% conversion
    ref_row = src_df[src_df["source_name"] == "Referrals"].iloc[0]
    assert ref_row["conversion_rate_pct"] == 100.0
    assert ref_row["total_revenue_inr"] == 300000.0
    
    # Website: 1/2 = 50% conversion
    web_row = src_df[src_df["source_name"] == "Website"].iloc[0]
    assert web_row["conversion_rate_pct"] == 50.0

def test_sales_rep_performance():
    data = [
        {"rep_name": "Aarav Sharma", "rep_region": "North", "rep_experience": 4, "is_converted": 1, "deal_value_inr": 250000.0, "response_time_days": 1.5, "funnel_stage": "Converted"},
        {"rep_name": "Aarav Sharma", "rep_region": "North", "rep_experience": 4, "is_converted": 0, "deal_value_inr": None, "response_time_days": 2.0, "funnel_stage": "Qualified"},
    ]
    df = pd.DataFrame(data)
    rep_df = calculate_sales_rep_performance(df)
    
    assert len(rep_df) == 1
    row = rep_df.iloc[0]
    assert row["rep_name"] == "Aarav Sharma"
    assert row["assigned_leads"] == 2
    assert row["converted_leads"] == 1
    assert row["conversion_rate_pct"] == 50.0
    assert row["revenue_inr"] == 250000.0
