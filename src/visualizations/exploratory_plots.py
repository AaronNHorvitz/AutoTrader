# src/visualizations/exploratory_plots.py

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
from src.statistics.smoothers import lowess_ci_pi, exp_smooth_ci_pi, sma_ci_pi, smooth_lowess, exponential_smoother, sma_smoother
from src.statistics.changepoints import detect_level_shifts
from src.utils.db_utils import get_db_connection, fetch_price_range, get_stock_name
from src.statistics.transformations import log_difference
from src.models.forecasting.arimax import select_best_arimax, prepare_data_and_fit_arimax, forecast_arimax

def _fetch_price_data(symbol, days_back, price_type, calendar_days):
    """
    Helper function to fetch price data and validate common parameters.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol.
    days_back : int
        Number of days of historical data to fetch.
    price_type : str
        Type of price data ('open', 'close', 'high', 'low').
    calendar_days : bool
        If True, uses calendar days; otherwise, trading days.

    Returns
    -------
    tuple
        (stock_name, prices, dates, date_type)

    Raises
    ------
    ValueError
        If price_type is invalid.
    """
    if price_type not in ["open", "close", "high", "low"]:
        raise ValueError("Invalid price type. Choose 'open', 'close', 'high', or 'low'.")

    if price_type == "open":
        price_label = "Opening"
    elif price_type == "close":
        price_label = "Closing"
    elif price_type == "high":
        price_label = "High"
    else:
        price_label = "Low"

    # Fetch price data
    conn = get_db_connection('assets.db')
    price_data = fetch_price_range(symbol, days_back, conn=conn, calendar_days=calendar_days)
    stock_name = get_stock_name(symbol, conn=conn)
    conn.close()

    prices = price_data[price_type]
    dates = price_data['date']

    date_type = "Calendar Days" if calendar_days else "Trading Days"

    return stock_name, prices, dates, date_type, price_label

def _setup_gridspec_axes(ax, figsize, dpi):
    """
    Helper function to set up a gridspec layout for scatter plot and histogram.

    Parameters
    ----------
    ax : matplotlib.axes.Axes or None
        Existing axes to plot on. If None, a new figure and axes are created.
    figsize : tuple
        Figure size as (width, height) in inches.
    dpi : int
        Dots per inch (resolution) of the figure.

    Returns
    -------
    tuple
        (fig, ax, ax_hist)
    """
    if ax is None:
        # Create a figure with a gridspec layout
        fig = plt.figure(figsize=figsize, dpi=dpi)
        gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])  # 4:1 width ratio for scatter plot and histogram

        # Create the main scatter plot axes
        ax = fig.add_subplot(gs[0])

        # Create the histogram axes
        ax_hist = fig.add_subplot(gs[1], sharey=ax)  # Share y-axis with the main plot
    else:
        # If ax is provided, create the histogram axes in the same figure
        fig = ax.get_figure()
        gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1], figure=fig)
        ax.set_position(gs[0].get_position(fig))  # Resize ax to fit the gridspec layout
        ax_hist = fig.add_subplot(gs[1], sharey=ax)

    return fig, ax, ax_hist

