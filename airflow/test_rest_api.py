"""
Test script to check Finnhub REST API connection and data format.
"""
import requests
import json

def test_finnhub_rest_api():
    """Test Finnhub REST API for stock data."""
    # API endpoint for stock quote
    api_token = "d4mkjupr01qnt4h0j7vgd4mkjupr01qnt4h0j800"
    symbol = "AAPL"  # Apple stock
    
    # REST API endpoint
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_token}"
    
    try:
        print(f"Testing Finnhub REST API for {symbol}...")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nStock Data (Head):")
            print(json.dumps(data, indent=2))
            
            # Print key fields
            if 'c' in data:  # current price
                print(f"\nKey Data Points:")
                print(f"Current Price: ${data.get('c', 'N/A')}")
                print(f"High Price: ${data.get('h', 'N/A')}")
                print(f"Low Price: ${data.get('l', 'N/A')}")
                print(f"Open Price: ${data.get('o', 'N/A')}")
                print(f"Previous Close: ${data.get('pc', 'N/A')}")
                print(f"Timestamp: {data.get('t', 'N/A')}")
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_finnhub_rest_api()
