# Economic Methodology: State-Wise Divergence in India Since 2011

## 1. Research Question
> **"How has state-wise per-capita income diverged in India since 2011?"**

---

## 2. Theoretical Background

### Neoclassical Growth Theory (Solow-Swan Model)
Standard neoclassical growth models predict **income convergence** across economies that share similar technology, institutions, and savings rates due to **diminishing returns to capital**:
- Poorer economies (with lower capital-labor ratios) have higher marginal products of capital ($MPK$) and should grow faster.
- Richer economies (with higher capital-labor ratios) should experience slower growth.
- **The Indian Paradox:** In India, empirical literature (e.g. Economic Survey of India 2016-17, Ch. 11; Chancel & Piketty 2019) suggests the opposite: regional disparities have often widened, leading to **regional divergence** rather than convergence.

---

## 3. Mathematical & Econometric Formulations

### A. Sigma ($\sigma$) Convergence
Measures whether the cross-sectional dispersion of real per-capita income among states diminishes over time.
- **Coefficient of Variation ($CV_t$):**
  $$CV_t = \frac{\sigma_t}{\mu_t} = \frac{\sqrt{\frac{1}{N}\sum_{i=1}^N (Y_{i,t} - \bar{Y}_t)^2}}{\frac{1}{N}\sum_{i=1}^N Y_{i,t}}$$
- **Decision Rule:**
  - $\frac{d(CV_t)}{dt} < 0 \implies \sigma\text{-convergence}$ (dispersion is decreasing).
  - $\frac{d(CV_t)}{dt} > 0 \implies \sigma\text{-divergence}$ (inequality between states is increasing).

### B. Unconditional Beta ($\beta$) Convergence
Tests if initially lagging states grow faster over the observation window $[0, T]$:
$$\frac{1}{T} \ln\left(\frac{Y_{i,T}}{Y_{i,0}}\right) = \alpha + \beta \ln(Y_{i,0}) + \varepsilon_i$$
- **Parameters:**
  - $Y_{i,0}$: Real per-capita income in base period (2011-12).
  - $Y_{i,T}$: Real per-capita income in final period.
  - Dependent variable: Annualized Compound Growth Rate (CAGR).
- **Decision Rule:**
  - If $\beta < 0$ (and statistically significant): Poor states grow faster $\rightarrow$ **Convergence**.
  - If $\beta > 0$: Rich states grow faster $\rightarrow$ **Divergence**.
  - If $\beta \approx 0$: No catch-up relationship.

---

## 4. Viva Defense Questions & Answers

1. **Q: Why start the study from 2011?**
   - **A:** The Government of India (MoSPI) shifted the National Accounts base year to 2011-12. Comparing pre-2011 series (base 2004-05) directly with post-2011 series creates splice and methodology distortions. Starting from 2011-12 provides a clean, homogeneous, unbroken series.

2. **Q: Can you have $\beta$-convergence without $\sigma$-convergence?**
   - **A:** Yes. $\beta$-convergence is a necessary but *not sufficient* condition for $\sigma$-convergence. Random shocks, interstate migration, structural transformation differentials, and capital agglomeration can increase overall dispersion ($\sigma$) even if poor states exhibit temporary growth spurts.
