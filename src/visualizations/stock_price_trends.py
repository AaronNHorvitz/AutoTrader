# src/visualizations/stock_price_trends.py
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
    calendar_days=False,
    ci=95,
):
    """
    Plot stock price trends with smoothing and confidence/prediction intervals.

    This function retrieves historical stock data from a SQLite database (`assets.db`) 
    and visualizes the price trends using a smoothing method (LOWESS, Exponential, or Simple Moving Average). 
    Confidence and prediction intervals are also displayed to indicate uncertainty around the smoothed estimates.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol (e.g., 'AAPL').
    days_back : int, optional
        Number of days back (calendar or trading) to fetch data, by default 125.
    smoothing_window : int, optional
        Window size for smoothing, by default 30.
    smoother : {'lowess', 'exponential', 'sma'}, optional
        Smoothing method to apply:
        - 'lowess': Locally Weighted Scatterplot Smoothing.
        - 'exponential': Exponential smoothing method.
        - 'sma': Simple moving average.
        Default is 'lowess'.
    price_type : {'open', 'close', 'high', 'low'}, optional
        Type of price data to visualize, by default 'close'.
    show_actual_line : bool, optional
        Whether to show a continuous line connecting actual price data points, by default False.
    calendar_days : bool, optional
        If True, `days_back` refers to calendar days; 
        if False, it refers to trading days, by default False.
    ci : float, optional
        Confidence interval percentage for the intervals shown on the plot, by default 95.

    Returns
    -------
    None
        Displays a Matplotlib plot.

    Raises
    ------
    ValueError
        - If `price_type` is not one of {'open', 'close', 'high', 'low'}.
        - If `smoother` is not one of {'lowess', 'exponential', 'sma'}.

    Examples
    --------
    Plot the last 30 trading days of Apple closing prices using LOWESS smoothing:

    >>> plot_stock_trends_with_intervals(
    ...     symbol="AAPL", days_back=30, smoother="lowess", price_type="close"
    ... )

    Plot opening prices for Tesla using exponential smoothing, showing the actual price line:

    >>> plot_stock_trends_with_intervals(
    ...     symbol="TSLA", days_back=60, smoother="exponential", price_type="open", show_actual_line=True
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

    if show_actual_line:
        plt.plot(dates, prices, color="dodgerblue", linewidth=0.5, label="Actual Line")
    
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
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
