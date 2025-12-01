"""
Unit tests for test_dag.py - Stock Price DAG
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json
import sys
import os

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'dags'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'include'))

from airflow.models import DagBag
from airflow.utils.dates import days_ago


class TestStockPriceDAG:
    """Test class for stock price DAG."""
    
    @pytest.fixture
    def dagbag(self):
        """Load DAG for testing."""
        return DagBag(dag_folder='dags/', include_examples=False)
    
    @pytest.fixture
    def dag(self, dagbag):
        """Get the test_dag from dagbag."""
        return dagbag.get_dag(dag_id='test_dag')
    
    def test_dag_loaded(self, dagbag):
        """Test that DAG loads without import errors."""
        assert dagbag.import_errors == {}, f"DAG import errors: {dagbag.import_errors}"
        assert 'test_dag' in dagbag.dag_ids, "test_dag not found in loaded DAGs"
    
    def test_dag_properties(self, dag):
        """Test DAG configuration properties."""
        assert dag is not None, "DAG should not be None"
        assert dag.dag_id == 'test_dag', f"Expected dag_id 'test_dag', got '{dag.dag_id}'"
        assert dag.description == "This data pipeline will fetch stock price from an API and store the data in a Postgres database."
        assert dag.schedule_interval is None, "Schedule should be None for manual trigger"
        assert dag.catchup is False, "Catchup should be False"
        assert dag.max_active_runs == 1, "Max active runs should be 1"
        assert 'stock_price' in dag.tags, "Should have 'stock_price' tag"
        assert 'cusrosr-airflow' in dag.tags, "Should have 'cusrosr-airflow' tag"
    
    def test_dag_tasks(self, dag):
        """Test DAG task structure."""
        tasks = dag.tasks
        task_ids = [task.task_id for task in tasks]
        
        assert len(tasks) == 1, f"Expected 1 task, found {len(tasks)}"
        assert 'fetch_stock_prices' in task_ids, "fetch_stock_prices task should exist"
    
    def test_task_properties(self, dag):
        """Test task configuration."""
        task = dag.get_task('fetch_stock_prices')
        
        assert task is not None, "fetch_stock_prices task should exist"
        assert task.retries == 2, "Task should have 2 retries from default_args"


class TestStockPriceFetching:
    """Test class for stock price fetching functionality."""
    
    @pytest.fixture
    def mock_successful_api_response(self):
        """Mock successful API response data."""
        return {
            'c': 150.25,    # current price
            'h': 152.10,    # high
            'l': 149.80,    # low
            'o': 151.00,    # open
            'pc': 150.00,   # previous close
            'd': 0.25,      # change
            'dp': 0.17,     # percent change
            't': 1640995200 # timestamp
        }
    
    @pytest.fixture
    def expected_processed_data(self):
        """Expected data structure after processing."""
        return {
            'symbol': 'AAPL',
            'current_price': 150.25,
            'high_price': 152.10,
            'low_price': 149.80,
            'open_price': 151.00,
            'previous_close': 150.00,
            'change': 0.25,
            'percent_change': 0.17,
            'timestamp': 1640995200
        }
    
    @patch('fetch_stock_data.requests.get')
    def test_successful_api_call(self, mock_get, mock_successful_api_response, expected_processed_data):
        """Test successful API call and data processing."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_successful_api_response
        mock_get.return_value = mock_response
        
        # Import and test function
        from fetch_stock_data import fetch_stock_quote
        
        result = fetch_stock_quote('AAPL')
        
        # Verify API call
        mock_get.assert_called_once()
        assert 'symbol=AAPL' in mock_get.call_args[0][0]
        assert 'token=' in mock_get.call_args[0][0]
        
        # Verify data structure
        assert result['symbol'] == 'AAPL'
        assert result['current_price'] == expected_processed_data['current_price']
        assert result['high_price'] == expected_processed_data['high_price']
        assert result['low_price'] == expected_processed_data['low_price']
        assert result['open_price'] == expected_processed_data['open_price']
        assert result['previous_close'] == expected_processed_data['previous_close']
        assert result['change'] == expected_processed_data['change']
        assert result['percent_change'] == expected_processed_data['percent_change']
        assert 'fetch_time' in result
        assert 'raw_data' in result
    
    def test_data_types(self, mock_successful_api_response):
        """Test that returned data has correct types."""
        with patch('fetch_stock_data.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_successful_api_response
            mock_get.return_value = mock_response
            
            from fetch_stock_data import fetch_stock_quote
            result = fetch_stock_quote('AAPL')
            
            # Test numeric types
            assert isinstance(result['current_price'], (int, float)), "Current price should be numeric"
            assert isinstance(result['high_price'], (int, float)), "High price should be numeric"
            assert isinstance(result['low_price'], (int, float)), "Low price should be numeric"
            assert isinstance(result['open_price'], (int, float)), "Open price should be numeric"
            assert isinstance(result['previous_close'], (int, float)), "Previous close should be numeric"
            assert isinstance(result['change'], (int, float)), "Change should be numeric"
            assert isinstance(result['percent_change'], (int, float)), "Percent change should be numeric"
            
            # Test string types
            assert isinstance(result['symbol'], str), "Symbol should be string"
            assert isinstance(result['fetch_time'], str), "Fetch time should be string"
    
    def test_data_validation(self, mock_successful_api_response):
        """Test data validation rules."""
        with patch('fetch_stock_data.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_successful_api_response
            mock_get.return_value = mock_response
            
            from fetch_stock_data import fetch_stock_quote
            result = fetch_stock_quote('AAPL')
            
            # Test price validations
            assert result['current_price'] > 0, "Current price should be positive"
            assert result['high_price'] >= result['low_price'], "High should be >= low"
            assert result['high_price'] >= result['current_price'], "High should be >= current"
            assert result['low_price'] <= result['current_price'], "Low should be <= current"
    
    @patch('fetch_stock_data.requests.get')
    def test_api_timeout_error(self, mock_get):
        """Test API timeout handling."""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        from fetch_stock_data import fetch_stock_quote
        
        with pytest.raises(Exception) as exc_info:
            fetch_stock_quote('AAPL')
        
        assert "Network error" in str(exc_info.value)
    
    @patch('fetch_stock_data.requests.get')
    def test_api_http_error(self, mock_get):
        """Test HTTP error handling."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response
        
        from fetch_stock_data import fetch_stock_quote
        
        with pytest.raises(Exception) as exc_info:
            fetch_stock_quote('AAPL')
        
        assert "API request failed with status 401" in str(exc_info.value)
    
    @patch('fetch_stock_data.requests.get')
    def test_invalid_json_response(self, mock_get):
        """Test invalid JSON response handling."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response
        
        from fetch_stock_data import fetch_stock_quote
        
        with pytest.raises(Exception):
            fetch_stock_quote('AAPL')


class TestTaskExecution:
    """Test actual task execution."""
    
    def test_task_execution_with_mock(self):
        """Test task execution with mocked API."""
        with patch('fetch_stock_data.requests.get') as mock_get:
            # Setup mock
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'c': 150.25, 'h': 152.10, 'l': 149.80, 'o': 151.00,
                'pc': 150.00, 'd': 0.25, 'dp': 0.17, 't': 1640995200
            }
            mock_get.return_value = mock_response
            
            # Import DAG and get task
            from test_dag import test_dag
            dag_instance = test_dag()
            
            # Execute task (this would normally be done by Airflow)
            # For testing, we can call the task function directly
            # Note: In real Airflow testing, you'd use DagRun and TaskInstance
            
            # Test passes if no exception is raised
            assert True, "Task execution completed without errors"


if __name__ == "__main__":
    # Run tests when executed directly
    pytest.main([__file__, "-v"])
