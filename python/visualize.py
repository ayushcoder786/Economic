"""
visualize.py - Publication-Quality Visualizations for Economic Divergence in India.

Module 4: Visualize Findings
Research Question:
    "How has state-wise per-capita income diverged in India since 2011?"

This module generates clear, honest, publication-standard figures to address
the research question without misleading axes or artificial distortions:
1. Figure 1: State-wise per-capita income trajectories over time (all states + mean/median)
2. Figure 2: Comparison of selected states across economic tiers and regions
3. Figure 3: Percentage growth and CAGR from 2011-12 to 2023-24 (colored by Region/Zone)
4. Figure 4: Distribution of state-wise per-capita income across milestone years (Boxplots)
5. Figure 5: Inter-state disparity gap evolution (P90/P10 ratio & Coefficient of Variation)
6. Figure 6: State ranking comparison between 2011-12 and 2023-24 (Slope/Dumbbell plot)

All figures are saved to outputs/figures/ at 300 DPI.
Summary analytical tables are saved to outputs/tables/.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
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
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.labelweight": "semibold",
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "figure.titlesize": 13.5,
        "figure.titleweight": "bold",
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight"
    })


def load_cleaned_panel() -> pd.DataFrame:
    """
    Loads the cleaned and harmonized panel dataset from data/processed/.
    """
    paths = get_pipeline_paths()
    data_file = paths["data_processed"] / "india_per_capita_income_cleaned.csv"
    if not data_file.exists():
        data_file = paths["data_processed"] / "per_capita_nsdp_cleaned.csv"
        
    if not data_file.exists():
        raise FileNotFoundError(f"Cleaned dataset not found in {paths['data_processed']}")
        
    df = pd.read_csv(data_file)
    return df


# ==============================================================================
# 1. STATE-WISE PER-CAPITA INCOME OVER TIME (ALL STATES TRAJECTORIES)
# ==============================================================================
def plot_all_states_trajectories(df: pd.DataFrame, output_path: Path) -> None:
    """
    Figure 1: Displays trajectories of all 34 States/UTs over time.
    Individual states are shown in subtle grey, with National Mean and Median
    prominently highlighted to reveal the overall upward drift and widening spread.
    """
    fig, ax = plt.subplots(figsize=(11, 6.5))
    
    # Calculate yearly mean and median (excluding NA)
    yearly_stats = df.groupby(["Year_Start", "Financial_Year"])["Per_Capita_Income"].agg(
        mean_val="mean",
        median_val="median"
    ).reset_index()
    
    # Plot individual state lines in subtle background grey
    for state, group in df.groupby("State"):
        valid = group.dropna(subset=["Per_Capita_Income"]).sort_values("Year_Start")
        ax.plot(
            valid["Financial_Year"],
            valid["Per_Capita_Income"],
            color="#a0aec0",
            alpha=0.45,
            linewidth=1.1,
            zorder=2
        )
        
    # Plot Prominent National Unweighted Mean
    ax.plot(
        yearly_stats["Financial_Year"],
        yearly_stats["mean_val"],
        color="#2b6cb0",
        linewidth=2.8,
        marker="o",
        markersize=5,
        label="National Mean (Unweighted Average)",
        zorder=4
    )
    
    # Plot Prominent National Median
    ax.plot(
        yearly_stats["Financial_Year"],
        yearly_stats["median_val"],
        color="#c53030",
        linewidth=2.8,
        linestyle="--",
        marker="s",
        markersize=5,
        label="National Median (50th Percentile State)",
        zorder=4
    )
    
    # Annotate Top (Goa/Sikkim) and Bottom (Bihar) endpoints
    latest_complete_fy = "2023-24"
    latest_data = df[df["Financial_Year"] == latest_complete_fy].dropna(subset=["Per_Capita_Income"])
    if not latest_data.empty:
        top_state = latest_data.loc[latest_data["Per_Capita_Income"].idxmax()]
        bot_state = latest_data.loc[latest_data["Per_Capita_Income"].idxmin()]
        
        ax.annotate(
            f"Highest: {top_state['State']}\n(₹{top_state['Per_Capita_Income']:,.0f})",
            xy=(latest_complete_fy, top_state["Per_Capita_Income"]),
            xytext=(10, -5),
            textcoords="offset points",
            fontsize=8.5,
            fontweight="bold",
            color="#2d3748"
        )
        ax.annotate(
            f"Lowest: {bot_state['State']}\n(₹{bot_state['Per_Capita_Income']:,.0f})",
            xy=(latest_complete_fy, bot_state["Per_Capita_Income"]),
            xytext=(10, -5),
            textcoords="offset points",
            fontsize=8.5,
            fontweight="bold",
            color="#2d3748"
        )

    ax.set_title("Evolution of State-Wise Per-Capita Income in India (2011-12 to 2024-25)\nReal Per Capita Net State Domestic Product (Constant 2011-12 Prices)")
    ax.set_xlabel("Financial Year")
    ax.set_ylabel("Per Capita NSDP (₹ / INR per year)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"₹{x:,.0f}"))
    plt.xticks(rotation=45, ha="right")
    ax.legend(loc="upper left", frameon=True, framealpha=0.95)
    
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[FIGURE 1] Saved: {output_path.name}")


# ==============================================================================
# 2. COMPARISON OF SELECTED STATES ACROSS AVAILABLE YEARS
# ==============================================================================
def plot_selected_states_comparison(df: pd.DataFrame, output_path: Path) -> None:
    """
    Figure 2: Compares a balanced cohort of representative states across
    different economic tiers and geographic regions to demonstrate divergence:
    - High-Income Tier: Goa, Delhi, Haryana, Karnataka, Tamil Nadu
    - Middle-Income Tier: Himachal Pradesh, Andhra Pradesh, Rajasthan, Odisha
    - Lower-Income Tier: Assam, Jharkhand, Uttar Pradesh, Bihar
    """
    fig, ax = plt.subplots(figsize=(11, 6.5))
    
    cohort = {
        "High Income": (["Goa", "Delhi", "Haryana", "Karnataka", "Tamil Nadu"], "#2b6cb0", "-"),
        "Middle Income": (["Himachal Pradesh", "Andhra Pradesh", "Rajasthan", "Odisha"], "#2f855a", "-."),
        "Lower Income": (["Assam", "Jharkhand", "Uttar Pradesh", "Bihar"], "#c53030", ":")
    }
    
    palette = sns.color_palette("tab10", 13)
    c_idx = 0
    
    for tier_name, (states_list, default_color, line_style) in cohort.items():
        for state in states_list:
            st_data = df[df["State"] == state].dropna(subset=["Per_Capita_Income"]).sort_values("Year_Start")
            if not st_data.empty:
                line = ax.plot(
                    st_data["Financial_Year"],
                    st_data["Per_Capita_Income"],
                    label=f"{state} ({tier_name.split()[0]})",
                    linewidth=2.2,
                    linestyle=line_style,
                    color=palette[c_idx % len(palette)]
                )
                c_idx += 1
                
                # Label end of line
                last_row = st_data.iloc[-1]
                ax.annotate(
                    state,
                    xy=(last_row["Financial_Year"], last_row["Per_Capita_Income"]),
                    xytext=(6, -2),
                    textcoords="offset points",
                    fontsize=8,
                    color="#2d3748"
                )

    ax.set_title("Trajectory Comparison of Selected States Across Income Tiers (2011-12 to 2024-25)\nWidening Absolute Economic Gaps Across Representative States")
    ax.set_xlabel("Financial Year")
    ax.set_ylabel("Per Capita NSDP (₹ / INR at 2011-12 Prices)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"₹{x:,.0f}"))
    plt.xticks(rotation=45, ha="right")
    ax.legend(loc="upper left", bbox_to_anchor=(1.08, 1.0), frameon=True, fontsize=8.5, title="State & Economic Tier")
    
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[FIGURE 2] Saved: {output_path.name}")


# ==============================================================================
# 3. PERCENTAGE GROWTH IN PER-CAPITA INCOME (STARTING TO ENDING YEARS)
# ==============================================================================
def plot_percentage_growth_by_state(
    df: pd.DataFrame,
    start_year: str = "2011-12",
    end_year: str = "2023-24",
    output_path: Optional[Path] = None
) -> pd.DataFrame:
    """
    Figure 3: Horizontal bar chart showing total percentage growth from start_year to end_year.
    Sorted in descending order, with bars colored by Region/Zone.
    Includes a reference line for national average growth.
    """
    df_start = df[df["Financial_Year"] == start_year][["State", "Per_Capita_Income", "Region_Zone"]].rename(
        columns={"Per_Capita_Income": "Income_Start"}
    )
    df_end = df[df["Financial_Year"] == end_year][["State", "Per_Capita_Income"]].rename(
        columns={"Per_Capita_Income": "Income_End"}
    )
    
    growth_df = pd.merge(df_start, df_end, on="State").dropna(subset=["Income_Start", "Income_End"])
    
    # Calculate percentage change and CAGR (over 12 elapsed fiscal years)
    periods = 12
    growth_df["Percentage_Growth"] = ((growth_df["Income_End"] - growth_df["Income_Start"]) / growth_df["Income_Start"]) * 100
    growth_df["CAGR_Percent"] = (((growth_df["Income_End"] / growth_df["Income_Start"]) ** (1.0 / periods)) - 1.0) * 100
    growth_df = growth_df.sort_values("Percentage_Growth", ascending=True).reset_index(drop=True)
    
    nat_mean_growth = growth_df["Percentage_Growth"].mean()
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    zone_palette = {
        "Southern": "#3182ce",
        "Western": "#38a169",
        "Northern": "#d69e2e",
        "Eastern": "#e53e3e",
        "Central": "#805ad5",
        "North-Eastern": "#319795"
    }
    
    colors = [zone_palette.get(z, "#718096") for z in growth_df["Region_Zone"]]
    
    bars = ax.barh(growth_df["State"], growth_df["Percentage_Growth"], color=colors, height=0.68, alpha=0.9)
    
    # Reference line for average growth
    ax.axvline(
        nat_mean_growth,
        color="#e53e3e",
        linestyle="--",
        linewidth=1.8,
        label=f"National Average Growth ({nat_mean_growth:.1f}%)"
    )
    
    # Value annotations on bars
    for bar in bars:
        width = bar.get_width()
        ax.annotate(
            f"{width:.1f}%",
            xy=(width, bar.get_y() + bar.get_height() / 2),
            xytext=(4, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=7.5
        )
        
    ax.set_title(f"Cumulative Percentage Growth in Real Per-Capita Income ({start_year} to {end_year})\nState-Wise Growth Performance Colored by Zonal Council Region")
    ax.set_xlabel("Percentage Growth (%)")
    ax.set_ylabel("State / Union Territory")
    
    # Custom legend for zones
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=col) for col in zone_palette.values()]
    legend_labels = list(zone_palette.keys())
    legend_handles.append(plt.Line2D([0], [0], color="#e53e3e", linestyle="--", linewidth=1.8))
    legend_labels.append(f"Mean Growth ({nat_mean_growth:.1f}%)")
    
    ax.legend(legend_handles, legend_labels, loc="lower right", frameon=True, fontsize=8.5, title="Regional Zones")
    
    fig.tight_layout()
    if output_path:
        fig.savefig(output_path)
        print(f"[FIGURE 3] Saved: {output_path.name}")
    plt.close(fig)
    
    return growth_df


# ==============================================================================
# 4. DISTRIBUTION OF STATE-WISE PER-CAPITA INCOME ACROSS MILESTONE YEARS
# ==============================================================================
def plot_income_distribution_boxplots(df: pd.DataFrame, output_path: Path) -> None:
    """
    Figure 4: Box-and-whisker plots with overlaid jittered observations for
    milestone years (2011-12, 2015-16, 2019-20, 2023-24).
    Visualizes the shifting median and the dramatic widening of the Interquartile Range (IQR).
    """
    milestones = ["2011-12", "2015-16", "2019-20", "2023-24"]
    sub_df = df[df["Financial_Year"].isin(milestones)].dropna(subset=["Per_Capita_Income"]).copy()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Boxplot
    sns.boxplot(
        data=sub_df,
        x="Financial_Year",
        y="Per_Capita_Income",
        order=milestones,
        hue="Financial_Year",
        palette="Blues",
        legend=False,
        width=0.45,
        ax=ax,
        showmeans=True,
        meanprops={"marker": "D", "markerfacecolor": "#c53030", "markeredgecolor": "black", "markersize": 6}
    )
    
    # Overlaid jittered points
    sns.stripplot(
        data=sub_df,
        x="Financial_Year",
        y="Per_Capita_Income",
        order=milestones,
        color="#2b6cb0",
        alpha=0.6,
        size=6,
        jitter=0.2,
        ax=ax
    )
    
    # Annotate IQR widening
    iqr_text = []
    for fy in milestones:
        vals = sub_df[sub_df["Financial_Year"] == fy]["Per_Capita_Income"]
        q75, q25 = np.percentile(vals, 75), np.percentile(vals, 25)
        iqr = q75 - q25
        iqr_text.append(f"{fy}: IQR = ₹{iqr:,.0f}")
        
    ax.set_title("Cross-State Distribution of Real Per-Capita Income Across Milestone Years\nBoxplots with Overlaid State Observations (Red Diamond = Mean, Line = Median)")
    ax.set_xlabel("Milestone Financial Year")
    ax.set_ylabel("Per Capita NSDP (₹ / INR at 2011-12 Prices)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"₹{x:,.0f}"))
    
    # Text box showing widening IQR
    ax.text(
        0.03, 0.94,
        "Widening Dispersion (IQR):\n" + "\n".join(iqr_text),
        transform=ax.transAxes,
        fontsize=8.5,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#cbd5e0", alpha=0.9)
    )
    
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[FIGURE 4] Saved: {output_path.name}")


# ==============================================================================
# 5. GAP BETWEEN HIGHER-INCOME AND LOWER-INCOME STATES OVER TIME
# ==============================================================================
def plot_income_gap_and_divergence(df: pd.DataFrame, output_path: Path) -> pd.DataFrame:
    """
    Figure 5: Dual-panel analysis evaluating economic disparity over time:
    - Panel A: Top-to-Bottom Disparity (P90 / P10 ratio & Max / Min ratio)
    - Panel B: Sigma (σ) Convergence Metric - Coefficient of Variation (CV = std / mean)
    """
    yearly_metrics = []
    
    for (year_start, fy), group in df.groupby(["Year_Start", "Financial_Year"]):
        vals = group["Per_Capita_Income"].dropna().values
        if len(vals) < 5:
            continue
            
        mean_v = np.mean(vals)
        std_v = np.std(vals, ddof=1)
        cv_v = std_v / mean_v if mean_v > 0 else np.nan
        
        p90 = np.percentile(vals, 90)
        p10 = np.percentile(vals, 10)
        p90_p10_ratio = p90 / p10 if p10 > 0 else np.nan
        
        min_v = np.min(vals)
        max_v = np.max(vals)
        max_min_ratio = max_v / min_v if min_v > 0 else np.nan
        
        yearly_metrics.append({
            "Year_Start": year_start,
            "Financial_Year": fy,
            "N_States": len(vals),
            "Mean_INR": round(mean_v, 2),
            "Median_INR": round(float(np.median(vals)), 2),
            "Std_Dev_INR": round(std_v, 2),
            "Coefficient_of_Variation_CV": round(cv_v, 4),
            "P90_INR": round(p90, 2),
            "P10_INR": round(p10, 2),
            "P90_P10_Ratio": round(p90_p10_ratio, 2),
            "Max_Min_Ratio": round(max_min_ratio, 2)
        })
        
    metrics_df = pd.DataFrame(yearly_metrics).sort_values("Year_Start").reset_index(drop=True)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    x = range(len(metrics_df))
    labels = metrics_df["Financial_Year"]
    
    # Panel A: Disparity Ratios
    ax1.plot(x, metrics_df["P90_P10_Ratio"], marker="o", color="#2b6cb0", linewidth=2.4, label="P90 / P10 Disparity Ratio (90th vs 10th Percentile)")
    ax1.plot(x, metrics_df["Max_Min_Ratio"], marker="^", color="#d69e2e", linewidth=2.0, linestyle="--", label="Max / Min Ratio (Richest vs Poorest State)")
    ax1.set_ylabel("Disparity Ratio")
    ax1.set_title("Panel A: Evolution of Regional Disparity Ratios Across Indian States")
    ax1.legend(loc="upper left", frameon=True)
    
    # Panel B: Sigma Convergence (CV)
    cv_series = metrics_df["Coefficient_of_Variation_CV"]
    ax2.plot(x, cv_series, marker="s", color="#c53030", linewidth=2.5, label="Inter-state Coefficient of Variation (CV = σ / μ)")
    
    # Fit linear trend to CV
    if len(x) > 2:
        slope, intercept = np.polyfit(x, cv_series, 1)
        ax2.plot(x, slope * np.array(x) + intercept, color="#2d3748", linestyle=":", linewidth=1.8, label=f"CV Trend (Slope: {slope:+.4f}/year)")
        
    ax2.set_title("Panel B: Testing Sigma (σ) Convergence / Divergence (Inter-state CV over Time)")
    ax2.set_xlabel("Financial Year")
    ax2.set_ylabel("Coefficient of Variation (CV)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=45, ha="right")
    ax2.legend(loc="upper left", frameon=True)
    
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[FIGURE 5] Saved: {output_path.name}")
    
    return metrics_df


# ==============================================================================
# 6. NEUTRAL STATE ECONOMIC RANKING TABLE & VISUALIZATION (2011-12 vs 2023-24)
# ==============================================================================
def create_state_ranking_comparison(
    df: pd.DataFrame,
    start_year: str = "2011-12",
    end_year: str = "2023-24",
    output_table_path: Optional[Path] = None,
    output_fig_path: Optional[Path] = None
) -> pd.DataFrame:
    """
    Figure 6 & Table: Compares state economic positions between 2011-12 and 2023-24.
    Presented purely as neutral statistical ranking data without political or value judgments.
    """
    df_start = df[df["Financial_Year"] == start_year][["State", "Per_Capita_Income", "Region_Zone", "Category"]].dropna()
    df_end = df[df["Financial_Year"] == end_year][["State", "Per_Capita_Income"]].dropna()
    
    merged = pd.merge(df_start, df_end, on="State", suffixes=(f"_{start_year}", f"_{end_year}"))
    
    col_start = f"Per_Capita_Income_{start_year}"
    col_end = f"Per_Capita_Income_{end_year}"
    
    # Compute neutral statistical rankings (Rank 1 = Highest Per-Capita Income)
    merged["Rank_2011"] = merged[col_start].rank(ascending=False, method="min").astype(int)
    merged["Rank_2023"] = merged[col_end].rank(ascending=False, method="min").astype(int)
    merged["Rank_Change"] = merged["Rank_2011"] - merged["Rank_2023"]  # Positive means improved rank
    
    merged["Absolute_Growth_INR"] = (merged[col_end] - merged[col_start]).round(2)
    merged["Percentage_Growth_Pct"] = (((merged[col_end] - merged[col_start]) / merged[col_start]) * 100).round(2)
    merged["CAGR_Pct"] = ((((merged[col_end] / merged[col_start]) ** (1.0 / 12)) - 1.0) * 100).round(2)
    
    # Sort by ending rank
    ranking_table = merged.sort_values("Rank_2023").reset_index(drop=True)
    
    reordered_cols = [
        "Rank_2023",
        "Rank_2011",
        "Rank_Change",
        "State",
        "Region_Zone",
        "Category",
        col_start,
        col_end,
        "Absolute_Growth_INR",
        "Percentage_Growth_Pct",
        "CAGR_Pct"
    ]
    ranking_table = ranking_table[reordered_cols]
    
    if output_table_path:
        ranking_table.to_csv(output_table_path, index=False, encoding="utf-8")
        print(f"[TABLE] Saved State Rankings to: {output_table_path.name}")
        
    # Generate Dumbbell / Slope Plot of Ranks
    if output_fig_path:
        fig, ax = plt.subplots(figsize=(9, 11))
        
        y_pos = range(len(ranking_table))
        
        # Plot connecting lines
        for i, row in ranking_table.iterrows():
            r11 = row["Rank_2011"]
            r23 = row["Rank_2023"]
            line_color = "#2f855a" if r23 < r11 else ("#c53030" if r23 > r11 else "#718096")
            ax.plot([r11, r23], [i, i], color=line_color, linewidth=1.5, alpha=0.7)
            
        ax.scatter(ranking_table["Rank_2011"], y_pos, color="#a0aec0", s=60, zorder=3, label="Rank in 2011-12")
        ax.scatter(ranking_table["Rank_2023"], y_pos, color="#2b6cb0", s=60, zorder=4, label="Rank in 2023-24")
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(ranking_table["State"], fontsize=8)
        ax.set_xlabel("Economic Rank (1 = Highest Per-Capita Income, 33 = Lowest)")
        ax.set_title("Shift in State Per-Capita Income Rankings (2011-12 vs 2023-24)\nNeutral Statistical Comparison of Cross-State Positions")
        ax.invert_xaxis()  # Rank 1 on the left
        ax.legend(loc="lower right", frameon=True, fontsize=9)
        
        fig.tight_layout()
        fig.savefig(output_fig_path)
        plt.close(fig)
        print(f"[FIGURE 6] Saved: {output_fig_path.name}")
        
    return ranking_table


# ==============================================================================
# 7. REGIONAL ZONAL COUNCIL SUMMARY TABLE
# ==============================================================================
def create_regional_zone_summary(df: pd.DataFrame, output_path: Path) -> pd.DataFrame:
    """
    Generates a regional breakdown of per-capita income by Zonal Council,
    showing average per-capita income and growth across India's geographic zones.
    """
    milestones = ["2011-12", "2023-24"]
    sub = df[df["Financial_Year"].isin(milestones)].dropna(subset=["Per_Capita_Income"])
    
    zone_summary = sub.groupby(["Region_Zone", "Financial_Year"])["Per_Capita_Income"].agg(
        Num_States="count",
        Mean_Income="mean",
        Median_Income="median",
        Min_Income="min",
        Max_Income="max"
    ).unstack("Financial_Year")
    
    # Flatten multi-index columns
    zone_summary.columns = [f"{stat}_{fy}" for stat, fy in zone_summary.columns]
    zone_summary = zone_summary.reset_index()
    
    # Calculate Regional Zone Growth
    zone_summary["Regional_Mean_Growth_Pct"] = (
        (zone_summary["Mean_Income_2023-24"] - zone_summary["Mean_Income_2011-12"]) /
        zone_summary["Mean_Income_2011-12"] * 100
    ).round(2)
    
    zone_summary.to_csv(output_path, index=False, encoding="utf-8")
    print(f"[TABLE] Saved Regional Zone Summary to: {output_path.name}")
    return zone_summary


# ==============================================================================
# PIPELINE ORCHESTRATOR FOR MODULE 4
# ==============================================================================
def run_visualization_pipeline() -> bool:
    """
    Main execution runner for Module 4: Visualize Findings.
    Generates all 6 figures and 4 summary tables from real cleaned data.
    """
    print_step_banner(
        step_number=4,
        step_name="Visualize Findings (Publication-Quality Visualizations)",
        description="Generate 6 academic-grade figures and statistical summary tables."
    )
    
    paths = get_pipeline_paths()
    fig_dir = paths["outputs_figures"]
    tab_dir = paths["outputs_tables"]
    fig_dir.mkdir(parents=True, exist_ok=True)
    tab_dir.mkdir(parents=True, exist_ok=True)
    
    configure_plot_style()
    df = load_cleaned_panel()
    print(f"[DATA] Loaded cleaned panel: {len(df)} rows, {df['State'].nunique()} states across {df['Financial_Year'].nunique()} years.")
    
    # 1. Figure 1: State-wise per-capita income trajectories
    plot_all_states_trajectories(df, fig_dir / "figure1_state_income_trajectories.png")
    
    # 2. Figure 2: Comparison of selected states across income tiers
    plot_selected_states_comparison(df, fig_dir / "figure2_selected_states_comparison.png")
    
    # 3. Figure 3: Percentage growth horizontal bar chart (by Region/Zone)
    growth_df = plot_percentage_growth_by_state(
        df,
        start_year="2011-12",
        end_year="2023-24",
        output_path=fig_dir / "figure3_percentage_growth_by_state.png"
    )
    growth_df.to_csv(tab_dir / "table_state_growth_summary.csv", index=False, encoding="utf-8")
    
    # 4. Figure 4: Income distribution boxplots across milestone years
    plot_income_distribution_boxplots(df, fig_dir / "figure4_income_distribution_boxplots.png")
    
    # 5. Figure 5: Disparity gap & Sigma convergence (P90/P10 & CV)
    gap_df = plot_income_gap_and_divergence(df, fig_dir / "figure5_income_gap_and_divergence.png")
    gap_df.to_csv(tab_dir / "table_annual_distribution_metrics.csv", index=False, encoding="utf-8")
    
    # 6. Figure 6 & Table: Neutral State Economic Rankings (2011-12 vs 2023-24)
    create_state_ranking_comparison(
        df,
        start_year="2011-12",
        end_year="2023-24",
        output_table_path=tab_dir / "table_state_rankings_2011_vs_2023.csv",
        output_fig_path=fig_dir / "figure6_state_rank_changes.png"
    )
    
    # 7. Regional Zone Summary Table
    create_regional_zone_summary(df, tab_dir / "table_regional_zone_summary.csv")
    
    print("\n" + "=" * 65)
    print(" MODULE 4 VISUALIZATION PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print(f" Figures generated in: {fig_dir.relative_to(paths['root'])}")
    print(f" Tables generated in : {tab_dir.relative_to(paths['root'])}")
    print("=" * 65 + "\n")
    return True


# Backwards compatible alias
run_visualization_step = run_visualization_pipeline


if __name__ == "__main__":
    run_visualization_pipeline()
