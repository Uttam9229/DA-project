"""
Data Loader Module for Lead Conversion Funnel Analysis
Provides caching and clean unified DataFrame access for Streamlit and analytics scripts.
"""

import os
import pandas as pd
from typing import Tuple, Dict, Any
from src.database import load_raw_tables, load_merged_lead_data
from src.data_cleaning import clean_lead_dataset, export_cleaned_data

try:
    import streamlit as st
    cache_decorator = st.cache_data
except ImportError:
    def cache_decorator(func):
        return func

@cache_decorator
def get_clean_data() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Cached function that loads raw merged data from SQLite,
    executes data cleaning & enrichment, exports cleaned CSV/Excel,
    and returns (cleaned_dataframe, audit_dictionary).
    """
    df_raw = load_merged_lead_data()
    df_clean, audit = clean_lead_dataset(df_raw)
    
    # Save cleaned files
    try:
        export_cleaned_data(df_clean)
    except Exception as e:
        print(f"Notice: Cleaned export skipped or handled: {e}")
        
    return df_clean, audit

@cache_decorator
def get_dimension_tables():
    """Loads dimension tables: df_sources, df_campaigns, df_reps."""
    _, df_sources, df_campaigns, df_reps = load_raw_tables()
    return df_sources, df_campaigns, df_reps
