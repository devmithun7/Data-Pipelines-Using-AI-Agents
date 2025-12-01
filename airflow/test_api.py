"""
Test script to check Finnhub API connection and data format.
"""
import json
import websocket
import threading
import time

def on_message(ws, message):
    """Handle incoming WebSocket messages."""
    try:
        data = json.loads(message)
        print("Received data:")
        print(json.dumps(data, indent=2))
        print("-" * 50)
    except json.JSONDecodeError:
        print(f"Raw message: {message}")

def on_error(ws, error):
    """Handle WebSocket errors."""
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket close."""
    print("WebSocket connection closed")

def on_open(ws):
    """Handle WebSocket open and subscribe to stock data."""
    print("WebSocket connection opened")
    # Subscribe to Apple (AAPL) stock trades
    subscribe_message = {"type": "subscribe", "symbol": "AAPL"}
    ws.send(json.dumps(subscribe_message))
    print("Subscribed to AAPL stock data")

def test_finnhub_websocket():
    """Test Finnhub WebSocket API connection."""
    # WebSocket URL with token
    ws_url = "wss://ws.finnhub.io/?token=d4mkjupr01qnt4h0j7vgd4mkjupr01qnt4h0j800"
    
    # Create WebSocket connection
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    # Run for 10 seconds to collect some data
    def stop_after_delay():
        time.sleep(10)
        ws.close()
    
    # Start timer to stop connection
    timer = threading.Timer(10.0, stop_after_delay)
    timer.start()
    
    print("Starting WebSocket connection test...")
    ws.run_forever()

if __name__ == "__main__":
    test_finnhub_websocket()
