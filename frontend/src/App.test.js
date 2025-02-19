// src/App.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
    test('renders the main heading', () => {
        render(<App />);
        const headingElement = screen.getByText(/Financial Assistant Agent/i);
        expect(headingElement).toBeInTheDocument();
    });

    test('renders Stock Price, Historical Data Query, and Financial News sections', () => {
        render(<App />);
        // Use getAllByText since "Stock Price" appears multiple times (header and button)
        const stockPriceElements = screen.getAllByText(/Stock Price/i);
        expect(stockPriceElements.length).toBeGreaterThan(0);
        expect(screen.getAllByText(/Historical Data Query/i).length).toBeGreaterThan(0);
        expect(screen.getAllByText(/Financial News/i).length).toBeGreaterThan(0);
    });
});
