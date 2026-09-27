# Cross-Language Reproducibility Report (Python & R)

**Project:** An Economic Data Pipeline  
**Research Question:** *"How has state-wise per-capita income diverged in India since 2011?"*  
**Module:** Module 5 — Reproduce the Analysis in R  
**Languages Evaluated:**  
- **Python:** 3.14.4 (Pandas 3.0.0, NumPy 2.4.2, Matplotlib 3.10.8, Seaborn 0.13.2)  
- **R:** 4.6.1 (tidyverse, readr 2.2.0, dplyr 1.2.1, ggplot2 4.0.3, tidyr 1.3.2, scales 1.4.0)  
**Primary Dataset:** `data/processed/india_per_capita_income_cleaned.csv` (Source: RBI *Handbook of Statistics on Indian States*, Pub ID: 23468).  

---

## 1. Executive Summary

A core standard of modern computational economics is **independent reproducibility across programming languages**. To guarantee that the empirical findings regarding Indian interstate income divergence are not artifacts of Python-specific libraries, numerical libraries, or visualization defaults, the entire analysis pipeline was independently implemented and executed in **R 4.6.1**.

### Primary Confirmation
- **100% Core Numerical Identity:** The calculated annual medians, state percentage growth rates, compound annual growth rates (CAGR), and ordinal state rankings in R match the Python outputs **identically**.
- **Negligible Differences:** The maximum absolute difference in interstate annual means between Python and R across all 14 years is **₹0.0048** (less than half a paisa), and for the Coefficient of Variation ($CV$) is **0.000048**, attributable entirely to display rounding (2 and 4 decimal places) in the Python CSV exports.
- **Visual Equivalence:** All 6 publication-grade figures were faithfully replicated using `ggplot2` in `outputs/figures/r/`, exhibiting the same trajectories, distribution shifts, decile ratios, and mobility patterns.

---

## 2. Key Statistical Comparison Table (Python vs. R)

The table below contrasts the headline statistics computed independently by Python and R from the common cleaned panel dataset:

| Economic Metric | Comparison Year / Group | Python Result | R Result | Absolute Difference | Identifiable Reason for Difference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **All-State Mean** | 2011-12 | ₹83,311.85 | ₹83,311.85 | ₹0.0015 | Python exported to 2 decimal places |
| **All-State Mean** | 2023-24 | ₹2,42,644.45 | ₹2,42,644.45 | ₹0.0045 | Python exported to 2 decimal places |
| **All-State Median** | 2011-12 | ₹73,540.00 | ₹73,540.00 | **₹0.0000** | Identical calculation |
| **All-State Median** | 2023-24 | ₹2,34,721.00 | ₹2,34,721.00 | **₹0.0000** | Identical calculation |
| **Standard Deviation ($\sigma$)** | 2011-12 | ₹49,338.13 | ₹49,338.13 | ₹0.0047 | Sample SD ($N-1$); display rounding |
| **Standard Deviation ($\sigma$)** | 2023-24 | ₹1,29,753.05 | ₹1,29,753.05 | ₹0.0030 | Sample SD ($N-1$); display rounding |
| **Coefficient of Variation ($CV$)** | 2011-12 | 0.5922 | 0.592210 | 0.000010 | Python rounded to 4 decimals |
| **Coefficient of Variation ($CV$)** | 2023-24 | 0.5347 | 0.534746 | 0.000046 | Python rounded to 4 decimals |
| **90th Percentile ($P_{90}$)** | 2011-12 | ₹1,50,863.40 | ₹1,50,863.40 | **₹0.0000** | Linear interpolation (Type 7) matches |
| **10th Percentile ($P_{10}$)** | 2011-12 | ₹40,038.00 | ₹40,038.00 | **₹0.0000** | Linear interpolation (Type 7) matches |
| **$P_{90} / P_{10}$ Decile Ratio** | 2011-12 | 3.7680 | 3.7680 | **0.0000** | Identical ratio |
| **$P_{90} / P_{10}$ Decile Ratio** | 2023-24 | 3.4894 | 3.4894 | **0.0000** | Identical ratio |
| **Karnataka Growth (%)** | 2011-12 to 2023-24 | 276.47% | 276.4699% | 0.0001% | Rounding to 2 decimal places |
| **Karnataka CAGR (%)** | 2011-12 to 2023-24 | 11.68% | 11.6805% | 0.0005% | Rounding to 2 decimal places |
| **Bihar Growth (%)** | 2011-12 to 2023-24 | 185.98% | 185.9816% | 0.0016% | Rounding to 2 decimal places |
| **Bihar CAGR (%)** | 2011-12 to 2023-24 | 9.15% | 9.1511% | 0.0011% | Rounding to 2 decimal places |
| **Top Rank 1 State** | 2023-24 | Sikkim | Sikkim | **0 ranks** | Identical ordinal ranking |
| **Bottom Rank 32 State** | 2023-24 | Bihar | Bihar | **0 ranks** | Identical ordinal ranking |
| **Top Rank Climber** | 2011-12 to 2023-24 | Tripura (+7) | Tripura (+7) | **0 ranks** | Identical rank mobility calculation |
| **Southern Zone Growth** | Regional Mean | 215.04% | 215.04% | **0.00%** | Identical zonal grouping & mean |
| **Eastern Zone Growth** | Regional Mean | 187.64% | 187.64% | **0.00%** | Identical zonal grouping & mean |

