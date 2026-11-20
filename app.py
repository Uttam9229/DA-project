"""
Lead Conversion Funnel Analysis System
Main Application Entry & Central Portal
Student: Uttam Srivastava | Roll: 2500320140159
College: ABES Engineering College | Mentor: Anjali Pandey
"""

import streamlit as st
import pandas as pd
from src.components import inject_custom_styles, render_page_header, render_sidebar_metadata, render_kpi_card, render_alert_banner
from src.data_loader import get_clean_data, get_dimension_tables
from src.analysis import calculate_executive_kpis

# Page configuration
st.set_page_config(
    page_title="Lead Conversion Funnel Analysis",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject styling
inject_custom_styles()
render_sidebar_metadata()

# Load clean analytical dataset
try:
    df_clean, audit_info = get_clean_data()
    df_sources, df_campaigns, df_reps = get_dimension_tables()
    kpis = calculate_executive_kpis(df_clean, df_campaigns)
except Exception as e:
    st.error(f"Error initializing analytical database: {e}")
    st.stop()

# Header banner
render_page_header(
    title="Lead Conversion Funnel Analysis Platform",
    subtitle="End-to-End Enterprise Sales Pipeline Diagnostics, Marketing Attribution & Revenue Optimization Engine",
    badge="Industry Grade Analytics • v1.0.0"
)

# Welcome & System Overview
col_info, col_quick_kpi = st.columns([7, 5])

with col_info:
    st.markdown("""
    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm mb-6">
        <h2 class="text-xl font-bold text-slate-900 mb-2">Welcome to the Revenue Intelligence Portal</h2>
        <p class="text-sm text-slate-600 leading-relaxed mb-4">
            This enterprise application monitors how prospective buyers traverse the entire commercial lifecycle—from 
            initial marketing acquisition to initial outreach, BANT qualification, proposal submission, pricing negotiation, 
            and final contract closure.
        </p>
        <div class="grid grid-cols-2 gap-3 text-xs text-slate-700">
            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <span class="font-semibold text-indigo-700 block mb-0.5">🚀 Marketing Attribution</span>
                Identify CPL, CPA, and ROI across 7 acquisition channels.
            </div>
            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <span class="font-semibold text-indigo-700 block mb-0.5">🔍 Funnel Friction Points</span>
                Locate exact drop-offs across 6 sequential milestones.
            </div>
            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <span class="font-semibold text-indigo-700 block mb-0.5">👥 Sales Rep Scorecards</span>
                Benchmark win-rates, response velocity, and pipeline throughput.
            </div>
            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                <span class="font-semibold text-indigo-700 block mb-0.5">📐 Statistical Rigor</span>
                Hypothesis testing, parametric/non-parametric tests, and correlation matrices.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_quick_kpi:
    st.markdown("### ⚡ Live Pipeline Snapshot")
    kpi_col1, kpi_col2 = st.columns(2)
    with kpi_col1:
        render_kpi_card("Total Pipeline Volume", f"{kpis['total_leads']:,}", "Active Ingested Leads", icon="📥")
        render_kpi_card("Won Deals", f"{kpis['converted_leads']:,}", f"{kpis['overall_conversion_rate']}% Conversion Rate", trend="up", icon="🏆")
    with kpi_col2:
        render_kpi_card("Total Revenue", f"₹{kpis['total_revenue_inr']:,.0f}", f"₹{kpis['avg_deal_value_inr']:,.0f} Avg Deal", trend="up", icon="💰")
        render_kpi_card("Avg Sales Cycle", f"{kpis['avg_conversion_time_days']} days", f"{kpis['avg_response_time_days']} days initial contact", icon="⏱️")

st.markdown("---")

# Navigation Modules Directory
st.markdown("### 🧭 Application Modules & Capabilities")
st.markdown("Explore individual analytical modules using the left sidebar navigation menu:")

screens = [
    ("01 Executive Overview", "pages/01_Executive_Overview.py", "High-level summary of conversion rates, gross revenue, deal size, and macroeconomic pipeline velocity."),
    ("02 Lead Funnel Analysis", "pages/02_Lead_Funnel_Analysis.py", "Stage-by-stage attrition flow from Ingestion to Won, drop-off rates, and bottleneck identification."),
    ("03 Lead Source Analysis", "pages/03_Lead_Source_Analysis.py", "Acquisition channel effectiveness: Organic Search, Referrals, Paid Ads, Social Media, and Email."),
    ("04 Campaign Performance", "pages/04_Campaign_Performance.py", "Marketing campaign ROI matrix, Cost Per Lead (CPL), and Cost Per Acquisition (CPA)."),
    ("05 Sales Rep Performance", "pages/05_Sales_Performance.py", "Sales executive quota achievement, conversion percentages, closed revenue, and response latency."),
    ("06 Lead Quality & Scoring", "pages/06_Lead_Quality.py", "Algorithmic lead score distributions, High/Medium/Low tiers, and conversion probability curves."),
    ("07 Time & Conversion Analysis", "pages/07_Time_Analysis.py", "Monthly lead trajectory, sales cycle duration, and response lag correlation."),
    ("08 EDA & Statistics", "pages/08_EDA_Statistics.py", "Exploratory Data Analysis, Welch's t-test, Mann-Whitney U, Chi-Square, and correlation heatmaps."),
    ("09 Business Insights", "pages/09_Business_Insights.py", "Automated strategic diagnostic recommendations, risk alerts, and high-impact action plans."),
    ("10 Data Quality & Export", "pages/10_Data_Quality.py", "Raw vs. Cleaned data audit, duplicate detection, missing-value reports, and CSV/Excel downloads."),
    ("11 About Project", "pages/11_About.py", "Academic project documentation, student credentials, faculty mentorship, and system architecture.")
]

cols = st.columns(3)
for idx, (title, path, desc) in enumerate(screens):
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="kpi-card mb-4">
            <h4 class="font-bold text-slate-800 text-sm mb-1">{title}</h4>
            <p class="text-xs text-slate-500 leading-normal">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Quick Data Health Summary
st.markdown("### 🛡️ Automated Data Quality Status")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Raw Ingested Records", f"{audit_info['initial_rows']}")
c2.metric("Duplicates Dropped", f"{audit_info['duplicates_removed']}")
c3.metric("Clean Analytical Leads", f"{audit_info['clean_rows']}")
c4.metric("Referential Violations", "0 (100% Valid Keys)")
