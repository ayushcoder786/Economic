"""
numpy_metrics.py - Reusable Numerical Computing Functions using NumPy.

Module 2: Compute with NumPy
Research Question:
    "How has state-wise per-capita income diverged in India since 2011?"

This module demonstrates vector-accelerated mathematical calculations using
NumPy arrays instead of slow Python loops. Every function is designed to be
reusable, beginner-friendly, and safe against invalid or missing values (NaN/inf).

Functions Included:
1. compute_percentage_change    - Percentage change between two points
2. compute_cagr                 - Compound Annual Growth Rate over T periods
3. compute_mean                 - Vectorized arithmetic mean (with NaN handling)
4. compute_median               - Vectorized median (with NaN handling)
5. compute_std                  - Standard deviation (dispersion metric)
6. compute_min_max              - Minimum and maximum values
7. compute_range                - Spread between maximum and minimum
8. compute_annual_growth_rates  - Consecutive year-to-year growth rates
9. clean_nan_and_inf            - Safe sanitization of missing/infinite values
10. compare_two_years           - Comprehensive pairwise year comparison
11. compute_coefficient_of_variation - Sigma (σ) convergence indicator (std / mean)
"""

from typing import Dict, Optional, Tuple, Union
import numpy as np


def clean_nan_and_inf(
    data: Union[np.ndarray, list],
    fill_value: Optional[float] = None
) -> np.ndarray:
    """
    Handles missing (NaN) and invalid (infinite) numerical values safely.
    
    If fill_value is provided, replaces NaN and infinite values with fill_value.
    If fill_value is None, filters out invalid values and returns a 1D array of valid numbers.
    
    Args:
        data: Input array-like data.
        fill_value: Optional replacement value for non-finite entries.
        
    Returns:
        np.ndarray: Cleaned NumPy array with valid floats.
    """
    arr = np.asarray(data, dtype=float)
    invalid_mask = ~np.isfinite(arr)
    
    if fill_value is not None:
        cleaned = arr.copy()
        cleaned[invalid_mask] = fill_value
        return cleaned
    else:
        # Return only the finite elements
        return arr[~invalid_mask]


def compute_percentage_change(
    old_value: Union[np.ndarray, float, int],
    new_value: Union[np.ndarray, float, int]
) -> np.ndarray:
    """
    Calculates percentage change from an old value to a new value:
        ((new_value - old_value) / old_value) * 100
        
    Uses vectorized NumPy operations and safeguards against division by zero.
    
    Args:
        old_value: Baseline value or array of baseline values.
        new_value: Comparison value or array of comparison values.
        
    Returns:
        np.ndarray: Percentage change (%).
    """
    old_arr = np.asarray(old_value, dtype=float)
    new_arr = np.asarray(new_value, dtype=float)
    
    # Avoid ZeroDivisionError using np.where
    with np.errstate(divide="ignore", invalid="ignore"):
        pct_change = np.where(
            old_arr != 0,
            ((new_arr - old_arr) / old_arr) * 100.0,
            np.nan
        )
    return pct_change


def compute_cagr(
    beginning_value: Union[np.ndarray, float, int],
    ending_value: Union[np.ndarray, float, int],
    periods: Union[float, int]
) -> np.ndarray:
    """
    Calculates Compound Annual Growth Rate (CAGR):
        CAGR = (((ending_value / beginning_value) ** (1 / periods)) - 1) * 100
        
    CAGR represents the smoothed annual growth rate over multiple years,
    essential for measuring state economic trajectory over 2011-2021+.
    
    Args:
        beginning_value: Initial per-capita income (e.g., Year 2011).
        ending_value: Final per-capita income (e.g., Year 2021).
        periods: Number of elapsed years (e.g., 10 for a decade).
        
    Returns:
        np.ndarray: Annualized percentage growth rate (%).
    """
    if periods <= 0:
        raise ValueError(f"Periods must be strictly positive, got {periods}")
        
    beg = np.asarray(beginning_value, dtype=float)
    end = np.asarray(ending_value, dtype=float)
    
    with np.errstate(divide="ignore", invalid="ignore"):
        # Ratio must be non-negative for fractional powers
        valid_mask = (beg > 0) & (end > 0)
        cagr = np.where(
            valid_mask,
            (((end / beg) ** (1.0 / periods)) - 1.0) * 100.0,
            np.nan
        )
    return cagr


