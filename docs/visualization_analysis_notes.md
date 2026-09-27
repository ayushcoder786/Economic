# Module 4: Visualization & Empirical Analysis Notes

**Project:** An Economic Data Pipeline  
**Research Question:** *"How has state-wise per-capita income diverged in India since 2011?"*  
**Data Source:** Reserve Bank of India (RBI) *Handbook of Statistics on Indian States* (Publication ID: 23468, Table: *Per Capita Net State Domestic Product at Current Prices*), merged with Official Zonal Council classifications.  
**Pipeline Module:** Module 4 (Visualize Findings)  
**Output Locations:**  
- Figures: `outputs/figures/` (High-resolution 300 DPI, publication standards)  
- Analytical Tables: `outputs/tables/`  

---

## 1. Methodological Framework: Epistemological Categories

To ensure analytical honesty and academic rigor, all findings in this module are strictly divided into three epistemological categories:

| Category | Definition | Examples in This Study |
| :--- | :--- | :--- |
| **Observed Data** | Direct, unmanipulated values collected and officially published by statistical authorities (RBI / MoSPI). | Per-capita NSDP of Bihar in 2011-12 was ₹21,750; Goa was ₹2,59,444; Delhi was ₹1,85,001. In 2023-24, Bihar was ₹62,201; Goa was ₹5,85,953; Delhi was ₹4,59,408. |
| **Calculated Statistics** | Mathematical transformations and summary metrics derived from the raw data using reproducible algorithms. | Compound Annual Growth Rate (CAGR), Percentage Growth, Interquartile Range (IQR), P90/P10 Ratio, Coefficient of Variation ($\sigma / \mu$), Relative Ordinal Rankings. |
| **Interpretation** | Economic hypotheses, theoretical frameworks, and contextual deductions explaining the mechanisms behind the calculated statistics. | Divergence driven by agglomeration economies, service-led growth in peninsular and capital regions, vs. lower capital formation and structural agricultural dependency in eastern states. |

---

## 2. Detailed Chart Breakdown & Measurements

### Figure 1: State-Wise Per-Capita Income Trajectories (2011-12 to 2024-25)
- **File Name:** `figure1_state_income_trajectories.png`
- **What It Measures:** Time-series trajectories of Per Capita Net State Domestic Product (NSDP) at current prices (₹ INR) for all 34 Indian States and Union Territories across 14 financial years.
- **Visual Design:** Semi-transparent background spaghetti plot (`alpha=0.35`) for all states, highlighting 7 representative macro-states (Goa, Delhi, Karnataka, Maharashtra, Tamil Nadu, Uttar Pradesh, Bihar) using distinct high-contrast colors, alongside a dashed black trajectory representing the **Interstate Mean**.
- **Observed Data:**
  - All states experienced upward nominal per-capita income trajectories between 2011-12 and 2023-24.
  - A brief deceleration or plateau is observed across nearly all states in 2020-21 coinciding with the COVID-19 pandemic shock, followed by a sharp recovery trajectory from 2021-22 onward.
- **Calculated Statistics:**
  - Mean state per-capita income rose from ₹83,312 (2011-12) to ₹2,42,644 (2023-24), representing an average nominal expansion of 191.2%.
  - The absolute gap between the top-ranked state (Goa / Sikkim) and the lowest-ranked state (Bihar) expanded from ₹2,37,694 in 2011-12 to ₹5,25,542 in 2023-24.
- **Interpretation:**
  - While all states grew in absolute terms, the "fan-out" pattern indicates absolute divergence: the trajectories widen significantly over time rather than clustering toward a common steady-state mean.

---

### Figure 2: Selected States Comparison Across Income Tiers and Geographic Zones
- **File Name:** `figure2_selected_states_comparison.png`
- **What It Measures:** A focused comparative analysis of 8 economically and geographically diverse states representing four distinct tiers:
  1. *High-Income Small / UT:* Goa, Delhi
  2. *High-Income Industrial / Tech Hubs:* Karnataka, Tamil Nadu
  3. *Middle-Income Agrarian / Mixed:* Rajasthan, Punjab
  4. *Low-Income High-Population:* Uttar Pradesh, Bihar
