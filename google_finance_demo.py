import yfinance as yf
import pandas as pd

def get_stock_data(ticker_symbol):
    """
    Fetches real-time and basic info for a given ticker using yfinance.
    """
    print(f"--- Fetching data for {ticker_symbol} ---")
    
    # Create ticker object
    ticker = yf.Ticker(ticker_symbol)
    
    # Get basic info
    info = ticker.info
    print(f"Name: {info.get('longName')}")
    print(f"Current Price: ${info.get('currentPrice')}")
    print(f"Market Cap: {info.get('marketCap')}")
    print(f"P/E Ratio: {info.get('trailingPE')}")
    
    # Get historical data (last 5 days)
    print(f"\nLast 5 days of history:")
    hist = ticker.history(period="5d")
    print(hist[['Open', 'High', 'Low', 'Close', 'Volume']])

if __name__ == "__main__":
    # Example Tickers: GOOGL (Google), AAPL (Apple), MSFT (Microsoft)
    get_stock_data("GOOGL")