def compute_mean(
    data: Union[np.ndarray, list],
    axis: Optional[int] = None,
    ignore_nan: bool = True
) -> Union[float, np.ndarray]:
    """
    Calculates the arithmetic mean of an array.
    
    Args:
        data: Input array or list.
        axis: Axis along which the mean is computed (None for all elements).
        ignore_nan: If True, ignores NaN values (np.nanmean).
        
    Returns:
        Mean value as float or NumPy array.
    """
    arr = np.asarray(data, dtype=float)
    if ignore_nan:
        return np.nanmean(arr, axis=axis)
    return np.mean(arr, axis=axis)


def compute_median(
    data: Union[np.ndarray, list],
    axis: Optional[int] = None,
    ignore_nan: bool = True
) -> Union[float, np.ndarray]:
    """
    Calculates the median (50th percentile) of an array.
    
    Median is robust against extreme high-income outliers (e.g. Goa, Sikkim)
    and gives a reliable picture of typical state performance.
    
    Args:
        data: Input array or list.
        axis: Axis along which the median is computed.
        ignore_nan: If True, ignores NaN values (np.nanmedian).
        
    Returns:
        Median value as float or NumPy array.
    """
    arr = np.asarray(data, dtype=float)
    if ignore_nan:
        return np.nanmedian(arr, axis=axis)
    return np.median(arr, axis=axis)


def compute_std(
    data: Union[np.ndarray, list],
    axis: Optional[int] = None,
    ddof: int = 0,
    ignore_nan: bool = True
) -> Union[float, np.ndarray]:
    """
    Calculates standard deviation of an array:
        std = sqrt( sum((x - mean)^2) / (N - ddof) )
        
    Measures the cross-sectional dispersion of per-capita incomes across states.
    
    Args:
        data: Input array or list.
        axis: Axis along which std is computed.
        ddof: Delta Degrees of Freedom (0 for population, 1 for sample).
        ignore_nan: If True, ignores NaN values (np.nanstd).
        
    Returns:
        Standard deviation as float or NumPy array.
    """
    arr = np.asarray(data, dtype=float)
    if ignore_nan:
        return np.nanstd(arr, axis=axis, ddof=ddof)
    return np.std(arr, axis=axis, ddof=ddof)


