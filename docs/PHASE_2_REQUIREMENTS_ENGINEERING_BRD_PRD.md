# PHASE 2: Requirements Engineering (BRD & PRD)
## Lead Conversion Funnel Analysis System

**Author:** Uttam Srivastava (Roll: 2500320140159)  
**Program:** MCA 2nd Year – Data Analytics, ABES Engineering College  
**Faculty Guide:** Prof. Anjali Pandey  
**Document Version:** 1.0.0  

---

### 1. How-Might-We (HMW) Innovation Statements
1. **HMW-01:** How might we provide revenue executives with immediate visibility into the exact transition point where qualified prospects drop out of the sales pipeline?
2. **HMW-02:** How might we objectively evaluate marketing campaigns by linking top-of-funnel acquisition expenditures directly with final deal conversion and ROI?
3. **HMW-03:** How might we identify high-converting sales representative practices so sales leaders can coach underperforming executives?
4. **HMW-04:** How might we predict and segment incoming leads by propensity to convert, ensuring high-value prospects receive immediate sales prioritization?
5. **HMW-05:** How might we automate data hygiene (duplicate deduplication, outlier clipping, and missing value imputation) so business intelligence metrics are 100% reliable?

---

### 2. Stakeholder Needs Analysis

| User Role | Expressed Need | Analytical Capability Required |
| :--- | :--- | :--- |
| **Executive Leadership** | "I need a 30-second snapshot of our pipeline health, revenue realization, and overall conversion trajectory." | Executive KPI ribbon, cumulative funnel diagram, gross revenue ticker, and monthly conversion velocity. |
| **Marketing Leadership** | "I need to terminate underperforming paid ad sets and allocate budget exclusively to channels with proven ROI." | Source & campaign attribution, Cost-per-Lead (CPL), Cost-per-Acquisition (CPA), and net campaign ROI calculator. |
| **Sales Enablement** | "I need to know which sales reps close deals fastest and which ones let leads grow cold." | Rep leaderboard, response time correlation, pipeline throughput per rep, and conversion rate distribution. |
| **Data Analyst & Auditor** | "I need complete transparency into data transformations, statistical distributions, and raw data quality." | Automated data cleaning logs, missing value reports, duplicate detectors, IQR outlier summaries, and parametric/non-parametric tests. |

---

### 3. Business Requirements Document (BRD)

- **BR-01 (Funnel Transparency):** The system must compute stage-to-stage transition ratios across all defined funnel milestones:
  $$\text{Stage Conversion Rate} = \frac{\text{Leads Reaching Stage } k+1}{\text{Leads Entering Stage } k} \times 100$$
- **BR-02 (Marketing Financial Efficiency):** The system must compute the financial return of marketing investments per channel and per campaign:
  $$\text{CPL} = \frac{\text{Total Campaign Spend}}{\text{Total Leads Generated}}, \quad \text{CPA} = \frac{\text{Total Campaign Spend}}{\text{Total Converted Leads}}, \quad \text{ROI} = \frac{\text{Revenue Generated} - \text{Campaign Cost}}{\text{Campaign Cost}} \times 100$$
- **BR-03 (Sales Representative Benchmarking):** The platform must benchmark rep efficacy based on conversion percentage, quota attainment, average response duration, and pipeline yield.
- **BR-04 (Predictive Lead Scoring Assessment):** The platform must segment leads into High, Medium, and Low conversion probability bands based on empirical scores (1-100) and correlate them with deal velocity.
- **BR-05 (Data Governance & Exportability):** The system must allow business users to inspect raw vs. cleaned datasets and download audited data in both CSV and Microsoft Excel formats.

---

### 4. Product Requirements Document (PRD)

#### 4.1 System Overview
A modular, multipage web application built with Streamlit and Plotly, supported by an SQLite relational persistence layer and Python statistical computing libraries (`scipy.stats`, `statsmodels`, `pandas`, `numpy`).

#### 4.2 Application Module Mapping (UI Architecture)
- **UI-01: Executive Overview:** High-level enterprise summary, KPI cards, macro funnel chart, source distribution, and conversion timeline.
- **UI-02: Lead Funnel Analysis:** Stage-wise funnel breakdown, drop-off percentages, bottleneck identification, and stage progression velocity.
- **UI-03: Lead Source Analysis:** Source volume, source conversion efficiency, revenue contribution, and effectiveness scoring.
- **UI-04: Campaign Performance:** Financial attribution, ad spend vs. revenue, CPL, CPA, and ROI quadrant matrix.
- **UI-05: Sales Representative Performance:** Rep conversion rate, pipeline volume, closed revenue, response speed, and win/loss ratios.
- **UI-06: Lead Quality & Segmentation:** Lead score distributions, qualification bands, conversion probability curves, and industry segmentation.
- **UI-07: Time & Conversion Analysis:** Sales cycle duration (days to convert), response latency, monthly velocity trends, and lag analysis.
- **UI-08: Exploratory Data Analysis & Statistics:** Descriptive statistics, correlation matrices, boxplot outlier visualizers, and normality/hypothesis tests.
- **UI-09: Business Insights & Recommendations:** Automated rule-based strategic recommendations, bottleneck alerts, and high-impact action plans.
- **UI-10: Data Management & Data Quality:** Raw vs. cleaned data explorer, null-value audit, duplicate record locator, and one-click CSV/Excel downloads.
- **UI-11: About Project:** Academic attribution, student credentials, architecture diagram, methodology, and technology manifest.

