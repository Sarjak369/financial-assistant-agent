import React, { useState } from 'react';
import axios from 'axios';

function HistoricalQuery() {
    const [query, setQuery] = useState('');
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');

    const runQuery = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/historical-data?query=${encodeURIComponent(query)}`);
            console.log("API Response:", response.data);  // Debugging line

            // Ensure the response is in the correct format before setting the result
            if (!response.data || !Array.isArray(response.data.result)) {
                throw new Error("Invalid data format received.");
            }

            setResult(response.data);
            setError('');
        } catch (err) {
            console.error("Query Error:", err);
            setError(err.response?.data?.detail || "Invalid data format received.");
            setResult(null);
        }
    };


    return (
        <div>
            <h2>Historical Data Query</h2>
            <div className="input-group">
                <input
                    type="text"
                    placeholder="Enter SQL query, e.g., SELECT * FROM stock_data"
                    value={query}
                    onChange={e => setQuery(e.target.value)}
                />
                <button onClick={runQuery}>Run Query</button>
            </div>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {result && Array.isArray(result.result) ? (
                <div className="query-result">
                    <p><strong>Query:</strong> {result.query}</p>
                    <table className="query-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Symbol</th>
                                <th>Open</th>
                                <th>Close</th>
                            </tr>
                        </thead>
                        <tbody>
                            {result.result.map((row, index) => (
                                <tr key={index}>
                                    <td>{row[0]}</td>
                                    <td>{row[1]}</td>
                                    <td>{row[2]}</td>
                                    <td>{row[3]}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                result && <p style={{ color: 'red' }}>Invalid data format received.</p>
            )}
        </div>
    );
}

export default HistoricalQuery;
