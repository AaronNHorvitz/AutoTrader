# src/models/forecasting/arimax.py

import pandas as pd
import numpy as np
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from src.statistics import log_difference, check_stationarity

warnings.filterwarnings("ignore")


def select_best_arimax(endog: pd.Series, exog: pd.Series, min_obs: int = 30):
    """
    Select the best ARIMAX model based on AIC/BIC.

    Parameters
    ----------
    endog : pd.Series
        Endogenous variable.
    exog : pd.Series
        Exogenous variable.
    min_obs : int, optional
        Minimum observations required to fit a model, default is 30.

    Returns
    -------
    tuple
        The fitted model and the best ARIMA order.

    Raises
    ------
    ValueError
        If insufficient data or if the input series is constant.
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
                except Exception as e:
                    continue

    if best_model is None:
        raise ValueError("Could not fit any ARIMAX model.")

    return best_model, best_order


def forecast_arimax(model, exog_future, steps=1, alpha=0.05):
    """
    Generate forecast with prediction intervals using ARIMAX model.

    Parameters
    ----------
    model : SARIMAXResults
        Fitted ARIMAX model.
    exog_future : pd.Series or pd.DataFrame
        Future values of exogenous variable(s) for forecasting.
    steps : int
        Number of steps to forecast ahead.
    alpha : float
        Significance level for prediction interval (default 0.05 for 95%).

    Returns
    -------
    pd.DataFrame
        Forecasted values and prediction intervals.
    """
    forecast_results = model.get_forecast(steps=steps, exog=exog_future)
    predictions = forecast_results.predicted_mean
    ci = forecast_results.conf_int(alpha=alpha)

    forecast_df = pd.DataFrame(
        {"forecast": predictions, "lower_ci": ci.iloc[:, 0], "upper_ci": ci.iloc[:, 1]}
    )

    return forecast_df


def prepare_data_and_fit_arimax(df, price_col, exog_col, signif=0.05):
    """
    Prepare data, check stationarity, and fit an optimal ARIMAX model.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing price and exogenous columns.
    price_col : str
        Name of the target price column (e.g., 'close').
    exog_col : str
        Name of the exogenous input column (e.g., 'open').
    signif : float, optional
        Significance level for stationarity tests, by default 0.05.

    Returns
    -------
    tuple
        (fitted_model, best_order, price_logdiff)

    Raises
    ------
    ValueError
        If the target price series is non-stationary after log-differencing.
    """
    price_logdiff = log_difference(df[price_col])
    exog_logdiff = log_difference(df[exog_col])

    stationarity_results = check_stationarity(price_logdiff, signif)

    price_stationary = (
        stationarity_results["conclusion"]["ADF_stationary"]
        and stationarity_results["conclusion"]["KPSS_stationary"]
    )

    if not price_stationary:
        raise ValueError(
            f"{price_col} series is not stationary after log-differencing."
        )

    best_model, order = select_best_arimax(price_logdiff, exog_logdiff)
    model = SARIMAX(price_logdiff, exog=exog_logdiff, order=order).fit(disp=False)

    return model, order, price_logdiff
