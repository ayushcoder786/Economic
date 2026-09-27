# Data Dictionary: Indian State Economic Accounts (Post-2011)

This document provides exact economic definitions, units, and source classifications for the variables used throughout the Economic Data Pipeline.

---

## 1. Core Variables

| Variable Name | Data Type | Units / Format | Description | Economic Significance |
| :--- | :--- | :--- | :--- | :--- |
| `State` | String | Categorical | Standardized name of Indian State or Union Territory | Unit of cross-sectional analysis (N ≈ 30+ states & UTs). |
| `Financial_Year` | String | `YYYY-YY` (e.g. `2011-12`) | Indian fiscal year running from April 1 to March 31 | Time dimension of the panel. |
| `Year_Start` | Integer | `YYYY` (e.g. `2011`) | Calendar year in which the financial year commences | Used for sorting, chronological calculations, and regressions. |
| `Per_Capita_NSDP_INR` | Float | Indian Rupees (INR) | Per Capita Net State Domestic Product at **Constant (2011-12) Prices** | **Primary metric:** Measures real average income per resident, adjusted for inflation using the 2011-12 base year deflator. |

---

## 2. Key Economic Concepts (Viva Preparation)

### Why Net State Domestic Product (NSDP) instead of Gross (GSDP)?
- **GSDP (Gross State Domestic Product):** Total market value of all finished goods and services produced within a state, inclusive of capital depreciation.
- **NSDP (Net State Domestic Product):** Equals $\text{GSDP} - \text{Consumption of Fixed Capital (Depreciation)}$. NSDP is a closer measure of actual income accruing to production factors within the state.
- **Per Capita NSDP:** $\frac{\text{NSDP}}{\text{Mid-Year Projected Population}}$. This is the standard indicator of living standards and economic output per resident across Indian states.

### Why Constant (2011-12) Prices instead of Current Prices?
- **Current Prices (Nominal):** Valued at prices prevailing during that specific year. High nominal growth can simply reflect high inflation.
- **Constant Prices (Real):** Uses prices from a fixed base year (2011-12 = 100) to isolate actual volume changes in goods and services from price inflation. To analyze real economic divergence, constant prices are mandatory.

---

## 3. Data Sources and Citations
1. **Reserve Bank of India (RBI):**
   - *Handbook of Statistics on Indian States*
   - Table: *Per Capita Net State Domestic Product - Constant Prices*
   - URL: [https://dbie.rbi.org.in](https://dbie.rbi.org.in)
2. **Ministry of Statistics and Programme Implementation (MoSPI):**
   - *National Accounts Division (NAD)*
   - Base Year: 2011-12 series
   - URL: [https://www.mospi.gov.in](https://www.mospi.gov.in)
