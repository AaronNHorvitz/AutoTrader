# src/models/forecasting/arimax.py

import pandas as pd
import numpy as np
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from src.statistics import log_difference, check_stationarity
from src.statistics.smoothers import smooth_lowess
from src.utils.db_utils import fetch_price_range

warnings.filterwarnings("ignore")


def select_best_arimax(endog: pd.Series, exog: pd.Series, min_obs: int = 30):
    """
    Select the best ARIMAX model based on AIC/BIC criteria.

    Parameters:
    ----------
    endog : pd.Series
        Endogenous variable (target).
    exog : pd.Series
        Exogenous variable (predictor).
    min_obs : int
        Minimum observations required for fitting.

    Returns:
    -------
    tuple
        (Fitted model, best ARIMA order)
    """
    if len(endog) < min_obs or len(exog) < min_obs:
        raise ValueError(
            f"Insufficient data: Need at least {min_obs} observations, got {len(endog)}"
        )

    if endog.var() == 0 or exog.var() == 0:
        raise ValueError("Input series cannot be constant (zero variance).")

    best_aic = np.inf
    best_order = None
    best_model = None

    for p in range(3):
        for d in range(2):
            for q in range(3):
                try:
                    model = SARIMAX(endog, exog=exog, order=(p, d, q))
                    results = model.fit(disp=False)
                    if results.aic < best_aic:
                        best_aic = results.aic
                        best_order = (p, d, q)
                        best_model = results
                except:
                    continue

    if best_model is None:
        raise ValueError("Could not fit any ARIMAX model.")

    return best_model, best_order


def forecast_arimax(
    model, exog_future, last_price, smoother="lowess", smoothing_window=30, alpha=0.05
):
    """
    Generate forecast with prediction intervals using ARIMAX model, integrating LOWESS smoothing.

    Parameters
    ----------
    model : SARIMAXResults
        Fitted ARIMAX model.
    exog_future : float
        Next day's opening price (raw scale).
    last_price : float
        Most recent observed price from historical data (raw scale).
    smoother : str, optional
        Smoothing method ('lowess', 'exponential', 'sma'), default 'lowess'.
    smoothing_window : int, optional
        Window length for smoothing.
    alpha : float, optional
        Significance level for prediction intervals (default 0.05 for 95% intervals).

    Returns
    -------
    pd.DataFrame
        Forecasted value and prediction intervals on original scale.
    """
    # Compute log-differenced future exogenous value using smoother
    log_exog_future = np.log(exog_future) - np.log(last_price)
    exog_future_array = np.array([[log_exog_future]])

    # Get ARIMAX forecast on log-difference scale
    forecast_results = model.get_forecast(steps=1, exog=exog_future_array)
    pred_mean_logdiff = forecast_results.predicted_mean.iloc[0]
    conf_int_logdiff = forecast_results.conf_int(alpha=alpha).iloc[0]

    # Transform back to original scale using last smoothed price
    forecast = np.exp(np.log(last_price) + pred_mean_logdiff)
    lower_ci = np.exp(np.log(last_price) + conf_int_logdiff.iloc[0])
    upper_ci = np.exp(np.log(last_price) + conf_int_logdiff.iloc[1])

    forecast_df = pd.DataFrame(
        {"forecast": [forecast], "lower_ci": [lower_ci], "upper_ci": [upper_ci]}
    )

    return forecast_df


def prepare_data_and_fit_arimax(
    df, price_col, exog_col, smoothing_window=30, signif=0.05
):
    """
    Prepare data, apply LOWESS smoothing, check stationarity, and fit ARIMAX model.

    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame containing price and exogenous columns.
    price_col : str
        Target price column to forecast (e.g., 'close', 'high', 'low').
    exog_col : str
        Exogenous price column (usually 'open').
    smoothing_window : int, optional
        Window length for LOWESS smoothing, default is 30.
    signif : float, optional
        Significance level for stationarity tests, default is 0.05.

    Returns:
    -------
    tuple
        Fitted ARIMAX model, ARIMA order, and smoothed log-differenced series.
    """

    # Apply LOWESS smoothing
    price_smoothed = smooth_lowess(df[price_col], window_length=smoothing_window)
    exog_smoothed = smooth_lowess(df[exog_col], window_length=smoothing_window)

    # Log-difference the smoothed data
    price_logdiff = log_difference(pd.Series(price_smoothed))
    exog_logdiff = log_difference(pd.Series(exog_smoothed))

    # Check stationarity
    stationarity_results = check_stationarity(price_logdiff, signif)
    price_stationary = (
        stationarity_results["conclusion"]["ADF_stationary"]
        and stationarity_results["conclusion"]["KPSS_stationary"]
    )

    if not price_stationary:
        raise ValueError(
            f"{price_col} series not stationary after smoothing and log-differencing."
        )

    # Fit ARIMAX model
    model, order = select_best_arimax(price_logdiff, exog_logdiff)

    return model, order, price_logdiff, exog_logdiff


def prepare_and_validate_data(ticker: str, days_back: int = 150):
    """
    Fetch historical prices, apply log-differencing, and check stationarity for Open, High, Low, Close.

    Parameters:
    ----------
    ticker : str
        Stock ticker symbol.
    days_back : int
        Number of historical days to fetch.

    Returns:
    -------
    pd.DataFrame
        Prepared DataFrame with log-differenced columns.
    """
    df = fetch_price_range(ticker, days_back)
    df.dropna(inplace=True)

    for col in ["open", "high", "low", "close"]:
        df[f"{col}_logdiff"] = log_difference(df[col])
        stationarity = check_stationarity(df[f"{col}_logdiff"])
        if not (
            stationarity["conclusion"]["ADF_stationary"]
            and stationarity["conclusion"]["KPSS_stationary"]
        ):
            raise ValueError(
                f"{col.capitalize()} series is not stationary after log-differencing."
            )

    return df.dropna()