- **Visual Design:** Multi-panel visualization. The upper panel presents nominal income trajectories on an absolute scale (₹ INR) with an all-state median benchmark. The lower panel displays an **Indexed Growth Trajectory** where each state's 2011-12 baseline is normalized to $100.0$.
- **Observed Data:**
  - In 2011-12, Karnataka (₹90,263) and Punjab (₹85,577) had nearly identical per-capita incomes.
  - By 2023-24, Karnataka reached ₹3,39,813, whereas Punjab reached ₹2,05,374—a gap of over ₹1,34,000 between two states that started at parity.
- **Calculated Statistics:**
  - Indexed growth ($2011\text{-}12 = 100$): Karnataka expanded to $376.5$ (CAGR 11.68%), Tamil Nadu to $336.5$ (CAGR 10.64%), Bihar to $286.0$ (CAGR 9.15%), and Punjab to $239.9$ (CAGR 7.57%).
- **Interpretation:**
  - States with high exposure to technology, advanced manufacturing, and export-oriented services (Karnataka, Tamil Nadu) experienced compounding advantages, accelerating past agrarian-heavy states (Punjab) that faced stagnant agricultural productivity gains.

---

### Figure 3: Percentage Growth & CAGR in Per-Capita Income (2011-12 to 2023-24)
- **File Name:** `figure3_percentage_growth_by_state.png`
- **What It Measures:** Total percentage growth (%) and Compound Annual Growth Rate (CAGR, %) over the complete 12-year comparative baseline (2011-12 to 2023-24) across 32 states with complete data, categorized by Official Zonal Council.
- **Visual Design:** Horizontal bar chart sorted descending by percentage growth. Each bar is color-coded by geographic zone (Southern, Western, Northern, Eastern, Central, North-Eastern). Direct numerical percentage labels and CAGR values are printed adjacent to each bar. A vertical dashed reference line marks the national all-state mean growth (196.4%).
- **Observed Data:**
  - Highest percentage growth states: Mizoram (307.6%), Telangana (281.6%), Karnataka (276.5%), Sikkim (270.4%), Tripura (265.4%), Madhya Pradesh (262.9%).
  - Lowest percentage growth states: Puducherry (110.8%), Goa (125.8%), Meghalaya (136.1%), Punjab (140.0%), Uttarakhand (145.4%), Delhi (148.3%).
- **Calculated Statistics:**
  - Southern zone states all exceeded national mean growth (averaging 215.0% growth, 10.3% CAGR).
  - Eastern zone states exhibited lower absolute baseline values, growing by an average of 187.6% (8.9% CAGR), failing to outgrow high-income states sufficiently to narrow the absolute gap.
- **Interpretation:**
  - Neoclassical convergence theory (Solow-Swan $\beta$-convergence) predicts that capital-scarce, lower-income economies should exhibit higher growth rates due to diminishing marginal returns to capital. The empirical data for Indian states does *not* exhibit strong uniform catch-up growth; instead, southern and western industrial states grow at rates equal to or higher than lower-income eastern states.

---

### Figure 4: Distribution and Dispersion of State-Wise Per-Capita Income
- **File Name:** `figure4_income_distribution_boxplots.png`
- **What It Measures:** The evolution of interstate income distribution across four distinct benchmark years: 2011-12 (Base), 2015-16, 2019-20 (Pre-COVID), and 2023-24 (Post-COVID Recovery).
- **Visual Design:** Box-and-whisker plots indicating the 25th percentile ($Q_1$), Median ($Q_2$), 75th percentile ($Q_3$), and 1.5 $\times$ IQR whiskers. Overlaid jittered points show individual state observations. Red diamond markers indicate the annual mean. A secondary embedded table reports Median, IQR, Mean, and Standard Deviation.
- **Observed Data:**
  - The median per-capita income rose from ₹73,540 in 2011-12 to ₹1,16,985 in 2015-16, ₹1,82,171 in 2019-20, and ₹2,34,721 in 2023-24.
  - The distribution is right-skewed in all years, with the mean consistently exceeding the median (e.g., 2023-24 Mean = ₹2,42,644 vs. Median = ₹2,34,721).
