# PHASE 7: Deployment & Operations Guide
## Lead Conversion Funnel Analysis System

**Project:** Lead Conversion Funnel Analysis  
**Student:** Uttam Srivastava (Roll: 2500320140159)  
**Institution:** ABES Engineering College | **Mentor:** Prof. Anjali Pandey  
**Target Platform:** Streamlit Community Cloud / Local Production  

---

### 1. Prerequisites & Environment Setup
- Python 3.12+ (Supports Python 3.12, 3.13, 3.14)
- Git version control installed
- Active GitHub account connected to Streamlit Community Cloud (`share.streamlit.io`)

---

### 2. Local Execution Instructions

1. **Clone the Repository / Open Workspace:**
   ```bash
   cd c:\Users\uttam\OneDrive\Desktop\DA
   ```

2. **Create and Activate Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Linux / macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Regenerate / Verify Dataset (Optional if SQLite already built):**
   ```bash
   python scripts/generate_dataset.py
   python scripts/validate_data.py
   ```

5. **Execute Automated Pytest Suite:**
   ```bash
   python -m pytest tests/ -v
   ```

6. **Launch Streamlit Application:**
   ```bash
   streamlit run app.py
   ```
   The portal opens at `http://localhost:8501`.

---

### 3. Streamlit Community Cloud Deployment Steps

1. **Initialize Git Repository & Commit:**
   ```bash
   git init
   git add .
   git commit -m "feat: complete Lead Conversion Funnel Analysis platform v1.0.0"
   ```

2. **Push to GitHub Remote:**
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/Lead-Conversion-Funnel-Analysis.git
   git push -u origin main
   ```

3. **Deploy on Streamlit Community Cloud:**
   - Log into [Streamlit Community Cloud](https://share.streamlit.io).
   - Click **"New App"**.
   - Select your GitHub repository: `<your-username>/Lead-Conversion-Funnel-Analysis`.
   - Branch: `main`.
   - Main file path: `app.py`.
   - Click **"Deploy"**.

4. **Post-Deployment Verification Checklist:**
   - Verify landing page loads and displays executive KPI cards.
   - Navigate across all 11 multipage screens (`pages/01_*.py` to `pages/11_*.py`).
   - Test sidebar interactive filters (Date Range, Source, Campaign, Sales Rep).
   - Verify CSV and Excel download buttons on `pages/10_Data_Quality.py`.
   - Verify Plotly chart tooltips and responsive viewport resizing.
