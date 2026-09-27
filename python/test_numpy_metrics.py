"""
test_numpy_metrics.py - Verification Suite for Module 2 NumPy Functions.

This test script uses strictly SYNTHETIC TEST DATA to mathematically verify
the correctness of all 10 NumPy analytical routines without using or inventing
real economic data.
"""

import sys
from pathlib import Path
import numpy as np

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from python.numpy_metrics import (
    compute_percentage_change,
    compute_cagr,
    compute_mean,
    compute_median,
    compute_std,
    compute_min_max,
    compute_range,
    compute_annual_growth_rates,
    clean_nan_and_inf,
    compare_two_years,
    compute_coefficient_of_variation
)


def test_1_percentage_change():
    """Test 1: (new - old) / old * 100"""
    old_vals = np.array([100.0, 200.0, 50.0, 0.0])
    new_vals = np.array([150.0, 180.0, 50.0, 10.0])
    
    result = compute_percentage_change(old_vals, new_vals)
    
    # 100 -> 150 = +50%
    assert np.isclose(result[0], 50.0), f"Expected 50.0, got {result[0]}"
    # 200 -> 180 = -10%
    assert np.isclose(result[1], -10.0), f"Expected -10.0, got {result[1]}"
    # 50 -> 50 = 0%
    assert np.isclose(result[2], 0.0), f"Expected 0.0, got {result[2]}"
    # Division by zero should return NaN safely without crashing
    assert np.isnan(result[3]), "Zero baseline should yield NaN safely"
    print("  [PASS] Test 1: compute_percentage_change")


def test_2_cagr():
    """Test 2: CAGR = ((end / beg) ** (1 / periods) - 1) * 100"""
    # 100 growing to 121 in 2 periods is exactly 10% per period: (100 * 1.10 * 1.10 = 121)
    beg = np.array([100.0, 1000.0])
    end = np.array([121.0, 1331.0])  # 1000 * 1.10^3 = 1331 in 3 periods
    
    cagr_2yr = compute_cagr(beg[0], end[0], periods=2)
    assert np.isclose(cagr_2yr, 10.0), f"Expected 10.0, got {cagr_2yr}"
    
    cagr_3yr = compute_cagr(beg[1], end[1], periods=3)
    assert np.isclose(cagr_3yr, 10.0), f"Expected 10.0, got {cagr_3yr}"
    print("  [PASS] Test 2: compute_cagr")


def test_3_mean():
    """Test 3: Vectorized mean with NaN handling"""
    data = np.array([10.0, 20.0, 30.0, np.nan])
    
    # nanmean of [10, 20, 30] = 20.0
    mean_val = compute_mean(data, ignore_nan=True)
    assert np.isclose(mean_val, 20.0), f"Expected 20.0, got {mean_val}"
    
    # 2D mean across columns (axis=0)
    data_2d = np.array([[10.0, 20.0], [30.0, 40.0]])
    mean_cols = compute_mean(data_2d, axis=0)
    assert np.allclose(mean_cols, [20.0, 30.0])
    print("  [PASS] Test 3: compute_mean")


def test_4_median():
    """Test 4: Vectorized median (robust to outliers)"""
    # Odd count: middle value
    odd_data = np.array([10.0, 15.0, 200.0])  # outlier 200 doesn't distort median
    assert np.isclose(compute_median(odd_data), 15.0)
    
    # Even count with NaN
    even_data = np.array([10.0, 20.0, 30.0, 40.0, np.nan])
    assert np.isclose(compute_median(even_data, ignore_nan=True), 25.0)
    print("  [PASS] Test 4: compute_median")


def test_5_std():
    """Test 5: Standard deviation (population vs sample ddof)"""
    # Values: [2, 4, 4, 4, 5, 5, 7, 9] -> mean = 5.0, pop std = 2.0
    data = np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0, np.nan])
    pop_std = compute_std(data, ddof=0, ignore_nan=True)
    assert np.isclose(pop_std, 2.0), f"Expected 2.0, got {pop_std}"
    
    sample_std = compute_std(data, ddof=1, ignore_nan=True)
    expected_sample_std = np.sqrt(32.0 / 7.0)
    assert np.isclose(sample_std, expected_sample_std)
    print("  [PASS] Test 5: compute_std")


def test_6_min_max():
    """Test 6: Minimum and Maximum with NaN protection"""
    data = np.array([45.0, 12.0, 89.0, -5.0, np.nan])
    min_val, max_val = compute_min_max(data, ignore_nan=True)
    assert np.isclose(min_val, -5.0)
    assert np.isclose(max_val, 89.0)
    print("  [PASS] Test 6: compute_min_max")


