# R Reproduction Directory (`R/`)

This directory contains R scripts for independent cross-language verification and replication of the Indian economic divergence analysis.

## Purpose in the Pipeline
An essential standard in empirical economics is **independent reproducibility across programming environments**:
1. **Python** executes automated data ingestion, cleaning, primary econometric analysis, and visualization.
2. **R** independently ingests the cleaned panel dataset (`data/processed/india_per_capita_income_cleaned.csv`) using `readr`, `dplyr`, and `tidyr` to compute all metrics (Means, Medians, Standard Deviations, Coefficient of Variation, CAGR, Percentages, and Ordinal Rankings).
3. **ggplot2** generates matching publication-grade visualizations.
4. If both Python and R yield matching statistical metrics, the results are validated.

## Executable Scripts
- **`reproduce_analysis.R`** *(Primary Module 5 Replication Script)*:
  - Ingests cleaned data.
  - Performs data audits.
  - Calculates annual dispersion, growth rates, and rankings.
  - Renders 6 `ggplot2` charts into `outputs/figures/r/`.
  - Exports 5 comparative tables into `outputs/tables/r/`.
  - Runs automated difference checks against Python outputs.
- **`reproduce_divergence.R`**:
  - Scaffolding script for quick CV verification.

## How to Run
From the project root:
```bash
Rscript R/reproduce_analysis.R
```
*(Required packages `readr`, `dplyr`, `ggplot2`, `tidyr`, `scales`, and `gridExtra` are automatically installed by the script if missing).*

## Outputs Produced
- **Figures:** `outputs/figures/r/` (300 DPI PNGs: `r_figure1_state_trajectories.png` through `r_figure6_state_rank_changes.png`).
- **Tables:** `outputs/tables/r/` (CSV summaries: `r_annual_distribution_metrics.csv`, `r_state_growth_summary.csv`, `r_state_rankings_2011_vs_2023.csv`, `r_regional_zone_summary.csv`, and `r_python_vs_r_reproducibility_comparison.csv`).
- **Report:** Detailed findings and difference reconciliations are in [`docs/cross_language_reproducibility_report.md`](../docs/cross_language_reproducibility_report.md).