def ax_smoothed_prices(
    symbol, 
    days_back=125,
    smoothing_window=30,
    smoother="lowess",
    price_type="close",
    show_actual_line=False,
    calendar_days=False,
    ci=95,
    level_shifts_model=None,
    level_shifts_penalty=5,
    level_shifts_min_size=10,
    ax=None,
    show_title=True,
    show_x_label=True,
    show_y_label=True,
    show_grid=True,
    show_legend=True,
    figsize=(14, 7), 
    dpi=150,          
):
    """
    Generate a Matplotlib plot on an Axes object visualizing stock price trends with smoothing, confidence and prediction intervals, and optional level shift detections.

    This function retrieves historical stock prices from a database, applies a smoothing technique, calculates confidence and prediction intervals, and optionally identifies and marks level shifts (changepoints).

    Parameters
    ----------
    symbol : str
        Stock ticker symbol (e.g., 'AAPL').
    days_back : int, optional
        Number of days of historical data to fetch, default is 125.
    smoothing_window : int, optional
        The window length for the smoothing algorithm, default is 30 days.
    smoother : {'lowess', 'exponential', 'sma'}, optional
        Smoothing method applied to price data:
        - 'lowess': Locally Weighted Scatterplot Smoothing.
        - 'exponential': Exponential smoothing.
        - 'sma': Simple Moving Average.
        Default is 'lowess'.
    price_type : {'open', 'close', 'high', 'low'}, optional
        The price metric to plot, default is 'close'.
    show_actual_line : bool, optional
        Whether to plot a line connecting actual price points, default is False.
    calendar_days : bool, optional
        If True, `days_back` considers calendar days, otherwise trading days, default is False.
    ci : float, optional
        Confidence level for confidence and prediction intervals (as a percentage), default is 95.
    level_shifts_model : {'l2', 'l1', 'rbf', 'linear', 'normal', None}, optional
        The model used by the ruptures library to detect level shifts. Default is None (no shifts).
    level_shifts_penalty : float, optional
        Penalty value controlling sensitivity in level shift detection (higher values yield fewer shifts), default is 5.
    level_shifts_min_size : int, optional
        Minimum number of data points between detected shifts, default is 10.
    ax : matplotlib.axes.Axes, optional
        Existing Axes object to plot on. If None, a new figure and axes are created.
    show_title : bool, optional
        Whether to display the plot title, default is True.
    show_x_label : bool, optional
        Whether to show the x-axis label ('Date'), default is True.
    show_y_label : bool, optional
        Whether to show the y-axis label ('Price (USD)'), default is True.
    show_grid : bool, optional
        Whether to display a grid on the plot, default is True.
    show_legend : bool, optional
        Whether to display the legend, default is True.
    figsize : tuple, optional
        Figure size as (width, height) in inches, default is (14, 7).
    dpi : int, optional
        Dots per inch (resolution) of the figure, default is 150.

    Returns
    -------
    matplotlib.axes.Axes
        Axes object with the generated plot, allowing further customization.

    Raises
    ------
    ValueError
        If invalid arguments are provided for `price_type` or `smoother`.

    Examples
    --------
    Plot smoothed closing prices of Apple stock with LOWESS smoothing:

    >>> ax_smoothed_prices('AAPL', days_back=90, smoother='lowess')

    Plot high prices of Tesla with exponential smoothing and level shift detection:

    >>> ax_smoothed_prices(
    ...     'TSLA',
    ...     smoother='exponential',
    ...     price_type='high',
    ...     level_shifts_model='l2',
    ...     level_shifts_penalty=10
    ... )
    """
    # Fetch data using helper function
    stock_name, prices, dates, date_type, price_label = _fetch_price_data(
        symbol, days_back, price_type, calendar_days
    )

    # Apply smoothing
    if smoother == "lowess":
        smoothed, ci_lower, ci_upper, pi_lower, pi_upper = lowess_ci_pi(
            prices, window_length=smoothing_window, ci=ci
        )
        label_smoother = "LOWESS"
    elif smoother == "exponential":
        smoothed, ci_lower, ci_upper, pi_lower, pi_upper = exp_smooth_ci_pi(
            prices, window_length=smoothing_window, ci=ci
        )
        label_smoother = "Exponential"
    elif smoother == "sma":
        smoothed, ci_lower, ci_upper, pi_lower, pi_upper = sma_ci_pi(
            prices, window_length=smoothing_window, ci=ci
        )
        label_smoother = "Simple Moving Average"
    else:
        raise ValueError("Invalid smoother type.")

    # Create ax if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Scatter actual prices
    ax.scatter(dates, prices, edgecolors="black", facecolors="lightblue",
               linewidth=1.5, marker="o", s=45, alpha=1.0,
               label=f"Actual {price_label} Prices")

    # Actual line connecting points
    if show_actual_line:
        ax.plot(dates, prices, color="lightblue", linewidth=0.5, label="Actual Line")

    # Plot smoothed line
    ax.plot(dates, smoothed, color="red", linestyle="--", linewidth=1.5,
            label=f"Smoothed {label_smoother} ({smoothing_window}-day)")

    # Confidence Interval
    ax.fill_between(dates, ci_lower, ci_upper, color="lightblue",
                    edgecolor="black", linewidth=0.5, alpha=0.2,
                    label=f"{ci}% Confidence Interval")

    # Prediction Interval
    ax.fill_between(dates, pi_lower, pi_upper, color="lightgrey",
                    edgecolor="black", linestyle="--", linewidth=0.5, alpha=0.3,
                    label=f"{ci}% Prediction Interval")

    # Level shift detection (optional)
    if level_shifts_model:
        shift_indices = detect_level_shifts(
            pd.Series(smoothed), 
            model=level_shifts_model, 
            penalty=level_shifts_penalty, 
            min_size=level_shifts_min_size
        )
        shift_dates = dates.iloc[shift_indices]
        for shift_date in shift_dates:
            ax.axvline(x=shift_date, color='purple', linestyle='--', linewidth=1.2, alpha=0.75,
                       label='Detected Level Shift' if shift_date == shift_dates.iloc[0] else "")

    latest_date = dates.max().strftime('%m/%d/%Y')
    earliest_date = dates.min().strftime('%m/%d/%Y')

    # Formatting
    if show_title:
        title = (f"\n{stock_name} ({symbol})\n{price_label} Prices ({len(dates)} {date_type})\n"
                 f"{earliest_date} to {latest_date}\n") 
        ax.set_title(title, fontsize=16)
    if show_x_label: ax.set_xlabel("Date")
    if show_y_label: ax.set_ylabel("Price (USD)")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.2f}"))

    if show_grid: ax.grid(True)
    if show_legend: ax.legend()

    return ax

