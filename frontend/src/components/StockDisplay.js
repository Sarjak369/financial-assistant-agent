import React, { useState } from 'react';

function StockDisplay() {
    const [symbol, setSymbol] = useState('');
    const [data, setData] = useState(null);
    const [error, setError] = useState('');


    const fetchStockPrice = async () => {
        setError(''); // Reset error message



        try {
            console.log("Fetching stock price for:", symbol);
            const response = await fetch(`http://127.0.0.1:8000/stock-price?symbol=${symbol}`);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to fetch stock data");
            }

            const jsonData = await response.json();
            console.log("API Response:", jsonData);  // Debugging

            if (jsonData.error) {
                setError("Error fetching stock data");
                setData(null);
            } else {
                setData(jsonData);
                setError("");
            }
        } catch (err) {
            console.error("Fetch Error:", err);
            setError("Failed to fetch. Is the backend running?");
            setData(null);
        }
    };

    return (
        <div>
            <h2>Stock Price</h2>

            {/* Wrap input & button in an input-group for styling */}
            <div className="input-group">
                <input
                    type="text"
                    placeholder="Enter symbol, e.g., AAPL"
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value)}
                />
                <button onClick={fetchStockPrice}>Fetch Stock Price</button>
            </div>

            {/* Show error message if any */}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {/* If data exists, wrap in .stock-data for styling */}
            {data && (
                <div className="stock-data">
                    <p><strong>Symbol:</strong> {data.symbol}</p>
                    <p><strong>Timestamp:</strong> {data.timestamp}</p>
                    <p><strong>Open:</strong> {data.open}</p>
                    <p><strong>High:</strong> {data.high}</p>
                    <p><strong>Low:</strong> {data.low}</p>
                    <p><strong>Close:</strong> {data.close}</p>
                    <p><strong>Volume:</strong> {data.volume}</p>
                </div>
            )}
        </div>
    );
}

export default StockDisplay;
