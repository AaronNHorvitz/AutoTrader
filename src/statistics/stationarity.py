# src/statistics/stationarity.py

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss


def adf_test(series: pd.Series, signif: float = 0.05, autolag: str = "AIC") -> dict:
    """
    Perform Augmented Dickey-Fuller (ADF) test for stationarity.

    Parameters
    ----------
    series : pd.Series
        Time series data to test.
    signif : float, optional
        Significance level for hypothesis testing, by default 0.05.
    autolag : str, optional
        Method to select lag ('AIC', 'BIC', 't-stat', None), by default 'AIC'.

    Returns
    -------
    dict
        Dictionary containing ADF test statistic, p-value, critical values, and stationarity decision.
    """
    if series.nunique() <= 1:
        return {
            "test": "ADF",
            "statistic": np.nan,
            "p_value": np.nan,
            "lags_used": None,
            "n_obs": len(series),
            "critical_values": None,
            "is_stationary": False,
            "error": "Series is constant",
        }

    result = adfuller(series.dropna(), autolag=autolag)
    is_stationary = result[1] < signif
    return {
        "test": "ADF",
        "statistic": result[0],
        "p_value": result[1],
        "lags_used": result[2],
        "n_obs": result[3],
        "critical_values": result[4],
        "is_stationary": is_stationary,
    }


def kpss_test(series: pd.Series, signif: float = 0.05, regression: str = "c") -> dict:
    """
    Perform KPSS test for stationarity.

    Parameters
    ----------
    series : pd.Series
        Time series data to test.
    signif : float, optional
        Significance level for hypothesis testing, by default 0.05.
    regression : str, optional
        Type of regression ('c' for constant, 'ct' for constant with trend), by default 'c'.

    Returns
    -------
    dict
        Dictionary containing KPSS test statistic, p-value, critical values, and stationarity decision.
    """
    if series.nunique() <= 1:
        # KPSS regards constant series as stationary
        return {
            "test": "KPSS",
            "statistic": np.nan,
            "p_value": np.nan,
            "lags_used": None,
            "critical_values": None,
            "is_stationary": True,
            "error": "Series is constant",
        }

    statistic, p_value, lags, critical_values = kpss(
        series.dropna(), regression=regression, nlags="auto"
    )
    is_stationary = p_value > signif  # KPSS null hypothesis: series is stationary
    return {
        "test": "KPSS",
        "statistic": statistic,
        "p_value": p_value,
        "lags_used": lags,
        "critical_values": critical_values,
        "is_stationary": is_stationary,
    }


def check_stationarity(series: pd.Series, signif: float = 0.05) -> dict:
    """
    Check stationarity using both ADF and KPSS tests.

    Parameters
    ----------
    series : pd.Series
        Time series data to test.
    signif : float, optional
        Significance level for hypothesis testing, by default 0.05.

    Returns
    -------
    dict
        Dictionary containing results from both ADF and KPSS tests.
    """
    adf_result = adf_test(series, signif)
    kpss_result = kpss_test(series, signif)

    return {
        "ADF": adf_result,
        "KPSS": kpss_result,
        "conclusion": {
            "ADF_stationary": adf_result["is_stationary"],
            "KPSS_stationary": kpss_result["is_stationary"],
        },
    }
