# src/tests/test_stationarity.py

import numpy as np
import pandas as pd
import warnings
from statsmodels.tools.sm_exceptions import InterpolationWarning
from src.statistics.stationarity import adf_test, kpss_test, check_stationarity

warnings.simplefilter("ignore", InterpolationWarning)

# Test ADF on stationary series (should detect as stationary).
def test_adf_test_stationary_series():
    series = pd.Series(np.random.normal(0, 1, 100))
    result = adf_test(series)
    assert result["is_stationary"], "ADF failed on stationary series."


# Test ADF on nonstationary series (should detect as non-stationary).
def test_adf_test_nonstationary_series():
    np.random.seed(42)
    series = pd.Series(np.cumsum(np.random.normal(0, 1, 100)))
    result = adf_test(series)
    assert not result["is_stationary"], "ADF failed to detect non-stationarity."


# Test KPSS on stationary series (should detect as stationary).
def test_kpss_test_stationary_series():
    series = pd.Series(np.random.normal(0, 1, 100))
    result = kpss_test(series)
    assert result["is_stationary"], "KPSS failed on stationary series."


# Test KPSS on nonstationary series with trend (should detect as non-stationary).
def test_kpss_test_nonstationary_series():
    np.random.seed(42)
    trend = np.linspace(0, 10, 200)
    noise = np.random.normal(0, 1, 200)
    series = pd.Series(trend + np.cumsum(noise))
    result = kpss_test(series)
    assert not result["is_stationary"], "KPSS failed to detect non-stationarity."


# Verify consistency of stationarity tests on a stationary series.
def test_check_stationarity_consistency_stationary():
    series = pd.Series(np.random.normal(0, 1, 100))
    result = check_stationarity(series)
    assert result["ADF"]["is_stationary"], "Check stationarity inconsistent ADF result."
    assert result["KPSS"][
        "is_stationary"
    ], "Check stationarity inconsistent KPSS result."


# Verify consistency of stationarity tests on a nonstationary series.
def test_check_stationarity_consistency_nonstationary():
    series = pd.Series(np.cumsum(np.random.normal(0, 1, 100)))
    result = check_stationarity(series)
    assert not result["ADF"][
        "is_stationary"
    ], "Check stationarity inconsistent ADF result."
    assert not result["KPSS"][
        "is_stationary"
    ], "Check stationarity inconsistent KPSS result."


# Test handling of very short series for both ADF and KPSS tests.
def test_short_series_handling():
    short_series = pd.Series(np.random.normal(0, 1, 10))
    adf_result = adf_test(short_series)
    kpss_result = kpss_test(short_series)
    assert "statistic" in adf_result, "ADF handling short series incorrectly."
    assert "statistic" in kpss_result, "KPSS handling short series incorrectly."


# Test handling of constant series (no variance).
def test_constant_series():
    const_series = pd.Series([5] * 100)

    adf_result = adf_test(const_series)
    assert (
        adf_result.get("error") == "Series is constant"
    ), "ADF failed to handle constant series correctly."

    kpss_result = kpss_test(const_series)
    assert (
        kpss_result.get("error") == "Series is constant"
    ), "KPSS failed to handle constant series correctly."
    assert kpss_result[
        "is_stationary"
    ], "KPSS incorrectly identified constant series as non-stationary."


if __name__ == "__main__":
    test_adf_test_stationary_series()
    test_adf_test_nonstationary_series()
    test_kpss_test_stationary_series()
    test_kpss_test_nonstationary_series()
    test_check_stationarity_consistency_stationary()
    test_check_stationarity_consistency_nonstationary()
    test_short_series_handling()
    test_constant_series()
    print("✅ All stationarity tests passed successfully!")
