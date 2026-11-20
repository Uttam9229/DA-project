"""
Data Cleaning & Quality Module for Lead Conversion Funnel Analysis
Handles deduplication, missing value treatment, outlier detection, and data export.
"""

import os
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any

def clean_lead_dataset(df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Cleans raw merged lead dataset:
    1. Removes duplicate records based on lead_id
    2. Validates and bounds lead_score between 1 and 100
    3. Identifies and treats financial outliers in deal_value_inr
    4. Imputes missing textual contact values (email, phone)
    5. Calculates analytical duration columns (conversion_days, response_days)
    6. Returns cleaned DataFrame and comprehensive audit dictionary
    """
    df = df_raw.copy()
    initial_rows = len(df)
    
    # 1. Deduplication
    duplicate_count = df.duplicated(subset=["lead_id"]).sum()
    df = df.drop_duplicates(subset=["lead_id"], keep="first").reset_index(drop=True)
    post_dedup_rows = len(df)
    
    # 2. Outlier Detection & Capping
    # Score out-of-bounds capping
    score_outliers_count = ((df["lead_score"] < 1) | (df["lead_score"] > 100)).sum()
    df["lead_score"] = df["lead_score"].clip(lower=1, upper=100)
    
    # Recalculate lead quality tier if score was capped
    df.loc[df["lead_score"] >= 75, "lead_quality"] = "High"
    df.loc[(df["lead_score"] >= 50) & (df["lead_score"] < 75), "lead_quality"] = "Medium"
    df.loc[df["lead_score"] < 50, "lead_quality"] = "Low"
    
    # Deal Value IQR Outlier detection
    converted_deals = df[df["deal_value_inr"].notnull()]["deal_value_inr"]
    q1 = converted_deals.quantile(0.25)
    q3 = converted_deals.quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + (3.0 * iqr) # Extreme threshold
    deal_outliers_count = (df["deal_value_inr"] > upper_bound).sum()
    
    # Cap extreme outlier deal value to 99th percentile for stabilized analytics
    cap_val = converted_deals.quantile(0.95)
    df["deal_value_original"] = df["deal_value_inr"]
    df.loc[df["deal_value_inr"] > upper_bound, "deal_value_inr"] = cap_val
    
    # 3. Missing Value Handling
    missing_email_count = df["email"].isnull().sum()
    missing_phone_count = df["phone"].isnull().sum()
    df["email"] = df["email"].fillna("contact_unavailable@domain.in")
    df["phone"] = df["phone"].fillna("+91 00000 00000")
    
    # 4. Date formatting and time deltas
    date_cols = [
        "creation_date", "first_contact_date", "qualification_date",
        "proposal_date", "negotiation_date", "conversion_date"
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            
    # Compute Response Time (Days between creation and first contact)
    df["response_time_days"] = (df["first_contact_date"] - df["creation_date"]).dt.total_seconds() / (24 * 3600)
    df["response_time_days"] = df["response_time_days"].apply(lambda x: max(0.0, x) if pd.notnull(x) else None)
    
    # Compute Conversion Velocity (Days between creation and conversion)
    df["conversion_time_days"] = (df["conversion_date"] - df["creation_date"]).dt.total_seconds() / (24 * 3600)
    df["conversion_time_days"] = df["conversion_time_days"].apply(lambda x: max(0.0, x) if pd.notnull(x) else None)

    # Creation Month / Quarter for temporal grouping
    df["creation_month"] = df["creation_date"].dt.strftime("%Y-%m")
    df["creation_quarter"] = df["creation_date"].dt.to_period("Q").astype(str)
    
    # Ensure converted flag aligns with funnel stage
    df.loc[df["funnel_stage"] == "Converted", "is_converted"] = 1
    df.loc[df["funnel_stage"] != "Converted", "is_converted"] = 0

    # Ensure lost reason is populated for non-converted leads
    df.loc[(df["is_converted"] == 0) & (df["lost_reason"].isnull()), "lost_reason"] = "General Drop-off / Timing"
    df.loc[df["is_converted"] == 1, "lost_reason"] = "Successfully Converted"

    # Audit Dictionary
    audit = {
        "initial_rows": initial_rows,
        "duplicates_removed": duplicate_count,
        "clean_rows": post_dedup_rows,
        "score_outliers_capped": score_outliers_count,
        "deal_value_outliers_adjusted": deal_outliers_count,
        "missing_email_imputed": missing_email_count,
        "missing_phone_imputed": missing_phone_count,
        "converted_leads_count": int(df["is_converted"].sum()),
        "overall_conversion_rate": round(float(df["is_converted"].sum() / len(df) * 100), 2) if len(df) > 0 else 0.0,
        "total_revenue_inr": round(float(df["deal_value_inr"].sum()), 2),
        "avg_deal_value_inr": round(float(df[df["is_converted"] == 1]["deal_value_inr"].mean()), 2) if df["is_converted"].sum() > 0 else 0.0
    }
    
    return df, audit

def export_cleaned_data(df_clean: pd.DataFrame) -> Tuple[str, str]:
    """Exports cleaned DataFrame to CSV and Excel."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cleaned_dir = os.path.join(base_dir, "data", "cleaned")
    os.makedirs(cleaned_dir, exist_ok=True)
    
    csv_path = os.path.join(cleaned_dir, "leads_cleaned.csv")
    excel_path = os.path.join(cleaned_dir, "leads_cleaned.xlsx")
    
    # For export, convert datetime back to string
    df_export = df_clean.copy()
    for col in df_export.select_dtypes(include=["datetime64[ns]"]).columns:
        df_export[col] = df_export[col].dt.strftime("%Y-%m-%d")
        
    df_export.to_csv(csv_path, index=False)
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_export.to_excel(writer, sheet_name="cleaned_leads", index=False)
        
    return csv_path, excel_path
