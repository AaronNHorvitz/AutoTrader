# src/tests/test_arimax.py

import pandas as pd
import numpy as np
import pytest
from src.models.forecasting.arimax import (
    select_best_arimax,
    forecast_arimax,
    prepare_data_and_fit_arimax,
    prepare_and_validate_data,
    fit_and_forecast_next_day
    )

# Test selecting the best ARIMAX model with sufficient data.
def test_select_best_arimax():
    np.random.seed(0)
    y = pd.Series(np.random.randn(150).cumsum())
    exog = pd.Series(np.random.randn(150).cumsum())

    model, best_order = select_best_arimax(y, exog)
    assert model is not None, "select_best_arimax did not return a model."
    assert isinstance(
        best_order, tuple
    ), "select_best_arimax did not return a tuple for order."
    assert len(best_order) == 3, "ARIMA order should be a tuple of length 3."


# Test handling of insufficient data (less than required observations).
def test_select_best_arimax_short_series():
    y = pd.Series(np.random.randn(5))
    exog = pd.Series(np.random.randn(5))

    with pytest.raises(ValueError, match="Insufficient data"):
        select_best_arimax(y, exog)


# Test handling of constant input series.
def test_select_best_arimax_constant_series():
    y = pd.Series([5] * 100)
    exog = pd.Series([10] * 100)

    with pytest.raises(ValueError, match="Input series cannot be constant"):
        select_best_arimax(y, exog)


# Test complete data preparation and ARIMAX fitting process with realistic positive data.
def test_prepare_data_and_fit_arimax():
    np.random.seed(42)
    data_size = 150
    open_prices = np.abs(np.random.normal(100, 5, data_size))
    close_prices = open_prices + np.random.normal(0, 2, data_size)

    df = pd.DataFrame({"open": open_prices, "close": close_prices})

    model, order, logdiff_series = prepare_data_and_fit_arimax(df, "close", "open")
    assert model is not None, "ARIMAX model fitting failed."
    assert len(logdiff_series) > 0, "Log differencing failed."
    assert isinstance(order, tuple) and len(order) == 3, "Invalid ARIMA order."


# Test handling missing values during data preparation.
def test_prepare_data_with_missing_values():
    np.random.seed(42)
    data_size = 150
    open_prices = np.random.normal(100, 5, data_size).cumsum()
    close_prices = open_prices + np.random.normal(0, 2, data_size)

    close_prices[::10] = np.nan  # Introduce missing values
    df = pd.DataFrame({"open": open_prices, "close": close_prices})

    with pytest.raises(ValueError):
        prepare_data_and_fit_arimax(df, "close", "open")


# Test forecasting functionality of ARIMAX.
def test_forecast_arimax():
    np.random.seed(123)
    y = pd.Series(np.random.randn(150).cumsum())
    exog = pd.Series(np.random.randn(150).cumsum())

    model, _ = select_best_arimax(y, exog)
    exog_future = np.array([[0.05]])
    forecast_df = forecast_arimax(model, exog_future)

    assert "forecast" in forecast_df, "Forecast column missing."
    assert "lower_ci" in forecast_df, "Lower CI missing."
    assert "upper_ci" in forecast_df, "Upper CI missing."
    assert len(forecast_df) == 1, "Forecast DataFrame should have exactly one row."


# Test forecasting with incorrect exogenous data shape.
def test_forecast_with_invalid_exog():
    y = pd.Series(np.random.randn(150).cumsum())
    exog = pd.Series(np.random.randn(150).cumsum())

    model, _ = select_best_arimax(y, exog)
    exog_future = np.array([0.05, 0.03])  # Incorrect shape

    with pytest.raises(ValueError):
        forecast_arimax(model, exog_future)


# Test robustness of ARIMAX model fitting with extreme outliers.
def test_arimax_with_extreme_outliers():
    np.random.seed(42)
    data_size = 150
    y = pd.Series(np.random.randn(data_size).cumsum())
    exog = pd.Series(np.random.randn(data_size).cumsum())

    y.iloc[10] = 1e6  # Extreme positive outlier
    exog.iloc[20] = -1e6  # Extreme negative outlier

    try:
        model, best_order = select_best_arimax(y, exog)
        assert model is not None, "Model fitting failed with extreme outliers."
        assert np.isfinite(
            model.params
        ).all(), "Model has infinite or NaN parameters due to outliers."
    except Exception as e:
        pytest.fail(
            f"Model fitting unexpectedly raised an exception with outliers: {e}"
        )

# Test the complete pipeline of preparing data, fitting ARIMAX, and forecasting.
def test_prepare_and_validate_data():
    ticker = 'AAPL'
    try:
        df = prepare_and_validate_data(ticker, days_back=150)
    except Exception as e:
        pytest.fail(f"prepare_and_validate_data raised an unexpected exception: {e}")

    expected_columns = ['open_logdiff', 'high_logdiff', 'low_logdiff', 'close_logdiff']
    for col in expected_columns:
        assert col in df.columns, f"{col} missing in prepared DataFrame."

    assert not df.empty, "Prepared DataFrame should not be empty."

# Test fitting and forecasting for the next day.
def test_fit_and_forecast_next_day():
    ticker = 'AAPL'
    df = prepare_and_validate_data(ticker, days_back=150)

    next_open_price = df['open'].iloc[-1] * 1.01  # Assume small increase for testing
    forecast_df = fit_and_forecast_next_day(df, 'close', 'open', next_open_price)

    for col in ["forecast", "lower_ci", "upper_ci"]:
        assert col in forecast_df.columns, f"{col} missing from forecast output."

    assert len(forecast_df) == 1, "Forecast DataFrame should contain exactly one row."
    assert forecast_df["lower_ci"].iloc[0] <= forecast_df["forecast"].iloc[0] <= forecast_df["upper_ci"].iloc[0], \
        "Forecasted value not within prediction interval."



if __name__ == "__main__":
    test_select_best_arimax()
    test_select_best_arimax_short_series()
    test_select_best_arimax_constant_series()
    test_prepare_data_and_fit_arimax()
    test_prepare_data_with_missing_values()
    test_forecast_arimax()
    test_forecast_with_invalid_exog()
    test_arimax_with_extreme_outliers()
    test_prepare_and_validate_data()
    test_fit_and_forecast_next_day

    print("✅ All ARIMAX robustness tests passed successfully!")
