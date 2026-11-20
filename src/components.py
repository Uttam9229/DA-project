"""
UI Component Library & Tailwind Styling Engine
Provides reusable, styled KPI cards, badges, and sidebar footers using Tailwind CSS.
"""

import streamlit as st

def inject_custom_styles():
    """Injects Tailwind CSS CDN and SaaS enterprise styling tweaks into the Streamlit DOM."""
    st.markdown("""
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }
        
        /* Metric card container adjustments */
        .stMetric {
            background: #FFFFFF !important;
            border-radius: 12px !important;
            padding: 16px !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05) !important;
        }

        /* Sidebar custom styling */
        section[data-testid="stSidebar"] {
            background-color: #0F172A !important;
            color: #F8FAFC !important;
            border-right: 1px solid #1E293B !important;
        }
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {
            color: #E2E8F0 !important;
        }
        
        /* Premium custom KPI cards */
        .kpi-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
            transition: all 0.2s ease-in-out;
        }
        .kpi-card:hover {
            border-color: #6366F1;
            box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def render_page_header(title: str, subtitle: str, badge: str = "Enterprise Analytics"):
    """Renders consistent, professional page headers with meta pill badges."""
    st.markdown(f"""
    <div class="mb-6 pb-4 border-b border-slate-200">
        <div class="flex items-center gap-2 mb-1">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200">
                {badge}
            </span>
        </div>
        <h1 class="text-2xl md:text-3xl font-extrabold text-slate-900 tracking-tight">{title}</h1>
        <p class="text-sm md:text-base text-slate-500 mt-1">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_card(title: str, value: str, subtext: str = "", trend: str = "neutral", icon: str = "📊"):
    """Renders a single high-conversion SaaS KPI metric card."""
    trend_color = "text-slate-500"
    if trend == "up":
        trend_color = "text-emerald-600 font-semibold"
    elif trend == "down":
        trend_color = "text-rose-600 font-semibold"

    html = f"""
    <div class="kpi-card">
        <div class="flex items-center justify-between">
            <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">{title}</span>
            <span class="text-lg">{icon}</span>
        </div>
        <div class="mt-2 text-2xl font-black text-slate-900">{value}</div>
        <div class="mt-1 text-xs {trend_color}">{subtext}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_alert_banner(title: str, message: str, level: str = "info"):
    """Renders contextual alert cards."""
    colors = {
        "info": ("bg-blue-50", "border-blue-200", "text-blue-900", "text-blue-700"),
        "success": ("bg-emerald-50", "border-emerald-200", "text-emerald-900", "text-emerald-700"),
        "warning": ("bg-amber-50", "border-amber-200", "text-amber-900", "text-amber-700"),
        "critical": ("bg-rose-50", "border-rose-200", "text-rose-900", "text-rose-700")
    }
    bg, border, text_head, text_body = colors.get(level, colors["info"])

    html = f"""
    <div class="rounded-xl border {border} {bg} p-4 mb-4">
        <h4 class="font-bold text-sm {text_head}">{title}</h4>
        <p class="text-xs {text_body} mt-1">{message}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_sidebar_metadata():
    """Renders project ownership, institution, and mentor information in the sidebar."""
    with st.sidebar:
        st.markdown("""
        <div class="p-3 bg-slate-800 rounded-lg border border-slate-700 mt-6 mb-4">
            <div class="text-xs font-bold text-indigo-400 uppercase tracking-wider">Project Metadata</div>
            <div class="mt-2 text-xs text-slate-300"><b>Student:</b> Uttam Srivastava</div>
            <div class="text-xs text-slate-300"><b>Roll No:</b> 2500320140159</div>
            <div class="text-xs text-slate-300"><b>Course:</b> MCA 2nd Year (DA)</div>
            <div class="text-xs text-slate-300"><b>College:</b> ABES Engineering College</div>
            <div class="text-xs text-slate-300"><b>Mentor:</b> Prof. Anjali Pandey</div>
        </div>
        """, unsafe_allow_html=True)

def apply_global_filters(df: pd.DataFrame):
    """
    Renders standard global sidebar filters and returns the filtered DataFrame:
    - Date Range
    - Lead Source
    - Campaign
    - Sales Rep
    """
    st.sidebar.markdown("### 🔍 Global Pipeline Filters")
    
    # 1. Date filter
    min_date = df["creation_date"].min().date()
    max_date = df["creation_date"].max().date()
    
    selected_dates = st.sidebar.date_input(
        "Lead Ingestion Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_d, end_d = selected_dates
        df_filtered = df[(df["creation_date"].dt.date >= start_d) & (df["creation_date"].dt.date <= end_d)].copy()
    else:
        df_filtered = df.copy()

    # 2. Source filter
    sources = ["All Sources"] + sorted(df["source_name"].dropna().unique().tolist())
    selected_source = st.sidebar.selectbox("Lead Source Channel", sources, index=0)
    if selected_source != "All Sources":
        df_filtered = df_filtered[df_filtered["source_name"] == selected_source]

    # 3. Campaign filter
    campaigns = ["All Campaigns"] + sorted(df["campaign_name"].dropna().unique().tolist())
    selected_camp = st.sidebar.selectbox("Marketing Campaign", campaigns, index=0)
    if selected_camp != "All Campaigns":
        df_filtered = df_filtered[df_filtered["campaign_name"] == selected_camp]

    # 4. Sales Rep filter
    reps = ["All Sales Executives"] + sorted(df["rep_name"].dropna().unique().tolist())
    selected_rep = st.sidebar.selectbox("Assigned Sales Executive", reps, index=0)
    if selected_rep != "All Sales Executives":
        df_filtered = df_filtered[df_filtered["rep_name"] == selected_rep]

    st.sidebar.markdown(f"**Filtered Pipeline:** `{len(df_filtered)}` of `{len(df)}` leads")
    st.sidebar.markdown("---")

    return df_filtered
