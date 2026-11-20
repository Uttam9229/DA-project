"""
UI-07: Time & Conversion Analysis
Sales Cycle Velocity, Days-to-Close, Monthly Trends & Follow-Up Latency Dynamics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.components import (
    inject_custom_styles, render_page_header, render_sidebar_metadata,
    render_kpi_card, render_alert_banner, apply_global_filters
)
from src.data_loader import get_clean_data
from src.analysis import calculate_time_metrics
from src.visualization import create_conversion_trend_chart, create_time_to_convert_chart

st.set_page_config(page_title="Time & Conversion Analysis | Lead Funnel", page_icon="⏱️", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

df_clean, _ = get_clean_data()
df_filtered = apply_global_filters(df_clean)

render_page_header(
    title="Time & Sales Cycle Velocity Analysis",
    subtitle="Lead Maturation Latency, Days-to-Close Dynamics, Follow-Up Response Times & Temporal Trends",
    badge="Temporal Dynamics"
)

if len(df_filtered) == 0:
    st.warning("No lead data matches the current filter settings.")
    st.stop()

time_info = calculate_time_metrics(df_filtered)
monthly_df = time_info["monthly_trends"]
conv_df = df_filtered[df_filtered["is_converted"] == 1]

avg_cycle = time_info["avg_cycle_days"]
med_cycle = time_info["median_cycle_days"]
avg_resp = df_filtered["response_time_days"].mean()

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Mean Sales Cycle", f"{avg_cycle} Days", "Creation to Signature", trend="neutral", icon="⏱️")
with c2:
    render_kpi_card("Median Sales Cycle", f"{med_cycle} Days", "Robust against outliers", trend="neutral", icon="📊")
with c3:
    render_kpi_card("Mean Initial Response", f"{avg_resp:.1f} Days", "Inflow to Rep Contact", trend="up", icon="📞")
with c4:
    fastest_close = conv_df["conversion_time_days"].min() if len(conv_df) > 0 else 0
    render_kpi_card("Fastest Closed Deal", f"{int(fastest_close)} Days", "Maximum Closure Velocity", trend="up", icon="⚡")

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Main Monthly Inbound & Conversion Trajectory
st.markdown("### 📈 Monthly Inbound Volume & Conversion Trajectory")
fig_trend = create_conversion_trend_chart(monthly_df)
st.plotly_chart(fig_trend, use_container_width=True)

# Row 2: Days to Close by Acquisition Source & Follow-up Speed vs Conversion
col_source_box, col_resp_dist = st.columns([7, 5])

with col_source_box:
    fig_box = create_time_to_convert_chart(df_filtered)
    st.plotly_chart(fig_box, use_container_width=True)

with col_resp_dist:
    # Response Time Cohorts
    df_filtered["resp_cohort"] = pd.cut(
        df_filtered["response_time_days"],
        bins=[-1, 2, 4, 10],
        labels=["Fast (< 48 hrs)", "Medium (2-4 days)", "Delayed (> 4 days)"]
    )
    cohort_summary = df_filtered.groupby("resp_cohort", observed=False).agg(
        leads=("lead_id", "count"),
        conversions=("is_converted", "sum")
    ).reset_index()
    cohort_summary["conversion_rate_pct"] = cohort_summary.apply(
        lambda r: round((r["conversions"] / r["leads"] * 100.0) if r["leads"] > 0 else 0.0, 1), axis=1
    )
    
    fig_cohort = px.bar(
        cohort_summary,
        x="resp_cohort",
        y="conversion_rate_pct",
        text=[f"{r}% ({c} won)" for r, c in zip(cohort_summary["conversion_rate_pct"], cohort_summary["conversions"])],
        title="<b>Conversion Rate by Initial Response Latency</b>",
        labels={"resp_cohort": "Response Speed Cohort", "conversion_rate_pct": "Win Rate (%)"},
        color="conversion_rate_pct",
        color_continuous_scale="Purples"
    )
    fig_cohort.update_layout(yaxis={"range": [0, 50], "gridcolor": "#F1F5F9"}, showlegend=False)
    st.plotly_chart(fig_cohort, use_container_width=True)

# Monthly Summary Table
st.markdown("### 📋 Monthly Commercial Trajectory Table")
st.dataframe(
    monthly_df.style.format({
        "total_leads": "{:,}",
        "converted_leads": "{:,}",
        "total_revenue": "₹{:,.0f}",
        "conversion_rate_pct": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)
