# Data Quality and Merge Validation Report

**Module 3: Clean and Merge Data**  
**Project:** An Economic Data Pipeline: State-wise Per-Capita Income Divergence in India (Post-2011)  
**Date:** 2026-09-27  

---

## 1. Executive Summary

This report provides the complete verification audit for the cleaning and merging of authentic Indian economic data.

- **Primary Source:** Reserve Bank of India (RBI) *Handbook of Statistics on Indian States* (Publication ID: 23468).
- **Secondary Source:** Ministry of Home Affairs / NITI Aayog (Zonal Council Classification & ISO Codes).
- **Metric:** Per Capita Net State Domestic Product (NSDP) in INR at Constant (2011-12) Prices.
- **Total Records:** 476 state-year panel observations.
- **States Covered:** 34 States & Union Territories.
- **Time Horizon:** 2011-12 to 2024-25 (14 fiscal years).
- **Duplicate Records:** 0 (Zero duplicate state-year keys).

---

## 2. Merge Diagnostics

| Diagnostic Indicator | Result | Status |
| :--- | :--- | :--- |
| **Rows Before Merge (Income Panel)** | 476 | Baseline |
| **Rows After Merge** | 476 | Matches 1:1 (No record inflation) |
| **States in Income Dataset** | 34 | Complete coverage of active reporting states/UTs |
| **States in Metadata Registry** | 36 | All 36 States/UTs of India |
| **Matched States** | 34 | 100% of income states successfully matched |
| **Unmatched Income States** | [] | None (0 unmatched) |
| **Unmatched Metadata States** | Dadra and Nagar Haveli and Daman and Diu, Lakshadweep | Lakshadweep, Dadra & Nagar Haveli (Expected per MoSPI policy) |

> [!NOTE]
> **Why are Dadra & Nagar Haveli/Daman & Diu and Lakshadweep in the metadata but not the income series?**  
> Per MoSPI and RBI official guidelines, small union territories without a legislative assembly (such as Lakshadweep and Dadra & Nagar Haveli) do not compile separate State Domestic Product (SDP) accounts. They are retained in the regional metadata registry for complete administrative coverage without corrupting the economic panel.

---

## 3. Data Cleaning Decisions Audit Trail

1. **Raw File Invariance:** Raw files in `data/raw/` were read in read-only mode and preserved without modification.
2. **State Name Harmonization:** Removed MediaWiki markup, brackets, trailing footnote asterisks (`*`), and normalized all spelling variants (e.g., `Andaman & Nicobar Islands` -> `Andaman and Nicobar Islands`, `Jammu & Kashmir*` -> `Jammu and Kashmir`).
3. **Currency Value Parsing:** Removed Indian comma notation (`1,06,085` -> `106085.0`) and non-breaking spaces.
4. **Missing Values Representation:** Replaced missing cell markers (`-`, `NA`) with IEEE standard `np.nan` (float64).
5. **No Data Deletion Rule:** In accordance with academic reproducibility rules, **no rows were dropped**. Years with missing provisional estimates (such as early years for Ladakh prior to its creation in 2019) are explicitly preserved as `NaN` with documented reasons.

---

## 4. Missing Value Audit by Column

| Column Name | Data Type | Missing Count | Valid Count | Completeness |
| :--- | :--- | :--- | :--- | :--- |
| `State` | String | 0 | 476 | 100.0% |
| `State_Code` | String | 0 | 476 | 100.0% |
| `Region_Zone` | String | 0 | 476 | 100.0% |
| `Category` | String | 0 | 476 | 100.0% |
| `Financial_Year` | String | 0 | 476 | 100.0% |
| `Year_Start` | Integer | 0 | 476 | 100.0% |
| `Per_Capita_Income` | Float64 | 21 | 455 | 95.6% |

---

## 5. Regional Zone Distribution

```
Region_Zone
Central          4
Eastern          4
North-Eastern    8
Northern         8
Southern         7
Western          3
```