def test_7_range():
    """Test 7: Range = max - min"""
    data = np.array([10.0, 25.0, 95.0, 5.0, np.nan])
    range_val = compute_range(data, ignore_nan=True)
    # 95 - 5 = 90
    assert np.isclose(range_val, 90.0), f"Expected 90.0, got {range_val}"
    print("  [PASS] Test 7: compute_range")


def test_8_annual_growth_rates():
    """Test 8: Consecutive year-to-year growth rates on 1D and 2D arrays"""
    # 1D time series: 100 -> 110 (+10%), 110 -> 132 (+20%)
    ts = np.array([100.0, 110.0, 132.0])
    rates_1d = compute_annual_growth_rates(ts)
    assert np.allclose(rates_1d, [10.0, 20.0])
    
    # 2D matrix (2 states x 3 years)
    matrix = np.array([
        [100.0, 110.0, 132.0],
        [200.0, 220.0, 242.0]  # 200 -> 220 (+10%), 220 -> 242 (+10%)
    ])
    rates_2d = compute_annual_growth_rates(matrix, axis=1)
    assert rates_2d.shape == (2, 2)
    assert np.allclose(rates_2d[0], [10.0, 20.0])
    assert np.allclose(rates_2d[1], [10.0, 10.0])
    print("  [PASS] Test 8: compute_annual_growth_rates")


def test_9_clean_nan_and_inf():
    """Test 9: Safe handling of missing or invalid numerical values"""
    dirty = np.array([10.0, np.nan, 20.0, np.inf, -np.inf, 30.0])
    
    # Filter mode: returns only finite elements [10, 20, 30]
    filtered = clean_nan_and_inf(dirty, fill_value=None)
    assert np.array_equal(filtered, [10.0, 20.0, 30.0])
    
    # Impute / Fill mode: replaces NaN and inf with designated constant (e.g. 0.0)
    filled = clean_nan_and_inf(dirty, fill_value=0.0)
    assert np.array_equal(filled, [10.0, 0.0, 20.0, 0.0, 0.0, 30.0])
    print("  [PASS] Test 9: clean_nan_and_inf")


def test_10_compare_two_years():
    """Test 10: Vectorized comparison between two years of income"""
    y1 = np.array([100.0, 200.0, 50.0])
    y2 = np.array([120.0, 210.0, 75.0])
    
    comp = compare_two_years(y1, y2)
    
    # Absolute change: [20, 10, 25]
    assert np.allclose(comp["absolute_change"], [20.0, 10.0, 25.0])
    # Percentage growth: [20%, 5%, 50%]
    assert np.allclose(comp["percentage_growth"], [20.0, 5.0, 50.0])
    # Mean growth: (20 + 5 + 50) / 3 = 25%
    assert np.isclose(comp["mean_growth"], 25.0)
    # Above average: 50% is above 25%, while 20% and 5% are not
    assert np.array_equal(comp["above_average_growth"], [False, False, True])
    print("  [PASS] Test 10: compare_two_years")


def test_11_coefficient_of_variation():
    """Test 11: Sigma-convergence metric CV = std / mean"""
    # [10, 10, 10] -> std = 0, CV = 0 (perfect equality)
    equal_data = np.array([10.0, 10.0, 10.0])
    assert np.isclose(compute_coefficient_of_variation(equal_data), 0.0)
    
    # [10, 20, 30] -> mean = 20, pop std = sqrt(200/3) ≈ 8.1649658
    unequal_data = np.array([10.0, 20.0, 30.0])
    expected_cv = np.std(unequal_data) / np.mean(unequal_data)
    actual_cv = compute_coefficient_of_variation(unequal_data)
    assert np.isclose(actual_cv, expected_cv)
    print("  [PASS] Test 11: compute_coefficient_of_variation (Sigma-convergence)")


def run_all_tests():
    print("=" * 65)
    print(" RUNNING MODULE 2 NUMPY VALIDATION TEST SUITE")
    print(" (All tests use strictly SYNTHETIC verification data)")
    print("=" * 65)
    
    test_1_percentage_change()
    test_2_cagr()
    test_3_mean()
    test_4_median()
    test_5_std()
    test_6_min_max()
    test_7_range()
    test_8_annual_growth_rates()
    test_9_clean_nan_and_inf()
    test_10_compare_two_years()
    test_11_coefficient_of_variation()
    
    print("=" * 65)
    print(" ALL 11 TESTS PASSED! NUMPY MODULE 2 IS FULLY OPERATIONAL.")
    print("=" * 65)


if __name__ == "__main__":
    run_all_tests()
