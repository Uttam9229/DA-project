"""
Statistical Computing Module for Lead Conversion Funnel Analysis
Leverages SciPy, NumPy, and Statsmodels for inferential and descriptive statistics.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, List

def compute_descriptive_stats(df: pd.DataFrame, numeric_cols: List[str] = None) -> pd.DataFrame:
    """Computes comprehensive parametric and non-parametric summary metrics."""
    if numeric_cols is None:
        numeric_cols = ["lead_score", "deal_value_inr", "response_time_days", "conversion_time_days"]
        
    valid_cols = [c for c in numeric_cols if c in df.columns]
    results = []
    
    for col in valid_cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue
            
        n = len(series)
        mean_val = series.mean()
        std_val = series.std()
        median_val = series.median()
        min_val = series.min()
        max_val = series.max()
        q25 = series.quantile(0.25)
        q75 = series.quantile(0.75)
        iqr = q75 - q25
        skew_val = series.skew()
        kurt_val = series.kurtosis()
        
        results.append({
            "Metric / Column": col,
            "Count (N)": int(n),
            "Mean": round(float(mean_val), 2),
            "Std Dev": round(float(std_val), 2),
            "Median": round(float(median_val), 2),
            "IQR": round(float(iqr), 2),
            "Min": round(float(min_val), 2),
            "25th Pct": round(float(q25), 2),
            "75th Pct": round(float(q75), 2),
            "Max": round(float(max_val), 2),
            "Skewness": round(float(skew_val), 2),
            "Kurtosis": round(float(kurt_val), 2)
        })
        
    return pd.DataFrame(results)

def compute_correlation_matrices(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Computes both Pearson and Spearman rank correlation matrices for numeric features."""
    candidate_cols = ["lead_score", "is_converted", "deal_value_inr", "response_time_days", "conversion_time_days"]
    valid_cols = [c for c in candidate_cols if c in df.columns]
    
    df_sub = df[valid_cols].copy()
    
    pearson_corr = df_sub.corr(method="pearson").round(3)
    spearman_corr = df_sub.corr(method="spearman").round(3)
    
    return {
        "pearson": pearson_corr,
        "spearman": spearman_corr
    }

def run_hypothesis_tests(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Executes formal statistical hypothesis tests:
    1. Two-sample t-test & Mann-Whitney U test: Lead Score of Converted vs. Non-Converted leads.
    2. Chi-Square Test of Independence: Lead Quality Category vs. Conversion Outcome.
    3. One-way ANOVA: Lead Score across different Marketing Sources.
    """
    tests = []
    
    # 1. Lead Score: Converted vs. Non-Converted
    conv_scores = df[df["is_converted"] == 1]["lead_score"].dropna()
    lost_scores = df[df["is_converted"] == 0]["lead_score"].dropna()
    
    if len(conv_scores) > 2 and len(lost_scores) > 2:
        # Two-sample t-test (Welch's t-test for unequal variances)
        t_stat, t_pval = stats.ttest_ind(conv_scores, lost_scores, equal_var=False)
        # Mann-Whitney U non-parametric test
        u_stat, u_pval = stats.mannwhitneyu(conv_scores, lost_scores, alternative="two-sided")
        
        # Cohen's d effect size
        pooled_std = np.sqrt(((len(conv_scores)-1)*conv_scores.std()**2 + (len(lost_scores)-1)*lost_scores.std()**2) / (len(conv_scores) + len(lost_scores) - 2))
        cohens_d = (conv_scores.mean() - lost_scores.mean()) / pooled_std if pooled_std > 0 else 0.0
        
        sig = t_pval < 0.05
        tests.append({
            "test_name": "Two-Sample Welch's t-test (Lead Score vs. Conversion)",
            "null_hypothesis": "The mean lead score of converted leads equals the mean lead score of unconverted leads.",
            "alt_hypothesis": "The mean lead score differs significantly between converted and unconverted leads.",
            "statistic": round(float(t_stat), 4),
            "p_value": float(t_pval),
            "effect_size_cohens_d": round(float(cohens_d), 3),
            "is_significant": sig,
            "interpretation": (
                f"Statistically Significant (p = {t_pval:.4e} < 0.05). Converted leads exhibit a significantly higher mean score "
                f"({conv_scores.mean():.1f} vs. {lost_scores.mean():.1f}) with a large effect size (Cohen's d = {cohens_d:.2f})."
                if sig else "No statistically significant difference in lead score detected."
            )
        })
        
        tests.append({
            "test_name": "Mann-Whitney U Test (Non-Parametric Lead Score Distribution)",
            "null_hypothesis": "The distribution of lead scores is identical for converted and unconverted cohorts.",
            "alt_hypothesis": "The distribution of lead scores is stochastically shifted between cohorts.",
            "statistic": round(float(u_stat), 2),
            "p_value": float(u_pval),
            "effect_size_cohens_d": None,
            "is_significant": u_pval < 0.05,
            "interpretation": (
                f"Statistically Significant (p = {u_pval:.4e} < 0.05). The non-parametric rank-sum test confirms that converted leads have systematically higher scoring ranks."
                if u_pval < 0.05 else "Ranks do not differ significantly."
            )
        })

    # 2. Chi-Square Test: Lead Quality Tier vs. Conversion Outcome
    if "lead_quality" in df.columns:
        contingency_table = pd.crosstab(df["lead_quality"], df["is_converted"])
        if contingency_table.shape == (3, 2):
            chi2_stat, chi2_pval, dof, _ = stats.chi2_contingency(contingency_table)
            chi_sig = chi2_pval < 0.05
            tests.append({
                "test_name": "Chi-Square (χ²) Test of Independence: Lead Quality vs. Conversion",
                "null_hypothesis": "Lead Quality tier (High, Medium, Low) and Conversion Outcome are mutually independent.",
                "alt_hypothesis": "Lead Quality tier and Conversion Outcome are statistically dependent.",
                "statistic": round(float(chi2_stat), 4),
                "p_value": float(chi2_pval),
                "effect_size_cohens_d": None,
                "is_significant": chi_sig,
                "interpretation": (
                    f"Statistically Significant (p = {chi2_pval:.4e} < 0.05, df={dof}). Lead qualification tier strongly predicts deal closure propensity."
                    if chi_sig else "Independence cannot be rejected."
                )
            })

    # 3. One-way ANOVA: Lead Score across Marketing Sources
    if "source_name" in df.columns:
        source_groups = [group["lead_score"].dropna().values for _, group in df.groupby("source_name") if len(group) > 2]
        if len(source_groups) >= 3:
            f_stat, f_pval = stats.f_oneway(*source_groups)
            f_sig = f_pval < 0.05
            tests.append({
                "test_name": "One-Way ANOVA: Lead Score Variance across Lead Sources",
                "null_hypothesis": "Mean lead scores are equal across all acquisition channels.",
                "alt_hypothesis": "At least one acquisition channel produces a significantly different mean lead score.",
                "statistic": round(float(f_stat), 4),
                "p_value": float(f_pval),
                "effect_size_cohens_d": None,
                "is_significant": f_sig,
                "interpretation": (
                    f"Statistically Significant (F = {f_stat:.2f}, p = {f_pval:.4e} < 0.05). Inbound acquisition channels generate systematically different lead quality tiers."
                    if f_sig else "No significant variation in score found across marketing channels."
                )
            })

    return tests