---

### 5. Functional Requirements (FR)

| Req ID | Module | Description | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **FR-01** | Database Engine | Load relational tables from SQLite (`lead_funnel.db`) into structured Pandas DataFrames. | Tables load cleanly without data corruption; handles missing DB gracefully. |
| **FR-02** | Data Cleaning | Detect and eliminate duplicate primary records, impute or report missing values, validate date sequences. | Cleaning report generated; duplicate count logged; no unhandled NaN breaks. |
| **FR-03** | Global Filtering | Provide interactive sidebar filters for Date Range, Lead Source, Campaign, and Sales Rep. | All downstream visualizations dynamically recalculate within 800ms. |
| **FR-04** | KPI Metric Ribbon | Display Total Leads, Qualified Leads, Converted Leads, Overall Conversion %, Revenue, Avg Deal Value, Avg Cycle Time. | Formatted using Tailwind CSS cards; values match mathematical definitions. |
| **FR-05** | Funnel Visualization | Render interactive multi-stage funnel using Plotly Funnel with stage counts and drop-off percentages. | Hover tooltips display transition rate and absolute loss at each gate. |
| **FR-06** | Channel Attribution | Analyze lead yield and revenue across 7 distinct marketing sources. | Visualized via bar and bubble charts ranking source conversion rates. |
| **FR-07** | Campaign ROI Analysis| Compare marketing spend against converted deal value for each active campaign. | ROI calculated safely; negative ROI clearly flagged in warning styling. |
| **FR-08** | Sales Rep Scorecard | Render performance matrix and bar charts ranking sales representatives. | Win rate %, closed revenue ₹, and average response hours displayed per rep. |
| **FR-09** | Quality Segmentation | Group leads into High (Score > 75), Medium (50-75), Low (< 50) tiers. | Distribution histogram and conversion probability per tier rendered. |
| **FR-10** | Time-to-Convert | Compute difference between creation date and conversion date for all won deals. | Average and median days displayed; distribution curve plotted. |
| **FR-11** | Statistical Engine | Execute Pearson/Spearman correlations, Student t-test or Mann-Whitney U test between converted vs. lost leads. | P-values, test statistics, and confidence intervals displayed with interpretation. |
| **FR-12** | Export Service | Offer one-click downloads for cleaned datasets in CSV and Excel format. | Valid MIME-type downloads with correctly formatted columns. |

---

### 6. Non-Functional Requirements (NFR)

- **NFR-01 (Performance):** Dashboard updates and page transitions must render in under 1.0 second under 300-10,000 records.
- **NFR-02 (Reliability & Robustness):** Zero division must be guarded across all ratio calculations (returning 0.0% instead of `NaN` or crash).
- **NFR-03 (Maintainability):** Modular architecture separating database access (`src/database.py`), transformations (`src/data_cleaning.py`), business logic (`src/analysis.py`), and visualization (`src/visualization.py`).
- **NFR-04 (Usability & Design):** Clean enterprise aesthetic utilizing Tailwind CSS, modern sans-serif typography, accessible contrast ratios, and intuitive layouts.
- **NFR-05 (Portability):** Runs seamlessly on Windows, macOS, Linux, and Streamlit Community Cloud with Python 3.12+.

---

### 7. Requirements Traceability Matrix (RTM)

| Business Req | Product Feature | Functional ID | UI Module | Test Case ID |
| :--- | :--- | :--- | :--- | :--- |
| **BR-01** | Funnel Diagnostics | FR-04, FR-05 | UI-01, UI-02 | TC-KPI-01, TC-FUNNEL-01 |
| **BR-02** | Marketing Attribution | FR-06, FR-07 | UI-03, UI-04 | TC-SOURCE-01, TC-ROI-01 |
| **BR-03** | Sales Rep Benchmarking | FR-08 | UI-05 | TC-SALES-01, TC-SALES-02 |
| **BR-04** | Lead Scoring Segmentation | FR-09 | UI-06 | TC-SCORE-01 |
| **BR-01, BR-05** | Velocity & Cycle Duration | FR-10 | UI-07 | TC-TIME-01 |
| **BR-05** | Statistical EDA & Hypotheses | FR-11 | UI-08 | TC-STAT-01, TC-STAT-02 |
| **BR-01, BR-02** | Prescriptive Recommendations | FR-04 - FR-10 | UI-09 | TC-INSIGHT-01 |
| **BR-05** | Data Hygiene & Export | FR-01, FR-02, FR-12 | UI-10 | TC-CLEAN-01, TC-EXPORT-01 |
| **Governance** | Academic Attribution | Manifest | UI-11 | TC-ABOUT-01 |
