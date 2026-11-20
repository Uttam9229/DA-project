"""
Database Access Module for Lead Conversion Funnel Analysis
Handles SQLite connection, schema queries, and relational data extraction.
"""

import os
import sqlite3
import pandas as pd
from typing import Tuple, Dict

def get_db_path() -> str:
    """Returns absolute path to SQLite database."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_dir, "data", "lead_funnel.db")

def get_db_connection() -> sqlite3.Connection:
    """Creates and returns an active SQLite connection."""
    db_path = get_db_path()
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}. Please run dataset generation first.")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def load_raw_tables() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Loads all four raw relational tables from SQLite database."""
    conn = get_db_connection()
    try:
        df_leads = pd.read_sql("SELECT * FROM fact_leads", conn)
        df_sources = pd.read_sql("SELECT * FROM dim_lead_sources", conn)
        df_campaigns = pd.read_sql("SELECT * FROM dim_campaigns", conn)
        df_reps = pd.read_sql("SELECT * FROM dim_sales_reps", conn)
    finally:
        conn.close()
    return df_leads, df_sources, df_campaigns, df_reps

def load_merged_lead_data() -> pd.DataFrame:
    """
    Executes relational SQL JOIN across fact_leads and all dimension tables
    to produce an enriched analytical dataset.
    """
    conn = get_db_connection()
    query = """
    SELECT 
        f.lead_id,
        f.first_name,
        f.last_name,
        (f.first_name || ' ' || f.last_name) AS full_name,
        f.email,
        f.phone,
        f.city,
        f.state,
        f.source_id,
        s.source_name,
        s.channel_type,
        s.cost_category,
        f.campaign_id,
        c.campaign_name,
        c.budget_inr AS campaign_budget,
        f.rep_id,
        r.rep_name,
        r.region AS rep_region,
        r.experience_years AS rep_experience,
        f.creation_date,
        f.first_contact_date,
        f.qualification_date,
        f.proposal_date,
        f.negotiation_date,
        f.conversion_date,
        f.funnel_stage,
        f.lead_score,
        f.lead_quality,
        f.deal_value_inr,
        f.is_converted,
        f.lost_reason,
        f.industry
    FROM fact_leads f
    LEFT JOIN dim_lead_sources s ON f.source_id = s.source_id
    LEFT JOIN dim_campaigns c ON f.campaign_id = c.campaign_id
    LEFT JOIN dim_sales_reps r ON f.rep_id = r.rep_id
    """
    try:
        df = pd.read_sql(query, conn)
    finally:
        conn.close()
    return df