def ax_residuals(
    symbol,
    days_back=125,
    smoothing_window=30,
    smoother="lowess",
    price_type="close",
    calendar_days=False,
    level_shifts_model=None,
    level_shifts_penalty=5,
    level_shifts_min_size=10,
    ax=None,
    show_title=True,
    show_x_label=True,
    show_y_label=True,
    show_grid=True,
    show_legend=True,
    figsize=(14, 7), 
    dpi=150,          
):
    """
    Plot residuals (actual prices minus smoothed prices) for stock data, along with a
    horizontal histogram to assess residual normality.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol (e.g., 'AAPL').
    days_back : int, optional
        Number of days of historical data to fetch, default is 125.
    smoothing_window : int, optional
        Window length for smoothing algorithm, default is 30.
    smoother : {'lowess', 'exponential', 'sma'}, optional
        Smoothing method, default is 'lowess'.
    price_type : {'open', 'close', 'high', 'low'}, optional
        Type of price data, default is 'close'.
    calendar_days : bool, optional
        If True, uses calendar days, otherwise trading days, default is False.
    level_shifts_model : {'l2', 'l1', 'rbf', 'linear', 'normal', None}, optional
        Ruptures model for detecting level shifts, default is None.
    level_shifts_penalty : float, optional
        Penalty for level shift detection, default is 5.
    level_shifts_min_size : int, optional
        Minimum points between detected shifts, default is 10.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on. If None, a new figure and axes are created.
    show_title : bool, optional
        Show the plot title, default is True.
    show_x_label : bool, optional
        Show the x-axis label, default is True.
    show_y_label : bool, optional
        Show the y-axis label, default is True.
    show_grid : bool, optional
        Show grid lines, default is True.
    show_legend : bool, optional
        Display legend, default is True.
    figsize : tuple, optional
        Figure size as (width, height) in inches, default is (14, 7).
    dpi : int, optional
        Dots per inch (resolution) of the figure, default is 150.

    Returns
    -------
    matplotlib.axes.Axes
        Axes containing the residual plot with horizontal histogram.

    Raises
    ------
    ValueError
        If an invalid `price_type` or `smoother` is provided.
    """
    # Fetch data using helper function
    stock_name, prices, dates, date_type, price_label = _fetch_price_data(
        symbol, days_back, price_type, calendar_days
    )

    # Apply smoothing
    if smoother == "lowess":
        smoothed, _, _, _, _ = lowess_ci_pi(prices, smoothing_window)
        label_smoother = "LOWESS"
    elif smoother == "exponential":
        smoothed, _, _, _, _ = exp_smooth_ci_pi(prices, smoothing_window)
        label_smoother = "Exponential"
    elif smoother == "sma":
        smoothed, _, _, _, _ = sma_ci_pi(prices, smoothing_window)
        label_smoother = "Simple Moving Average"
    else:
        raise ValueError("Invalid smoother type.")

    residuals = prices - smoothed

    # Set up axes using helper function
    fig, ax, ax_hist = _setup_gridspec_axes(ax, figsize, dpi)

    # Scatter residuals
    ax.scatter(dates, residuals, edgecolors="black", facecolors="lightblue",
               linewidth=1.5, marker="o", s=55, alpha=1.0,
               label=f"Actual {price_label} Price Residuals")

    # Draw thin lines from y=0 to each scatter point
    ax.vlines(dates, 0, residuals, colors='lightblue', linestyles='solid', linewidth=0.5, alpha=0.7)

    # Plot smoothed line - horizontal 
    ax.axhline(0, color='red', linestyle='--', linewidth=3.0, label=f"Smoothed {label_smoother} ({smoothing_window}-day)")

    # Level shift detection (optional)
    if level_shifts_model:
        shift_indices = detect_level_shifts(
            pd.Series(smoothed),
            model=level_shifts_model,
            penalty=level_shifts_penalty,
            min_size=level_shifts_min_size
        )
        shift_dates = dates.iloc[shift_indices]
        for shift_date in shift_dates:
            ax.axvline(x=shift_date, color='purple', linestyle='--', linewidth=1.2, alpha=0.75,
                       label='Detected Level Shift' if shift_date == shift_dates.iloc[0] else "")

    latest_date = dates.max().strftime('%m/%d/%Y')
    earliest_date = dates.min().strftime('%m/%d/%Y')

    if show_title:
        title = (f"\n{stock_name} ({symbol})\n{price_label} Residuals ({len(dates)} {date_type})\n"
                 f"{earliest_date} to {latest_date}\n")
        ax.set_title(title, fontsize=16)
    ax.set_xlabel("Date") if show_x_label else None
    ax.set_ylabel("Residuals (USD)") if show_y_label else None
    ax.grid(show_grid)

    # Set vertical limits for residuals
    maximum_vert_limit = max(
        abs(residuals.max()), 
        abs(residuals.min())
    ) * 1.10  # 10% padding

    ax.set_ylim(
        bottom=-maximum_vert_limit, 
        top=maximum_vert_limit
    )

    # Horizontal histogram for residual distribution
    ax_hist.hist(residuals, bins=50, orientation='horizontal', color='lightblue', alpha=0.4, edgecolor='black')
    ax_hist.axhline(0, color='red', linestyle='--', linewidth=3.0)
    ax_hist.grid(False)
    ax_hist.set_xlabel("Freq.")
    ax_hist.set_yticklabels([])

    if show_legend:
        ax.legend()

    # Adjust layout to prevent overlap
    plt.tight_layout()

    return ax

