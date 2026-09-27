# An Economic Data Pipeline: State-Wise Per-Capita Income Divergence in India (Post-2011)

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![R 4.0+](https://img.shields.io/badge/R-4.0%2B-blue.svg)](https://www.r-project.org/)
[![Status](https://img.shields.io/badge/Pipeline-Complete%20(Modules%201--6)-brightgreen.svg)]()
[![Reproducibility](https://img.shields.io/badge/Reproducibility-Cross--Language%20(Python%20%2B%20R)-orange.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. Project Title
**An Economic Data Pipeline: State-Wise Per-Capita Income Divergence in India (Post-2011)**  
*An end-to-end, automated, and cross-language reproducible empirical study for college course evaluation and viva defense.*

---

## 2. Research Question
> ### *"How has state-wise per-capita income diverged in India since 2011?"*

### Economic Background
Classical neoclassical growth theory (the Solow-Swan model) predicts that in an integrated economy with free factor mobility (labor, capital, and goods), capital-scarce regions will experience faster growth rates than capital-abundant regions due to diminishing marginal returns. Over time, this should produce:
1. **$\sigma$-Convergence:** A steady reduction in the interstate dispersion of per-capita income (measured by a declining Coefficient of Variation, $CV = \sigma / \mu$).
2. **$\beta$-Convergence:** A statistically negative relationship between initial baseline income level and subsequent economic growth rate.

However, in large developing federations like India, agglomeration economies, differentiated human capital formation, and structural shifts toward high-productivity services often counteract convergence. Following the Government of India's benchmark revision to the **2011-12 base series**, this project investigates whether Indian states have converged, diverged, or stratified into persistent regional economic clubs.

---

## 3. Project Objective
1. **Construct a Reliable Data Pipeline:** Ingest, audit, and clean authentic public macroeconomic data from the Reserve Bank of India (RBI) without manual copy-paste errors or data fabrication.
2. **Quantify Interstate Disparities:** Implement vectorized mathematical algorithms (in pure NumPy and Pandas) to evaluate growth rates, compounding (CAGR), percentiles, decile ratios ($P_{90}/P_{10}$), and dispersion metrics ($CV, IQR$).
3. **Produce Publication-Standard Visualizations:** Generate 6 academic-grade figures adhering to strict visual integrity (honest axes, explicit units, zero distortions).
4. **Cross-Language Validation:** Replicate the complete empirical analysis independently in **R (tidyverse/ggplot2)** to prove computational reproducibility.
5. **Package for Open Academic Review:** Structure the repository using standard Git hygiene so any student or faculty evaluator can reproduce all findings from scratch.

---

## 4. Data Sources & Provenance
In accordance with ethical academic research standards, all data in this repository is 100% authentic and verifiable:

1. **Primary Economic Data:**  
   - **Source:** Reserve Bank of India (RBI) Database on Indian Economy (DBIE).  
   - **Handbook:** *Handbook of Statistics on Indian States* (Annual Report).  
   - **Publication ID:** `23468`  
   - **Table Title:** *Per Capita Net State Domestic Product at Current Prices* (Base Year: 2011-12).  
   - **Local File:** `data/raw/raw_rbi_per_capita_nsdp.csv`  
2. **Geographical & Regional Metadata:**  
   - **Source:** Ministry of Home Affairs (MHA), Government of India — Official Zonal Councils Act.  
   - **Zones Defined:** Northern, Central, Eastern, Western, Southern, and North-Eastern Zonal Councils.  
   - **Local File:** `data/raw/raw_state_regional_metadata.csv`  
3. **Provenance Manifest:**  
   - Machine-readable hashes, source URLs, and acquisition timestamps are recorded in `data/raw/dataset_provenance.json`.

---

## 5. Dataset Description

The cleaning pipeline (`python/clean_data.py`) unifies the raw tables into an official long-format panel dataset saved at `data/processed/india_per_capita_income_cleaned.csv`:

| Column Name | Data Type | Description | Example Values |
| :--- | :--- | :--- | :--- |
| `State` | String | Standardized state or UT name | `Karnataka`, `Bihar`, `Delhi` |
| `State_Code` | String | ISO 3166-2:IN jurisdiction identifier | `IN-KA`, `IN-BR`, `IN-DL` |
| `Region_Zone` | String | Official Zonal Council classification | `Southern`, `Eastern`, `Northern` |
| `Category` | String | Administrative tier | `State`, `Union Territory` |
| `Financial_Year` | String | Indian fiscal year (April–March) | `2011-12`, `2019-20`, `2023-24` |
| `Year_Start` | Integer | Starting calendar year of fiscal period | `2011`, `2019`, `2023` |
| `Per_Capita_Income` | Float | Per Capita NSDP at current prices (₹ INR) | `90263.0`, `339813.0` |
| `Per_Capita_NSDP_INR` | Float | Duplicate alias for cross-script compatibility | `90263.0`, `339813.0` |

### Panel Dimensions:
- **Total Jurisdictions:** 34 States and Union Territories.
- **Time Horizon:** 14 Financial Years (2011-12 through 2024-25).
- **Total Panel Cells:** 476 observations ($34 \times 14$).
- **Valid Observations:** 455 valid income entries (21 missing data points due to unreleased state statistical bulletins, primarily in 2024-25).
- **Primary Comparative Sample:** 32 jurisdictions with continuous observations from 2011-12 to 2023-24.

---

## 6. Tools and Technologies
- **Core Languages:** Python 3.9+ and R 4.0+
- **Data Manipulation:** `pandas` (panel pivoting, cleaning), `numpy` (vectorized math), `dplyr`, `tidyr`, `readr`
- **Statistical & Econometric Analysis:** Vectorized implementations of Bessel-corrected sample standard deviation, IQR, CAGR, and Coefficient of Variation.
- **Visualization:** `matplotlib`, `seaborn`, `ggplot2`, `scales`, `gridExtra`
- **File Management & Environment:** `pathlib` (cross-platform path resolution), `unittest` (automated verification)
- **Version Control:** Git

---

## 7. Project Folder Structure

```text
Project/
│
├── data/
│   ├── raw/                             # Immutable source datasets from RBI/MHA
│   │   ├── dataset_provenance.json      # Provenance metadata, hashes, and download dates
│   │   ├── raw_rbi_per_capita_nsdp.csv  # Raw RBI per-capita NSDP table
│   │   ├── raw_state_regional_metadata.csv # State ISO codes and Zonal Council classifications
│   │   └── README.md
│   │
│   └── processed/                       # Standardized panel datasets created by Module 3
│       ├── india_per_capita_income_cleaned.csv # Primary cleaned panel (476 rows)
│       ├── per_capita_nsdp_cleaned.csv         # Direct alias for pipeline compatibility
│       ├── data_quality_summary.csv            # Per-state observation completeness audit
│       └── README.md
│
├── python/                              # Modular Python source code
│   ├── __init__.py                      # Package exports
│   ├── utils.py                         # Cross-platform pathlib helpers & banners
│   ├── download_data.py                 # Data integrity verification & provenance writer
│   ├── clean_data.py                    # Harmonization, state renaming, and panel formatting
│   ├── numpy_metrics.py                 # Vectorized NumPy functions (CAGR, CV, growth rates)
│   ├── test_numpy_metrics.py            # Automated unit tests on synthetic data (11/11 passing)
│   ├── analysis.py                      # Statistical distribution & growth tables
│   ├── visualize.py                     # Publication-grade Matplotlib/Seaborn figures (Figures 1 to 6)
│   └── main.py                          # Master end-to-end pipeline orchestrator
│
├── R/                                   # Independent R reproduction scripts
│   ├── README.md                        # R reproduction guide
│   ├── reproduce_analysis.R             # Primary Module 5 R reproduction pipeline
│   └── reproduce_divergence.R           # Quick standalone CV verification script
│
├── outputs/                             # Final project deliverables
│   ├── figures/                         # Python high-resolution charts (.png at 300 DPI)
│   │   ├── figure1_state_income_trajectories.png
│   │   ├── figure2_selected_states_comparison.png
│   │   ├── figure3_percentage_growth_by_state.png
│   │   ├── figure4_income_distribution_boxplots.png
│   │   ├── figure5_income_gap_and_divergence.png
│   │   ├── figure6_state_rank_changes.png
│   │   └── r/                           # Independent R ggplot2 replications (300 DPI)
│   │       ├── r_figure1_state_trajectories.png
│   │       ├── r_figure2_selected_states.png
│   │       ├── r_figure3_growth_by_state.png
│   │       ├── r_figure4_distribution_boxplots.png
│   │       ├── r_figure5_gap_and_divergence.png
│   │       └── r_figure6_state_rank_changes.png
│   │
│   └── tables/                          # Python summary and econometric tables (.csv)
│       ├── table_annual_distribution_metrics.csv
│       ├── table_state_growth_summary.csv
│       ├── table_state_rankings_2011_vs_2023.csv
│       ├── table_regional_zone_summary.csv
│       └── r/                           # Independent R analytical tables (.csv)
│           ├── r_annual_distribution_metrics.csv
│           ├── r_state_growth_summary.csv
│           ├── r_state_rankings_2011_vs_2023.csv
│           ├── r_regional_zone_summary.csv
│           └── r_python_vs_r_reproducibility_comparison.csv
│
├── docs/                                # Complete methodological and academic documentation
│   ├── data_dictionary.md               # Definitions of economic variables & base years
│   ├── methodology_divergence.md        # Econometric models, formulas & viva Q&A
│   ├── data_quality_report.md           # Module 3 data audit & verification log
│   ├── visualization_analysis_notes.md  # Module 4 empirical findings & figure breakdowns
│   ├── cross_language_reproducibility_report.md # Module 5 Python vs R validation report
│   └── final_project_checklist.md       # Module 6 quality and audit checklist
│
├── requirements.txt                     # Pinned Python package dependencies
├── .gitignore                           # Excludes bytecode, environments, temp files & secrets
└── README.md                            # Comprehensive project manual
```

---

## 8. Installation Instructions & Setup

### Prerequisites
- **Python:** 3.9 or higher
- **R (Optional, for cross-language validation):** 4.0 or higher
- **Git**

### Step-by-Step Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Project
   ```

---

## 9. Python Environment Setup
It is recommended to run the project in an isolated virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Activate on macOS / Linux:
source .venv/bin/activate
```

---

## 10. Required Python Packages
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

---

## 11. How to Run the Python Pipeline

### Option A: End-to-End Orchestrator (Recommended)
Run the entire pipeline from raw data checks to R reproduction in a single command:
```bash
python python/main.py
```

### Option B: Run Individual Modules Step-by-Step
```bash
# 1. Verify raw data and write provenance hashes
python python/download_data.py

# 2. Run NumPy unit tests on edge cases
python -m unittest python/test_numpy_metrics.py

# 3. Clean, reshape, and merge data
python python/clean_data.py

# 4. Generate statistical tables
python python/analysis.py

# 5. Generate publication figures (outputs/figures/)
python python/visualize.py
```

---

## 12. How to Reproduce the Analysis
To verify that all outputs can be regenerated completely from scratch:
1. Delete generated artifacts:
   ```powershell
   Remove-Item outputs/figures/*.png, outputs/tables/*.csv -Force
   ```
2. Re-run `python python/main.py`.
3. Check `outputs/figures/` and `outputs/tables/` to verify that all 6 figures and 4 CSV tables are recreated cleanly.

---

## 13. How to Run the R Analysis
To execute the independent R replication pipeline:
```bash
Rscript R/reproduce_analysis.R
```
*Note: Missing R packages (`readr`, `dplyr`, `ggplot2`, `tidyr`, `scales`, `gridExtra`) are automatically installed on first run.*

---

## 14. Where the Outputs are Generated

| Deliverable Type | Directory | Format & Resolution | Key Contents |
| :--- | :--- | :--- | :--- |
| **Python Figures** | `outputs/figures/` | PNG (300 DPI) | Figures 1 to 6 (Trajectories, Comparisons, Growth Bars, Boxplots, Gap Evolution, Rank Mobility) |
| **R Figures** | `outputs/figures/r/` | PNG (300 DPI) | R Figures 1 to 6 replicated via `ggplot2` |
| **Python Tables** | `outputs/tables/` | CSV | Annual Distribution Metrics, State Growth Summary, State Rankings, Regional Zone Summary |
| **R Tables** | `outputs/tables/r/` | CSV | R Annual Metrics, State Growth, Rankings, Zonal Aggregations, Cross-Language Comparison Table |

---

## 15. Main Findings Regarding the Research Question

### 1. Widening Absolute Disparity (Absolute Divergence)
- **Top-to-Poorest Rupee Gap:** The absolute per-capita income difference between the richest state (Goa / Sikkim) and the lowest state (Bihar) expanded from **₹2,37,694 in 2011-12** to **₹5,23,752 in 2023-24** (more than doubling in nominal terms).
- **Interquartile Range ($IQR$):** The spread of the middle 50% of states expanded from **₹47,725** to **₹1,63,607**, showing that interstate living standards have grown increasingly heterogeneous.

### 2. Stubborn Persistence of Relative Inequality (Lack of $\sigma$-Convergence)
- **Interstate Coefficient of Variation ($CV = \sigma / \mu$):** Neoclassical economic theory predicts a declining $CV$ as poorer economies catch up. Empirically, interstate CV started at **0.592** in 2011-12, dipped slightly to 0.510 in 2013-14, rose back to 0.561 by 2017-18, and stood at **0.535 in 2023-24**.
- **Decile Ratio ($P_{90} / P_{10}$):** The threshold income of the 90th percentile state remained between **3.5x and 3.9x** that of the 10th percentile state throughout the entire period.

### 3. Southern & Western Dynamism vs. Agrarian Stagnation
- In 2011-12, **Karnataka** (₹90,263) and **Punjab** (₹85,577) had nearly identical per-capita incomes.
- By 2023-24, Karnataka reached **₹3,39,813** (CAGR: 11.68%), whereas Punjab reached **₹2,05,374** (CAGR: 7.57%) — creating a **₹1,34,439 gap** between two states that started at parity.
- The **Southern Zone** achieved the highest regional mean growth (+215.0%), with Telangana (+6 ranks, to 5th) and Karnataka (+6 ranks, to 6th) entering the top echelon.

### 4. Bottom Tail Structural Immobility
- **Bihar** (Rank 32) and **Uttar Pradesh** (Rank 31) occupied the identical bottom two positions in 2023-24 as they did in 2011-12, demonstrating severe structural barriers to economic catch-up despite positive nominal growth.

---

## 16. Limitations
1. **Nominal Current Prices:** The underlying RBI series records Per Capita NSDP at Current Prices. Nominal figures reflect both real volume growth and state-specific inflation rates.
2. **Purchasing Power Parity (PPP):** Nominal per-capita figures do not adjust for interstate cost-of-living differentials (e.g., housing and living expenses in Delhi or Chandigarh are materially higher than in rural Bihar or Odisha).
3. **Provisional 2024-25 Figures:** Financial Year 2024-25 figures are currently available for only 25 of 34 jurisdictions in the RBI repository; comparative growth rankings are therefore evaluated through 2023-24 to maintain consistent sample integrity.

---

## 17. Reproducibility Instructions & Cross-Language Validation

To verify reproducibility across programming environments:
1. Run `python python/main.py`.
2. Inspect `outputs/tables/r/r_python_vs_r_reproducibility_comparison.csv`:
   - Annual Median Difference: **₹0.00 across all 14 years**.
   - Maximum Mean Difference: **₹0.0048** (< half a paisa, due to display rounding in CSVs).
   - Maximum CV Difference: **0.000048** (due to 4 decimal place rounding in CSVs).
3. Full documentation is provided in [`docs/cross_language_reproducibility_report.md`](docs/cross_language_reproducibility_report.md).

---

## 18. Data Citation & Academic Source Information

When citing the data and methodology in academic papers or course evaluations:

```bibtex
@misc{rbi_handbook_nsdp_2024,
  author       = {{Reserve Bank of India}},
  title        = {Handbook of Statistics on Indian States: Per Capita Net State Domestic Product at Current Prices (2011-12 Series)},
  year         = {2024},
  howpublished = {RBI Database on Indian Economy (DBIE)},
  note         = {Publication ID: 23468. Access Date: September 2026}
}

@misc{mospi_sna_2015,
  author       = {{Ministry of Statistics and Programme Implementation}},
  title        = {Changes in Methodology and Base Year of National Accounts Statistics (Base 2011-12)},
  year         = {2015},
  publisher    = {Government of India, New Delhi}
}
```

---

## 19. Viva Defense Cheat Sheet

| Question | Short Viva Answer |
| :--- | :--- |
| **Why use `pathlib`?** | `pathlib` provides object-oriented paths that adapt across Windows (`\`) and UNIX (`/`), eliminating hardcoded paths. |
| **Why separate raw and processed data?** | Preserves raw data provenance; raw data remains immutable, while transformations remain 100% reproducible. |
| **What is $\sigma$-convergence?** | A reduction in interstate dispersion of real per-capita income over time, measured by the Coefficient of Variation ($CV = \sigma / \mu$). |
| **What is $\beta$-convergence?** | A negative relationship between initial income (2011-12) and subsequent growth rate, showing whether poor states catch up. |
| **Did India converge post-2011?** | No. Absolute gaps widened, relative inequality ($CV \approx 0.53 - 0.59$) persisted, and southern tech states pulled away from northern agrarian states. |
| **Why test across Python and R?** | Independent cross-language reproduction proves the findings are mathematical realities, not artifacts of software libraries. |

---

## 20. Git Publishing Guide

To publish or clone this project repository to GitHub or another Git host:

```bash
# 1. Check current status
git status

# 2. Stage all files (respecting .gitignore)
git add .

# 3. Create a descriptive commit
git commit -m "feat: complete economic data pipeline (Modules 1-6)"

# 4. Check branch name
git branch -M main

# 5. Link to your remote GitHub repository (replace with your repo URL)
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# 6. Push to remote
git push -u origin main
```
