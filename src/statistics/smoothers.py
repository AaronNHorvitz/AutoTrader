# src/statistics/smoothers.py

"""
Statistical smoothing methods with associated confidence and prediction intervals.

This module provides multiple smoothing techniques commonly used in financial time series analysis,
including LOWESS (Locally Weighted Scatterplot Smoothing), exponential smoothing, and simple moving average (SMA).
Each method includes functions for calculating smoothed values along with their respective confidence
and prediction intervals.

Functions
---------
smooth_lowess(y_series, window_length=30, iterations=2)
    Apply LOWESS smoothing to the input series.

exponential_smoother(y_series, window_length=30)
    Perform exponential smoothing on the input series with a fixed smoothing factor derived from window length.

sma_smoother(y_series, window_length=30)
    Calculate the simple moving average (SMA) of the input series.

lowess_ci_pi(y_series, window_length=30, iterations=2, num_bootstrap=500, ci=95)
    Compute LOWESS smoothing along with confidence and prediction intervals.

exp_smooth_ci_pi(y_series, window_length=30, ci=95)
    Compute exponential smoothing along with confidence and prediction intervals.

sma_ci_pi(y_series, window_length=30, ci=95)
    Calculate SMA smoothing along with confidence and prediction intervals.

Dependencies
------------
- numpy
- pandas
- statsmodels

Usage Examples
--------------
Calculate LOWESS smoothed data:
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.holtwinters import SimpleExpSmoothing


def smooth_lowess(y_series, window_length=30, iterations=2):
    """
    Apply LOWESS (Locally Weighted Scatterplot Smoothing) to smooth the input series.

    Parameters
    ----------
    y_series : pd.Series
        Input data series.
    window_length : int, optional
        Window size for smoothing, by default 30.
    iterations : int, optional
        Number of smoothing iterations, by default 2.

    Returns
    -------
    np.array
        Smoothed data.
    """
    y_series = y_series.fillna(0)
    x_series = np.arange(len(y_series))
    frac = min(max(window_length / len(x_series), 0.01), 1)
    smooth = sm.nonparametric.lowess(y_series, x_series, frac=frac, it=iterations)
    return smooth[:, 1]


def exponential_smoother(y_series, window_length=30):
    """
    Perform simple exponential smoothing on the input series.

    Parameters
    ----------
    y_series : pd.Series
        Input data series.
    window_length : int, optional
        Window length used to initialize smoothing factor alpha (0 < alpha <= 1).

    Returns
    -------
    tuple
        Fitted values as pd.Series and the fitted model object.
    """
    smoothing_level = 2 / (window_length + 1)
    model = SimpleExpSmoothing(y_series, initialization_method="estimated")
    fit = model.fit(smoothing_level=smoothing_level, optimized=False)
    return fit.fittedvalues, fit


def sma_smoother(y_series, window_length=30):
    """
    Compute Simple Moving Average (SMA) of the input series.

    Parameters
    ----------
    y_series : pd.Series
        Input data series.
    window_length : int, optional
        Window size for SMA calculation, by default 30.

    Returns
    -------
    np.array
        SMA smoothed data.
    """
    return (
        y_series.rolling(window=window_length, min_periods=1, center=True).mean().values
    )


def lowess_ci_pi(y_series, window_length=30, iterations=2, num_bootstrap=500, ci=95):
    """
    Calculate LOWESS smoothing with bootstrap-based confidence and prediction intervals.

    Parameters
    ----------
    y_series : pd.Series
        Input data series.
    window_length : int, optional
        Window size for LOWESS, by default 30.
    iterations : int, optional
        LOWESS iterations, by default 2.
    num_bootstrap : int, optional
        Number of bootstrap samples for confidence intervals, by default 500.
    ci : float, optional
        Confidence interval percentage, by default 95.

    Returns
    -------
    tuple
        Original LOWESS smooth, lower CI bound, upper CI bound, lower PI bound, upper PI bound.
    """
    # Fit the LOWESS smoother
    x_series = np.arange(len(y_series))
    frac = min(max(window_length / len(x_series), 0.01), 1)
    fitted_lowess_smoother = sm.nonparametric.lowess(
        y_series, x_series, frac=frac, it=iterations
    )[:, 1]

    # Calculate residuals and standard deviation
    residuals = y_series - fitted_lowess_smoother
    sigma = np.std(residuals)
    z_score = np.abs(np.percentile(np.random.randn(100000), (100 - ci) / 2))

    # Calculate confidence and prediction intervals
    ci_margin = z_score * (sigma / np.sqrt(window_length))
    ci_lower = fitted_lowess_smoother - ci_margin
    ci_upper = fitted_lowess_smoother + ci_margin

    pi_margin = z_score * sigma
    pi_lower = fitted_lowess_smoother - pi_margin
    pi_upper = fitted_lowess_smoother + pi_margin

    return fitted_lowess_smoother, ci_lower, ci_upper, pi_lower, pi_upper


def exp_smooth_ci_pi(y_series, window_length=30, ci=95):
    """
    Compute exponential smoothing with associated confidence and prediction intervals.

    Parameters
    ----------
    y_series : pd.Series
        Input data series.
    window_length : int, optional
        Window length to initialize smoothing factor.
    ci : float, optional
        Confidence interval percentage, by default 95.

    Returns
    -------
    tuple
        Exponentially smoothed series, lower CI bound, upper CI bound, lower PI bound, upper PI bound.
    """
    # Fit the exponential smoother
    fitted_exponential_smoother, fit = exponential_smoother(y_series, window_length)

    # Calculate residuals and standard deviation
    residuals = y_series - fitted_exponential_smoother
    sigma = np.std(residuals)
    z_score = np.abs(np.percentile(np.random.randn(100000), (100 - ci) / 2))

    # Calculate confidence and prediction intervals
    ci_margin = z_score * (sigma / np.sqrt(window_length))
    ci_lower = fitted_exponential_smoother - ci_margin
    ci_upper = fitted_exponential_smoother + ci_margin

    pi_margin = z_score * sigma
    pi_lower = fitted_exponential_smoother - pi_margin
    pi_upper = fitted_exponential_smoother + pi_margin

    return fitted_exponential_smoother, ci_lower, ci_upper, pi_lower, pi_upper


def sma_ci_pi(y_series, window_length=30, ci=95):
    """
    Calculate SMA with associated confidence and prediction intervals.

    Parameters
    ----------
    y_series : pd.Series
        Input data series.
    window_length : int, optional
        SMA window length, by default 30.
    ci : float, optional
        Confidence interval percentage, by default 95.

    Returns
    -------
    tuple
        SMA series, lower CI bound, upper CI bound, lower PI bound, upper PI bound.
    """
    # Fit the SMA smoother
    fitted_sma_smoother = sma_smoother(y_series, window_length)

    # Calculate residuals and standard deviation
    residuals = y_series - fitted_sma_smoother
    sigma = np.std(residuals[~np.isnan(residuals)])
    z_score = np.abs(np.percentile(np.random.randn(100000), (100 - ci) / 2))

    # Calculate confidence and prediction intervals
    ci_margin = z_score * (sigma / np.sqrt(window_length))
    ci_lower = fitted_sma_smoother - ci_margin
    ci_upper = fitted_sma_smoother + ci_margin

    pi_margin = z_score * sigma
    pi_lower = fitted_sma_smoother - pi_margin
    pi_upper = fitted_sma_smoother + pi_margin

    return fitted_sma_smoother, ci_lower, ci_upper, pi_lower, pi_upper
