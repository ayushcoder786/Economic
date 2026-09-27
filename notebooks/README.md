# Jupyter Notebooks Directory (`notebooks/`)

This directory contains interactive Jupyter notebooks providing exploratory data analysis, econometric modeling, and visual reporting for the Indian economic divergence research project.

## Available Notebooks

### 1. [`01_exploratory_inspection.ipynb`](01_exploratory_inspection.ipynb)
- **Focus:** Initial exploratory data analysis (EDA), panel structure validation, missing data audits, and cross-sectional distribution inspection.
- **Key Analyses:**
  - Ingestion of the 476-observation cleaned panel dataset.
  - Verification of jurisdiction counts (34 States/UTs) and financial year span (2011-12 to 2024-25).
  - Annual summary statistics (Mean, Median, Standard Deviation, Min, Max, and CV).
  - Kernel Density Estimation (KDE) across milestone years showing distribution flattening and right-skewness.
  - Mean vs. Median longitudinal comparison.

### 2. [`02_divergence_deep_dive.ipynb`](02_divergence_deep_dive.ipynb)
- **Focus:** Econometric evaluation of the core research question: *"How has state-wise per-capita income diverged in India since 2011?"*
- **Key Analyses:**
  - Quantitative testing of **$\sigma$-convergence** (interstate dispersion & Coefficient of Variation).
  - Interquartile Range ($IQR$) and Decile Ratio ($P_{90} / P_{10}$) tracking.
  - Longitudinal growth rate and Compound Annual Growth Rate (CAGR) calculations over the 12-year primary comparative horizon (2011-12 to 2023-24).
  - Zonal Council regional grouping and clustering analysis.
  - Ordinal state ranking and mobility assessment.
  - **Embedded High-Resolution Visualizations:** Displays all 6 publication figures inline.

---

## How to Run & Regenerate

### Option A: Open Interactively in VS Code / Jupyter Lab
Open either `.ipynb` file directly in VS Code, JupyterLab, or GitHub's online notebook viewer.

### Option B: Programmatically Regenerate from Scratch
To regenerate and re-execute both notebooks with fresh data:
```bash
python python/generate_notebooks.py
```
