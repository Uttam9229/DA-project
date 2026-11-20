"""
UI-05: Sales Representative Performance
Individual Quota Attainment, Conversion Percentages, Revenue Realization & Response Latency
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.components import (
    inject_custom_styles, render_page_header, render_sidebar_metadata,
    render_kpi_card, render_alert_banner, apply_global_filters
)
from src.data_loader import get_clean_data
from src.analysis import calculate_sales_rep_performance
from src.visualization import create_sales_rep_chart

st.set_page_config(page_title="Sales Rep Performance | Lead Funnel", page_icon="👔", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

df_clean, _ = get_clean_data()
df_filtered = apply_global_filters(df_clean)

render_page_header(
    title="Sales Representative Performance Scorecard",
    subtitle="Individual Revenue Yield, Conversion Rates, Pipeline Throughput & Initial Outreach Latency",
    badge="Sales Enablement"
)

rep_df = calculate_sales_rep_performance(df_filtered)

if len(rep_df) == 0:
    st.warning("No sales representative data matching current filter criteria.")
    st.stop()

# Highlights
top_rep_rev = rep_df.iloc[0]
top_rep_rate = rep_df.sort_values(by="conversion_rate_pct", ascending=False).iloc[0]
fastest_rep = rep_df.sort_values(by="avg_response_time_days", ascending=True).iloc[0]

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Top Revenue Producer", top_rep_rev["rep_name"], f"₹{top_rep_rev['revenue_inr']:,.0f} Closed Revenue", trend="up", icon="🥇")
with c2:
    render_kpi_card("Highest Win Rate", top_rep_rate["rep_name"], f"{top_rep_rate['conversion_rate_pct']}% Conversion Rate", trend="up", icon="🎯")
with c3:
    render_kpi_card("Fastest First Outreach", fastest_rep["rep_name"], f"{fastest_rep['avg_response_time_days']} Days Avg Latency", trend="up", icon="⚡")
with c4:
    render_kpi_card("Active Sales Force", f"{len(rep_df)} Executives", "Across 4 Indian Territories", icon="👥")

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Main Revenue & Conversion Chart
fig_rep = create_sales_rep_chart(rep_df)
st.plotly_chart(fig_rep, use_container_width=True)

# Row 2: Throughput stages per Rep & Outreach Latency
col_stages, col_resp = st.columns([7, 5])

with col_stages:
    fig_stg = px.bar(
        rep_df,
        x="rep_name",
        y=["assigned_leads", "contacted_leads", "qualified_leads", "converted_leads"],
        barmode="group",
        title="<b>Sales Rep Pipeline Progression Throughput</b>",
        labels={"value": "Leads", "rep_name": "Sales Executive", "variable": "Funnel Milestone"},
        color_discrete_map={
            "assigned_leads": "#94A3B8",
            "contacted_leads": "#64748B",
            "qualified_leads": "#4F46E5",
            "converted_leads": "#10B981"
        }
    )
    fig_stg.update_layout(
        xaxis={"tickangle": -15},
        yaxis={"gridcolor": "#F1F5F9"},
        legend={"title": "", "orientation": "h", "y": -0.3, "x": 0.5, "xanchor": "center"}
    )
    st.plotly_chart(fig_stg, use_container_width=True)

with col_resp:
    fig_resp = px.scatter(
        rep_df,
        x="avg_response_time_days",
        y="conversion_rate_pct",
        size="revenue_inr",
        color="region",
        text="rep_name",
        title="<b>Response Speed vs. Win Rate Correlation</b>",
        labels={
            "avg_response_time_days": "Avg Response Time (Days)",
            "conversion_rate_pct": "Win Rate (%)",
            "region": "Territory"
        }
    )
    fig_resp.update_traces(textposition="top center")
    fig_resp.update_layout(
        xaxis={"gridcolor": "#F1F5F9"},
        yaxis={"gridcolor": "#F1F5F9"}
    )
    st.plotly_chart(fig_resp, use_container_width=True)

# Detailed Sales Rep Scorecard Table
st.markdown("### 📋 Sales Executive Benchmark Matrix")
display_rep = rep_df.copy()
display_rep.columns = [
    "Sales Executive", "Territory Region", "Experience (Yrs)", "Assigned Leads",
    "Contacted Leads", "Qualified Leads", "Converted Leads", "Conversion Rate (%)",
    "Closed Revenue (₹)", "Avg Response Time (Days)"
]

st.dataframe(
    display_rep.style.format({
        "Assigned Leads": "{:,}",
        "Contacted Leads": "{:,}",
        "Qualified Leads": "{:,}",
        "Converted Leads": "{:,}",
        "Conversion Rate (%)": "{:.2f}%",
        "Closed Revenue (₹)": "₹{:,.0f}",
        "Avg Response Time (Days)": "{:.1f} d"
    }),
    use_container_width=True,
    hide_index=True
)