def ax_log_difference(
    symbol,
    days_back=125,
    smoothing_window=30,
    smoother="lowess",
    price_type="close",
    apply_smoothing=True,
    periods=1,  
    calendar_days=False,
    level_shifts_model=None,
    level_shifts_penalty=5,
    level_shifts_min_size=10,
    ax=None,
    show_title=True,
    show_x_label=True,
    show_y_label=True,
    show_grid=True,
    show_legend=True,
    figsize=(14, 7),
    dpi=150,
):
    """
    Plot log-differenced stock price data, with an optional smoothing step, along with a horizontal histogram to assess the distribution.

    This function retrieves historical stock prices from a database, optionally applies a smoothing technique,
    computes the log-differenced series, and plots the result as a scatter plot with a horizontal histogram on the side.
    It also supports optional level shift detection. Note that the resulting series will have `days_back - periods`
    data points due to the differencing operation.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol (e.g., 'AAPL').
    days_back : int, optional
        Number of days of historical data to fetch, default is 125.
    smoothing_window : int, optional
        Window length for smoothing algorithm, default is 30. Used only if `apply_smoothing` is True.
    smoother : {'lowess', 'exponential', 'sma'}, optional
        Smoothing method to apply before log-differencing, default is 'lowess'.
        - 'lowess': Locally Weighted Scatterplot Smoothing.
        - 'exponential': Exponential smoothing.
        - 'sma': Simple Moving Average.
        Used only if `apply_smoothing` is True.
    price_type : {'open', 'close', 'high', 'low'}, optional
        Type of price data to use, default is 'close'.
    apply_smoothing : bool, optional
        If True, applies the specified smoothing method to the price data before log-differencing, default is True.
    periods : int, optional
        Number of periods for differencing in log-difference calculation, default is 1.
    calendar_days : bool, optional
        If True, uses calendar days, otherwise trading days, default is False.
    level_shifts_model : {'l2', 'l1', 'rbf', 'linear', 'normal', None}, optional
        Ruptures model for detecting level shifts in the log-differenced series, default is None.
    level_shifts_penalty : float, optional
        Penalty for level shift detection, default is 5.
    level_shifts_min_size : int, optional
        Minimum points between detected shifts, default is 10.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on. If None, a new figure and axes are created.
    show_title : bool, optional
        Show the plot title, default is True.
    show_x_label : bool, optional
        Show the x-axis label ('Date'), default is True.
    show_y_label : bool, optional
        Show the y-axis label ('Log-Difference'), default is True.
    show_grid : bool, optional
        Show grid lines, default is True.
    show_legend : bool, optional
        Display legend, default is True.
    figsize : tuple, optional
        Figure size as (width, height) in inches, default is (14, 7).
    dpi : int, optional
        Dots per inch (resolution) of the figure, default is 150.

    Returns
    -------
    matplotlib.axes.Axes
        Axes containing the log-difference plot with horizontal histogram.

    Raises
    ------
    ValueError
        If `days_back` is not greater than `periods`, as differencing requires sufficient data points.
        If price data contains non-positive values, as log-difference requires strictly positive data.
        If an invalid `price_type` or `smoother` is provided.

    Examples
    --------
    Plot log-differenced closing prices of Apple stock with LOWESS smoothing:

    >>> ax_log_difference('AAPL', days_back=90, smoother='lowess')

    Plot log-differenced high prices of Tesla without smoothing:

    >>> ax_log_difference(
    ...     'TSLA',
    ...     price_type='high',
    ...     apply_smoothing=False
    ... )
    """
    # Validate days_back
    if days_back <= periods:
        raise ValueError(f"days_back ({days_back}) must be greater than periods ({periods}) to produce a non-empty log-differenced series.")

    # Fetch data using helper function
    stock_name, prices, dates, date_type, price_label = _fetch_price_data(
        symbol, days_back, price_type, calendar_days
    )

    # Apply smoothing
    if apply_smoothing:
        if smoother == "lowess":
            smoothed, ci_lower, ci_upper, pi_lower, pi_upper = lowess_ci_pi(
                prices, window_length=smoothing_window, ci=95
            )
            label_smoother = "LOWESS"
            # Convert smoothed array to pd.Series with the same index as prices
            prices = pd.Series(smoothed, index=prices.index)

        elif smoother == "exponential":
            smoothed, ci_lower, ci_upper, pi_lower, pi_upper = exp_smooth_ci_pi(
                prices, window_length=smoothing_window, ci=95
            )
            label_smoother = "Exponential"
            # Convert smoothed array to pd.Series with the same index as prices
            prices = pd.Series(smoothed, index=prices.index)

        elif smoother == "sma":
            smoothed, ci_lower, ci_upper, pi_lower, pi_upper = sma_ci_pi(
                prices, window_length=smoothing_window, ci=95
            )
            label_smoother = "Simple Moving Average"
            # Convert smoothed array to pd.Series with the same index as prices
            prices = pd.Series(smoothed, index=prices.index)

        else:
            raise ValueError("Invalid smoother type.")
    
    # Compute log-differenced series
    try:
        log_diff_series = log_difference(prices, periods=periods)
    except ValueError as e:
        raise ValueError(f"Cannot compute log-difference: {str(e)}")

    # Align dates with log-differenced series
    # log_difference drops the first 'periods' rows due to differencing
    log_diff_dates = dates.iloc[periods:]

    # Set up axes using helper function
    fig, ax, ax_hist = _setup_gridspec_axes(ax, figsize, dpi)

    # Scatter log-differences
    if apply_smoothing:
        scatter_label = f"Log-Differenced {label_smoother} Smoothed {price_label} Prices"
    else:
        scatter_label = f"Log-Differenced {price_label} Prices"
    ax.scatter(log_diff_dates, log_diff_series, edgecolors="black", facecolors="lightblue",
               linewidth=1.5, marker="o", s=55, alpha=1.0,
               label=scatter_label)

    # Draw thin lines from y=0 to each scatter point
    ax.vlines(log_diff_dates, 0, log_diff_series, colors='lightblue', linestyles='solid', linewidth=0.5, alpha=0.7)

    # Plot horizontal line at y=0
    ax.axhline(0, color='red', linestyle='--', linewidth=3.0, label="Zero Line")

    # Level shift detection (optional)
    if level_shifts_model:
        shift_indices = detect_level_shifts(
            pd.Series(log_diff_series),
            model=level_shifts_model,
            penalty=level_shifts_penalty,
            min_size=level_shifts_min_size
        )
        shift_dates = log_diff_dates.iloc[shift_indices]
        for shift_date in shift_dates:
            ax.axvline(x=shift_date, color='purple', linestyle='--', linewidth=1.2, alpha=0.75,
                       label='Detected Level Shift' if shift_date == shift_dates.iloc[0] else "")

    latest_date = log_diff_dates.max().strftime('%m/%d/%Y')
    earliest_date = log_diff_dates.min().strftime('%m/%d/%Y')

    if show_title:
        if apply_smoothing:
            title = (f"\n{stock_name} ({symbol})\nLog-Differenced {label_smoother} Smoothed {price_label} Prices ({len(log_diff_dates)} {date_type})\n"
                     f"{earliest_date} to {latest_date}\n")
        else:
            title = (f"\n{stock_name} ({symbol})\nLog-Differenced {price_label} Prices ({len(log_diff_dates)} {date_type})\n"
                     f"{earliest_date} to {latest_date}\n")
        ax.set_title(title, fontsize=16)
    ax.set_xlabel("Date") if show_x_label else None
    ax.set_ylabel("Log-Difference") if show_y_label else None
    ax.grid(show_grid)

    # Set vertical limits for log-differences
    maximum_vert_limit = max(
        abs(log_diff_series.max()),
        abs(log_diff_series.min())
    ) * 1.10  # 10% padding

    ax.set_ylim(
        bottom=-maximum_vert_limit,
        top=maximum_vert_limit
    )

    # Horizontal histogram for log-difference distribution
    ax_hist.hist(log_diff_series, bins=50, orientation='horizontal', color='lightblue', alpha=0.4, edgecolor='black')
    ax_hist.axhline(0, color='red', linestyle='--', linewidth=3.0)
    ax_hist.grid(False)
    ax_hist.set_xlabel("Freq.")
    ax_hist.set_yticklabels([])

    if show_legend:
        ax.legend()

    # Adjust layout to prevent overlap
    plt.tight_layout()

    return ax