def compute_min_max(
    data: Union[np.ndarray, list],
    axis: Optional[int] = None,
    ignore_nan: bool = True
) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Finds the minimum and maximum values in an array.
    
    Identifies the poorest and richest states in a given year.
    
    Args:
        data: Input array or list.
        axis: Axis along which min and max are evaluated.
        ignore_nan: If True, ignores NaN values.
        
    Returns:
        Tuple of (min_value, max_value).
    """
    arr = np.asarray(data, dtype=float)
    if ignore_nan:
        return np.nanmin(arr, axis=axis), np.nanmax(arr, axis=axis)
    return np.min(arr, axis=axis), np.max(arr, axis=axis)


def compute_range(
    data: Union[np.ndarray, list],
    axis: Optional[int] = None,
    ignore_nan: bool = True
) -> Union[float, np.ndarray]:
    """
    Calculates the range (spread between maximum and minimum):
        range = max_value - min_value
        
    A rising range over calendar years indicates expanding economic disparity.
    
    Args:
        data: Input array or list.
        axis: Axis along which the range is computed.
        ignore_nan: If True, ignores NaN values.
        
    Returns:
        Range value as float or NumPy array.
    """
    min_val, max_val = compute_min_max(data, axis=axis, ignore_nan=ignore_nan)
    return max_val - min_val


def compute_annual_growth_rates(
    time_series: Union[np.ndarray, list],
    axis: int = -1
) -> np.ndarray:
    """
    Calculates year-to-year percentage growth rates across consecutive periods.
    
    Formula:
        growth_rate_t = ((value_t - value_{t-1}) / value_{t-1}) * 100
        
    Uses vectorized NumPy array slicing: (arr[1:] - arr[:-1]) / arr[:-1] * 100.
    Supports 1D time series (single state) or 2D matrices (states x years).
    
    Args:
        time_series: Array of values ordered chronologically along `axis`.
        axis: Axis representing the time dimension (default: -1, last axis).
        
    Returns:
        np.ndarray: Array of year-to-year growth rates (has length N-1 along `axis`).
    """
    arr = np.asarray(time_series, dtype=float)
    
    # Slice consecutive time steps along specified axis
    prev_vals = np.take(arr, indices=range(0, arr.shape[axis] - 1), axis=axis)
    curr_vals = np.take(arr, indices=range(1, arr.shape[axis]), axis=axis)
    
    with np.errstate(divide="ignore", invalid="ignore"):
        growth_rates = np.where(
            prev_vals != 0,
            ((curr_vals - prev_vals) / prev_vals) * 100.0,
            np.nan
        )
    return growth_rates


def compute_coefficient_of_variation(
    data: Union[np.ndarray, list],
    axis: Optional[int] = None,
    ignore_nan: bool = True
) -> Union[float, np.ndarray]:
    """
    Calculates the Coefficient of Variation (CV):
        CV = Standard_Deviation / Mean
        
    Direct Economic Application:
        In regional economics, Sigma (σ) convergence is evaluated using CV.
        Because states grow in overall scale, standard deviation naturally grows.
        CV normalizes standard deviation by the mean income, providing a scale-free
        measure of regional inequality.
        - If CV increases over time -> Sigma Divergence.
        - If CV decreases over time -> Sigma Convergence.
    """
    std_val = compute_std(data, axis=axis, ignore_nan=ignore_nan)
    mean_val = compute_mean(data, axis=axis, ignore_nan=ignore_nan)
    
    with np.errstate(divide="ignore", invalid="ignore"):
        cv = np.where(mean_val != 0, std_val / mean_val, np.nan)
    return float(cv) if np.ndim(cv) == 0 else cv


def compare_two_years(
    year1_values: Union[np.ndarray, list],
    year2_values: Union[np.ndarray, list]
) -> Dict[str, np.ndarray]:
    """
    Performs a vectorized comparison between two cross-sections of per-capita income.
    (e.g., comparing Year 2011-12 baseline vs Year 2021-22).
    
    Returns a dictionary of key comparison metrics:
    - absolute_change: year2 - year1 (in currency units, INR)
    - percentage_growth: ((year2 - year1) / year1) * 100
    - disparity_ratio: year2 / year1
    - above_average_growth: boolean mask of states that beat the national mean growth
    
    Args:
        year1_values: Baseline per-capita incomes across states.
        year2_values: Later-period per-capita incomes across states.
        
    Returns:
        dict: Named metric arrays.
    """
    y1 = np.asarray(year1_values, dtype=float)
    y2 = np.asarray(year2_values, dtype=float)
    
    abs_change = y2 - y1
    pct_growth = compute_percentage_change(y1, y2)
    
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(y1 != 0, y2 / y1, np.nan)
        
    mean_growth = np.nanmean(pct_growth)
    above_avg = pct_growth > mean_growth
    
    return {
        "absolute_change": abs_change,
        "percentage_growth": pct_growth,
        "disparity_ratio": ratio,
        "mean_growth": mean_growth,
        "above_average_growth": above_avg
    }


# ==============================================================================
# SYNTHETIC TEST HARNESS (FOR DEMONSTRATION & UNIT VERIFICATION ONLY)
# ==============================================================================
# NOTE: The data below is strictly SYNTHETIC MOCK DATA designed solely to test
# numerical routines and vectorization. It does NOT represent real economic figures.
# ==============================================================================

def get_synthetic_test_dataset() -> Tuple[np.ndarray, list, list]:
    """
    Returns a clean synthetic 2D array (4 mock states x 4 synthetic years)
    for testing functions, plus state names and year labels.
    
    Synthetic Matrix Layout:
        Row 0: Mock State North  [100, 110, 125, 140] (fast grower)
        Row 1: Mock State South  [200, 210, 220, 235] (moderate high-income)
        Row 2: Mock State West   [150, 165, np.nan, 200] (contains test NaN)
        Row 3: Mock State East   [80,  85,  90,  95]   (slower low-income)
    """
    mock_matrix = np.array([
        [100.0, 110.0, 125.0, 140.0],
        [200.0, 210.0, 220.0, 235.0],
        [150.0, 165.0, np.nan, 200.0],
        [80.0,  85.0,  90.0,  95.0]
    ], dtype=float)
    
    mock_states = ["Synthetic State A", "Synthetic State B", "Synthetic State C", "Synthetic State D"]
    mock_years = ["Year 1 (Base)", "Year 2", "Year 3", "Year 4 (Final)"]
    
    return mock_matrix, mock_states, mock_years


def demonstrate_numpy_computations() -> None:
    """
    Executes and prints a full demonstration of all Module 2 NumPy functions
    using the synthetic test dataset.
    """
    print("=" * 70)
    print(" MODULE 2: COMPUTE WITH NUMPY - FUNCTION DEMONSTRATION")
    print(" (Using explicitly labeled SYNTHETIC TEST DATA only)")
    print("=" * 70)
    
    matrix, states, years = get_synthetic_test_dataset()
    
    print("\n1. SYNTHETIC INPUT MATRIX (States as Rows, Years as Columns):")
    print(f"   Shape: {matrix.shape} (4 states, 4 time points)")
    for i, state in enumerate(states):
        print(f"   - {state:18s}: {matrix[i]}")
        
    print("\n2. CROSS-SECTIONAL DESCRIPTIVE STATISTICS (Across States in Base Year 1):")
    base_year_incomes = matrix[:, 0]
    mean_val = compute_mean(base_year_incomes)
    median_val = compute_median(base_year_incomes)
    std_val = compute_std(base_year_incomes, ddof=1)
    min_val, max_val = compute_min_max(base_year_incomes)
    range_val = compute_range(base_year_incomes)
    cv_val = compute_coefficient_of_variation(base_year_incomes)
    
    print(f"   - Mean Income         : {mean_val:.2f}")
    print(f"   - Median Income       : {median_val:.2f}")
    print(f"   - Sample Std Dev      : {std_val:.2f}")
    print(f"   - Minimum Income      : {min_val:.2f}")
    print(f"   - Maximum Income      : {max_val:.2f}")
    print(f"   - Income Range (Gap)  : {range_val:.2f}")
    print(f"   - Coeff of Variation  : {cv_val:.4f} (Disparity index)")

    print("\n3. YEAR-TO-YEAR PERCENTAGE GROWTH RATES (Vectorized Along Time Axis):")
    annual_growth = compute_annual_growth_rates(matrix, axis=1)
    for i, state in enumerate(states):
        growth_formatted = [f"{g:+.2f}%" if np.isfinite(g) else "NaN" for g in annual_growth[i]]
        print(f"   - {state:18s}: {growth_formatted}")

    print("\n4. COMPOUND ANNUAL GROWTH RATE (CAGR over 3 elapsed periods):")
    initial_incomes = matrix[:, 0]
    final_incomes = matrix[:, 3]
    cagr_values = compute_cagr(initial_incomes, final_incomes, periods=3)
    for i, state in enumerate(states):
        print(f"   - {state:18s}: CAGR = {cagr_values[i]:+.2f}% per year")

    print("\n5. TWO-YEAR COMPARISON (Base Year 1 vs Final Year 4):")
    comparison = compare_two_years(initial_incomes, final_incomes)
    for i, state in enumerate(states):
        print(f"   - {state:18s}: Abs Change = +{comparison['absolute_change'][i]:.1f}, "
              f"Total Growth = {comparison['percentage_growth'][i]:+.1f}%, "
              f"Above Avg? {comparison['above_average_growth'][i]}")

    print("\n6. HANDLING MISSING OR INVALID NUMERICAL VALUES:")
    row_with_nan = matrix[2]  # State C has a NaN
    cleaned_filtered = clean_nan_and_inf(row_with_nan)
    cleaned_filled = clean_nan_and_inf(row_with_nan, fill_value=0.0)
    print(f"   - Original with NaN   : {row_with_nan}")
    print(f"   - Filtered (valid)    : {cleaned_filtered}")
    print(f"   - Imputed / Filled 0  : {cleaned_filled}")

    print("\n7. SIGMA (σ) CONVERGENCE CHECK ACROSS ALL SYNTHETIC YEARS:")
    for yr_idx, yr_label in enumerate(years):
        yr_data = matrix[:, yr_idx]
        yr_cv = compute_coefficient_of_variation(yr_data)
        print(f"   - {yr_label:15s}: CV = {yr_cv:.4f}")

    print("=" * 70)
    print(" ALL NUMPY FUNCTIONS DEMONSTRATED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_numpy_computations()
