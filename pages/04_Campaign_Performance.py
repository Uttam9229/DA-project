"""
UI-04: Campaign Performance
Financial Attribution, Marketing ROI, Cost-Per-Lead (CPL) & Cost-Per-Acquisition (CPA)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.components import (
    inject_custom_styles, render_page_header, render_sidebar_metadata,
    render_kpi_card, render_alert_banner, apply_global_filters
)
from src.data_loader import get_clean_data, get_dimension_tables
from src.analysis import calculate_campaign_performance
from src.visualization import create_campaign_roi_chart

st.set_page_config(page_title="Campaign Performance | Lead Funnel", page_icon="📢", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

df_clean, _ = get_clean_data()
_, df_campaigns, _ = get_dimension_tables()
df_filtered = apply_global_filters(df_clean)

render_page_header(
    title="Marketing Campaign Performance & ROI",
    subtitle="Financial Return, Cost Efficiency, Cost per Lead (CPL), and Acquisition Metrics per Campaign",
    badge="Campaign Economics"
)

camp_df = calculate_campaign_performance(df_filtered, df_campaigns)

if len(camp_df) == 0:
    st.warning("No campaign data available for the active filter selection.")
    st.stop()

# Aggregate marketing KPIs
total_budget = camp_df["budget_inr"].sum()
total_rev = camp_df["revenue_inr"].sum()
total_camp_leads = camp_df["total_leads"].sum()
total_camp_won = camp_df["converted_leads"].sum()

blended_cpl = (total_budget / total_camp_leads) if total_camp_leads > 0 else 0.0
blended_cpa = (total_budget / total_camp_won) if total_camp_won > 0 else 0.0
blended_roi = ((total_rev - total_budget) / total_budget * 100.0) if total_budget > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Total Campaign Budget", f"₹{total_budget:,.0f}", f"{len(camp_df)} Active Initiatives", icon="💳")
with c2:
    render_kpi_card("Attributed Closed Revenue", f"₹{total_rev:,.0f}", f"{total_camp_won} Won Customers", trend="up", icon="💰")
with c3:
    render_kpi_card("Blended Cost per Lead (CPL)", f"₹{blended_cpl:,.0f}", "Budget / Leads Generated", icon="🎯")
with c4:
    render_kpi_card("Blended Campaign ROI", f"{blended_roi:.1f}%", f"₹{blended_cpa:,.0f} Cost per Acquisition", trend="up" if blended_roi > 0 else "down", icon="📈")

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Top & Bottom Campaign Alerts
top_camp = camp_df.iloc[0]
if top_camp["roi_pct"] > 0:
    render_alert_banner(
        title=f"Star Performer: {top_camp['campaign_name']}",
        message=(
            f"Achieved the highest Return on Investment at <b>{top_camp['roi_pct']}%</b>. "
            f"Generated ₹{top_camp['revenue_inr']:,.0f} revenue from a budget of ₹{top_camp['budget_inr']:,.0f} "
            f"({top_camp['converted_leads']} conversions at a CPA of ₹{top_camp['cpa_inr']:,.0f})."
        ),
        level="success"
    )

# Visualization 1: Budget vs Generated Revenue
st.markdown("### 📊 Budget Allocation vs. Converted Revenue")
fig_spend_rev = create_campaign_roi_chart(camp_df)
st.plotly_chart(fig_spend_rev, use_container_width=True)

# Row 2: CPL vs CPA & ROI Comparison
col_cpa, col_roi = st.columns([6, 6])

with col_cpa:
    fig_cpa = px.bar(
        camp_df.sort_values(by="cpa_inr", ascending=True),
        x="campaign_name",
        y=["cpl_inr", "cpa_inr"],
        barmode="group",
        title="<b>Cost-per-Lead (CPL) vs. Cost-per-Acquisition (CPA) (₹)</b>",
        labels={"value": "Cost (INR ₹)", "campaign_name": "Campaign", "variable": "Metric"},
        color_discrete_map={"cpl_inr": "#64748B", "cpa_inr": "#4F46E5"}
    )
    fig_cpa.update_layout(
        xaxis={"tickangle": -15},
        yaxis={"gridcolor": "#F1F5F9"},
        legend={"title": "", "orientation": "h", "y": -0.3, "x": 0.5, "xanchor": "center"}
    )
    st.plotly_chart(fig_cpa, use_container_width=True)

with col_roi:
    fig_roi = px.bar(
        camp_df.sort_values(by="roi_pct", ascending=True),
        y="campaign_name",
        x="roi_pct",
        orientation="h",
        text="roi_pct",
        title="<b>Net Campaign Return on Investment (ROI %)</b>",
        labels={"roi_pct": "ROI (%)", "campaign_name": ""},
        color="roi_pct",
        color_continuous_scale="Temps"
    )
    fig_roi.update_traces(texttemplate="%{x:.1f}%", textposition="outside")
    fig_roi.update_layout(xaxis={"gridcolor": "#F1F5F9"}, showlegend=False)
    st.plotly_chart(fig_roi, use_container_width=True)

# Comprehensive Campaign Scorecard Table
st.markdown("### 📋 Campaign Performance Matrix")
display_camp = camp_df.copy()
display_camp.columns = [
    "Campaign ID", "Campaign Name", "Allocated Budget (₹)", "Total Inflow Leads",
    "Converted Leads", "Conversion Rate (%)", "Generated Revenue (₹)",
    "Cost per Lead (₹)", "Cost per Acquisition (₹)", "Net ROI (%)"
]

st.dataframe(
    display_camp.style.format({
        "Allocated Budget (₹)": "₹{:,.0f}",
        "Total Inflow Leads": "{:,}",
        "Converted Leads": "{:,}",
        "Conversion Rate (%)": "{:.2f}%",
        "Generated Revenue (₹)": "₹{:,.0f}",
        "Cost per Lead (₹)": "₹{:,.0f}",
        "Cost per Acquisition (₹)": "₹{:,.0f}",
        "Net ROI (%)": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)
