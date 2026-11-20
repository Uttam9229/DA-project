# PHASE 4: Data Generation & Validation Audit Report

```text
=======================================================
DATASET INTEGRITY & VALIDATION AUDIT REPORT
=======================================================
Primary Fact Table Record Count: 243
Dimension Lead Sources Count:    7
Dimension Campaigns Count:       6
Dimension Sales Reps Count:      7
-------------------------------------------------------
Referential Integrity - Orphan Source IDs:    0 violations
Referential Integrity - Orphan Campaign IDs:  0 violations
Referential Integrity - Orphan Sales Rep IDs: 0 violations
Primary Key Duplicate Rows Detected:         6 rows

Missing Values Audit (Columns with nulls):
  - email                 :   5 missing ( 2.06%)
  - phone                 :   6 missing ( 2.47%)
  - first_contact_date    :  36 missing (14.81%)
  - qualification_date    :  93 missing (38.27%)
  - proposal_date         : 140 missing (57.61%)
  - negotiation_date      : 173 missing (71.19%)
  - conversion_date       : 197 missing (81.07%)
  - deal_value_inr        : 196 missing (80.66%)
  - lost_reason           :  46 missing (18.93%)

Outlier Detection:
  - Average Deal Value: INR 326,276.60
  - Maximum Deal Value: INR 4,850,000.00 (Deliberate Outlier Flagged)
  - Maximum Lead Score: 108 (Deliberate Score Outlier Flagged)

Funnel Stage Breakdown:
  - Contacted         :  57 leads (23.46%)
  - Qualified         :  47 leads (19.34%)
  - Converted         :  46 leads (18.93%)
  - Lead Acquisition  :  36 leads (14.81%)
  - Proposal          :  33 leads (13.58%)
  - Negotiation       :  24 leads ( 9.88%)
```

### Validation Conclusions:
- **Primary Fact Table:** 243 records generated (complies with 150-300 record parameter).
- **Referential Integrity:** 100% valid foreign keys across all dimension tables.
- **Cleaning Exercise Fixtures:** 3 deliberate duplicate rows, 2-3% missing phone/email entries, and extreme outliers successfully generated for automated cleaning pipeline validation.
- **Storage Formats:** Excel multi-sheet workbook, separate CSV files, and SQLite database successfully populated.
