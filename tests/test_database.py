"""
Test Suite: Database Connectivity, Schema Integrity, and Table Loading
"""

import os
import pytest
import sqlite3
import pandas as pd
from src.database import get_db_path, get_db_connection, load_raw_tables, load_merged_lead_data

def test_database_file_exists():
    db_path = get_db_path()
    assert os.path.exists(db_path), f"Database not found at {db_path}"

def test_database_connection():
    conn = get_db_connection()
    assert isinstance(conn, sqlite3.Connection)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    assert "fact_leads" in tables
    assert "dim_lead_sources" in tables
    assert "dim_campaigns" in tables
    assert "dim_sales_reps" in tables

def test_load_raw_tables():
    df_leads, df_sources, df_campaigns, df_reps = load_raw_tables()
    
    assert len(df_leads) >= 150 and len(df_leads) <= 300
    assert len(df_sources) == 7
    assert len(df_campaigns) >= 5
    assert len(df_reps) >= 5

def test_load_merged_lead_data():
    df_merged = load_merged_lead_data()
    assert len(df_merged) >= 150
    assert "source_name" in df_merged.columns
    assert "campaign_name" in df_merged.columns
    assert "rep_name" in df_merged.columns
    assert "lead_score" in df_merged.columns
    assert "funnel_stage" in df_merged.columns
