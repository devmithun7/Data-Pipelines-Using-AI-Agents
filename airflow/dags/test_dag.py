"""
Test DAG for stock price data pipeline.
"""

from airflow.decorators import dag, task
from pendulum import duration
import sys
import os

# Add include directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'include'))


default_args = {
    "retries": 2,
}


@dag(
    dag_id="test_dag",
    description="This data pipeline will fetch stock price from an API and store the data in a Postgres database.",
    schedule=None,
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=duration(minutes=30),
    default_args=default_args,
    tags=["stock_price", "cusrosr-airflow"],
)
def test_dag():
    """
    Test data pipeline for fetching stock prices.
    
    This DAG is structured to be easily extensible for future tasks:
    - API data fetching
    - Data transformation
    - Database storage
    """
    
    @task
    def fetch_stock_prices() -> dict:
        """
        Fetch stock prices from Finnhub API.
        
        Returns:
            Dictionary containing stock price data
        """
        from fetch_stock_data import fetch_stock_quote
        
        # Fetch Apple stock data
        stock_data = fetch_stock_quote("AAPL")
        
        print("Stock Price Data Head:")
        print(f"Symbol: {stock_data['symbol']}")
        print(f"Current Price: ${stock_data['current_price']}")
        print(f"High: ${stock_data['high_price']}")
        print(f"Low: ${stock_data['low_price']}")
        print(f"Open: ${stock_data['open_price']}")
        print(f"Previous Close: ${stock_data['previous_close']}")
        print(f"Change: {stock_data['change']} ({stock_data['percent_change']}%)")
        print(f"Fetch Time: {stock_data['fetch_time']}")
        
        return stock_data
    
    # Define task
    stock_task = fetch_stock_prices()


# Instantiate the DAG
test_dag()
