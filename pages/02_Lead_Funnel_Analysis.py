"""
UI-02: Lead Funnel Analysis
Granular Stage-by-Stage Attrition Diagnostics, Conversion Rates & Drop-Off Metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.components import (
    inject_custom_styles, render_page_header, render_sidebar_metadata,
    render_kpi_card, render_alert_banner, apply_global_filters
)
from src.data_loader import get_clean_data
from src.analysis import calculate_funnel_stages
from src.visualization import create_funnel_chart

st.set_page_config(page_title="Funnel Analysis | Lead Funnel", page_icon="🔻", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

df_clean, _ = get_clean_data()
df_filtered = apply_global_filters(df_clean)

render_page_header(
    title="Lead Funnel Analysis",
    subtitle="Detailed Stage-Wise Attrition Diagnostics, Retention Ratios & Bottleneck Detection",
    badge="Funnel Diagnostics"
)

# Funnel calculations
stages_df = calculate_funnel_stages(df_filtered)

if len(stages_df) == 0:
    st.warning("No lead records match the selected filter criteria.")
    st.stop()

# Metric summary ribbon across all 6 sequential stages
stage_names = stages_df["stage"].tolist()
counts = stages_df["lead_count"].tolist()
retentions = stages_df["overall_retention_pct"].tolist()

cols = st.columns(len(stage_names))
for i, col in enumerate(cols):
    with col:
        stage_name = stage_names[i]
        count = counts[i]
        ret = retentions[i]
        icon = "🏁" if stage_name == "Converted" else "🔹"
        render_kpi_card(
            title=stage_name,
            value=f"{count:,}",
            subtext=f"{ret}% Retention",
            trend="up" if stage_name == "Converted" else "neutral",
            icon=icon
        )

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Main Funnel Visualization and Drop-off Analysis
col_chart, col_drop = st.columns([7, 5])

with col_chart:
    fig_funnel = create_funnel_chart(stages_df)
    st.plotly_chart(fig_funnel, use_container_width=True)

with col_drop:
    st.markdown("### ⚠️ Drop-off & Attrition Analysis")
    
    # Calculate critical drop-off points
    drop_df = stages_df.iloc[1:].copy()
    max_drop = drop_df.sort_values(by="drop_off_pct", ascending=False).iloc[0]
    
    render_alert_banner(
        title=f"Critical Bottleneck: {max_drop['stage']} Stage",
        message=(
            f"The largest single point of pipeline leakage is at the <b>{max_drop['stage']}</b> stage, "
            f"where <b>{max_drop['drop_off_pct']}%</b> of leads drop out ({max_drop['drop_off_count']} leads lost)."
        ),
        level="critical"
    )

    # Horizontal Bar Chart for Drop-off percentage
    fig_drop = px.bar(
        drop_df,
        x="drop_off_pct",
        y="stage",
        orientation="h",
        text=[f"{val}% ({cnt} lost)" for val, cnt in zip(drop_df["drop_off_pct"], drop_df["drop_off_count"])],
        labels={"drop_off_pct": "Drop-Off Rate (%)", "stage": "Stage Gate"},
        color="drop_off_pct",
        color_continuous_scale="Reds"
    )
    fig_drop.update_layout(
        title="<b>Drop-off Rate at Each Transition Stage (%)</b>",
        xaxis={"gridcolor": "#F1F5F9"},
        showlegend=False,
        margin={"l": 20, "r": 20, "t": 40, "b": 20}
    )
    st.plotly_chart(fig_drop, use_container_width=True)

# Stage Performance Audit Table
st.markdown("### 📋 Full Stage-to-Stage Transition Audit Table")
audit_display = stages_df.copy()
audit_display.columns = [
    "Funnel Stage", "Leads Reaching Stage", "Cumulative Retention (%)",
    "Stage Conversion Rate (%)", "Stage Drop-Off Rate (%)", "Absolute Leads Lost"
]

st.dataframe(
    audit_display.style.format({
        "Leads Reaching Stage": "{:,}",
        "Cumulative Retention (%)": "{:.1f}%",
        "Stage Conversion Rate (%)": "{:.1f}%",
        "Stage Drop-Off Rate (%)": "{:.1f}%",
        "Absolute Leads Lost": "{:,}"
    }),
    use_container_width=True,
    hide_index=True
)

# Stage Progression Velocity Explanation
with st.expander("ℹ️ How Stage Conversion and Drop-off Rates are Mathematically Calculated"):
    st.markdown("""
    - **Stage Conversion Rate ($CR_k$):** Percentage of leads in Stage $k$ that successfully transitioned to Stage $k+1$.
      $$\\text{Stage Conversion Rate} = \\frac{\\text{Leads Reaching Stage } k+1}{\\text{Leads Entering Stage } k} \\times 100$$
    - **Stage Drop-Off Rate ($DO_k$):** Percentage of leads that abandoned negotiations or were disqualified at Stage $k$.
      $$\\text{Drop-Off Rate} = 100\\% - \\text{Stage Conversion Rate}$$
    - **Cumulative Retention:** Proportion of initial top-of-funnel leads that reach the given milestone.
    """)
