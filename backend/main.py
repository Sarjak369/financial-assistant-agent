# backend/main.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn
from utils import setup_logging
from agent import FinancialAgent

# Load environment variables from .env file
load_dotenv()

# Initialize logging
setup_logging()


# Initialize FastAPI app
app = FastAPI(title="React-Based Financial Agent")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize FinancialAgent (which handles our external API calls and Spark integration)
agent = FinancialAgent()

# Data model for SQL queries


class SQLQuery(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "Financial Agent API is running!"}


@app.get("/stock-price")
def get_stock_price(symbol: str = Query(..., description="Stock symbol, e.g., AAPL")):
    result = agent.get_stock_price(symbol)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/historical-data")
def get_historical_data(query: str = Query(..., description="SQL query for historical data")):
    result = agent.query_historical_data(query)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/news")
def get_news(symbol: str = Query(..., description="Stock symbol for news, e.g., AAPL")):
    result = agent.get_financial_news(symbol)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/external")
def external_api(url: str = Query(..., description="External API URL"),
                 params: str = Query("", description="Query parameters in key=value format, separated by &")):
    """Calls an external API with query parameters."""
    # Convert query string to dictionary
    param_dict = {kv.split("=")[0]: kv.split("=")[1]
                  for kv in params.split("&") if "=" in kv}
    result = agent.external_api_call(url, param_dict)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


"""
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000


"""
