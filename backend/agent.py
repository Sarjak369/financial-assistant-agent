# backend/agent.py

import logging
import os
from dotenv import load_dotenv
import requests
from pyspark.sql import SparkSession, Row
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.tools.spark_sql.tool import QuerySparkSQLTool
from langchain_community.utilities.spark_sql import SparkSQL
import time

import redis
import json
import time

# Connect to Redis (adjust host/port if needed)
redis_client = redis.Redis(host='localhost', port=6379,
                           db=0, decode_responses=True)


last_news_fetch_time = 0  # Store last fetch time
NEWS_API_DELAY = 5  # 5 seconds between requests


class FinancialAgent:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.alpha_vantage_api_key:
            raise ValueError(
                "Alpha Vantage API key is required. Please set it in your .env file.")
        self.logger = logging.getLogger("FinancialAgent")
        self._init_tools()

    def _init_tools(self):
        """Initialize tools for the agent."""
        # For stock data, we will use a direct requests call (see get_stock_price)
        # Initialize Spark Session with Java security fix
        self.spark = SparkSession.builder \
            .appName("FinancialDataAnalysis") \
            .getOrCreate()
        # .config("spark.driver.extraJavaOptions", "-Djava.security.manager=allow") \

        # Create a sample DataFrame (replace with your actual data source)
        data = [
            Row(date="2024-02-10", symbol="AAPL", open=184.2, close=185.3),
            Row(date="2024-02-11", symbol="AAPL", open=185.3, close=186.0)
        ]
        df = self.spark.createDataFrame(data)
        df.createOrReplaceTempView("stock_data")  # Creates an in-memory table

        # Create SparkSQL instance and initialize QuerySparkSQLTool with it
        self.spark_sql = SparkSQL(self.spark)
        self.spark_sql_tool = QuerySparkSQLTool(db=self.spark_sql)

        # Initialize Yahoo Finance News Tool
        self.yahoo_finance_news_tool = YahooFinanceNewsTool()

    # def get_stock_price(self, symbol: str) -> dict:
    #     """Fetches real-time stock prices from Alpha Vantage via a direct API call."""
    #     self.logger.info(f"Fetching stock price for: {symbol}")
    #     url = "https://www.alphavantage.co/query"
    #     params = {
    #         "function": "TIME_SERIES_INTRADAY",
    #         "symbol": symbol,
    #         "interval": "5min",
    #         "apikey": self.alpha_vantage_api_key,
    #         "datatype": "json"
    #     }
    #     try:
    #         response = requests.get(url, params=params)
    #         if response.status_code != 200:
    #             return {"error": f"HTTP error: {response.status_code}"}
    #         result = response.json()
    #         # Check for errors in the response
    #         if "Error Message" in result or "Note" in result:
    #             return {"error": result.get("Error Message") or result.get("Note")}
    #         time_series = result.get("Time Series (5min)", {})
    #         if not time_series:
    #             return {"error": "No stock data found"}
    #         latest_timestamp = max(time_series.keys())
    #         latest_data = time_series[latest_timestamp]
    #         return {
    #             "symbol": symbol,
    #             "timestamp": latest_timestamp,
    #             "open": latest_data["1. open"],
    #             "high": latest_data["2. high"],
    #             "low": latest_data["3. low"],
    #             "close": latest_data["4. close"],
    #             "volume": latest_data["5. volume"]
    #         }
    #     except Exception as e:
    #         self.logger.error(f"Error fetching stock price: {e}")
    #         return {"error": str(e)}

    def get_stock_price(self, symbol: str) -> dict:
        """Fetches real-time stock prices from Alpha Vantage via a direct API call with caching."""
        self.logger.info(f"Fetching stock price for: {symbol}")

        # Check if the data is in cache
        cache_key = f"stock_price:{symbol}"
        cached_data = redis_client.get(cache_key)
        if cached_data:
            self.logger.info(f"Returning cached data for {symbol}")
            return json.loads(cached_data)

        # If not cached, call the external API
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": "5min",
            "apikey": self.alpha_vantage_api_key,
            "datatype": "json"
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()

            # Log the full API response for debugging
            self.logger.info(f"Alpha Vantage Response: {data}")

            if response.status_code != 200:
                return {"error": f"HTTP error: {response.status_code}"}
            if "Error Message" in data or "Note" in data:
                return {"error": data.get("Error Message") or data.get("Note")}
            time_series = data.get("Time Series (5min)", {})
            if not time_series:
                return {"error": "No stock data found"}
            latest_timestamp = max(time_series.keys())
            latest_data = time_series[latest_timestamp]

            result = {
                "symbol": symbol,
                "timestamp": latest_timestamp,
                "open": latest_data["1. open"],
                "high": latest_data["2. high"],
                "low": latest_data["3. low"],
                "close": latest_data["4. close"],
                "volume": latest_data["5. volume"]
            }

            # Cache the result in Redis with an expiration time (e.g., 5 minutes)
            redis_client.setex(cache_key, 300, json.dumps(result))
            return result

        except Exception as e:
            self.logger.error(f"Error fetching stock price: {e}")
            return {"error": str(e)}

    def query_historical_data(self, sql_query: str) -> dict:
        """Executes a Spark SQL query and returns the result as a structured JSON object."""
        self.logger.info(f"Running Spark SQL query: {sql_query}")
        try:
            result = self.spark_sql_tool.run(tool_input=sql_query)

            # If the result is a string, try converting it to a list
            if isinstance(result, str):
                try:
                    import ast
                    result = ast.literal_eval(result)  # Convert string to list
                except Exception:
                    return {"error": "Invalid data format received from Spark."}

            # Ensure result is a list of lists (table format)
            if not isinstance(result, list):
                return {"error": "Invalid data format received from Spark."}

            return {"query": sql_query, "result": result}
        except Exception as e:
            self.logger.error(f"Error running SQL query: {e}")
            return {"error": str(e)}

    # def get_financial_news(self, symbol: str) -> dict:
    #     global last_news_fetch_time

    #     # ✅ Check time since last request
    #     current_time = time.time()
    #     if current_time - last_news_fetch_time < NEWS_API_DELAY:
    #         return {"error": "Too many requests. Please wait a few seconds."}

    #     self.logger.info(f"Fetching financial news for: {symbol}")
    #     try:
    #         response = self.yahoo_finance_news_tool.run(symbol)
    #         if response is None:
    #             raise ValueError("Yahoo Finance API returned no data.")

    #         last_news_fetch_time = time.time()  # ✅ Update last fetch time
    #         return {"symbol": symbol, "news": response}

    #     except Exception as e:
    #         self.logger.error(f"Error fetching financial news: {e}")
    #         return {"error": f"Failed to fetch news for {symbol}: {str(e)}"}

    """
    ✅ Fix the Yahoo Finance API Issue
    Since Yahoo Finance is blocking requests, use an alternative method to fetch news:

    1️⃣ Use an Alternative API for News
    Try replacing Yahoo Finance with Alpha Vantage's news API (which you're already using for stock prices).

    🔹 Modify get_financial_news() in agent.py
    Replace Yahoo Finance with Alpha Vantage:

    Why? ✅ Uses Alpha Vantage API (no request limits like Yahoo Finance)
    ✅ Avoids NoneType error by checking if "feed" exists in response
    ✅ Improves reliability with structured error messages


    """

    def get_financial_news(self, symbol: str) -> dict:
        """Fetches financial news using Alpha Vantage instead of Yahoo Finance."""
        self.logger.info(f"Fetching financial news for: {symbol}")

        url = "https://www.alphavantage.co/query"
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": symbol,
            "apikey": self.alpha_vantage_api_key
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if "feed" in data:
                return {"symbol": symbol, "news": data["feed"]}
            else:
                return {"error": f"Failed to fetch news for {symbol}: {data}"}

        except Exception as e:
            self.logger.error(f"Error fetching financial news: {e}")
            return {"error": f"Failed to fetch news for {symbol}: {str(e)}"}

    def external_api_call(self, url: str, params: dict) -> dict:
        """Makes an external API call using the requests module."""
        self.logger.info(
            f"Making external API call to: {url} with params: {params}")
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error in external API call: {e}")
            return {"error": str(e)}
