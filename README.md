# An Economic Data Pipeline: Indian State-Wise Per-Capita Income Divergence (Post-2011)

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Module%203-Data%20Cleaning%20%26%20Merging%20Completed-brightgreen.svg)]()
[![Reproducibility](https://img.shields.io/badge/Reproducibility-Cross--Language%20(Python%20%2B%20R)-orange.svg)]()

---

## 1. Project Objective & Research Question

### Research Question
> **"How has state-wise per-capita income diverged in India since 2011?"**

### Academic Context
Standard neoclassical growth models (Solow-Swan) predict economic convergence across regional units with free movement of goods, labor, and capital. However, empirical studies in developing federations—particularly India—often suggest persistent or widening regional disparities between wealthier coastal/southern states and poorer inland/northern states.

Following the Government of India's revision of national accounts to the **2011-12 base year**, this course-long project builds an automated, end-to-end reproducible data pipeline to evaluate:
1. **Sigma ($\sigma$) Convergence:** Is the interstate dispersion (Coefficient of Variation) of real per capita income narrowing or expanding?
2. **Beta ($\beta$) Convergence:** Are initially poorer states in 2011 growing faster than richer states, or is divergence intensifying?

---

## 2. End-to-End Pipeline Workflow

The project follows a linear, reproducible research pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│                       1. Raw Data                           │
│     RBI DBIE / MoSPI Handbooks (Placed in data/raw/)        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       2. Cleaning                           │
│  Standardize State Names, Clean Years, Reshape (Wide→Long)   │
│                 Saves to data/processed/                    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       3. Analysis                           │
│  Compute Coefficient of Variation (σ) & CAGR Growth (β)     │
│                 Saves to outputs/tables/                    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    4. Visualization                         │
│  Generate Publication Charts (DPI=300) in outputs/figures/  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    5. R Reproduction                        │
│   Cross-Language Statistical Verification (R scripts in R/) │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    6. Git Repository                        │
│   Version-Controlled Codebase & Artifacts for Viva Defense  │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Directory Structure

```text
Project/
│
├── data/
│   ├── raw/                 # Unaltered source files from RBI/MoSPI
│   │   ├── .gitkeep
│   │   ├── README.md
│   │   └── dataset_provenance.json
│   └── processed/           # Cleaned, standardized panel datasets
│       ├── .gitkeep
│       └── README.md
│
├── notebooks/               # Exploratory data analysis (EDA) & experiments
│   ├── .gitkeep
│   └── README.md
│
├── python/                  # Modular Python source code
│   ├── __init__.py          # Package initialization (exports Module 2 NumPy functions)
│   ├── utils.py             # Cross-platform paths (pathlib) & helper utilities
│   ├── download_data.py     # Data verification, guide, & provenance manifest
│   ├── clean_data.py        # Harmonization, state renaming, and panel formatting
│   ├── numpy_metrics.py     # Vectorized NumPy functions (Module 2: CAGR, CV, growth rates)
│   ├── test_numpy_metrics.py# Comprehensive unit test suite with synthetic data
│   ├── analysis.py          # σ-convergence (CV) and β-convergence (CAGR) metrics
│   ├── visualize.py         # Publication-grade Matplotlib/Seaborn figures
│   └── main.py              # Master pipeline orchestrator
│
├── R/                       # Independent cross-validation scripts
│   ├── .gitkeep
│   ├── README.md
│   └── reproduce_divergence.R
│
├── outputs/                 # Final deliverables
│   ├── figures/             # High-resolution charts (.png at 300 dpi)
│   └── tables/              # Summary and econometric tables (.csv)
│
├── docs/                    # Theoretical and methodological documentation
│   ├── data_dictionary.md   # Definitions of economic variables & base years
│   └── methodology_divergence.md # Econometric models, formulas & viva Q&A
│
├── requirements.txt         # Required Python packages
├── .gitignore               # Git rules excluding caches, environments & artifacts
└── README.md                # Project documentation
```

---

## 4. Setup and Quickstart

### Prerequisites
- Python 3.9 or higher
- Optional: R 4.0+ (for Stage 5 cross-validation)

### Installation
1. Clone or open the repository:
   ```bash
   cd Project
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Module 1 Pipeline Checks
To verify directory structures, paths, and compile each module:
```bash
python python/main.py
```

Or execute individual modules independently:
```bash
python python/utils.py
python python/download_data.py
python python/clean_data.py
python python/analysis.py
python python/visualize.py
```

---

## 5. Academic Data Integrity
In accordance with ethical academic research standards:
- **No data fabrication:** This project does not generate synthetic or fictitious economic numbers.
- **Official Sources:** Real historical series are sourced directly from:
  1. **Reserve Bank of India (RBI):** *Handbook of Statistics on Indian States*
  2. **Ministry of Statistics and Programme Implementation (MoSPI):** *State Domestic Product at Constant 2011-12 Prices*
- Data ingestion guidelines are built directly into `python/download_data.py`.

---

## 6. Viva Defense Cheat Sheet

| Question | Short Viva Answer |
| :--- | :--- |
| **Why use `pathlib`?** | `pathlib` provides object-oriented paths that adapt across Windows (`\`) and UNIX (`/`), eliminating hardcoded paths. |
| **Why separate raw and processed data?** | Preserves raw data provenance; raw data remains immutable, while transformations remain 100% reproducible. |
| **What is $\sigma$-convergence?** | A reduction in interstate dispersion of real per-capita income over time, measured by the Coefficient of Variation ($CV = \sigma / \mu$). |
| **What is $\beta$-convergence?** | A negative relationship between initial income (2011-12) and subsequent growth rate, showing whether poor states catch up. |
| **Why Constant (2011-12) Prices?** | Constant prices adjust for price inflation, isolating real volume growth in output per resident. |
