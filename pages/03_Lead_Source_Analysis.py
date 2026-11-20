"""
UI-03: Lead Source Analysis
Marketing Acquisition Channels, Conversion Efficiency, Revenue Attribution & Source Ranking
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.components import (
    inject_custom_styles, render_page_header, render_sidebar_metadata,
    render_kpi_card, render_alert_banner, apply_global_filters
)
from src.data_loader import get_clean_data
from src.analysis import calculate_source_performance
from src.visualization import create_source_performance_chart

st.set_page_config(page_title="Lead Source Analysis | Lead Funnel", page_icon="🌐", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

df_clean, _ = get_clean_data()
df_filtered = apply_global_filters(df_clean)

render_page_header(
    title="Lead Source Analysis",
    subtitle="Comparative Diagnostics across Inbound, Outbound, Referral, and Organic Acquisition Channels",
    badge="Channel Attribution"
)

source_df = calculate_source_performance(df_filtered)

if len(source_df) == 0:
    st.warning("No lead data matches the current filter settings.")
    st.stop()

# Highlights
best_source = source_df.iloc[0]
highest_rev_source = source_df.sort_values(by="total_revenue_inr", ascending=False).iloc[0]

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Top Converting Source", best_source["source_name"], f"{best_source['conversion_rate_pct']}% Conversion Rate", trend="up", icon="🥇")
with c2:
    render_kpi_card("Highest Revenue Source", highest_rev_source["source_name"], f"₹{highest_rev_source['total_revenue_inr']:,.0f} Total Closed", trend="up", icon="💰")
with c3:
    render_kpi_card("Active Acquisition Channels", f"{len(source_df)} Channels", "Inbound, Outbound, Organic", icon="🌐")
with c4:
    total_src_leads = source_df["total_leads"].sum()
    render_kpi_card("Total Source Inflow", f"{total_src_leads:,} Leads", f"{source_df['converted_leads'].sum():,} Total Converted", icon="📥")

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Row 1: Source Performance Chart & Volume Breakdown
col_chart, col_vol = st.columns([7, 5])

with col_chart:
    fig_conv = create_source_performance_chart(source_df)
    st.plotly_chart(fig_conv, use_container_width=True)

with col_vol:
    fig_pie = px.pie(
        source_df,
        values="total_leads",
        names="source_name",
        title="<b>Inbound Lead Share by Acquisition Channel</b>",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_pie.update_layout(
        font={"family": "Inter, sans-serif"},
        legend={"orientation": "h", "y": -0.2, "x": 0.5, "xanchor": "center"},
        margin={"l": 20, "r": 20, "t": 40, "b": 20}
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Row 2: Revenue Contribution & Average Lead Quality Score
col_rev, col_score = st.columns([6, 6])

with col_rev:
    fig_rev = px.bar(
        source_df.sort_values(by="total_revenue_inr", ascending=True),
        x="total_revenue_inr",
        y="source_name",
        orientation="h",
        text="total_revenue_inr",
        labels={"total_revenue_inr": "Total Closed Revenue (₹)", "source_name": ""},
        color="total_revenue_inr",
        color_continuous_scale="Viridis"
    )
    fig_rev.update_traces(texttemplate="₹%{x:,.0f}", textposition="outside")
    fig_rev.update_layout(
        title="<b>Total Closed Revenue by Acquisition Source (₹)</b>",
        xaxis={"gridcolor": "#F1F5F9"},
        showlegend=False
    )
    st.plotly_chart(fig_rev, use_container_width=True)

with col_score:
    fig_score = px.bar(
        source_df.sort_values(by="avg_lead_score", ascending=True),
        x="avg_lead_score",
        y="source_name",
        orientation="h",
        text="avg_lead_score",
        labels={"avg_lead_score": "Average Lead Score (1-100)", "source_name": ""},
        color="avg_lead_score",
        color_continuous_scale="Purples"
    )
    fig_score.update_traces(texttemplate="%{x:.1f} pts", textposition="outside")
    fig_score.update_layout(
        title="<b>Average Lead Quality Score by Source (1 - 100)</b>",
        xaxis={"range": [0, 100], "gridcolor": "#F1F5F9"},
        showlegend=False
    )
    st.plotly_chart(fig_score, use_container_width=True)

# Source Effectiveness Ranking Matrix
st.markdown("### 🏆 Comprehensive Acquisition Channel Scorecard")
display_df = source_df.copy()
display_df.columns = [
    "Source Name", "Channel Type", "Total Inflow Leads", "Converted Leads",
    "Conversion Rate (%)", "Total Revenue (₹)", "Avg Deal Size (₹)", "Avg Lead Score"
]

st.dataframe(
    display_df.style.format({
        "Total Inflow Leads": "{:,}",
        "Converted Leads": "{:,}",
        "Conversion Rate (%)": "{:.2f}%",
        "Total Revenue (₹)": "₹{:,.0f}",
        "Avg Deal Size (₹)": "₹{:,.0f}",
        "Avg Lead Score": "{:.1f}"
    }),
    use_container_width=True,
    hide_index=True
)
