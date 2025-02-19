# backend/tests/test_main.py


"""
test_main.py → Integration tests for your FastAPI endpoints
"""


import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Financial Agent API is running!"}


def test_stock_price():
    """Integration test for /stock-price endpoint."""
    response = client.get("/stock-price?symbol=AAPL")
    # Depending on the actual API call, it might be real data or mocked data.
    assert response.status_code in [200, 400]
    # If it’s 200, we check for valid structure
    if response.status_code == 200:
        data = response.json()
        assert "symbol" in data
        assert data["symbol"] == "AAPL"


def test_historical_data():
    """Integration test for /historical-data endpoint."""
    query = "SELECT * FROM stock_data"
    response = client.get(f"/historical-data?query={query}")
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.json()
        assert data["query"] == query


def test_news():
    """Integration test for /news endpoint."""
    response = client.get("/news?symbol=AAPL")
    assert response.status_code in [200, 400]


def test_external():
    """Integration test for /external endpoint."""
    response = client.get(
        "/external?url=https://jsonplaceholder.typicode.com/todos/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] == 1
