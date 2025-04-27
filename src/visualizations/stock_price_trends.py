# src/visualizations/stock_price_trends.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from src.statistics.smoothers import lowess_ci_pi, exp_smooth_ci_pi, sma_ci_pi
from src.utils.db_utils import get_db_connection, fetch_price_range, get_stock_name

def plot_stock_trends_with_intervals(
    symbol, 
    days_back=125,
    smoothing_window=30,
    smoother="lowess",
    price_type="close",
    show_actual_line=False,
    show_grid=True,
    show_legend=True,
    calendar_days=False,
    ci=95,
    level_shifts_model=None,  # 'l2', 'l1', 'rbf', 'linear', 'normal', or None
    level_shifts_penalty=5,
    level_shifts_min_size=10
):
    """
    Plot stock price trends with smoothing, confidence/prediction intervals, and optional level shift detections.

    This function retrieves historical stock data from a SQLite database (`assets.db`) 
    and visualizes the price trends using selected smoothing methods (LOWESS, Exponential, or Simple Moving Average). 
    Confidence and prediction intervals are shown to indicate uncertainty around the smoothed estimates.
    Additionally, the function can detect and plot level shifts (changepoints) in the stock price trend.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol (e.g., 'AAPL').
    days_back : int, optional
        Number of days back (calendar or trading) to fetch data, default is 125.
    smoothing_window : int, optional
        Window size for smoothing, default is 30.
    smoother : {'lowess', 'exponential', 'sma'}, optional
        Smoothing method applied:
        - 'lowess': Locally Weighted Scatterplot Smoothing (default).
        - 'exponential': Exponential smoothing.
        - 'sma': Simple moving average.
    price_type : {'open', 'close', 'high', 'low'}, optional
        Type of price data to visualize, default is 'close'.
    show_actual_line : bool, optional
        Show a continuous line connecting actual price points, default False.
    show_grid : bool, optional
        Display gridlines on the plot, default True.
    show_legend : bool, optional
        Display the plot legend, default True.
    calendar_days : bool, optional
        If True, `days_back` refers to calendar days; otherwise, trading days (default False).
    ci : float, optional
        Confidence interval percentage for the intervals shown, default is 95.
    level_shifts_model : {'l2', 'l1', 'rbf', 'linear', 'normal', None}, optional
        Model for level shift detection:
        - 'l2': Mean shifts using squared deviations.
        - 'l1': Robust shifts detection using absolute deviations.
        - 'rbf': Shifts in distribution (general-purpose).
        - 'linear': Shifts in linear trends.
        - 'normal': Shifts assuming normal distribution.
        - None: No level shift detection (default).
    level_shifts_penalty : int or float, optional
        Penalty value controlling sensitivity to changes (higher means fewer shifts), default is 5.
    level_shifts_min_size : int, optional
        Minimum observations between detected changepoints, default is 10.

    Returns
    -------
    None
        Displays a Matplotlib plot.

    Raises
    ------
    ValueError
        - If `price_type` is invalid.
        - If `smoother` is invalid.

    Examples
    --------
    Plot closing prices of Apple for the last 30 trading days with LOWESS smoothing and level shift detection:

    >>> plot_stock_trends_with_intervals(
    ...     symbol="AAPL", days_back=30, smoother="lowess", price_type="close",
    ...     level_shifts_model='l2'
    ... )

    Plot Tesla opening prices with exponential smoothing, showing the actual price line and no level shift detection:

    >>> plot_stock_trends_with_intervals(
    ...     symbol="TSLA", days_back=60, smoother="exponential", price_type="open", 
    ...     show_actual_line=True, level_shifts_model=None
    ... )
    """
    
    # Make sure price type is valid
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

    # Initialize database connection and fetch price data
    conn = get_db_connection('assets.db')
    price_data = fetch_price_range(symbol, days_back, conn=conn)
    stock_name = get_stock_name(symbol, conn=conn)
    conn.close()
    
    # Extract price information
    prices = price_data[price_type]

    # Extract date information
    dates = price_data['date']
    date_format = '%m/%d/%Y'
    latest_date = dates.max().strftime(date_format)
    earliest_date = dates.min().strftime(date_format)
    num_dates = len(dates.unique())

    if calendar_days:
        date_type = "Calendar Days"
    else: 
        date_type = "Trading Days"

    # Calculate and plot intervals based on selected smoother
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
        raise ValueError("Invalid smoother type. Choose 'lowess', 'exponential', or 'sma'.")
    
    # Matplotlib gumph ---

    # Set figure params
    plt.figure(figsize=(14, 7), dpi=150)

    # Scatter plot of actual prices
    plt.scatter(
        x=dates,
        y=prices,
        edgecolors="black",
        facecolors="lightblue",
        linewidth=1.5,
        marker="o",
        s=45,
        alpha=1.0,
        label=f"Actual {price_label} Prices",
    )

    # Line between actual prices
    if show_actual_line:
        plt.plot(dates, prices, color="dodgerblue", linewidth=0.5, label="Actual Line")        
    
    # Level Shift Detection
    if level_shifts_model is not None:
        from src.statistics.changepoints import detect_level_shifts

        shift_indices = detect_level_shifts(
            pd.Series(smoothed), 
            model=level_shifts_model, 
            penalty=level_shifts_penalty, 
            min_size=level_shifts_min_size
        )

        shift_dates = dates.iloc[shift_indices]

        # Plot vertical lines for detected shifts
        for shift_date in shift_dates:
            plt.axvline(
                x=shift_date,
                color='purple',
                linestyle='--',
                linewidth=1.2,
                alpha=0.75,
                label='Detected Level Shift' if shift_date == shift_dates.iloc[0] else ""
            )
    
    plt.plot(
        dates,
        smoothed,
        color="red",
        linestyle="--",
        linewidth=1.5,
        label=f"Smoothed {label_smoother} ({smoothing_window}-day smoothing window)",
    )

    # Fill Confidence Interval (dark grey)
    plt.fill_between(
        dates,
        ci_lower,
        ci_upper,
        color="dodgerblue",
        edgecolor="black",
        linewidth=0.5,
        alpha=0.2,
        label=f"{ci}% Confidence Interval",
    )

    # Fill Prediction Interval (lighter grey)
    plt.fill_between(
        dates,
        pi_lower,
        pi_upper,
        color="lightgrey",
        edgecolor="black",
        linestyle="--",
        linewidth=0.5,
        alpha=0.30,
        label=f"{ci}% Prediction Interval",
    )

    title_string = f"\n{stock_name}({symbol})\n{price_label} Prices({num_dates} {date_type})\n{earliest_date} to {latest_date}\n"
    plt.title(title_string, fontsize=16)
    plt.xlabel("\nDate\n")
    plt.ylabel("\nPrice (USD)\n")
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.2f}"))
    if show_grid:
        plt.grid(True)
    if show_legend:
        plt.legend()
    plt.tight_layout()
    plt.show()