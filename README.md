# Financial Assistant Agent

## Project Overview

The **Financial Assistant Agent** is a React-based application that integrates multiple financial data tools to provide real-time stock prices, historical financial data, and the latest financial news. The backend is built using FastAPI and Python, leveraging various APIs and tools, including:

- **Alpha Vantage:** For fetching real-time stock prices.
- **Spark SQL:** For querying and analyzing historical financial data.
- **Yahoo Finance News (via Alpha Vantage’s NEWS_SENTIMENT API):** For retrieving the latest financial news.
- **Requests Tool:** For making REST API calls.
- **Redis Caching:** To cache frequently requested stock data and reduce repeated external API calls.

This project is designed with modularity, robust error handling, and validations, making it easily extendable for future enhancements.

---

## Features and Tools

- **React Frontend:**  
  - Displays stock prices, historical queries, and news.
  - Provides a user-friendly interface with real-time feedback.
- **FastAPI Backend:**  
  - Serves as the API gateway for financial data interactions.
  - Integrates Alpha Vantage for stock prices.
  - Uses Spark SQL to query historical data.
  - Fetches financial news via Alpha Vantage’s news API.
  - Implements caching using Redis to minimize external API calls.
- **Custom Tool Integration & Validations:**  
  - The backend is structured around a `FinancialAgent` class that integrates multiple financial tools.
  - Robust error handling and logging are implemented to track API calls and capture failures.

---

## Setup Instructions

### Cloning the Repository

Clone the repository from GitHub:
```bash
git clone https://github.com/yourusername/financial-assistant-agent.git
cd financial-assistant-agent
```

### Backend Setup

#### Create and Activate Virtual Environment:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

#### Install Python Dependencies:
Ensure `requirements.txt` exists in `backend/` and run:
```bash
pip install -r requirements.txt
```

#### Set Up the .env File:
Create a file named `.env` in `backend/` with the following content:
```env
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
```

#### Run the Backend Server:
```bash
uvicorn main:app --reload
```
The backend should be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Frontend Setup

#### Install Node.js and npm:
Download and install Node.js (v16 or later) from [nodejs.org](https://nodejs.org).

#### Set Up the Frontend:
```bash
cd ../frontend
```
If not already set up:
```bash
npx create-react-app .
```

#### Install Frontend Dependencies:
```bash
npm install axios
```

#### Run the Frontend App:
```bash
npm start
```
The app will be accessible at [http://localhost:3000](http://localhost:3000).

---

## Testing Instructions

### Backend Tests (pytest):
```bash
pytest
```
Runs all backend tests.

### Frontend Tests (Jest):
Ensure `src/setupTests.js` contains:
```js
import '@testing-library/jest-dom';
```
Run tests:
```bash
npm test
```

---

## Deployment Instructions

### Docker Containerization

#### Backend Dockerfile
```dockerfile
FROM python:3.11-slim-bullseye
WORKDIR /app
RUN apt-get update && apt-get install -y openjdk-11-jdk procps && apt-get clean
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
RUN java -version
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

#### Docker Compose
```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
       - backend/.env
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
```
To build and run:
```bash
docker-compose up --build
```

### Deployment Platforms
- **Frontend:** Deploy to Vercel or Netlify.
- **Backend:** Deploy to Railway, Render, or Fly.io.

---

## Usage Examples

- **Test the Backend:**
```bash
curl http://127.0.0.1:8000/
```
Expected output:
```json
{"message": "Financial Agent API is running!"}
```

- **Fetch Stock Price:**
```bash
curl "http://127.0.0.1:8000/stock-price?symbol=AAPL"
```

- **Fetch Historical Data:**
```bash
curl "http://127.0.0.1:8000/historical-data?query=SELECT%20*%20FROM%20stock_data"
```

- **Fetch Financial News:**
```bash
curl "http://127.0.0.1:8000/news?symbol=AAPL"
```

---

## Caching Implementation

The backend uses **Redis Caching**:
- Before making an API call, it checks Redis for cached data.
- If cached data exists and is valid (TTL of 5 minutes), it returns the cached result.
- Otherwise, data is fetched from Alpha Vantage, stored in Redis, and then returned.

This strategy minimizes external API calls and helps avoid exceeding rate limits.

---

## Future Enhancements

- **Authentication:** Implement API key-based or JWT authentication.
- **Real-Time Updates:** Add WebSocket support for live stock price updates.
- **Advanced Caching:** Enhance caching strategies using Redis.
- **Monitoring:** Integrate tools like Sentry for error tracking.
- **Additional Data Sources:** Expand to include more financial data APIs.

---


## Conclusion

The **Financial Assistant Agent** is a fully integrated financial tool providing real-time stock prices, historical data analysis, and financial news through a user-friendly React interface. The application is containerized with Docker and is deployment-ready. Future enhancements include authentication, real-time updates, and further optimizations.

