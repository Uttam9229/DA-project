"""
Analytics & Business Logic Engine for Lead Conversion Funnel Analysis
Contains validated KPI formulas, safe zero-division handling, and aggregation metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple

def safe_divide(numerator: float, denominator: float, multiplier: float = 1.0) -> float:
    """Performs safe division guarding against ZeroDivisionError and NaN."""
    if denominator is None or denominator == 0 or np.isnan(denominator) or np.isinf(denominator):
        return 0.0
    if numerator is None or np.isnan(numerator) or np.isinf(numerator):
        return 0.0
    return float((numerator / denominator) * multiplier)

def calculate_executive_kpis(df: pd.DataFrame, df_campaigns: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Computes top-level executive KPIs:
    - Total Leads
    - Qualified Leads
    - Converted Leads
    - Overall Conversion Rate (%)
    - Lead Qualification Rate (%)
    - Total Converted Revenue (INR)
    - Average Deal Value (INR)
    - Average Conversion Time (Days)
    - Average Response Time (Days)
    - Total Marketing Spend & Blended ROI
    """
    total_leads = len(df)
    
    # Qualified leads include those at or beyond 'Qualified' stage
    qualified_stages = {"Qualified", "Proposal", "Negotiation", "Converted"}
    qualified_leads = df[df["funnel_stage"].isin(qualified_stages)].shape[0]
    
    converted_leads = int(df["is_converted"].sum())
    
    conversion_rate = safe_divide(converted_leads, total_leads, 100.0)
    qualification_rate = safe_divide(qualified_leads, total_leads, 100.0)
    
    converted_df = df[df["is_converted"] == 1]
    total_revenue = float(converted_df["deal_value_inr"].sum())
    avg_deal_value = safe_divide(total_revenue, converted_leads, 1.0)
    
    avg_conversion_time = float(converted_df["conversion_time_days"].mean()) if converted_leads > 0 and converted_df["conversion_time_days"].notnull().any() else 0.0
    
    contacted_df = df[df["response_time_days"].notnull()]
    avg_response_time = float(contacted_df["response_time_days"].mean()) if len(contacted_df) > 0 else 0.0
    
    # Marketing spend calculation
    total_marketing_spend = float(df_campaigns["budget_inr"].sum()) if df_campaigns is not None and len(df_campaigns) > 0 else 0.0
    blended_cpl = safe_divide(total_marketing_spend, total_leads, 1.0)
    blended_cpa = safe_divide(total_marketing_spend, converted_leads, 1.0)
    blended_roi = safe_divide(total_revenue - total_marketing_spend, total_marketing_spend, 100.0)

    return {
        "total_leads": total_leads,
        "qualified_leads": qualified_leads,
        "converted_leads": converted_leads,
        "overall_conversion_rate": round(conversion_rate, 2),
        "lead_qualification_rate": round(qualification_rate, 2),
        "total_revenue_inr": round(total_revenue, 2),
        "avg_deal_value_inr": round(avg_deal_value, 2),
        "avg_conversion_time_days": round(avg_conversion_time, 1),
        "avg_response_time_days": round(avg_response_time, 1),
        "total_marketing_spend_inr": round(total_marketing_spend, 2),
        "blended_cpl_inr": round(blended_cpl, 2),
        "blended_cpa_inr": round(blended_cpa, 2),
        "blended_roi_percent": round(blended_roi, 2)
    }

