"""
analysis.py - Economic Divergence Analysis Framework.

Research Question:
    "How has state-wise per-capita income diverged in India since 2011?"

Theoretical Framework:
1. Sigma (σ) Convergence:
   Measures whether cross-sectional dispersion of per-capita income across
   states is decreasing (convergence) or increasing (divergence) over time.
   Metric: Coefficient of Variation (CV_t = std_t / mean_t) and Standard Deviation of log(income).

2. Beta (β) Convergence:
   Tests whether initially poorer states in 2011 grew faster than richer states.
   Model: (1/T) * ln(Y_i,T / Y_i,0) = alpha + beta * ln(Y_i,0) + error
   A negative beta indicates catch-up convergence; positive indicates divergence.

3. Regional Disparities:
   Comparison of richest states vs poorest states over the decade.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd

try:
    from python.utils import get_pipeline_paths, print_step_banner
except ImportError:
    from utils import get_pipeline_paths, print_step_banner


def load_cleaned_dataset(filename: str = "per_capita_nsdp_cleaned.csv") -> Optional[pd.DataFrame]:
    """
    Loads the cleaned panel dataset from data/processed/.
    
    Args:
        filename (str): Name of the processed CSV file.
        
    Returns:
        Optional[pd.DataFrame]: Cleaned DataFrame or None if not found.
    """
    paths = get_pipeline_paths()
    processed_path = paths["data_processed"] / filename
    
    if not processed_path.exists():
        print(f"[SKIP] Processed file not found: {processed_path}")
        print("       Run clean_data.py first once raw data is placed.")
        return None
        
    df = pd.read_csv(processed_path)
    return df


def compute_annual_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates annual cross-sectional summary statistics across all Indian states:
    Mean, Median, Standard Deviation, Min, Max, and Interquartile Range (IQR).
    
    Args:
        df (pd.DataFrame): Cleaned panel DataFrame.
        
    Returns:
        pd.DataFrame: Table of annual economic indicators.
    """
    # Exclude aggregate 'All India' row if present to analyze interstate dispersion
    state_df = df[~df["State"].str.lower().isin(["all india", "all-india"])].dropna(subset=["Per_Capita_NSDP_INR"])
    
    summary = state_df.groupby(["Year_Start", "Financial_Year"])["Per_Capita_NSDP_INR"].agg(
        num_states="count",
        mean_income="mean",
        median_income="median",
        std_dev="std",
        min_income="min",
        max_income="max"
    ).reset_index()
    
    # Calculate Interquartile Range (IQR = Q75 - Q25)
    iqr_series = state_df.groupby(["Year_Start", "Financial_Year"])["Per_Capita_NSDP_INR"].apply(
        lambda s: s.quantile(0.75) - s.quantile(0.25)
    ).values
    summary["iqr_income"] = iqr_series
    
    # Max-to-Min Disparity Ratio (indicates gap between richest and poorest state)
    summary["max_min_ratio"] = summary["max_income"] / summary["min_income"]
    
    return summary.sort_values(by="Year_Start").reset_index(drop=True)


