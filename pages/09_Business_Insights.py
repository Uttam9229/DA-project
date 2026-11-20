"""
UI-09: Business Insights & Strategic Recommendations
Data-Driven Diagnostic Findings, Risk Alerts, and Actionable Prescriptions
"""

import streamlit as st
import pandas as pd
from src.components import (
    inject_custom_styles, render_page_header, render_sidebar_metadata,
    render_kpi_card, render_alert_banner, apply_global_filters
)
from src.data_loader import get_clean_data, get_dimension_tables
from src.analysis import generate_business_insights, calculate_executive_kpis

st.set_page_config(page_title="Business Insights | Lead Funnel", page_icon="💡", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

df_clean, _ = get_clean_data()
_, df_campaigns, _ = get_dimension_tables()
df_filtered = apply_global_filters(df_clean)

render_page_header(
    title="Business Insights & Actionable Recommendations",
    subtitle="Algorithmic Diagnostic Findings, Bottleneck Remediations & Growth Directives",
    badge="Strategic Directives"
)

kpis = calculate_executive_kpis(df_filtered, df_campaigns)
insights = generate_business_insights(df_filtered, df_campaigns)

st.markdown("### 🔍 High-Impact Strategic Findings")
st.markdown("Synthesized dynamically from live pipeline analytics and statistical models:")

for ins in insights:
    icon = "🚀" if ins["type"] == "Success" else ("⚠️" if ins["type"] == "Warning" else "🚨")
    badge_bg = (
        "bg-emerald-100 text-emerald-800" if ins["type"] == "Success" 
        else ("bg-amber-100 text-amber-800" if ins["type"] == "Warning" else "bg-rose-100 text-rose-800")
    )
    
    st.markdown(f"""
    <div class="kpi-card mb-4 border-l-4 {'border-l-emerald-500' if ins['type'] == 'Success' else ('border-l-amber-500' if ins['type'] == 'Warning' else 'border-l-rose-500')}">
        <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-500">{ins['category']}</span>
            <span class="px-2 py-0.5 rounded text-xs font-semibold {badge_bg}">{ins['type']}</span>
        </div>
        <h3 class="text-base font-bold text-slate-900 mb-1">{icon} {ins['title']}</h3>
        <p class="text-xs text-slate-600 mb-3">{ins['description']}</p>
        <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
            <span class="text-xs font-bold text-indigo-700 block mb-0.5">🎯 Recommended Strategic Action:</span>
            <span class="text-xs text-slate-700">{ins['recommendation']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Executive Action Plan Roadmap
st.markdown("### 🗺️ Commercial Optimization Roadmap")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-sm h-full">
        <span class="px-2 py-1 rounded bg-indigo-50 text-indigo-700 font-bold text-xs uppercase">Priority 1 (0-30 Days)</span>
        <h4 class="font-bold text-slate-800 text-sm mt-3 mb-2">Enforce Outreach SLAs</h4>
        <p class="text-xs text-slate-600 leading-relaxed">
            Mandate that all inbound inquiries receive phone outreach within 24 hours. Data shows that leads contacted within 48 hours convert at over 2x the rate of delayed leads.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-sm h-full">
        <span class="px-2 py-1 rounded bg-indigo-50 text-indigo-700 font-bold text-xs uppercase">Priority 2 (30-60 Days)</span>
        <h4 class="font-bold text-slate-800 text-sm mt-3 mb-2">Plug Proposal Drop-Offs</h4>
        <p class="text-xs text-slate-600 leading-relaxed">
            Re-architect proposal decks and include transparent ROI calculators for prospects. Address the dominant lost reason ('Price too high') with tiered payment structures.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="p-4 bg-white rounded-xl border border-slate-200 shadow-sm h-full">
        <span class="px-2 py-1 rounded bg-indigo-50 text-indigo-700 font-bold text-xs uppercase">Priority 3 (60-90 Days)</span>
        <h4 class="font-bold text-slate-800 text-sm mt-3 mb-2">Reallocate Marketing Budget</h4>
        <p class="text-xs text-slate-600 leading-relaxed">
            Shift ad budget away from low-ROI campaigns and boost high-converting Referral incentives and Google High Intent search keywords to lower overall Cost-per-Acquisition.
        </p>
    </div>
    """, unsafe_allow_html=True)