def calculate_funnel_stages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes strict stage-to-stage cumulative progression across sales milestones:
    1. Lead Acquisition
    2. Contacted
    3. Qualified
    4. Proposal
    5. Negotiation
    6. Converted
    """
    total_leads = len(df)
    if total_leads == 0:
        return pd.DataFrame(columns=["stage", "lead_count", "conversion_rate_pct", "drop_off_pct", "drop_off_count"])

    stage_hierarchy = [
        ("Lead Acquisition", {"Lead Acquisition", "Contacted", "Qualified", "Proposal", "Negotiation", "Converted"}),
        ("Contacted",        {"Contacted", "Qualified", "Proposal", "Negotiation", "Converted"}),
        ("Qualified",        {"Qualified", "Proposal", "Negotiation", "Converted"}),
        ("Proposal",         {"Proposal", "Negotiation", "Converted"}),
        ("Negotiation",      {"Negotiation", "Converted"}),
        ("Converted",        {"Converted"})
    ]

    stages_data = []
    prev_count = total_leads

    for idx, (stage_name, valid_set) in enumerate(stage_hierarchy):
        count = df[df["funnel_stage"].isin(valid_set)].shape[0]
        
        # Stage conversion rate: leads reaching this stage / leads entering previous stage
        if idx == 0:
            stage_conv_rate = 100.0
            drop_count = 0
            drop_rate = 0.0
        else:
            stage_conv_rate = safe_divide(count, prev_count, 100.0)
            drop_count = max(0, prev_count - count)
            drop_rate = safe_divide(drop_count, prev_count, 100.0)

        stages_data.append({
            "stage": stage_name,
            "lead_count": count,
            "overall_retention_pct": round(safe_divide(count, total_leads, 100.0), 2),
            "stage_conversion_rate_pct": round(stage_conv_rate, 2),
            "drop_off_pct": round(drop_rate, 2),
            "drop_off_count": drop_count
        })
        prev_count = count

    return pd.DataFrame(stages_data)

def calculate_source_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates leads, conversion rates, and revenue by lead source."""
    if len(df) == 0:
        return pd.DataFrame()
        
    source_stats = []
    grouped = df.groupby("source_name")
    
    for source_name, group in grouped:
        total = len(group)
        converted = int(group["is_converted"].sum())
        conv_rate = safe_divide(converted, total, 100.0)
        revenue = float(group[group["is_converted"] == 1]["deal_value_inr"].sum())
        avg_score = float(group["lead_score"].mean())
        avg_deal = safe_divide(revenue, converted, 1.0)
        channel_type = group["channel_type"].iloc[0] if "channel_type" in group.columns else "Unknown"
        
        source_stats.append({
            "source_name": source_name,
            "channel_type": channel_type,
            "total_leads": total,
            "converted_leads": converted,
            "conversion_rate_pct": round(conv_rate, 2),
            "total_revenue_inr": round(revenue, 2),
            "avg_deal_value_inr": round(avg_deal, 2),
            "avg_lead_score": round(avg_score, 1)
        })
        
    df_result = pd.DataFrame(source_stats).sort_values(by="conversion_rate_pct", ascending=False).reset_index(drop=True)
    return df_result

def calculate_campaign_performance(df: pd.DataFrame, df_campaigns: pd.DataFrame) -> pd.DataFrame:
    """Computes campaign lead generation, spend, revenue, CPL, CPA, and ROI."""
    if len(df) == 0 or df_campaigns is None or len(df_campaigns) == 0:
        return pd.DataFrame()
        
    camp_stats = []
    
    for _, camp in df_campaigns.iterrows():
        camp_id = camp["campaign_id"]
        camp_name = camp["campaign_name"]
        budget = float(camp["budget_inr"])
        
        leads_subset = df[df["campaign_id"] == camp_id]
        total_leads = len(leads_subset)
        converted_leads = int(leads_subset["is_converted"].sum()) if total_leads > 0 else 0
        conv_rate = safe_divide(converted_leads, total_leads, 100.0)
        
        revenue = float(leads_subset[leads_subset["is_converted"] == 1]["deal_value_inr"].sum()) if converted_leads > 0 else 0.0
        
        cpl = safe_divide(budget, total_leads, 1.0)
        cpa = safe_divide(budget, converted_leads, 1.0)
        roi = safe_divide(revenue - budget, budget, 100.0)
        
        camp_stats.append({
            "campaign_id": camp_id,
            "campaign_name": camp_name,
            "budget_inr": round(budget, 2),
            "total_leads": total_leads,
            "converted_leads": converted_leads,
            "conversion_rate_pct": round(conv_rate, 2),
            "revenue_inr": round(revenue, 2),
            "cpl_inr": round(cpl, 2),
            "cpa_inr": round(cpa, 2),
            "roi_pct": round(roi, 2)
        })
        
    return pd.DataFrame(camp_stats).sort_values(by="roi_pct", ascending=False).reset_index(drop=True)

def calculate_sales_rep_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Computes individual sales representative metrics."""
    if len(df) == 0:
        return pd.DataFrame()
        
    rep_stats = []
    for rep_name, group in df.groupby("rep_name"):
        assigned = len(group)
        contacted = group[group["response_time_days"].notnull()].shape[0]
        qualified = group[group["funnel_stage"].isin({"Qualified", "Proposal", "Negotiation", "Converted"})].shape[0]
        converted = int(group["is_converted"].sum())
        conv_rate = safe_divide(converted, assigned, 100.0)
        revenue = float(group[group["is_converted"] == 1]["deal_value_inr"].sum())
        avg_resp = float(group["response_time_days"].mean()) if contacted > 0 else 0.0
        region = group["rep_region"].iloc[0] if "rep_region" in group.columns else "Unknown"
        experience = group["rep_experience"].iloc[0] if "rep_experience" in group.columns else 0
        
        rep_stats.append({
            "rep_name": rep_name,
            "region": region,
            "experience_years": experience,
            "assigned_leads": assigned,
            "contacted_leads": contacted,
            "qualified_leads": qualified,
            "converted_leads": converted,
            "conversion_rate_pct": round(conv_rate, 2),
            "revenue_inr": round(revenue, 2),
            "avg_response_time_days": round(avg_resp, 1)
        })
        
    return pd.DataFrame(rep_stats).sort_values(by="revenue_inr", ascending=False).reset_index(drop=True)

def calculate_time_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes detailed cycle times and monthly lead/conversion trends."""
    if len(df) == 0:
        return {"monthly_trends": pd.DataFrame(), "avg_cycle_days": 0.0, "median_cycle_days": 0.0}
        
    converted_df = df[df["is_converted"] == 1]
    avg_cycle = float(converted_df["conversion_time_days"].mean()) if len(converted_df) > 0 else 0.0
    median_cycle = float(converted_df["conversion_time_days"].median()) if len(converted_df) > 0 else 0.0
    
    # Monthly trend
    monthly = df.groupby("creation_month").agg(
        total_leads=("lead_id", "count"),
        converted_leads=("is_converted", "sum"),
        total_revenue=("deal_value_inr", "sum")
    ).reset_index()
    monthly["conversion_rate_pct"] = monthly.apply(
        lambda r: safe_divide(r["converted_leads"], r["total_leads"], 100.0), axis=1
    ).round(2)
    
    return {
        "monthly_trends": monthly,
        "avg_cycle_days": round(avg_cycle, 1),
        "median_cycle_days": round(median_cycle, 1)
    }