- **Calculated Statistics:**
  - The Interquartile Range ($IQR = Q_3 - Q_1$) widened dramatically from ₹47,725 in 2011-12 to ₹85,550 in 2015-16, ₹1,29,747 in 2019-20, and ₹1,63,607 in 2023-24.
  - The standard deviation expanded from ₹49,338 to ₹1,29,753 over the period.
- **Interpretation:**
  - While median living standards across Indian states have improved steadily, the dispersion among the middle 50% of states has more than tripled in nominal terms, illustrating that state outcomes are increasingly heterogeneous.

---

### Figure 5: Interstate Inequality & Gap Dynamics ($\sigma$-Divergence and Decile Ratios)
- **File Name:** `figure5_income_gap_and_divergence.png`
- **What It Measures:** Quantitative testing of **$\sigma$-convergence** (the dispersion of per-capita income across economies over time) and ratio-based inequality metrics.
- **Visual Design:** Dual-panel time-series visualization.
  - *Left Panel:* Coefficient of Variation ($CV = \frac{\sigma}{\mu}$) plotted annually from 2011-12 to 2023-24. A horizontal dashed line marks the 2011-12 baseline.
  - *Right Panel:* The Decile Ratio ($P_{90} / P_{10}$) representing the income threshold of the 90th percentile state divided by the 10th percentile state.
- **Observed Data:**
  - In 2011-12, the 90th percentile state income was ₹1,50,863 and the 10th percentile state was ₹40,038.
  - In 2023-24, the 90th percentile state income reached ₹4,32,308 and the 10th percentile state was ₹1,23,893.
- **Calculated Statistics:**
  - The Coefficient of Variation ($CV$) declined moderately in the early decade from 0.592 (2011-12) to 0.510 (2013-14), then trended upward between 2014-15 (0.536) and 2017-18 (0.561), before stabilizing around 0.535 in 2023-24.
  - The $P_{90} / P_{10}$ ratio fluctuated between 3.5 and 3.9 throughout the period, finishing at 3.49 in 2023-24.
  - The absolute rupee gap between $P_{90}$ and $P_{10}$ expanded from ₹1,10,825 to ₹3,08,415.
- **Interpretation:**
  - Relative inequality (measured by CV and decile ratios) remained stubbornly persistent rather than declining, while absolute disparity increased by nearly 3-fold. This confirms the absence of strong $\sigma$-convergence across Indian states since 2011.

---

### Figure 6: Relative State Mobility & Ordinal Rank Trajectories
- **File Name:** `figure6_state_rank_changes.png`
- **What It Measures:** Changes in the relative ordinal rank of 32 Indian states and UTs between 2011-12 and 2023-24 (where Rank 1 = highest per-capita income and Rank 32 = lowest).
- **Visual Design:** A slopegraph / bump chart connecting each state's 2011-12 rank to its 2023-24 rank. Upward climbers are highlighted in vibrant green, downward movers in dark amber, and unchanged ranks in slate grey.
- **Observed Data:**
  - States with significant rank improvements:
    - **Tripura:** +7 ranks (from 26th to 19th)
    - **Telangana:** +6 ranks (from 11th to 5th)
    - **Karnataka:** +6 ranks (from 12th to 6th)
    - **Mizoram:** +4 ranks (from 19th to 15th)
    - **Sikkim:** +3 ranks (from 4th to 1st)
  - States with notable rank declines:
    - **Meghalaya:** -8 ranks (from 18th to 26th)
    - **Puducherry:** -7 ranks (from 5th to 12th)
    - **Uttarakhand:** -6 ranks (from 7th to 13th)
    - **Jammu & Kashmir:** -4 ranks (from 23rd to 27th)
    - **Punjab:** -3 ranks (from 15th to 18th)
  - Both top and bottom anchors remained highly static:
    - Bihar remained at Rank 32 (lowest) in both 2011-12 and 2023-24.
    - Uttar Pradesh remained at Rank 31 in both 2011-12 and 2023-24.
    - Goa, Delhi, Chandigarh, and Sikkim remained consistently within the top 4.
