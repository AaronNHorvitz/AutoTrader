# src/models/forecasting/arimax.py

import pandas as pd
import numpy as np
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from src.statistics import log_difference, check_stationarity
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
        raise ValueError(f"Insufficient data: Need at least {min_obs} observations, got {len(endog)}")

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


def forecast_arimax(model, exog_future, steps=1, alpha=0.05):
    """
    Generate forecast with prediction intervals using ARIMAX model.

    Parameters:
    ----------
    model : SARIMAXResults
        Fitted ARIMAX model.
    exog_future : pd.Series or np.array
        Future exogenous variables for prediction.
    steps : int
        Forecast steps ahead.
    alpha : float
        Significance level for prediction intervals.

    Returns:
    -------
    pd.DataFrame
        Forecast and prediction intervals.
    """
    forecast_results = model.get_forecast(steps=steps, exog=exog_future)
    predictions = forecast_results.predicted_mean
    ci = forecast_results.conf_int(alpha=alpha)

    return pd.DataFrame({
        "forecast": predictions,
        "lower_ci": ci.iloc[:, 0],
        "upper_ci": ci.iloc[:, 1]
    })


def prepare_data_and_fit_arimax(df, price_col, exog_col, signif=0.05):
    """
    Prepare data, check stationarity, and fit ARIMAX model.

    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame containing price and exogenous columns.
    price_col : str
        Column name for target prices.
    exog_col : str
        Column name for exogenous prices.

    Returns:
    -------
    tuple
        Fitted model, ARIMA order, log-differenced target series.
    """
    price_logdiff = log_difference(df[price_col])
    exog_logdiff = log_difference(df[exog_col])

    stationarity_results = check_stationarity(price_logdiff, signif)

    price_stationary = (
        stationarity_results["conclusion"]["ADF_stationary"]
        and stationarity_results["conclusion"]["KPSS_stationary"]
    )

    if not price_stationary:
        raise ValueError(f"{price_col} series is not stationary after log-differencing.")

    model, order = select_best_arimax(price_logdiff, exog_logdiff)

    return model, order, price_logdiff


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

    for col in ['open', 'high', 'low', 'close']:
        df[f'{col}_logdiff'] = log_difference(df[col])
        stationarity = check_stationarity(df[f'{col}_logdiff'])
        if not (stationarity['conclusion']['ADF_stationary'] and stationarity['conclusion']['KPSS_stationary']):
            raise ValueError(f"{col.capitalize()} series is not stationary after log-differencing.")

    return df.dropna()


def fit_and_forecast_next_day(df: pd.DataFrame, target_col: str, exog_col: str, next_open_price: float):
    """
    Fit ARIMAX and forecast the next day's target price with prediction intervals.

    Parameters:
    ----------
    df : pd.DataFrame
        Prepared DataFrame with log-differenced prices.
    target_col : str
        Target column (e.g., 'close', 'high', 'low').
    exog_col : str
        Exogenous column (typically 'open').
    next_open_price : float
        Known next-day open price.

    Returns:
    -------
    pd.DataFrame
        Forecasted next-day price and prediction intervals.
    """
    endog = df[f'{target_col}_logdiff']
    exog = df[f'{exog_col}_logdiff']

    model, _ = select_best_arimax(endog, exog)

    next_exog = np.array([[np.log(next_open_price) - np.log(df[exog_col].iloc[-1])]])

    forecast_df = forecast_arimax(model, next_exog)

    # Convert back to original scale
    forecast_df['forecast'] = np.exp(np.log(df[target_col].iloc[-1]) + forecast_df['forecast'])
    forecast_df['lower_ci'] = np.exp(np.log(df[target_col].iloc[-1]) + forecast_df['lower_ci'])
    forecast_df['upper_ci'] = np.exp(np.log(df[target_col].iloc[-1]) + forecast_df['upper_ci'])

    return forecast_df


# Example usage within arimax.py for demonstration (can be removed in production)
if __name__ == "__main__":
    ticker = 'AAPL'
    df = prepare_and_validate_data(ticker)

    next_day_open_price = 150.00  # hypothetical next-day open price

    forecast_close = fit_and_forecast_next_day(df, 'close', 'open', next_day_open_price)
    forecast_high = fit_and_forecast_next_day(df, 'high', 'open', next_day_open_price)
    forecast_low = fit_and_forecast_next_day(df, 'low', 'open', next_day_open_price)

    print(f"\nForecast for {ticker} using ARIMAX:")
    print("Close Price Forecast:\n", forecast_close)
    print("High Price Forecast:\n", forecast_high)
    print("Low Price Forecast:\n", forecast_low)
