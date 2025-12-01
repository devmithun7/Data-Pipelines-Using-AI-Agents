# Stock Price Data Pipeline - Airflow Project

A comprehensive Apache Airflow data pipeline for fetching real-time stock prices from the Finnhub API, built with AI assistance and following modern data engineering best practices.

## 🎯 Overview

This Airflow project demonstrates a complete ETL pipeline that:
- Fetches real-time stock price data from Finnhub API
- Processes and validates the data with comprehensive error handling
- Includes a full pytest test suite with API mocking
- Follows all Airflow DAG writing guidelines and best practices
- Ready for database integration and production deployment

## 🏗️ Project Structure

```
airflow/
├── dags/
│   └── test_dag.py                    # Main stock price DAG
├── include/
│   └── fetch_stock_data.py           # API integration functions
├── tests/
│   └── dags/test_dag/
│       └── test_test_dag.py          # Comprehensive test suite
├── todolist.md                       # Detailed implementation docs
├── pytest.ini                       # Testing configuration
├── requirements.txt                  # Dependencies with testing libs
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker Desktop running
- Astronomer Astro CLI installed

### Launch Airflow
```bash
# Start the Airflow environment
astro dev start

# Access Airflow UI at http://localhost:8080
# Username: admin, Password: admin
```

### Run the Stock Price DAG
1. Open Airflow UI at http://localhost:8080
2. Find the `test_dag` in the DAGs list
3. Toggle it ON and trigger manually
4. View logs to see real-time stock data

## 📊 Stock Price DAG Details

### Configuration
- **DAG ID**: `test_dag`
- **Schedule**: Manual trigger only (`schedule=None`)
- **Stock Symbol**: AAPL (Apple Inc.)
- **API**: Finnhub.io real-time stock data
- **Timeout**: 30 minutes
- **Retries**: 2 attempts

### Sample Output
```
Stock Price Data Head:
Symbol: AAPL
Current Price: $150.25
High: $152.10
Low: $149.80
Open: $151.00
Previous Close: $150.00
Change: 0.25 (0.17%)
Fetch Time: 2025-12-01T10:30:00
```

### Data Fields Captured
- **Current Price**: Real-time stock price
- **High/Low**: Daily high and low prices
- **Open Price**: Market opening price
- **Previous Close**: Previous trading day close
- **Change**: Price change and percentage
- **Timestamp**: Data fetch time

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test class
pytest tests/dags/test_dag/test_test_dag.py::TestStockPriceFetching -v
```

### Test Coverage
- ✅ **DAG Loading**: Validates DAG imports and configuration
- ✅ **API Integration**: Mocked API calls and response processing
- ✅ **Data Validation**: Type checking and price relationship validation
- ✅ **Error Handling**: Network timeouts, HTTP errors, invalid JSON
- ✅ **Task Execution**: End-to-end task running tests

## 🔧 API Configuration

### Finnhub API
- **Current Token**: Demo token included (rate limited)
- **Get Your Token**: Sign up at [Finnhub.io](https://finnhub.io/) for free
- **Update Token**: Modify `api_token` in `include/fetch_stock_data.py`

### Supported Symbols
Currently configured for AAPL, but easily extensible to any stock symbol:
```python
# In fetch_stock_data.py
stock_data = fetch_stock_quote("TSLA")  # Tesla
stock_data = fetch_stock_quote("GOOGL") # Google
```

## 📝 Development Guidelines

This project follows strict Airflow best practices:

- **@dag decorator**: Modern DAG definition
- **@task decorator**: TaskFlow API for Python functions  
- **Type hints**: Complete type annotations
- **Error handling**: Comprehensive exception handling
- **Testing**: Every function has corresponding tests
- **Include directory**: External scripts and functions
- **No top-level code**: All code wrapped in functions

See `.cursor/rules/` for complete coding guidelines.

## 🔄 Next Steps

### Ready for Extension
- **Database Storage**: Add PostgreSQL task to store data
- **Multiple Symbols**: Extend to fetch multiple stocks
- **Scheduling**: Convert to `@daily` or `@hourly` schedule
- **Data Transformation**: Add data cleaning and enrichment
- **Alerting**: Email/Slack notifications for failures

### Production Deployment
- Replace demo API token with production token
- Add connection management for databases
- Set up proper scheduling intervals
- Configure monitoring and alerting

## 🛠️ Troubleshooting

### Common Issues
1. **DAG not appearing**: Check for import errors in Airflow logs
2. **API failures**: Verify Finnhub token and network connectivity
3. **Test failures**: Ensure all dependencies installed via `requirements.txt`

### Logs Location
- **Airflow UI**: Task logs available in the web interface
- **Local logs**: Check `logs/` directory in Astro project

## 📋 Implementation History

See `todolist.md` for detailed implementation tracking including:
- Phase 1: Initial DAG setup
- Phase 2: API integration  
- Phase 3: Comprehensive testing
- Phase 4: Version control and deployment

---

**Built with modern data engineering practices and AI-assisted development** 🚀

