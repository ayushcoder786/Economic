# Processed Data Directory (`data/processed/`)

This directory contains clean, analysis-ready datasets produced programmatically by `python/clean_data.py`.

## Files Produced
- **`per_capita_nsdp_cleaned.csv`**: Standardized panel dataset with columns:
  - `State`: Standardized State or UT name (e.g., 'Odisha', 'Uttarakhand').
  - `Financial_Year`: Fiscal year string (e.g., '2011-12', '2012-13').
  - `Year_Start`: Integer starting calendar year (e.g., 2011, 2012).
  - `Per_Capita_NSDP_INR`: Real Per Capita NSDP at constant 2011-12 prices in INR.

## Reproducibility Note
Never edit files in this folder manually. If raw data changes, regenerate these files by running:
```bash
python python/clean_data.py
```