def ax_arima_forecast(
    symbol,
    days_back=125,
    test_size=5,
    forecast_horizon=5,
    smoothing_window=40,  # Increased default to 40
    smoother="lowess",
    price_type="close",
    exog_price_type="open",
    periods=1,
    ci=95,
    calendar_days=False,
    level_shifts_model=None,
    level_shifts_penalty=5,
    level_shifts_min_size=10,
    strict_stationarity=True,  # New parameter to control stationarity enforcement
    ax=None,
    show_title=True,
    show_x_label=True,
    show_y_label=True,
    show_grid=True,
    show_legend=True,
    figsize=(14, 7),
    dpi=150,
):
    """
    Plot smoothed stock price data with an ARIMA forecast, including a train-test split and prediction intervals.

    This function retrieves historical stock prices, applies smoothing and log-differencing, splits the data into
    training and test sets, fits an ARIMA model, and forecasts future prices with prediction intervals. The plot
    shows the training data, test data, and forecasted prices with intervals.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol (e.g., 'AAPL').
    days_back : int, optional
        Number of days of historical data to fetch, default is 125.
    test_size : int, optional
        Number of days to use for the test set, default is 5.
    forecast_horizon : int, optional
        Number of days to forecast into the future, default is 5.
    smoothing_window : int, optional
        Window length for smoothing algorithm, default is 40.
    smoother : {'lowess', 'exponential', 'sma'}, optional
        Smoothing method to apply to the price data, default is 'lowess'.
        - 'lowess': Locally Weighted Scatterplot Smoothing.
        - 'exponential': Exponential smoothing.
        - 'sma': Simple Moving Average.
    price_type : {'open', 'close', 'high', 'low'}, optional
        Type of price data to forecast, default is 'close'.
    exog_price_type : {'open', 'close', 'high', 'low'}, optional
        Type of price data to use as the exogenous variable, default is 'open'.
    periods : int, optional
        Number of periods for differencing in log-difference calculation, default is 1.
    ci : float, optional
        Confidence level for prediction intervals (as a percentage), default is 95.
    calendar_days : bool, optional
        If True, uses calendar days, otherwise trading days, default is False.
    level_shifts_model : {'l2', 'l1', 'rbf', 'linear', 'normal', None}, optional
        Ruptures model for detecting level shifts in the smoothed series, default is None.
    level_shifts_penalty : float, optional
        Penalty for level shift detection, default is 5.
    level_shifts_min_size : int, optional
        Minimum points between detected shifts, default is 10.
    strict_stationarity : bool, optional
        If True, enforces strict stationarity (both ADF and KPSS must pass); if False, proceeds with a warning if the series is not stationary, default is True.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on. If None, a new figure and axes are created.
    show_title : bool, optional
        Show the plot title, default is True.
    show_x_label : bool, optional
        Show the x-axis label ('Date'), default is True.
    show_y_label : bool, optional
        Show the y-axis label ('Price (USD)'), default is True.
    show_grid : bool, optional
        Show grid lines, default is True.
    show_legend : bool, optional
        Display legend, default is True.
    figsize : tuple, optional
        Figure size as (width, height) in inches, default is (14, 7).
    dpi : int, optional
        Dots per inch (resolution) of the figure, default is 150.

    Returns
    -------
    matplotlib.axes.Axes
        Axes containing the ARIMA forecast plot.

    Raises
    ------
    ValueError
        If `days_back` is not sufficient to accommodate the test set and training data.
        If price data contains non-positive values, as log-difference requires strictly positive data.
        If an invalid `price_type`, `exog_price_type`, or `smoother` is provided.
        If `strict_stationarity` is True and the series is not stationary after preprocessing.
    """
    # Validate input parameters
    min_obs = 30  # Minimum observations required for ARIMA fitting (from select_best_arimax)
    if days_back < test_size + min_obs + periods:
        raise ValueError(
            f"days_back ({days_back}) must be greater than test_size ({test_size}) + minimum observations ({min_obs}) + periods ({periods}) for ARIMA fitting."
        )

    # Fetch data using helper function
    stock_name, prices, dates, date_type, price_label = _fetch_price_data(
        symbol, days_back, price_type, calendar_days
    )

    # Fetch exogenous data (e.g., opening prices)
    _, exog_prices, _, _, _ = _fetch_price_data(
        symbol, days_back, exog_price_type, calendar_days
    )

    # Create DataFrame for ARIMA preparation
    df = pd.DataFrame({
        price_type: prices,
        exog_price_type: exog_prices
    }, index=dates)

    # Apply smoothing
    if smoother == "lowess":
        smoothed_prices = smooth_lowess(prices, window_length=smoothing_window)
        smoothed_exog = smooth_lowess(exog_prices, window_length=smoothing_window)
        label_smoother = "LOWESS"
    elif smoother == "exponential":
        smoothed_prices, _ = exponential_smoother(prices, window_length=smoothing_window)
        smoothed_exog, _ = exponential_smoother(exog_prices, window_length=smoothing_window)
        smoothed_prices = smoothed_prices.values  # Convert to numpy array
        smoothed_exog = smoothed_exog.values
        label_smoother = "Exponential"
    elif smoother == "sma":
        smoothed_prices = sma_smoother(prices, window_length=smoothing_window)
        smoothed_exog = sma_smoother(exog_prices, window_length=smoothing_window)
        label_smoother = "Simple Moving Average"
    else:
        raise ValueError("Invalid smoother type.")

    # Convert smoothed data back to pd.Series for consistency
    smoothed_prices_series = pd.Series(smoothed_prices, index=dates)
    smoothed_exog_series = pd.Series(smoothed_exog, index=dates)

    # Train-test split
    train_size = len(smoothed_prices) - test_size
    train_dates = dates[:train_size]
    test_dates = dates[train_size:]
    train_smoothed_prices = smoothed_prices_series[:train_size]
    test_smoothed_prices = smoothed_prices_series[train_size:]
    train_exog = smoothed_exog_series[:train_size]
    test_exog = smoothed_exog_series[train_size:]

    # Fit ARIMA model on training data
    train_df = pd.DataFrame({
        price_type: train_smoothed_prices,
        exog_price_type: train_exog
    }, index=train_dates)
    try:
        model, order, price_logdiff, exog_logdiff = prepare_data_and_fit_arimax(
            train_df, price_type, exog_price_type, smoothing_window=smoothing_window
        )
    except ValueError as e:
        if strict_stationarity:
            raise ValueError(
                f"Failed to fit ARIMA model due to stationarity issues: {str(e)}\n"
                "Consider increasing smoothing_window (e.g., 40 or 50), trying a different smoother (e.g., 'exponential' or 'sma'), "
                "or setting strict_stationarity=False to proceed with a warning."
            )
        else:
            print(
                f"Warning: Series is not stationary after preprocessing: {str(e)}\n"
                "Proceeding with ARIMA forecast, but results may be unreliable. "
                "Consider adjusting smoothing_window, smoother, or preprocessing steps."
            )
            # Fit ARIMA model with a higher differencing order
            model, order = select_best_arimax(price_logdiff, exog_logdiff)

    # Forecast over the test period and future horizon
    forecasts = []
    lower_cis = []
    upper_cis = []
    forecast_dates = []

    # Combine test dates and future dates
    last_date = dates.max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon, freq='B')
    all_forecast_dates = list(test_dates) + list(future_dates)
    all_exog = list(test_exog) + [test_exog[-1]] * forecast_horizon  # Assume last exog value for future

    alpha = 1 - (ci / 100)  # Convert confidence level to alpha for prediction intervals
    last_price = train_smoothed_prices.iloc[-1]
    for i in range(len(all_forecast_dates)):
        exog_future = all_exog[i]
        forecast_df = forecast_arimax(
            model, exog_future, last_price, smoother=smoother, smoothing_window=smoothing_window, alpha=alpha
        )
        forecasts.append(forecast_df['forecast'].iloc[0])
        lower_cis.append(forecast_df['lower_ci'].iloc[0])
        upper_cis.append(forecast_df['upper_ci'].iloc[0])
        forecast_dates.append(all_forecast_dates[i])
        last_price = forecasts[-1]  # Update last price for next forecast

    # Convert forecasts to pd.Series for plotting
    forecast_series = pd.Series(forecasts, index=forecast_dates)
    lower_ci_series = pd.Series(lower_cis, index=forecast_dates)
    upper_ci_series = pd.Series(upper_cis, index=forecast_dates)

    # Create ax if not provided
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    # Plot training data
    ax.plot(train_dates, train_smoothed_prices, color="blue", linestyle="-", linewidth=1.5,
            label=f"Training Smoothed {price_label} Prices")

    # Plot test data
    ax.plot(test_dates, test_smoothed_prices, color="green", linestyle="-", linewidth=1.5,
            label=f"Test Smoothed {price_label} Prices")

    # Plot forecast
    ax.plot(forecast_dates, forecast_series, color="red", linestyle="--", linewidth=1.5,
            label=f"ARIMA Forecast ({forecast_horizon}-day)")

    # Plot prediction intervals
    ax.fill_between(forecast_dates, lower_ci_series, upper_ci_series, color="red",
                    alpha=0.2, label=f"{ci}% Prediction Interval")

    # Level shift detection (optional)
    if level_shifts_model:
        shift_indices = detect_level_shifts(
            pd.Series(smoothed_prices_series),
            model=level_shifts_model,
            penalty=level_shifts_penalty,
            min_size=level_shifts_min_size
        )
        shift_dates = dates.iloc[shift_indices]
        for shift_date in shift_dates:
            ax.axvline(x=shift_date, color='purple', linestyle='--', linewidth=1.2, alpha=0.75,
                       label='Detected Level Shift' if shift_date == shift_dates.iloc[0] else "")

    # Formatting
    latest_date = forecast_dates[-1].strftime('%m/%d/%Y')
    earliest_date = dates.min().strftime('%m/%d/%Y')
    if show_title:
        title = (f"\n{stock_name} ({symbol})\nARIMA Forecast on {label_smoother} Smoothed {price_label} Prices ({len(dates)} {date_type})\n"
                 f"{earliest_date} to {latest_date}\n")
        ax.set_title(title, fontsize=16)
    ax.set_xlabel("Date") if show_x_label else None
    ax.set_ylabel("Price (USD)") if show_y_label else None
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.2f}"))
    ax.grid(show_grid)
    if show_legend:
        ax.legend()

    return ax