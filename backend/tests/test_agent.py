import pytest
import json
import time
from unittest.mock import patch, MagicMock
from agent import FinancialAgent, redis_client


@pytest.fixture
def agent():
    """Fixture to initialize FinancialAgent once for all tests."""
    # Clear cache for a clean test environment
    redis_client.flushdb()
    return FinancialAgent()


def test_get_stock_price_valid(agent):
    """Test get_stock_price with a valid symbol."""
    # Mock the requests.get call to return a fake response
    with patch("agent.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Fake Alpha Vantage intraday JSON response
        mock_response.json.return_value = {
            "Time Series (5min)": {
                "2025-02-14 19:55:00": {
                    "1. open": "244.7100",
                    "2. high": "244.7500",
                    "3. low": "244.5000",
                    "4. close": "244.6400",
                    "5. volume": "2096"
                }
            }
        }
        mock_get.return_value = mock_response

        result = agent.get_stock_price("AAPL")
        assert "error" not in result
        assert result["symbol"] == "AAPL"
        assert result["open"] == "244.7100"


def test_get_stock_price_invalid_symbol(agent):
    """Test get_stock_price with an invalid symbol."""
    with patch("agent.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Error Message": "Invalid API call"
        }
        mock_get.return_value = mock_response

        result = agent.get_stock_price("INVALID_SYMBOL")
        assert "error" in result
        assert "Invalid API call" in result["error"]


def test_query_historical_data(agent):
    """Test query_historical_data with a valid SQL query."""
    result = agent.query_historical_data("SELECT * FROM stock_data")
    assert "error" not in result
    assert result["query"] == "SELECT * FROM stock_data"
    # Since our backend returns a list (not a string) for historical data
    assert isinstance(result["result"], list)
    assert len(result["result"]) > 0


def test_get_financial_news(agent):
    """Test get_financial_news with a valid symbol."""
    with patch("agent.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Fake news response from Alpha Vantage
        mock_response.json.return_value = {
            "feed": [
                {
                    "title": "Sample news article",
                    "url": "http://example.com",
                    "summary": "Sample summary",
                    "source": "Example Source"
                }
            ]
        }
        mock_get.return_value = mock_response

        result = agent.get_financial_news("AAPL")
        assert "error" not in result
        assert result["symbol"] == "AAPL"
        assert isinstance(result["news"], list)
        assert result["news"][0]["title"] == "Sample news article"


def test_stock_price_caching(agent):
    """Test caching: After a successful call, verify that data is cached in Redis."""
    # Clear cache for symbol "AAPL" first
    cache_key = "stock_price:AAPL"
    redis_client.delete(cache_key)

    with patch("agent.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Time Series (5min)": {
                "2025-02-14 19:55:00": {
                    "1. open": "244.7100",
                    "2. high": "244.7500",
                    "3. low": "244.5000",
                    "4. close": "244.6400",
                    "5. volume": "2096"
                }
            }
        }
        mock_get.return_value = mock_response

        # First call should fetch from API and cache the result
        result = agent.get_stock_price("AAPL")
        assert result["symbol"] == "AAPL"
        cached_data = redis_client.get(cache_key)
        assert cached_data is not None
        cached = json.loads(cached_data)
        assert cached["symbol"] == "AAPL"

        # Now, simulate a second call: To test caching, we make sure axios.get is not called again
        # Clear the mock so that if it is called, the test will fail
        mock_get.reset_mock()
        result_cached = agent.get_stock_price("AAPL")
        # Check that the function returns cached data without calling the API
        mock_get.assert_not_called()
        assert result_cached["symbol"] == "AAPL"


"""
cd backend
export PYTHONPATH=$(pwd)
pytest
"""