def generate_business_insights(df: pd.DataFrame, df_campaigns: pd.DataFrame = None) -> List[Dict[str, str]]:
    """Synthesizes high-impact strategic business insights from real analytics data."""
    insights = []
    
    # 1. Best marketing channel
    src_df = calculate_source_performance(df)
    if len(src_df) > 0:
        best_source = src_df.iloc[0]
        insights.append({
            "category": "Marketing Channel Optimization",
            "type": "Success",
            "title": f"Top Performing Channel: {best_source['source_name']}",
            "description": f"{best_source['source_name']} generates the highest conversion yield at {best_source['conversion_rate_pct']}% with ₹{best_source['total_revenue_inr']:,.0f} in closed revenue.",
            "recommendation": f"Scale marketing allocation into {best_source['source_name']} while refining messaging across lower-converting inbound avenues."
        })
        
        worst_source = src_df.iloc[-1]
        insights.append({
            "category": "Channel Attrition Risk",
            "type": "Warning",
            "title": f"Lowest Converting Channel: {worst_source['source_name']}",
            "description": f"{worst_source['source_name']} has an attrition rate of {100 - worst_source['conversion_rate_pct']:.1f}% ({worst_source['conversion_rate_pct']}% conversion).",
            "recommendation": "Conduct landing page A/B tests and review intent qualification before dedicating further budget."
        })

    # 2. Funnel Bottleneck
    funnel_df = calculate_funnel_stages(df)
    if len(funnel_df) > 1:
        # Find stage with highest drop-off percentage (excluding stage 0)
        max_drop_stage = funnel_df.iloc[1:].sort_values(by="drop_off_pct", ascending=False).iloc[0]
        insights.append({
            "category": "Funnel Attrition Bottleneck",
            "type": "Critical",
            "title": f"Major Pipeline Leakage at '{max_drop_stage['stage']}' Stage",
            "description": f"The '{max_drop_stage['stage']}' milestone loses {max_drop_stage['drop_off_pct']}% of prospective leads ({max_drop_stage['drop_off_count']} leads dropped).",
            "recommendation": f"Review sales enablement materials, objection handling, and proposal turn-around SLAs at the {max_drop_stage['stage']} stage."
        })

    # 3. Sales Rep Champion
    rep_df = calculate_sales_rep_performance(df)
    if len(rep_df) > 0:
        top_rep = rep_df.iloc[0]
        insights.append({
            "category": "Sales Leadership & Quota",
            "type": "Success",
            "title": f"Leading Sales Executive: {top_rep['rep_name']}",
            "description": f"{top_rep['rep_name']} leads revenue generation with ₹{top_rep['revenue_inr']:,.0f} closed ({top_rep['conversion_rate_pct']}% conversion rate and {top_rep['avg_response_time_days']} days avg response).",
            "recommendation": "Document and templatize their outreach sequence and objection handling playbook for the wider sales floor."
        })

    # 4. Campaign ROI
    if df_campaigns is not None and len(df_campaigns) > 0:
        camp_df = calculate_campaign_performance(df, df_campaigns)
        if len(camp_df) > 0:
            top_camp = camp_df.iloc[0]
            insights.append({
                "category": "Campaign Financial Yield",
                "type": "Success",
                "title": f"Highest Campaign ROI: {top_camp['campaign_name']}",
                "description": f"Delivered an exceptional {top_camp['roi_pct']}% ROI with ₹{top_camp['revenue_inr']:,.0f} revenue against a budget of ₹{top_camp['budget_inr']:,.0f}.",
                "recommendation": "Renew and expand budget allocations for this campaign concept in the upcoming quarter."
            })

    return insights
