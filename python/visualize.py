"""
visualize.py - Publication-Quality Visualizations for Economic Divergence.

Research Question:
    "How has state-wise per-capita income diverged in India since 2011?"

This module generates academic-standard figures to communicate economic trends:
1. Figure 1: Sigma (σ) Convergence - Trajectory of Coefficient of Variation over time.
2. Figure 2: Beta (β) Convergence - Initial Income (2011) vs Subsequent Growth Rate (CAGR).
3. Figure 3: State Income Trajectories - Real Per Capita NSDP time series (2011-12 onwards).
4. Figure 4: Regional Disparity Ratio - Ratio of Richest to Poorest States over time.
"""

from pathlib import Path
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

try:
    from python.utils import get_pipeline_paths, print_step_banner
except ImportError:
    from utils import get_pipeline_paths, print_step_banner


def configure_plot_style() -> None:
    """
    Sets clean, professional, publication-ready visual styling.
    Uses high-contrast colors, clear fonts, and subtle grid lines suitable for
    academic submission and viva slides.
    """
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams.update({
        "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Helvetica", "Arial"],
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.labelweight": "semibold",
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "figure.titlesize": 14,
        "figure.titleweight": "bold",
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight"
    })


def plot_sigma_convergence_trend(sigma_df: pd.DataFrame, output_path: Path) -> None:
    """
    Figure 1: Plots the Coefficient of Variation (CV) over time.
    An upward-sloping trend signifies Sigma-Divergence.
    """
    fig, ax = plt.subplots(figsize=(9, 5))
    
    x = range(len(sigma_df))
    y = sigma_df["Coefficient_of_Variation_CV"]
    labels = sigma_df["Financial_Year"]
    
    ax.plot(x, y, marker="o", color="#1f77b4", linewidth=2.5, markersize=7, label="Interstate CV (σ)")
    
    # Fit linear trendline to clearly illustrate convergence or divergence
    if len(x) > 2:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), "--", color="#d62728", linewidth=1.8, label=f"Trendline (Slope: {z[0]:+.4f})")
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_title("Testing Sigma (σ) Convergence in India (Post-2011)\nInterstate Coefficient of Variation of Real Per-Capita NSDP")
    ax.set_xlabel("Financial Year")
    ax.set_ylabel("Coefficient of Variation (CV)")
    ax.legend(loc="best", frameon=True)
    
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[FIGURE] Saved: {output_path.name}")


def plot_beta_convergence_scatter(growth_df: pd.DataFrame, output_path: Path) -> None:
    """
    Figure 2: Plots Initial Per-Capita Income vs CAGR (Beta-Convergence).
    A positive slope indicates that richer states grew faster (Divergence).
    A negative slope indicates that poorer states caught up (Convergence).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = growth_df["Log_Initial_Income"]
    y = growth_df["CAGR_Percent"]
    
    ax.scatter(x, y, color="#2ca02c", s=70, alpha=0.85, edgecolors="black", linewidth=0.8)
    
    # Linear fit for Beta estimate
    if len(growth_df) > 2:
        m, b = np.polyfit(x, y, 1)
        ax.plot(x, m * x + b, color="#d62728", linewidth=2, label=f"Beta Fit (Slope β = {m:.2f})")
        
    # Annotate prominent states
    for _, row in growth_df.iterrows():
        state = row["State"]
        # Label select states or top/bottom to avoid text clutter
        if state in ["Bihar", "Uttar Pradesh", "Kerala", "Tamil Nadu", "Gujarat", "Maharashtra", "Goa", "Haryana", "Odisha"]:
            ax.annotate(
                state,
                (row["Log_Initial_Income"], row["CAGR_Percent"]),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=8,
                fontweight="medium"
            )
            
    ax.set_title("Testing Unconditional Beta (β) Convergence in India\nInitial Per-Capita Income (2011-12) vs Subsequent Growth Rate (CAGR %)")
    ax.set_xlabel("Log of Initial Per Capita NSDP (2011-12 Prices)")
    ax.set_ylabel("Compound Annual Growth Rate (%)")
    ax.legend(loc="best", frameon=True)
    
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[FIGURE] Saved: {output_path.name}")


def plot_state_income_trajectories(cleaned_df: pd.DataFrame, output_path: Path) -> None:
    """
    Figure 3: Plots Real Per Capita NSDP trajectory for Indian States over time.
    """
    fig, ax = plt.subplots(figsize=(11, 6))
    
    state_df = cleaned_df[~cleaned_df["State"].str.lower().isin(["all india", "all-india"])].copy()
    
    # Sort and plot
    for state, group in state_df.groupby("State"):
        # Highlight key contrast states, keep others subtle
        if state in ["Goa", "Delhi", "NCT of Delhi", "Haryana", "Gujarat", "Tamil Nadu"]:
            ax.plot(group["Financial_Year"], group["Per_Capita_NSDP_INR"], linewidth=2.2, label=state)
        elif state in ["Bihar", "Uttar Pradesh", "Jharkhand", "Odisha"]:
            ax.plot(group["Financial_Year"], group["Per_Capita_NSDP_INR"], linewidth=2.2, linestyle="--", label=state)
        else:
            ax.plot(group["Financial_Year"], group["Per_Capita_NSDP_INR"], color="gray", alpha=0.3, linewidth=1)
            
    ax.set_title("Trajectories of Real Per Capita Net State Domestic Product (2011-12 Prices)\nWidening Income Disparities Across Indian States")
    ax.set_xlabel("Financial Year")
    ax.set_ylabel("Per Capita NSDP (INR at 2011-12 Constant Prices)")
    plt.xticks(rotation=45, ha="right")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), frameon=True, fontsize=9)
    
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[FIGURE] Saved: {output_path.name}")


def run_visualization_step() -> bool:
    """
    Entry point for Step 4 of the pipeline.
    Loads table outputs from analysis.py and generates presentation figures.
    """
    print_step_banner(
        step_number=4,
        step_name="Visualizations & Figure Generation",
        description="Generate publication-standard charts saved to outputs/figures/."
    )
    
    paths = get_pipeline_paths()
    fig_dir = paths["outputs_figures"]
    fig_dir.mkdir(parents=True, exist_ok=True)
    
    tables_dir = paths["outputs_tables"]
    sigma_file = tables_dir / "table2_sigma_convergence_cv.csv"
    growth_file = tables_dir / "table3_state_growth_rates_cagr.csv"
    processed_file = paths["data_processed"] / "per_capita_nsdp_cleaned.csv"
    
    if not (sigma_file.exists() and growth_file.exists() and processed_file.exists()):
        print("[INFO] Visualization step paused: Awaiting analysis tables from Step 3.")
        return False
        
    configure_plot_style()
    
    sigma_df = pd.read_csv(sigma_file)
    growth_df = pd.read_csv(growth_file)
    cleaned_df = pd.read_csv(processed_file)
    
    plot_sigma_convergence_trend(sigma_df, fig_dir / "figure1_sigma_convergence_cv.png")
    plot_beta_convergence_scatter(growth_df, fig_dir / "figure2_beta_convergence_scatter.png")
    plot_state_income_trajectories(cleaned_df, fig_dir / "figure3_state_income_trajectories.png")
    
    print("\n[SUCCESS] All figures generated and saved to outputs/figures/.")
    return True


if __name__ == "__main__":
    run_visualization_step()
