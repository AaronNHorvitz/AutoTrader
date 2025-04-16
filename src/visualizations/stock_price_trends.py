# src/visualizations/stock_price_trends.py
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from src.statistics.smoothers import smooth_lowess  # Clear import here

def plot_stock_trends(dates, prices, symbol, smoother='lowess', window = 30):

    plt.figure(figsize=(14, 6), dpi=150)
    plt.scatter(dates, prices, edgecolors='black', facecolors='none', s=60, label='Actual Prices')
    plt.plot(dates, prices, color='blue', linewidth=1, label='Actual')
    
    # Plot Smoother
    if smoother == 'lowess':
        smoothed_prices = smooth_lowess(prices, window=window)
        plt.plot(dates, smoothed_prices, color='red', linestyle='--', linewidth=3, label='Smoothed LOWESS')
    
    plt.title(f'Stock Price Trend for {symbol}', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.2f}'))
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()