---

## 3. Technical & Algorithmic Notes on Cross-Language Behavior

When reconciling computational outputs between Python (NumPy/Pandas) and R (base/tidyverse), three primary methodological considerations were addressed:

### 1. Degrees of Freedom for Variance & Standard Deviation
- **Python / NumPy:** `np.std(ddof=0)` computes the population standard deviation ($N$), whereas `pandas.Series.std()` defaults to `ddof=1` (sample standard deviation, $N-1$).
- **R:** `sd()` exclusively calculates sample standard deviation using denominator $N - 1$.
- **Reconciliation:** Both pipelines consistently apply **sample standard deviation ($N - 1$)**, ensuring identical values.

### 2. Quantile & Percentile Estimation
- **Python:** `np.percentile()` and `pandas.Series.quantile()` default to `method="linear"`.
- **R:** The `quantile()` function in base R defaults to `type = 7` ($\hat{Q}(p) = (1-\gamma) x_{[j]} + \gamma x_{[j+1]}$ where $j = \lfloor (n-1)p + 1 \rfloor$ and $\gamma = (n-1)p + 1 - j$).
- **Reconciliation:** `type = 7` in R is mathematically equivalent to the linear interpolation default in Python. Consequently, all quantiles ($Q_1$, Median, $Q_3$, $P_{10}$, $P_{90}$) match with **zero difference**.

### 3. CAGR & Compounding Horizon
- Both implementations utilize the standard continuous-discrete compounding formulation:
  $$\text{CAGR} = \left(\frac{Y_{2023\text{-}24}}{Y_{2011\text{-}12}}\right)^{1/12} - 1$$
- With baseline $t_0 = 2011\text{-}12$ and terminal year $t = 2023\text{-}24$, $n = 12$ complete elapsed annual periods. Both pipelines yield identical annualized percentage growth rates.

---

## 4. Replicated Deliverables in R

### A. R Generated Figures (`outputs/figures/r/`)
All figures were plotted with `ggplot2` and exported at **300 DPI**:
1. `r_figure1_state_trajectories.png`: State-wise per-capita income trajectories (2011-12 to 2024-25) highlighting macro-states against the national interstate mean.
2. `r_figure2_selected_states.png`: Indexed relative growth trajectories ($2011\text{-}12 = 100$) for 8 representative macro-states.
3. `r_figure3_growth_by_state.png`: Horizontal bar chart of cumulative percentage growth and CAGR by state, sorted and grouped by Zonal Council region.
4. `r_figure4_distribution_boxplots.png`: Distribution boxplots across milestone years with overlaid individual jittered observations and mean diamonds.
5. `r_figure5_gap_and_divergence.png`: Dual-panel time series of Interstate Coefficient of Variation ($CV$) and $P_{90} / P_{10}$ decile disparity ratio.
6. `r_figure6_state_rank_changes.png`: Ordinal rank mobility slopegraph tracking state position shifts between 2011-12 and 2023-24.

### B. R Generated Summary Tables (`outputs/tables/r/`)
1. `r_annual_distribution_metrics.csv`: 14-year cross-sectional dispersion series.
2. `r_state_growth_summary.csv`: 32-state panel summary with baseline, end-period, percentage growth, and CAGR.
3. `r_state_rankings_2011_vs_2023.csv`: State ordinal ranking and mobility table.
4. `r_regional_zone_summary.csv`: Zonal Council economic performance aggregations.
5. `r_python_vs_r_reproducibility_comparison.csv`: Year-by-year direct comparative difference matrix between Python and R.

---

## 5. Instructions for Independent Replication

To verify that another student or reviewer can independently run this pipeline on any machine:

### Running the Python Pipeline:
```bash
python python/visualize.py
```

### Running the R Pipeline:
```powershell
Rscript R/reproduce_analysis.R
```
*(Packages `readr`, `dplyr`, `ggplot2`, `tidyr`, `scales`, and `gridExtra` are automatically installed by the script if not already present on the host system).*