- **Interpretation:**
  - While there is notable dynamism in the middle tiers (particularly Southern states climbing and traditional agrarian northern states slipping), structural immobility characterizes the lower tail: the lowest-income states have remained trapped at the bottom of the distribution across the entire 12-year horizon.

---

## 3. Summary of Generated Analytical Tables

All tables have been saved in CSV format to `outputs/tables/`:

1. **`table_annual_distribution_metrics.csv`:**  
   Contains year-by-year sample size, mean, median, standard deviation, coefficient of variation, 90th percentile, 10th percentile, P90/P10 ratio, and Max/Min ratio across all 14 financial years.
2. **`table_state_growth_summary.csv`:**  
   Complete listing of all 32 states with 2011-12 baseline income, 2023-24 end-period income, regional zone, cumulative percentage growth, and annualized CAGR.
3. **`table_state_rankings_2011_vs_2023.csv`:**  
   Neutral ranking table displaying 2011 Rank, 2023 Rank, net rank change, per-capita income levels, absolute change in ₹ INR, and growth metrics.
4. **`table_regional_zone_summary.csv`:**  
   Zonal Council aggregation (Central, Eastern, North-Eastern, Northern, Southern, Western) reporting mean, median, min, max per-capita income in 2011-12 vs. 2023-24, and zonal average growth rate.

---

## 4. Key Empirical Takeaways Regarding the Research Question

1. **Has per-capita income diverged in India since 2011?**
   - **In Absolute Terms:** **Yes, emphatically.** The gap between the richest and poorest states has more than doubled, and the Interquartile Range (IQR) has widened from ₹47,725 to ₹1,63,607.
   - **In Relative Terms:** **Persistent disparity with localized divergence.** The interstate Coefficient of Variation did not exhibit the sustained downward trend that neoclassical economic theory predicts ($\sigma$-convergence); instead, it fluctuated in the range of $0.51 - 0.59$.
2. **Regional Clustering:**
   - **Southern Zone:** Demonstrated the highest growth momentum, with Telangana and Karnataka climbing 6 places into the top 6 states nationally.
   - **Eastern Zone:** Retains the lowest average per-capita income (₹1,17,165 in 2023-24 vs. ₹2,92,606 in the Southern Zone), with Bihar and Jharkhand facing ongoing structural growth headwinds.
3. **Bottom Tail Immobility:**
   - Despite healthy nominal growth in absolute terms, the bottom 2 states (Uttar Pradesh and Bihar) occupied the identical 31st and 32nd ranks in 2023-24 as they did in 2011-12.

---

## 5. Scope, Limitations, and Analytical Caveats

- **Current vs. Constant Prices:** The underlying RBI dataset records Per Capita NSDP at **Current Prices** (nominal terms). These figures reflect both real output expansion and state-specific inflation/price level adjustments.
- **Interstate Price Parity:** Nominal per-capita figures do not adjust for purchasing power parity (PPP) across states; the cost of living in urban union territories (Delhi, Chandigarh) is materially higher than in rural states (Bihar, Odisha).
- **Provisional Data for 2024-25:** Financial Year 2024-25 figures are currently available for only 25 of 34 jurisdictions in the RBI repository; consequently, multi-state comparative growth rates and rankings were evaluated through 2023-24 to maintain consistent sample integrity.
