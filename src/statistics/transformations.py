# src/statistics/transformations.py

import numpy as np
import pandas as pd


def check_positive(series: pd.Series) -> None:
    """
    Check if the series contains only positive values.

    Parameters
    ----------
    series : pd.Series
        The series to check.

    Raises
    ------
    ValueError
        If the series contains non-positive values.
    """
    if (series <= 0).any():
        raise ValueError("Series must contain only positive values.")


def log_transform(series: pd.Series) -> pd.Series:
    """
    Perform a log transform on a strictly positive series.

    Parameters
    ----------
    series : pd.Series
        The series to transform.

    Returns
    -------
    pd.Series
        The log-transformed series.
    """
    check_positive(series)
    return np.log(series)


def difference(series: pd.Series, periods: int = 1) -> pd.Series:
    """
    Perform differencing operation on a series.

    Parameters
    ----------
    series : pd.Series
        The series to difference.
    periods : int, optional
        Number of periods for differencing, by default 1.

    Returns
    -------
    pd.Series
        The differenced series.
    """
    return series.diff(periods=periods).dropna()


def log_difference(series: pd.Series, periods: int = 1) -> pd.Series:
    """
    Apply log transformation followed by differencing to stabilize variance and achieve stationarity.

    Parameters
    ----------
    series : pd.Series
        Original time series data (prices).
    periods : int, optional
        Number of periods for differencing, by default 1.

    Returns
    -------
    pd.Series
        Log-differenced series.
    """
    log_series = log_transform(series)
    return difference(log_series, periods)
