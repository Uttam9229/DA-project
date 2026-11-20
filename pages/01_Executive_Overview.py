"""
UI-01: Executive Overview
High-Level Strategic Pipeline Health, Revenue Realization & Conversion Velocity
"""

import streamlit as st
import pandas as pd
from src.components import (
    inject_custom_styles, render_page_header, render_sidebar_metadata,
    render_kpi_card, render_alert_banner, apply_global_filters
)
from src.data_loader import get_clean_data, get_dimension_tables
from src.analysis import (
    calculate_executive_kpis, calculate_funnel_stages,
    calculate_source_performance, calculate_time_metrics
)
from src.visualization import (
    create_funnel_chart, create_conversion_trend_chart,
    create_source_performance_chart
)

st.set_page_config(page_title="Executive Overview | Funnel Analytics", page_icon="📈", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

df_clean, audit_info = get_clean_data()
df_sources, df_campaigns, df_reps = get_dimension_tables()

# Apply global filters
df_filtered = apply_global_filters(df_clean)

render_page_header(
    title="Executive Overview",
    subtitle="Macro-Level Commercial Revenue Health, Funnel Velocity & Channel Attribution Snapshot",
    badge="Executive Dashboard"
)

# Compute KPIs
kpis = calculate_executive_kpis(df_filtered, df_campaigns)

# Row 1: Primary Executive KPI Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Total Leads Ingested", f"{kpis['total_leads']:,}", "Top of Sales Funnel", icon="📥")
with c2:
    render_kpi_card("Qualified Leads", f"{kpis['qualified_leads']:,}", f"{kpis['lead_qualification_rate']}% Qualification Rate", trend="up", icon="🎯")
with c3:
    render_kpi_card("Converted Deals", f"{kpis['converted_leads']:,}", f"{kpis['overall_conversion_rate']}% Conversion Rate", trend="up", icon="🏆")
with c4:
    render_kpi_card("Total Converted Revenue", f"₹{kpis['total_revenue_inr']:,.0f}", f"₹{kpis['avg_deal_value_inr']:,.0f} Avg Deal Size", trend="up", icon="💰")

# Row 2: Secondary Velocity & Marketing Cards
c5, c6, c7, c8 = st.columns(4)
with c5:
    render_kpi_card("Overall Conversion Rate", f"{kpis['overall_conversion_rate']}%", "Won Deals / Total Inflow", trend="up", icon="📊")
with c6:
    render_kpi_card("Lead Qualification Rate", f"{kpis['lead_qualification_rate']}%", "Qualified / Total Inflow", trend="neutral", icon="⭐")
with c7:
    render_kpi_card("Avg Conversion Cycle", f"{kpis['avg_conversion_time_days']} Days", "Creation to Signature", trend="neutral", icon="⏱️")
with c8:
    render_kpi_card("Avg Initial Contact Lag", f"{kpis['avg_response_time_days']} Days", "Inflow to Rep Contact", trend="neutral", icon="📞")

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Strategic Highlights Banner
if kpis['converted_leads'] > 0:
    render_alert_banner(
        title="Executive Strategic Summary",
        message=(
            f"The current pipeline has realized ₹{kpis['total_revenue_inr']:,.0f} across {kpis['converted_leads']} closed transactions "
            f"from {kpis['total_leads']} inbound inquiries ({kpis['overall_conversion_rate']}% conversion rate). "
            f"Average time to close stands at {kpis['avg_conversion_time_days']} days, with sales reps initiating contact within an average of {kpis['avg_response_time_days']} days."
        ),
        level="success"
    )

# Visualizations Row: Funnel Overview & Conversion Trend
col_funnel, col_trend = st.columns([6, 6])

with col_funnel:
    stages_df = calculate_funnel_stages(df_filtered)
    fig_funnel = create_funnel_chart(stages_df)
    st.plotly_chart(fig_funnel, use_container_width=True)

with col_trend:
    time_metrics = calculate_time_metrics(df_filtered)
    fig_trend = create_conversion_trend_chart(time_metrics["monthly_trends"])
    st.plotly_chart(fig_trend, use_container_width=True)

# Secondary Row: Lead Source Performance
st.markdown("### 🌐 Acquisition Channel Conversion Efficiency")
col_src_chart, col_src_table = st.columns([6, 6])

with col_src_chart:
    src_df = calculate_source_performance(df_filtered)
    fig_src = create_source_performance_chart(src_df)
    st.plotly_chart(fig_src, use_container_width=True)

with col_src_table:
    st.markdown("#### Channel Performance Matrix")
    if len(src_df) > 0:
        display_src = src_df[["source_name", "channel_type", "total_leads", "converted_leads", "conversion_rate_pct", "total_revenue_inr"]].copy()
        display_src.columns = ["Channel", "Type", "Leads", "Won", "Win Rate (%)", "Revenue (INR ₹)"]
        st.dataframe(
            display_src.style.format({
                "Leads": "{:,}",
                "Won": "{:,}",
                "Win Rate (%)": "{:.1f}%",
                "Revenue (INR ₹)": "₹{:,.0f}"
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No lead data matches the current filter selection.")
