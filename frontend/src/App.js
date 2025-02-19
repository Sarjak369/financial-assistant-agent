import React from 'react';
import StockDisplay from './components/StockDisplay';
import HistoricalQuery from './components/HistoricalQuery';
import NewsFeed from './components/NewsFeed';


function App() {
  return (
    <div className="container">
      <header>
        <h1>Financial Assistant Agent</h1>
      </header>
      <main>
        <StockDisplay />
        <HistoricalQuery />
        <NewsFeed />
      </main>
    </div>
  );
}

export default App;


// cd frontend
// npm start
