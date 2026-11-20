"""
Dataset Generator Script for Lead Conversion Funnel Analysis
Student Name: Uttam Srivastava | Roll Number: 2500320140159
College: ABES Engineering College | Mentor: Anjali Pandey
Random Seed: 42
"""

import os
import random
import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_all_data():
    np.random.seed(42)
    random.seed(42)

    # 1. Dimension: Lead Sources
    sources_data = [
        {"source_id": "SRC-01", "source_name": "Website", "channel_type": "Inbound", "cost_category": "Organic"},
        {"source_id": "SRC-02", "source_name": "Social Media", "channel_type": "Inbound", "cost_category": "Paid"},
        {"source_id": "SRC-03", "source_name": "Email Marketing", "channel_type": "Outbound", "cost_category": "Hybrid"},
        {"source_id": "SRC-04", "source_name": "Paid Advertising", "channel_type": "Inbound", "cost_category": "Paid"},
        {"source_id": "SRC-05", "source_name": "Referrals", "channel_type": "Referral", "cost_category": "Organic"},
        {"source_id": "SRC-06", "source_name": "Organic Search", "channel_type": "Inbound", "cost_category": "Organic"},
        {"source_id": "SRC-07", "source_name": "Direct Traffic", "channel_type": "Inbound", "cost_category": "Organic"},
    ]
    df_sources = pd.DataFrame(sources_data)

    # 2. Dimension: Campaigns
    campaigns_data = [
        {"campaign_id": "CMP-01", "campaign_name": "SaaS Growth Sprint Q1", "source_id": "SRC-04", "budget_inr": 280000.0, "start_date": "2024-01-10", "end_date": "2024-03-31", "target_audience": "B2B Tech Leaders"},
        {"campaign_id": "CMP-02", "campaign_name": "Diwali Special Offer", "source_id": "SRC-02", "budget_inr": 220000.0, "start_date": "2024-10-01", "end_date": "2024-11-15", "target_audience": "Mid-Market Retailers"},
        {"campaign_id": "CMP-03", "campaign_name": "Tech Summit Webinar 2024", "source_id": "SRC-03", "budget_inr": 150000.0, "start_date": "2024-04-01", "end_date": "2024-06-30", "target_audience": "Engineering Directors"},
        {"campaign_id": "CMP-04", "campaign_name": "Google High Intent Search", "source_id": "SRC-04", "budget_inr": 350000.0, "start_date": "2024-01-15", "end_date": "2024-12-15", "target_audience": "Active Software Buyers"},
        {"campaign_id": "CMP-05", "campaign_name": "LinkedIn B2B Leadership", "source_id": "SRC-02", "budget_inr": 250000.0, "start_date": "2024-03-01", "end_date": "2024-09-30", "target_audience": "C-Suite & Founders"},
        {"campaign_id": "CMP-06", "campaign_name": "Partner Referral Drive", "source_id": "SRC-05", "budget_inr": 100000.0, "start_date": "2024-02-01", "end_date": "2024-11-30", "target_audience": "Existing Client Networks"},
    ]
    df_campaigns = pd.DataFrame(campaigns_data)

    # 3. Dimension: Sales Representatives (Indian fictional names)
    reps_data = [
        {"rep_id": "REP-01", "rep_name": "Aarav Sharma", "region": "North", "experience_years": 4, "email": "aarav.sharma@leadfunnel.in"},
        {"rep_id": "REP-02", "rep_name": "Pooja Verma", "region": "West", "experience_years": 6, "email": "pooja.verma@leadfunnel.in"},
        {"rep_id": "REP-03", "rep_name": "Rohan Nair", "region": "South", "experience_years": 5, "email": "rohan.nair@leadfunnel.in"},
        {"rep_id": "REP-04", "rep_name": "Neha Gupta", "region": "North", "experience_years": 3, "email": "neha.gupta@leadfunnel.in"},
        {"rep_id": "REP-05", "rep_name": "Vikramaditya Rao", "region": "South", "experience_years": 8, "email": "vikram.rao@leadfunnel.in"},
        {"rep_id": "REP-06", "rep_name": "Ananya Deshmukh", "region": "West", "experience_years": 4, "email": "ananya.deshmukh@leadfunnel.in"},
        {"rep_id": "REP-07", "rep_name": "Kunal Banerjee", "region": "East", "experience_years": 5, "email": "kunal.banerjee@leadfunnel.in"},
    ]
    df_reps = pd.DataFrame(reps_data)

    # 4. Fact Table: Leads (240 unique records + deliberate anomalies for cleaning)
    first_names = [
        "Aadesh", "Abhinav", "Aditi", "Alok", "Amit", "Amrita", "Anand", "Ankit", "Anushka", "Arjun",
        "Ashok", "Ayush", "Bhavna", "Chetan", "Deepak", "Devika", "Divya", "Gaurav", "Harish", "Ishaan",
        "Jatin", "Kavita", "Kishore", "Madhuri", "Manish", "Meera", "Manoj", "Naveen", "Nikhil", "Pallavi",
        "Pranav", "Priyanka", "Rahul", "Rajesh", "Rakesh", "Rashmi", "Ritu", "Sachin", "Sanjay", "Saurabh",
        "Shikha", "Shivani", "Siddharth", "Sneha", "Subhash", "Sunil", "Suresh", "Tanvi", "Tarun", "Varun"
    ]
    last_names = [
        "Agarwal", "Bhatia", "Chauhan", "Chopra", "Das", "Deshmukh", "Dubey", "Goswami", "Gupta", "Iyer",
        "Jadhav", "Jain", "Kapoor", "Kashyap", "Khan", "Kumar", "Mehta", "Mishra", "Mukherjee", "Nair",
        "Pandey", "Patel", "Prasad", "Puri", "Reddy", "Saxena", "Sen", "Sharma", "Shukla", "Singh",
        "Singhania", "Srivastava", "Suri", "Tiwari", "Tripathi", "Varma", "Verma", "Vyas", "Yadav", "Zaveri"
    ]
    cities_states = [
        ("Delhi NCR", "Delhi"), ("Gurugram", "Haryana"), ("Noida", "Uttar Pradesh"),
        ("Mumbai", "Maharashtra"), ("Pune", "Maharashtra"), ("Bengaluru", "Karnataka"),
        ("Hyderabad", "Telangana"), ("Chennai", "Tamil Nadu"), ("Kolkata", "West Bengal"),
        ("Ahmedabad", "Gujarat"), ("Jaipur", "Rajasthan"), ("Lucknow", "Uttar Pradesh")
    ]
    industries = ["FinTech", "EdTech", "Healthcare", "E-Commerce", "SaaS / IT Services", "Manufacturing", "Logistics"]
    lost_reasons = [
        "Price too high", "Competitor selected", "Lack of budget",
        "No response after proposal", "Feature requirements mismatch", "Project put on hold"
    ]

    base_date = datetime(2024, 1, 5)
    records = []

    # Target: ~240 primary records
    # Conversion probability by source: Referrals (highest), Website (medium), Paid Ads (medium), Social Media (lower), Direct (medium)
    source_conversion_weights = {
        "SRC-01": 0.22, # Website
        "SRC-02": 0.14, # Social Media
        "SRC-03": 0.18, # Email
        "SRC-04": 0.20, # Paid Ads
        "SRC-05": 0.38, # Referrals
        "SRC-06": 0.24, # Organic Search
        "SRC-07": 0.16  # Direct Traffic
    }

    # Generate 240 structured records
    for i in range(1, 241):
        lead_id = f"LEAD-{1000 + i}"
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        email = f"{fn.lower()}.{ln.lower()}{random.randint(10, 99)}@outlook.in"
        phone = f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}"
        city, state = random.choice(cities_states)
        industry = random.choice(industries)
        
        # Source & Campaign selection
        src = random.choices(
            df_sources["source_id"].tolist(),
            weights=[25, 20, 15, 25, 10, 20, 15],
            k=1
        )[0]
        
        # Filter campaigns matching or relevant to source
        matching_camps = df_campaigns[df_campaigns["source_id"] == src]["campaign_id"].tolist()
        if matching_camps and random.random() < 0.75:
            campaign_id = random.choice(matching_camps)
        else:
            campaign_id = random.choice(df_campaigns["campaign_id"].tolist())

        # Sales Rep assignment (weighted by experience)
        rep = random.choices(
            df_reps["rep_id"].tolist(),
            weights=[15, 18, 16, 12, 22, 14, 13],
            k=1
        )[0]

        # Lead Score (1 - 100)
        # Higher scores correlate with conversion
        src_wt = source_conversion_weights[src]
        score = int(np.clip(np.random.normal(loc=40 + src_wt * 60, scale=14), 15, 99))
        
        if score >= 75:
            lead_quality = "High"
        elif score >= 50:
            lead_quality = "Medium"
        else:
            lead_quality = "Low"

        # Dates progression
        days_from_start = random.randint(0, 320)
        creation_date = base_date + timedelta(days=days_from_start)
        
        # Initial response time (1 to 5 days, influenced by rep)
        contact_lag = random.randint(1, 5)
        first_contact_date = creation_date + timedelta(days=contact_lag)
        
        # Funnel stage progression logic
        # 1. Lead Acquisition (100% reach)
        # 2. Contacted (~88% reach)
        # 3. Qualified (~68% reach)
        # 4. Proposal (~48% reach)
        # 5. Negotiation (~30% reach)
        # 6. Converted (~18-20% reach)
        
        # Progression roll influenced by score
        prob_boost = (score - 50) / 100.0 # -0.35 to +0.49
        
        # Contact stage
        is_contacted = (random.random() < (0.88 + prob_boost * 0.15))
        is_qualified = is_contacted and (random.random() < (0.75 + prob_boost * 0.25))
        is_proposal = is_qualified and (random.random() < (0.70 + prob_boost * 0.25))
        is_negotiation = is_proposal and (random.random() < (0.62 + prob_boost * 0.25))
        is_converted = is_negotiation and (random.random() < (0.60 + prob_boost * 0.30))

        qual_date = None
        prop_date = None
        neg_date = None
        conv_date = None
        lost_reason = None
        deal_value = None

        if not is_contacted:
            funnel_stage = "Lead Acquisition"
            first_contact_date = None
            lost_reason = "Unresponsive to initial outreach"
        elif not is_qualified:
            funnel_stage = "Contacted"
            lost_reason = "Failed BANT qualification"
        elif not is_proposal:
            funnel_stage = "Qualified"
            qual_date = first_contact_date + timedelta(days=random.randint(2, 6))
            lost_reason = "No budget / timing not right"
        elif not is_negotiation:
            funnel_stage = "Proposal"
            qual_date = first_contact_date + timedelta(days=random.randint(2, 6))
            prop_date = qual_date + timedelta(days=random.randint(3, 8))
            lost_reason = random.choice(["Competitor selected", "Feature requirements mismatch", "Price too high"])
        elif not is_converted:
            funnel_stage = "Negotiation"
            qual_date = first_contact_date + timedelta(days=random.randint(2, 6))
            prop_date = qual_date + timedelta(days=random.randint(3, 8))
            neg_date = prop_date + timedelta(days=random.randint(4, 10))
            lost_reason = random.choice(["Price too high", "Project put on hold", "Competitor selected"])
        else:
            funnel_stage = "Converted"
            qual_date = first_contact_date + timedelta(days=random.randint(2, 6))
            prop_date = qual_date + timedelta(days=random.randint(3, 8))
            neg_date = prop_date + timedelta(days=random.randint(4, 10))
            conv_date = neg_date + timedelta(days=random.randint(3, 12))
            lost_reason = None
            # Deal value in INR: 50,000 to 450,000 based on industry
            deal_base = {
                "FinTech": 280000, "EdTech": 140000, "Healthcare": 220000,
                "E-Commerce": 160000, "SaaS / IT Services": 310000, "Manufacturing": 340000, "Logistics": 190000
            }
            deal_value = float(int(np.random.normal(loc=deal_base.get(industry, 200000), scale=40000) / 1000) * 1000)
            if deal_value < 50000:
                deal_value = 50000.0

        records.append({
            "lead_id": lead_id,
            "first_name": fn,
            "last_name": ln,
            "email": email,
            "phone": phone,
            "city": city,
            "state": state,
            "source_id": src,
            "campaign_id": campaign_id,
            "rep_id": rep,
            "creation_date": creation_date.strftime("%Y-%m-%d"),
            "first_contact_date": first_contact_date.strftime("%Y-%m-%d") if first_contact_date else None,
            "qualification_date": qual_date.strftime("%Y-%m-%d") if qual_date else None,
            "proposal_date": prop_date.strftime("%Y-%m-%d") if prop_date else None,
            "negotiation_date": neg_date.strftime("%Y-%m-%d") if neg_date else None,
            "conversion_date": conv_date.strftime("%Y-%m-%d") if conv_date else None,
            "funnel_stage": funnel_stage,
            "lead_score": score,
            "lead_quality": lead_quality,
            "deal_value_inr": deal_value,
            "is_converted": 1 if is_converted else 0,
            "lost_reason": lost_reason,
            "industry": industry
        })

    df_leads = pd.DataFrame(records)

    # Introduce realistic 2-3% missing values for data cleaning exercises
    # e.g., missing phone or email
    missing_phone_idx = np.random.choice(df_leads.index, size=6, replace=False)
    df_leads.loc[missing_phone_idx, "phone"] = None
    
    missing_email_idx = np.random.choice(df_leads.index, size=5, replace=False)
    df_leads.loc[missing_email_idx, "email"] = None

    # Introduce deliberate duplicates (3 duplicate records to test deduplication)
    dup_rows = df_leads.iloc[[12, 45, 88]].copy()
    df_leads = pd.concat([df_leads, dup_rows], ignore_index=True)

    # Introduce 2 extreme financial outliers for outlier detection testing
    df_leads.loc[5, "deal_value_inr"] = 4850000.0 # extreme deal value outlier
    df_leads.loc[19, "lead_score"] = 108 # out-of-bound score outlier

    print(f"Generated fact_leads total rows (including anomalies): {len(df_leads)}")
    print(f"Total converted leads: {df_leads['is_converted'].sum()}")
    print(f"Overall conversion rate: {(df_leads['is_converted'].sum() / len(df_leads))*100:.2f}%")

    # Output paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_dir = os.path.join(base_dir, "data", "raw")
    cleaned_dir = os.path.join(base_dir, "data", "cleaned")
    db_path = os.path.join(base_dir, "data", "lead_funnel.db")

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(cleaned_dir, exist_ok=True)

    # 1. Save Raw CSVs
    df_sources.to_csv(os.path.join(raw_dir, "dim_lead_sources.csv"), index=False)
    df_campaigns.to_csv(os.path.join(raw_dir, "dim_campaigns.csv"), index=False)
    df_reps.to_csv(os.path.join(raw_dir, "dim_sales_reps.csv"), index=False)
    df_leads.to_csv(os.path.join(raw_dir, "fact_leads.csv"), index=False)
    print(f"Saved raw CSVs to {raw_dir}")

    # 2. Save Multi-Sheet Excel Workbook
    excel_path = os.path.join(raw_dir, "lead_conversion_data.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_leads.to_excel(writer, sheet_name="fact_leads", index=False)
        df_sources.to_excel(writer, sheet_name="dim_lead_sources", index=False)
        df_campaigns.to_excel(writer, sheet_name="dim_campaigns", index=False)
        df_reps.to_excel(writer, sheet_name="dim_sales_reps", index=False)
    print(f"Saved Excel workbook to {excel_path}")

    # 3. Create SQLite Database and load tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop existing tables if present
    cursor.execute("DROP TABLE IF EXISTS fact_leads;")
    cursor.execute("DROP TABLE IF EXISTS dim_campaigns;")
    cursor.execute("DROP TABLE IF EXISTS dim_sales_reps;")
    cursor.execute("DROP TABLE IF EXISTS dim_lead_sources;")

    # Create tables with primary & foreign keys
    cursor.execute("""
    CREATE TABLE dim_lead_sources (
        source_id TEXT PRIMARY KEY,
        source_name TEXT NOT NULL,
        channel_type TEXT NOT NULL,
        cost_category TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE dim_campaigns (
        campaign_id TEXT PRIMARY KEY,
        campaign_name TEXT NOT NULL,
        source_id TEXT NOT NULL,
        budget_inr REAL NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        target_audience TEXT,
        FOREIGN KEY (source_id) REFERENCES dim_lead_sources(source_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE dim_sales_reps (
        rep_id TEXT PRIMARY KEY,
        rep_name TEXT NOT NULL,
        region TEXT NOT NULL,
        experience_years INTEGER NOT NULL,
        email TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE fact_leads (
        lead_id TEXT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        source_id TEXT NOT NULL,
        campaign_id TEXT NOT NULL,
        rep_id TEXT NOT NULL,
        creation_date TEXT NOT NULL,
        first_contact_date TEXT,
        qualification_date TEXT,
        proposal_date TEXT,
        negotiation_date TEXT,
        conversion_date TEXT,
        funnel_stage TEXT NOT NULL,
        lead_score INTEGER NOT NULL,
        lead_quality TEXT NOT NULL,
        deal_value_inr REAL,
        is_converted INTEGER NOT NULL,
        lost_reason TEXT,
        industry TEXT NOT NULL,
        FOREIGN KEY (source_id) REFERENCES dim_lead_sources(source_id),
        FOREIGN KEY (campaign_id) REFERENCES dim_campaigns(campaign_id),
        FOREIGN KEY (rep_id) REFERENCES dim_sales_reps(rep_id)
    );
    """)

    # Insert data
    df_sources.to_sql("dim_lead_sources", conn, if_exists="append", index=False)
    df_campaigns.to_sql("dim_campaigns", conn, if_exists="append", index=False)
    df_reps.to_sql("dim_sales_reps", conn, if_exists="append", index=False)
    df_leads.to_sql("fact_leads", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()
    print(f"Created SQLite database and loaded tables at {db_path}")

    return len(df_leads), df_leads['is_converted'].sum()

if __name__ == "__main__":
    generate_all_data()
