# src/visualizations/exploratory_plots.py

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
from src.statistics.smoothers import lowess_ci_pi, exp_smooth_ci_pi, sma_ci_pi
from src.statistics.changepoints import detect_level_shifts
from src.utils.db_utils import get_db_connection, fetch_price_range, get_stock_name

def ax_smoothed_prices(
    symbol, 
    days_back=125,
    smoothing_window=30,
    smoother="lowess",
    price_type="close",
    show_actual_line=False,
    calendar_days=False,
    ci=95,
    level_shifts_model=None,  # Options: 'l2', 'l1', 'rbf', 'linear', 'normal', or None
    level_shifts_penalty=5,
    level_shifts_min_size=10,
    ax=None,
    show_title=True,
    show_x_label=True,
    show_y_label=True,
    show_grid=True,
    show_legend=True,
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

    if price_type not in ["open", "close", "high", "low"]:
        raise ValueError("Invalid price type. Choose 'open', 'close', 'high', or 'low'.")

    price_label = price_type.capitalize()

    # Fetch price data
    conn = get_db_connection('assets.db')
    price_data = fetch_price_range(symbol, days_back, conn=conn, calendar_days=calendar_days)
    stock_name = get_stock_name(symbol, conn=conn)
    conn.close()

    prices = price_data[price_type]
    dates = price_data['date']

    if calendar_days:
        date_type = "Calendar Days"
    else: 
        date_type = "Trading Days"

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
        fig, ax = plt.subplots(figsize=(14, 7), dpi=150)

    # Scatter actual prices
    ax.scatter(dates, prices, edgecolors="black", facecolors="lightblue",
               linewidth=1.5, marker="o", s=45, alpha=1.0,
               label=f"Actual {price_label} Prices")

    # Actual line connecting points
    if show_actual_line:
        ax.plot(dates, prices, color="dodgerblue", linewidth=0.5, label="Actual Line")

    # Plot smoothed line
    ax.plot(dates, smoothed, color="red", linestyle="--", linewidth=1.5,
            label=f"Smoothed {label_smoother} ({smoothing_window}-day)")

    # Confidence Interval
    ax.fill_between(dates, ci_lower, ci_upper, color="dodgerblue",
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
    if show_x_label: ax.set_xlabel("\nDate\n")
    if show_y_label: ax.set_ylabel("\nPrice (USD)\n")
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
        If True, uses calendar days, otherwise trading days, default False.
    level_shifts_model : {'l2', 'l1', 'rbf', 'linear', 'normal', None}, optional
        Ruptures model for detecting level shifts, default None.
    level_shifts_penalty : float, optional
        Penalty for level shift detection, default is 5.
    level_shifts_min_size : int, optional
        Minimum points between detected shifts, default is 10.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on. Created if None.
    show_title : bool, optional
        Show the plot title, default True.
    show_x_label : bool, optional
        Show the x-axis label, default True.
    show_y_label : bool, optional
        Show the y-axis label, default True.
    show_grid : bool, optional
        Show grid lines, default True.
    show_legend : bool, optional
        Display legend, default True.

    Returns
    -------
    matplotlib.axes.Axes
        Axes containing the residual plot with horizontal histogram.
    """

    # Fetch historical data
    conn = get_db_connection('assets.db')
    price_data = fetch_price_range(symbol, days_back, conn=conn, calendar_days=calendar_days)
    stock_name = get_stock_name(symbol, conn=conn)
    conn.close()

    prices = price_data[price_type]
    dates = price_data['date']

    # Apply smoothing
    if smoother == "lowess":
        smoothed, _, _, _, _ = lowess_ci_pi(prices, smoothing_window)
    elif smoother == "exponential":
        smoothed, _, _, _, _ = exp_smooth_ci_pi(prices, smoothing_window)
    elif smoother == "sma":
        smoothed, _, _, _, _ = sma_ci_pi(prices, smoothing_window)
    else:
        raise ValueError("Invalid smoother type.")

    residuals = prices - smoothed

    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 7), dpi=150)

    # Plot residuals
    ax.plot(dates, residuals, color="black", linestyle='-', linewidth=1.0, label="Residuals")
    ax.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.7)

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

    ax.set_title(f"Residuals of {stock_name} ({symbol}) {price_type.capitalize()} Prices", fontsize=16) if show_title else None
    ax.set_xlabel("Date") if show_x_label else None
    ax.set_ylabel("Residuals (USD)") if show_y_label else None
    ax.grid(show_grid)

    # Horizontal histogram for residual distribution
    ax_hist = ax.inset_axes([1.02, 0.1, 0.2, 0.8])
    ax_hist.hist(residuals, bins=25, orientation='horizontal', color='gray', edgecolor='black')
    ax_hist.axhline(0, color='red', linestyle='--', linewidth=1)
    ax_hist.grid(False)
    ax_hist.set_xlabel("Freq.")
    ax_hist.set_yticklabels([])

    if show_legend:
        ax.legend()

    plt.tight_layout()

    return ax
