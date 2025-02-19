import React, { useState } from "react";

function NewsFeed() {
    const [symbol, setSymbol] = useState("");
    const [news, setNews] = useState([]);
    const [error, setError] = useState("");

    const fetchNews = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/news?symbol=${symbol}`);
            const data = await response.json();

            console.log("News API Response:", data); // Debugging line

            if (data.error || !data.news || data.news.length === 0) {
                setError("No news available for this stock.");
                setNews([]);
            } else {
                setNews(data.news);  // Store news array properly
                setError("");
            }
        } catch (err) {
            console.error("Fetch Error:", err);
            setError("Failed to fetch financial news.");
        }
    };

    return (
        <div>
            <h2>Financial News</h2>
            <div className="input-group">
                <input
                    type="text"
                    placeholder="Enter symbol, e.g., AAPL"
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value)}
                />
                <button onClick={fetchNews}>Fetch News</button>
            </div>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {/* Updated news section with card-like styling */}
            <div className="news-section">
                {news.map((article, index) => (
                    <div key={index} className="news-item">
                        <a href={article.url} target="_blank" rel="noopener noreferrer">
                            <strong>{article.title}</strong>
                        </a>
                        <p>{article.summary}</p>
                        <p><small>Source: {article.source}</small></p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default NewsFeed;
