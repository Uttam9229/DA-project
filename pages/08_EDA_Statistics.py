"""
UI-08: Exploratory Data Analysis & Inferential Statistics
Descriptive Metrics, Correlation Matrices, Hypothesis Testing, and Outlier Diagnostics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.components import (
    inject_custom_styles, render_page_header, render_sidebar_metadata,
    render_kpi_card, render_alert_banner, apply_global_filters
)
from src.data_loader import get_clean_data
from src.statistics import (
    compute_descriptive_stats, compute_correlation_matrices, run_hypothesis_tests
)
from src.visualization import create_correlation_heatmap

st.set_page_config(page_title="EDA & Statistics | Lead Funnel", page_icon="📐", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

df_clean, audit_info = get_clean_data()
df_filtered = apply_global_filters(df_clean)

render_page_header(
    title="Exploratory Data Analysis & Inferential Statistics",
    subtitle="Parametric & Non-Parametric Metrics, Feature Correlations, Hypothesis Tests & Distribution Models",
    badge="Statistical Computing"
)

if len(df_filtered) == 0:
    st.warning("No lead data matches the current filter settings.")
    st.stop()

# Tabs for structured exploration
tab_eda, tab_corr, tab_hyp, tab_outlier = st.tabs([
    "📊 Descriptive Summaries",
    "🔗 Correlation Matrices",
    "🧪 Hypothesis Testing (Inferential)",
    "📦 Outlier Diagnostics"
])

with tab_eda:
    st.markdown("### 📋 Parametric & Non-Parametric Metric Summaries")
    st.markdown("Detailed central tendency, dispersion, skewness, and kurtosis computed across numerical variables:")
    
    desc_df = compute_descriptive_stats(df_filtered)
    st.dataframe(
        desc_df.style.format({
            "Count (N)": "{:,}",
            "Mean": "{:,.2f}",
            "Std Dev": "{:,.2f}",
            "Median": "{:,.2f}",
            "IQR": "{:,.2f}",
            "Min": "{:,.2f}",
            "25th Pct": "{:,.2f}",
            "75th Pct": "{:,.2f}",
            "Max": "{:,.2f}",
            "Skewness": "{:.2f}",
            "Kurtosis": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 🔬 Data Schema & Column Types")
    col_types = pd.DataFrame({
        "Column Name": df_filtered.columns,
        "Data Type": [str(t) for t in df_filtered.dtypes],
        "Non-Null Count": df_filtered.notnull().sum().values,
        "Null Count": df_filtered.isnull().sum().values,
        "Null %": (df_filtered.isnull().sum().values / len(df_filtered) * 100).round(2)
    })
    st.dataframe(col_types, use_container_width=True, hide_index=True)

with tab_corr:
    st.markdown("### 🔗 Correlation Analysis (Pearson & Spearman)")
    corr_dict = compute_correlation_matrices(df_filtered)
    
    c_p, c_s = st.columns(2)
    with c_p:
        st.markdown("#### Pearson Correlation (Linear Relationship)")
        fig_p = create_correlation_heatmap(corr_dict["pearson"])
        st.plotly_chart(fig_p, use_container_width=True)
        
    with c_s:
        st.markdown("#### Spearman Rank Correlation (Monotonic Relationship)")
        fig_s = create_correlation_heatmap(corr_dict["spearman"])
        st.plotly_chart(fig_s, use_container_width=True)

    st.info("💡 **Key Statistical Takeaway:** Strong positive correlation observed between `lead_score` and `is_converted`, confirming that the scoring model is an effective predictor of deal conversion.")

with tab_hyp:
    st.markdown("### 🧪 Inferential Hypothesis Testing")
    st.markdown("Formal statistical testing at $\\alpha = 0.05$ significance level to evaluate operational business relationships:")

    tests = run_hypothesis_tests(df_filtered)

    for t in tests:
        level = "success" if t["is_significant"] else "info"
        badge_text = "SIGNIFICANT (p < 0.05)" if t["is_significant"] else "NOT SIGNIFICANT (p >= 0.05)"
        
        st.markdown(f"""
        <div class="kpi-card mb-4">
            <div class="flex items-center justify-between mb-2">
                <h4 class="font-bold text-slate-800 text-base">{t['test_name']}</h4>
                <span class="px-2.5 py-0.5 rounded text-xs font-bold {'bg-emerald-100 text-emerald-800' if t['is_significant'] else 'bg-slate-100 text-slate-800'}">{badge_text}</span>
            </div>
            <div class="text-xs text-slate-600 mb-2"><b>Null Hypothesis (H₀):</b> {t['null_hypothesis']}</div>
            <div class="text-xs text-slate-600 mb-2"><b>Alternative Hypothesis (H₁):</b> {t['alt_hypothesis']}</div>
            <div class="flex gap-4 text-xs font-mono bg-slate-50 p-2 rounded border border-slate-200 mb-2">
                <div><b>Statistic:</b> {t['statistic']}</div>
                <div><b>p-value:</b> {t['p_value']:.4e}</div>
                {f"<div><b>Cohen's d:</b> {t['effect_size_cohens_d']}</div>" if t['effect_size_cohens_d'] is not None else ""}
            </div>
            <p class="text-xs text-slate-700 italic"><b>Conclusion:</b> {t['interpretation']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab_outlier:
    st.markdown("### 📦 Outlier Identification & Box Plots")
    st.markdown("Visual detection of distribution extremes and anomalies:")

    col_box1, col_box2 = st.columns(2)
    with col_box1:
        fig_box1 = px.box(
            df_filtered,
            y="deal_value_inr",
            points="all",
            title="<b>Deal Value (INR ₹) Box Plot (Treated & Clipped)</b>",
            color_discrete_sequence=["#4F46E5"]
        )
        fig_box1.update_layout(yaxis={"gridcolor": "#F1F5F9"})
        st.plotly_chart(fig_box1, use_container_width=True)

    with col_box2:
        fig_box2 = px.box(
            df_filtered,
            y="lead_score",
            points="all",
            title="<b>Lead Score (1 - 100) Spread</b>",
            color_discrete_sequence=["#10B981"]
        )
        fig_box2.update_layout(yaxis={"gridcolor": "#F1F5F9"})
        st.plotly_chart(fig_box2, use_container_width=True)