def compute_sigma_convergence(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Sigma (σ) convergence metrics for each financial year since 2011.
    
    Formula:
        Coefficient of Variation (CV_t) = Standard Deviation_t / Mean_t
        Log Standard Deviation = std(ln(Income_i,t))
        
    Economic Interpretation:
        If CV increases over time -> Sigma Divergence (inequality is widening).
        If CV decreases over time -> Sigma Convergence (inequality is narrowing).
    """
    state_df = df[~df["State"].str.lower().isin(["all india", "all-india"])].dropna(subset=["Per_Capita_NSDP_INR"]).copy()
    state_df["log_income"] = np.log(state_df["Per_Capita_NSDP_INR"])
    
    sigma_metrics = []
    grouped = state_df.groupby(["Year_Start", "Financial_Year"])
    
    for (year_start, fy), group in grouped:
        income = group["Per_Capita_NSDP_INR"]
        log_inc = group["log_income"]
        
        mean_val = income.mean()
        std_val = income.std()
        cv_val = std_val / mean_val if mean_val > 0 else np.nan
        std_log_val = log_inc.std()
        
        sigma_metrics.append({
            "Year_Start": year_start,
            "Financial_Year": fy,
            "Number_of_States": len(group),
            "Mean_NSDP_INR": round(mean_val, 2),
            "Std_Dev_NSDP_INR": round(std_val, 2),
            "Coefficient_of_Variation_CV": round(cv_val, 4),
            "Std_Dev_Log_Income": round(std_log_val, 4)
        })
        
    return pd.DataFrame(sigma_metrics).sort_values("Year_Start").reset_index(drop=True)


def compute_state_growth_rates(
    df: pd.DataFrame,
    start_year: int = 2011,
    end_year: Optional[int] = None
) -> pd.DataFrame:
    """
    Computes Compound Annual Growth Rate (CAGR) for each state from initial year to final year.
    Prepares data for testing Beta (β) convergence.
    
    CAGR Formula:
        CAGR = ( (Y_T / Y_0) ** (1 / (T - 0)) ) - 1
    """
    state_df = df[~df["State"].str.lower().isin(["all india", "all-india"])].dropna(subset=["Per_Capita_NSDP_INR"])
    
    available_years = sorted(state_df["Year_Start"].unique())
    if not available_years:
        return pd.DataFrame()
        
    t0 = start_year if start_year in available_years else available_years[0]
    t_end = end_year if (end_year is not None and end_year in available_years) else available_years[-1]
    
    periods = t_end - t0
    if periods <= 0:
        print(f"[WARNING] Insufficient time span for CAGR calculation (t0={t0}, t_end={t_end}).")
        return pd.DataFrame()
        
    df_t0 = state_df[state_df["Year_Start"] == t0][["State", "Per_Capita_NSDP_INR"]].rename(
        columns={"Per_Capita_NSDP_INR": f"Income_{t0}"}
    )
    df_tend = state_df[state_df["Year_Start"] == t_end][["State", "Per_Capita_NSDP_INR"]].rename(
        columns={"Per_Capita_NSDP_INR": f"Income_{t_end}"}
    )
    
    merged = pd.merge(df_t0, df_tend, on="State", how="inner")
    
    # Compute Initial Log Income and CAGR
    merged["Log_Initial_Income"] = np.log(merged[f"Income_{t0}"])
    merged["CAGR_Percent"] = (((merged[f"Income_{t_end}"] / merged[f"Income_{t0}"]) ** (1.0 / periods)) - 1.0) * 100
    merged["CAGR_Percent"] = merged["CAGR_Percent"].round(2)
    merged["Log_Growth_Per_Year"] = (np.log(merged[f"Income_{t_end}"]) - np.log(merged[f"Income_{t0}"])) / periods
    
    return merged.sort_values(by="CAGR_Percent", ascending=False).reset_index(drop=True)


def save_tables(tables_dict: Dict[str, pd.DataFrame]) -> None:
    """
    Exports summary and analytical tables to outputs/tables/ in CSV format.
    """
    paths = get_pipeline_paths()
    tables_dir = paths["outputs_tables"]
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, table in tables_dict.items():
        if table is not None and not table.empty:
            out_file = tables_dir / filename
            table.to_csv(out_file, index=False, encoding="utf-8")
            print(f"[TABLE] Saved: {out_file.relative_to(paths['root'])}")


def run_analysis_step() -> bool:
    """
    Entry point for Step 3 of the pipeline.
    """
    print_step_banner(
        step_number=3,
        step_name="Economic Analysis (Sigma & Beta Convergence)",
        description="Compute Coefficient of Variation, growth rates, and interstate disparity metrics."
    )
    
    df = load_cleaned_dataset()
    if df is None:
        print("[INFO] Analysis step paused: Waiting for cleaned data from Step 2.")
        return False
        
    summary_df = compute_annual_summary_statistics(df)
    sigma_df = compute_sigma_convergence(df)
    growth_df = compute_state_growth_rates(df)
    
    save_tables({
        "table1_annual_summary_statistics.csv": summary_df,
        "table2_sigma_convergence_cv.csv": sigma_df,
        "table3_state_growth_rates_cagr.csv": growth_df
    })
    
    print("\n[SUCCESS] Analysis completed successfully.")
    return True


if __name__ == "__main__":
    run_analysis_step()
