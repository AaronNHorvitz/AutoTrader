# src/statistics/smoothers.py
import numpy as np
import statsmodels.api as sm

def smooth_lowess(y_series, window_length=21, iterations=2):
    """
    Applies LOWESS smoothing to the given data.

    Args:
        y_series (pd.Series): The input data series.
        window_length (int): Window size for smoothing.
        iterations (int): Number of smoothing iterations.

    Returns:
        np.array: Smoothed data.
    """
    y_series = y_series.fillna(0)
    x_series = np.arange(len(y_series))
    frac = min(max(window_length / len(x_series), 0.01), 1)
    smooth = sm.nonparametric.lowess(y_series, x_series, frac=frac, it=iterations)
    return smooth[:, 1]