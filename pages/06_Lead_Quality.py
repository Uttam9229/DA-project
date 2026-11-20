"""
UI-06: Lead Quality & Segmentation
Lead Scoring Distributions, Quality Tiers, Intent Propensity & Conversion Probability Patterns
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.components import (
    inject_custom_styles, render_page_header, render_sidebar_metadata,
    render_kpi_card, render_alert_banner, apply_global_filters
)
from src.data_loader import get_clean_data
from src.visualization import create_lead_score_distribution_chart

st.set_page_config(page_title="Lead Quality & Segmentation | Lead Funnel", page_icon="⭐", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

df_clean, _ = get_clean_data()
df_filtered = apply_global_filters(df_clean)

render_page_header(
    title="Lead Quality & Propensity Segmentation",
    subtitle="Algorithmic Lead Scoring, Qualification Tiers, Score Distributions & Conversion Likelihood",
    badge="Predictive Scoring"
)

if len(df_filtered) == 0:
    st.warning("No lead data matches the current filter settings.")
    st.stop()

# Segment metrics
tier_stats = []
for tier in ["High", "Medium", "Low"]:
    sub = df_filtered[df_filtered["lead_quality"] == tier]
    total = len(sub)
    conv = int(sub["is_converted"].sum())
    rate = (conv / total * 100.0) if total > 0 else 0.0
    tier_stats.append({
        "tier": tier,
        "count": total,
        "converted": conv,
        "rate": round(rate, 2),
        "pct_of_total": round(total / len(df_filtered) * 100.0, 1)
    })

tier_df = pd.DataFrame(tier_stats)

c1, c2, c3, c4 = st.columns(4)
high_t = tier_df[tier_df["tier"] == "High"].iloc[0]
med_t = tier_df[tier_df["tier"] == "Medium"].iloc[0]
low_t = tier_df[tier_df["tier"] == "Low"].iloc[0]

with c1:
    render_kpi_card("High Quality Tier (Score 75+)", f"{high_t['count']:,} Leads", f"{high_t['rate']}% Conversion Rate", trend="up", icon="🌟")
with c2:
    render_kpi_card("Medium Quality Tier (50-74)", f"{med_t['count']:,} Leads", f"{med_t['rate']}% Conversion Rate", trend="neutral", icon="⚖️")
with c3:
    render_kpi_card("Low Quality Tier (< 50)", f"{low_t['count']:,} Leads", f"{low_t['rate']}% Conversion Rate", trend="down", icon="🔻")
with c4:
    avg_score = df_filtered["lead_score"].mean()
    render_kpi_card("Mean Pipeline Lead Score", f"{avg_score:.1f} / 100", f"{df_filtered[df_filtered['is_converted'] == 1]['lead_score'].mean():.1f} Won Deals Avg", trend="up", icon="🎯")

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Main Score Distribution Histogram
st.markdown("### 📊 Lead Score Distribution by Conversion Outcome")
fig_hist = create_lead_score_distribution_chart(df_filtered)
st.plotly_chart(fig_hist, use_container_width=True)

# Row 2: Lead Quality Tier Share & Lead Score by Industry
col_tier_bar, col_ind_box = st.columns([5, 7])

with col_tier_bar:
    fig_tier = px.bar(
        tier_df,
        x="tier",
        y="rate",
        text=[f"{r}% ({c} won)" for r, c in zip(tier_df["rate"], tier_df["converted"])],
        title="<b>Conversion Probability by Lead Quality Tier (%)</b>",
        labels={"tier": "Quality Tier", "rate": "Conversion Rate (%)"},
        color="tier",
        color_discrete_map={"High": "#10B981", "Medium": "#F59E0B", "Low": "#EF4444"}
    )
    fig_tier.update_layout(yaxis={"range": [0, 100], "gridcolor": "#F1F5F9"}, showlegend=False)
    st.plotly_chart(fig_tier, use_container_width=True)

with col_ind_box:
    fig_ind = px.box(
        df_filtered,
        x="industry",
        y="lead_score",
        color="industry",
        title="<b>Lead Score Spread across Target Industries</b>",
        labels={"lead_score": "Lead Score (1-100)", "industry": "Industry Sector"}
    )
    fig_ind.update_layout(
        xaxis={"tickangle": -20},
        yaxis={"gridcolor": "#F1F5F9"},
        showlegend=False
    )
    st.plotly_chart(fig_ind, use_container_width=True)

# Lead Score Decile Probability Table
st.markdown("### 🎯 Lead Score Decile Conversion Probability Curve")
df_filtered["score_decile"] = pd.cut(
    df_filtered["lead_score"],
    bins=[0, 20, 40, 60, 80, 100],
    labels=["0 - 20 (Very Low)", "21 - 40 (Low)", "41 - 60 (Moderate)", "61 - 80 (High)", "81 - 100 (Exceptional)"]
)

decile_df = df_filtered.groupby("score_decile", observed=False).agg(
    total_leads=("lead_id", "count"),
    converted_leads=("is_converted", "sum"),
    total_revenue=("deal_value_inr", "sum")
).reset_index()

decile_df["conversion_rate_pct"] = decile_df.apply(
    lambda r: round((r["converted_leads"] / r["total_leads"] * 100.0) if r["total_leads"] > 0 else 0.0, 2), axis=1
)

st.dataframe(
    decile_df.style.format({
        "total_leads": "{:,}",
        "converted_leads": "{:,}",
        "total_revenue": "₹{:,.0f}",
        "conversion_rate_pct": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)
