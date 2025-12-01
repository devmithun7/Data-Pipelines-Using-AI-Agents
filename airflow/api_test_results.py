"""
Simple API test that writes results to a file.
"""
import requests
import json
from datetime import datetime

def test_api():
    try:
        # Test Finnhub REST API
        url = "https://finnhub.io/api/v1/quote?symbol=AAPL&token=d4mkjupr01qnt4h0j7vgd4mkjupr01qnt4h0j800"
        
        response = requests.get(url, timeout=10)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "status_code": response.status_code,
            "url": url,
            "success": response.status_code == 200
        }
        
        if response.status_code == 200:
            data = response.json()
            result["data"] = data
            result["sample_fields"] = {
                "current_price": data.get('c'),
                "high": data.get('h'),
                "low": data.get('l'),
                "open": data.get('o'),
                "previous_close": data.get('pc'),
                "timestamp": data.get('t')
            }
        else:
            result["error"] = response.text
            
        # Write results to file
        with open('api_test_output.json', 'w') as f:
            json.dump(result, f, indent=2)
            
        print("API test completed. Check api_test_output.json for results.")
        return result
        
    except Exception as e:
        error_result = {
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "success": False
        }
        with open('api_test_output.json', 'w') as f:
            json.dump(error_result, f, indent=2)
        print(f"Error occurred: {e}")
        return error_result

if __name__ == "__main__":
    test_api()
