"""
UI-10: Data Management & Data Quality
Data Hygiene Audits, Duplicate Detection, Missing-Value Profiling & Certified Data Exports
"""

import os
import io
import streamlit as st
import pandas as pd
from src.components import (
    inject_custom_styles, render_page_header, render_sidebar_metadata,
    render_kpi_card, render_alert_banner
)
from src.database import load_raw_tables
from src.data_loader import get_clean_data

st.set_page_config(page_title="Data Quality & Export | Lead Funnel", page_icon="🛡️", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

df_clean, audit_info = get_clean_data()
df_raw_leads, df_sources, df_campaigns, df_reps = load_raw_tables()

render_page_header(
    title="Data Quality & Data Management",
    subtitle="Automated ETL Hygiene Auditing, Duplicate Record Removal, Missing-Value Imputation & Export Gateway",
    badge="Data Governance"
)

# Quality Health Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Raw Primary Records", f"{audit_info['initial_rows']:,}", "Pre-cleaning fact leads", icon="📥")
with c2:
    render_kpi_card("Duplicate Records Removed", f"{audit_info['duplicates_removed']:,}", "100% Deduplicated", trend="up", icon="✂️")
with c3:
    render_kpi_card("Extreme Outliers Clipped", f"{audit_info['deal_value_outliers_adjusted'] + audit_info['score_outliers_capped']:,}", "IQR & Domain Bound", trend="up", icon="🎯")
with c4:
    render_kpi_card("Clean Analytical Records", f"{audit_info['clean_rows']:,}", "Production Fact Table", trend="up", icon="✅")

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Tabs: Raw vs Clean, Missing Values, Duplicates & Exports
tab_preview, tab_missing, tab_dups, tab_export = st.tabs([
    "🔍 Raw vs. Clean Comparison",
    "❓ Missing Value Profile",
    "👥 Duplicate Record Audit",
    "💾 Data Export Gateway (CSV / Excel)"
])

with tab_preview:
    st.markdown("### 🔍 Raw vs. Cleaned Dataset Comparison")
    view_mode = st.radio("Select View:", ["Cleaned Analytical Dataset (Production)", "Raw Ingested Dataset (Pre-ETL)"], horizontal=True)
    
    if view_mode == "Cleaned Analytical Dataset (Production)":
        st.dataframe(df_clean.head(50), use_container_width=True)
        st.caption(f"Showing first 50 rows of {len(df_clean)} cleaned records.")
    else:
        st.dataframe(df_raw_leads.head(50), use_container_width=True)
        st.caption(f"Showing first 50 rows of {len(df_raw_leads)} raw records.")

with tab_missing:
    st.markdown("### ❓ Missing Values & Imputation Audit")
    
    raw_missing = df_raw_leads.isnull().sum()
    raw_missing_df = pd.DataFrame({
        "Attribute": raw_missing.index,
        "Missing Count (Raw)": raw_missing.values,
        "Missing % (Raw)": (raw_missing.values / len(df_raw_leads) * 100).round(2),
        "Cleaned Status / Handling": [
            "Imputed fallback" if col in ["email", "phone"] 
            else ("Naturally Null (Only populated if reached milestone)" if "date" in col or col in ["deal_value_inr", "lost_reason"] 
            else "Fully Complete")
            for col in raw_missing.index
        ]
    })
    st.dataframe(raw_missing_df[raw_missing_df["Missing Count (Raw)"] > 0], use_container_width=True, hide_index=True)

with tab_dups:
    st.markdown("### 👥 Duplicate Record Identification")
    dups_raw = df_raw_leads[df_raw_leads.duplicated(subset=["lead_id"], keep=False)]
    
    if len(dups_raw) > 0:
        render_alert_banner(
            title=f"Detected {len(dups_raw)} Duplicate Row Instances in Raw Data",
            message="These records shared identical primary keys (lead_id). The automated ETL pipeline kept the first occurrence and dropped subsequent duplicates.",
            level="warning"
        )
        st.dataframe(dups_raw.sort_values(by="lead_id"), use_container_width=True, hide_index=True)
    else:
        st.success("No duplicate records found.")

with tab_export:
    st.markdown("### 💾 Export Cleaned Analytical Data")
    st.markdown("Download production-ready, audited lead datasets for external reporting or offline model training:")

    col_csv, col_excel = st.columns(2)

    with col_csv:
        st.markdown("#### 📄 Comma-Separated Values (CSV)")
        csv_data = df_clean.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Cleaned CSV (leads_cleaned.csv)",
            data=csv_data,
            file_name="leads_cleaned.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_excel:
        st.markdown("#### 📊 Microsoft Excel Workbook (XLSX)")
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df_clean.to_excel(writer, sheet_name="cleaned_leads", index=False)
            df_sources.to_excel(writer, sheet_name="dim_sources", index=False)
            df_campaigns.to_excel(writer, sheet_name="dim_campaigns", index=False)
            df_reps.to_excel(writer, sheet_name="dim_sales_reps", index=False)
        excel_data = excel_buffer.getvalue()
        st.download_button(
            label="📥 Download Excel Multi-Sheet Workbook (.xlsx)",
            data=excel_data,
            file_name="leads_cleaned_workbook.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
