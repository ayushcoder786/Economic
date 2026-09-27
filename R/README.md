# R Reproduction Directory (`R/`)

This directory is designated for cross-language verification and econometric replication using R.

## Purpose in the Pipeline
An essential standard in empirical economics is **independent reproducibility**:
1. Python executes the automated data harvesting, cleaning, primary econometric analysis, and visualization.
2. R ingests the tidy dataset (`data/processed/per_capita_nsdp_cleaned.csv`) to independently replicate the Sigma (σ) and Beta (β) convergence calculations.
3. If both Python and R yield matching statistical metrics (e.g. identical Coefficient of Variation and regression coefficients), the results are validated.

## Planned Files
- `reproduce_divergence.R`: Replicates the annual CV dispersion and regression estimation using `tidyverse` / `ggplot2`.
