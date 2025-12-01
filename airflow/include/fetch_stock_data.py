"""
Stock data fetching functions for Airflow tasks.
"""
import requests
import json
from typing import Dict, Any
from datetime import datetime


def fetch_stock_quote(symbol: str = "AAPL") -> Dict[str, Any]:
    """
    Fetch current stock quote from Finnhub API.
    
    Args:
        symbol: Stock symbol to fetch (default: AAPL)
        
    Returns:
        Dictionary containing stock data
    """
    api_token = "d4mkjupr01qnt4h0j7vgd4mkjupr01qnt4h0j800"
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_token}"
    
    try:
        print(f"Fetching stock data for {symbol}...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Add metadata
            result = {
                "symbol": symbol,
                "fetch_time": datetime.now().isoformat(),
                "current_price": data.get('c'),
                "high_price": data.get('h'),
                "low_price": data.get('l'),
                "open_price": data.get('o'),
                "previous_close": data.get('pc'),
                "change": data.get('d'),
                "percent_change": data.get('dp'),
                "timestamp": data.get('t'),
                "raw_data": data
            }
            
            print(f"Successfully fetched data for {symbol}")
            print(f"Current Price: ${result['current_price']}")
            print(f"Change: {result['change']} ({result['percent_change']}%)")
            
            return result
            
        else:
            error_msg = f"API request failed with status {response.status_code}: {response.text}"
            print(error_msg)
            raise Exception(error_msg)
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error fetching stock data: {str(e)}"
        print(error_msg)
        raise Exception(error_msg)
    except Exception as e:
        error_msg = f"Error fetching stock data: {str(e)}"
        print(error_msg)
        raise


def test_api_connection() -> bool:
    """
    Test API connection and print sample data.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        print("Testing Finnhub API connection...")
        data = fetch_stock_quote("AAPL")
        
        print("\n" + "="*50)
        print("API TEST RESULTS - SAMPLE DATA HEAD:")
        print("="*50)
        print(json.dumps(data, indent=2))
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"API test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the API when run directly
    test_api_connection()
