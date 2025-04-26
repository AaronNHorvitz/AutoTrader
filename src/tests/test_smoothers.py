# src/tests/test_smoothers.py

import numpy as np
import pandas as pd
from src.statistics.smoothers import (
    smooth_lowess,
    exponential_smoother,
    sma_smoother,
    lowess_ci_pi,
    exp_smooth_ci_pi,
    sma_ci_pi,
)

# Test LOWESS smoother with normal random data.
def test_smooth_lowess():
    series = pd.Series(np.random.randn(100))
    smooth = smooth_lowess(series)
    assert isinstance(smooth, np.ndarray), "Output must be a numpy array."
    assert len(smooth) == len(series), "Output length must match input length."
    assert not np.isnan(smooth).any(), "LOWESS smoother output contains NaNs."


# Test exponential smoother with normal random data.
def test_exponential_smoother():
    series = pd.Series(np.random.randn(100))
    fitted, fit_model = exponential_smoother(series)
    assert isinstance(fitted, pd.Series), "Fitted output must be a Pandas Series."
    assert len(fitted) == len(series), "Fitted values length must match input length."
    assert not np.isnan(fitted).any(), "Exponential smoother output contains NaNs."


# Test Simple Moving Average smoother with normal random data.
def test_sma_smoother():
    series = pd.Series(np.random.randn(100))
    sma = sma_smoother(series)
    assert isinstance(sma, np.ndarray), "Output must be a numpy array."
    assert len(sma) == len(series), "SMA length must match input length."
    assert not np.isnan(sma).any(), "SMA output contains NaNs."


# Test LOWESS smoothing intervals (confidence and prediction).
def test_lowess_ci_pi():
    series = pd.Series(np.random.randn(100))
    fitted, ci_lower, ci_upper, pi_lower, pi_upper = lowess_ci_pi(series)
    assert np.all(ci_lower <= fitted), "LOWESS CI lower bound invalid."
    assert np.all(fitted <= ci_upper), "LOWESS CI upper bound invalid."
    assert np.all(pi_lower <= fitted), "LOWESS PI lower bound invalid."
    assert np.all(fitted <= pi_upper), "LOWESS PI upper bound invalid."


# Test exponential smoothing intervals (confidence and prediction).
def test_exp_smooth_ci_pi():
    series = pd.Series(np.random.randn(100))
    fitted, ci_lower, ci_upper, pi_lower, pi_upper = exp_smooth_ci_pi(series)
    assert np.all(ci_lower <= fitted), "Exponential smoother CI lower bound invalid."
    assert np.all(fitted <= ci_upper), "Exponential smoother CI upper bound invalid."
    assert np.all(pi_lower <= fitted), "Exponential smoother PI lower bound invalid."
    assert np.all(fitted <= pi_upper), "Exponential smoother PI upper bound invalid."


# Test SMA smoothing intervals (confidence and prediction).
def test_sma_ci_pi():
    series = pd.Series(np.random.randn(100))
    fitted, ci_lower, ci_upper, pi_lower, pi_upper = sma_ci_pi(series)
    assert np.all(ci_lower <= fitted), "SMA CI lower bound invalid."
    assert np.all(fitted <= ci_upper), "SMA CI upper bound invalid."
    assert np.all(pi_lower <= fitted), "SMA PI lower bound invalid."
    assert np.all(fitted <= pi_upper), "SMA PI upper bound invalid."


# Test smoothers on a very short series.
def test_short_series():
    short_series = pd.Series([1, 2, 3])

    smooth_lowess_out = smooth_lowess(short_series)
    assert len(smooth_lowess_out) == len(short_series), "LOWESS fails on short series."
    assert not np.isnan(smooth_lowess_out).any(), "LOWESS NaNs on short series."

    sma_out = sma_smoother(short_series)
    assert len(sma_out) == len(short_series), "SMA fails on short series."
    assert not np.isnan(sma_out).any(), "SMA NaNs on short series."

    exp_out, _ = exponential_smoother(short_series)
    assert len(exp_out) == len(
        short_series
    ), "Exponential smoother fails on short series."
    assert not np.isnan(exp_out).any(), "Exponential smoother NaNs on short series."


# Test smoothers on a constant series (no variance).
def test_constant_series():
    const_series = pd.Series([5] * 100)

    for func in [lowess_ci_pi, exp_smooth_ci_pi, sma_ci_pi]:
        fitted, ci_lower, ci_upper, pi_lower, pi_upper = func(const_series)
        assert np.allclose(
            fitted, 5
        ), f"{func.__name__} not stable for constant series."
        assert np.allclose(
            ci_lower, fitted
        ), f"{func.__name__} CI lower bound mismatch on constant series."
        assert np.allclose(
            ci_upper, fitted
        ), f"{func.__name__} CI upper bound mismatch on constant series."
        assert np.allclose(
            pi_lower, fitted
        ), f"{func.__name__} PI lower bound mismatch on constant series."
        assert np.allclose(
            pi_upper, fitted
        ), f"{func.__name__} PI upper bound mismatch on constant series."


# Test smoothers' handling of empty series (invalid input).
def test_invalid_inputs():
    empty_series = pd.Series([])
    try:
        smooth_lowess(empty_series)
    except Exception as e:
        assert isinstance(e, ValueError) or isinstance(
            e, ZeroDivisionError
        ), "LOWESS does not handle empty series."

    try:
        exponential_smoother(empty_series)
    except Exception as e:
        assert isinstance(e, ValueError) or isinstance(
            e, IndexError
        ), "Exponential smoother does not handle empty series."

    try:
        sma_smoother(empty_series)
    except Exception as e:
        assert isinstance(e, ValueError), "SMA does not handle empty series."


if __name__ == "__main__":
    test_smooth_lowess()
    test_exponential_smoother()
    test_sma_smoother()
    test_lowess_ci_pi()
    test_exp_smooth_ci_pi()
    test_sma_ci_pi()
    test_short_series()
    test_constant_series()
    test_invalid_inputs()
    print("✅ All smoothing function tests passed successfully!")
