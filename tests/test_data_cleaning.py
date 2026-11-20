"""
Test Suite: Data Cleaning Pipeline, Deduplication, Outlier Handling, and Export
"""

import pytest
import pandas as pd
import numpy as np
from src.data_cleaning import clean_lead_dataset, export_cleaned_data

def test_deduplication():
    raw_data = [
        {"lead_id": "L1", "first_name": "Aarav", "lead_score": 70, "deal_value_inr": 100000.0, "funnel_stage": "Qualified", "is_converted": 0, "email": "a@b.com", "phone": "123", "creation_date": "2024-01-01", "first_contact_date": "2024-01-02", "qualification_date": "2024-01-03", "proposal_date": None, "negotiation_date": None, "conversion_date": None, "lost_reason": None},
        {"lead_id": "L1", "first_name": "Aarav", "lead_score": 70, "deal_value_inr": 100000.0, "funnel_stage": "Qualified", "is_converted": 0, "email": "a@b.com", "phone": "123", "creation_date": "2024-01-01", "first_contact_date": "2024-01-02", "qualification_date": "2024-01-03", "proposal_date": None, "negotiation_date": None, "conversion_date": None, "lost_reason": None},
        {"lead_id": "L2", "first_name": "Pooja", "lead_score": 85, "deal_value_inr": 200000.0, "funnel_stage": "Converted", "is_converted": 1, "email": None, "phone": None, "creation_date": "2024-01-01", "first_contact_date": "2024-01-02", "qualification_date": "2024-01-03", "proposal_date": "2024-01-04", "negotiation_date": "2024-01-05", "conversion_date": "2024-01-10", "lost_reason": None},
    ]
    df_raw = pd.DataFrame(raw_data)
    df_clean, audit = clean_lead_dataset(df_raw)
    
    assert audit["initial_rows"] == 3
    assert audit["duplicates_removed"] == 1
    assert audit["clean_rows"] == 2
    assert len(df_clean) == 2
    assert audit["missing_email_imputed"] == 1
    assert audit["missing_phone_imputed"] == 1
    assert df_clean.loc[df_clean["lead_id"] == "L2", "email"].iloc[0] == "contact_unavailable@domain.in"

def test_score_and_outlier_capping():
    raw_data = [
        {"lead_id": "L1", "first_name": "Rohan", "lead_score": 125, "deal_value_inr": 100000.0, "funnel_stage": "Converted", "is_converted": 1, "email": "r@b.in", "phone": "123", "creation_date": "2024-01-01", "first_contact_date": "2024-01-02", "qualification_date": "2024-01-03", "proposal_date": "2024-01-04", "negotiation_date": "2024-01-05", "conversion_date": "2024-01-10", "lost_reason": None},
        {"lead_id": "L2", "first_name": "Neha", "lead_score": -5, "deal_value_inr": 200000.0, "funnel_stage": "Contacted", "is_converted": 0, "email": "n@b.in", "phone": "123", "creation_date": "2024-01-01", "first_contact_date": "2024-01-02", "qualification_date": None, "proposal_date": None, "negotiation_date": None, "conversion_date": None, "lost_reason": None},
    ]
    df_raw = pd.DataFrame(raw_data)
    df_clean, audit = clean_lead_dataset(df_raw)
    
    # 125 should be capped to 100, -5 to 1
    assert df_clean.loc[df_clean["lead_id"] == "L1", "lead_score"].iloc[0] == 100
    assert df_clean.loc[df_clean["lead_id"] == "L2", "lead_score"].iloc[0] == 1
    assert audit["score_outliers_capped"] == 2
