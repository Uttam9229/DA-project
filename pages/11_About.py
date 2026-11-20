"""
UI-11: About Project & Academic Metadata
Institutional Details, Architecture Documentation, Technology Manifest, and SDLC Methodology
"""

import streamlit as st
from src.components import inject_custom_styles, render_page_header, render_sidebar_metadata

st.set_page_config(page_title="About Project | Lead Funnel", page_icon="🎓", layout="wide")
inject_custom_styles()
render_sidebar_metadata()

render_page_header(
    title="About Project & Academic Metadata",
    subtitle="Institutional Governance, Student Attribution, Architectural Blueprints & Development Lifecycle",
    badge="Academic Project Documentation"
)

# Student & Institutional Profile
st.markdown("### 🎓 Academic Credentials & Project Governance")
c_stu, c_inst = st.columns(2)

with c_stu:
    st.markdown("""
    <div class="kpi-card">
        <h4 class="font-bold text-slate-900 text-sm mb-3">👨‍🎓 Student Investigator</h4>
        <div class="space-y-1.5 text-xs text-slate-700">
            <div><b>Full Name:</b> Uttam Srivastava</div>
            <div><b>University Roll Number:</b> 2500320140159</div>
            <div><b>Program:</b> Master of Computer Applications (MCA) – 2nd Year</div>
            <div><b>Specialization Domain:</b> Data Analytics</div>
            <div><b>Academic Session:</b> 2024 – 2026</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c_inst:
    st.markdown("""
    <div class="kpi-card">
        <h4 class="font-bold text-slate-900 text-sm mb-3">🏛️ Institution & Mentorship</h4>
        <div class="space-y-1.5 text-xs text-slate-700">
            <div><b>College / Institution:</b> ABES Engineering College, Ghaziabad</div>
            <div><b>Department:</b> Department of Computer Applications</div>
            <div><b>Faculty Project Mentor:</b> Prof. Anjali Pandey</div>
            <div><b>Project Title:</b> Lead Conversion Funnel Analysis System</div>
            <div><b>Development Status:</b> Release Candidate v1.0.0 (Production-Ready)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Technology Stack Manifest
st.markdown("### 💻 Fixed Enterprise Technology Stack")

tech_items = [
    ("Python 3.12+", "Core backend language providing rapid execution, strong typing, and rich data analysis libraries."),
    ("Pandas & NumPy", "High-performance vector operations, tabular data manipulation, and star-schema querying."),
    ("SciPy & Statsmodels", "Parametric/non-parametric tests (Welch's t-test, Mann-Whitney U, Chi-square, ANOVA) and correlation matrices."),
    ("Plotly & Plotly Express", "Interactive enterprise-grade charts with custom tooltips, gradients, and responsive layouts."),
    ("Streamlit", "Multipage web application platform enabling rapid interactive data science dashboard delivery."),
    ("Tailwind CSS CDN", "Utility-first design system delivering premium SaaS card aesthetics and responsive typography."),
    ("SQLite Database", "Relational database engine enforcing foreign key integrity and ACID persistence."),
    ("Pytest Suite", "Comprehensive automated test harness validating KPI formulas, data cleaning, and database queries.")
]

t_cols = st.columns(4)
for i, (tech, desc) in enumerate(tech_items):
    with t_cols[i % 4]:
        st.markdown(f"""
        <div class="p-3 bg-white rounded-xl border border-slate-200 shadow-sm mb-4 h-full">
            <span class="font-bold text-xs text-indigo-700 block mb-1">{tech}</span>
            <p class="text-xs text-slate-500 leading-relaxed">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# 7-Phase SDLC Methodology
st.markdown("### 🔄 7-Phase Software Development Lifecycle (SDLC) Methodology")

st.markdown("""
1. **Phase 1 — Business Understanding:** Formulated problem statements, defined operational questions, identified stakeholder personas, and established SMART targets.
2. **Phase 2 — Requirements Engineering:** Created How-Might-We statements, authored comprehensive BRD/PRD documents, and prepared the Requirements Traceability Matrix (RTM).
3. **Phase 3 — Technical Design:** Architected the multi-tier system, drafted the Star Schema ER diagram, defined data dictionaries, and codified mathematical KPI formulas.
4. **Phase 4 — Dataset Generation:** Programmed a synthetic lead generation engine (`seed=42`) with realistic Indian demographic distributions, intentional duplicates, missing values, and outliers.
5. **Phase 5 — Application Development:** Engineered 11 multipage Streamlit modules with Tailwind CSS UI components, interactive Plotly visualizations, and modular `src/` logic.
6. **Phase 6 — Quality Assurance:** Authored automated unit test suites in Pytest validating zero-division safety, cleaning pipelines, database integrity, and KPI accuracy.
7. **Phase 7 — Deployment & Documentation:** Configured `.streamlit/config.toml`, `requirements.txt`, deployment guide, and Git version control for Streamlit Community Cloud.
""")
