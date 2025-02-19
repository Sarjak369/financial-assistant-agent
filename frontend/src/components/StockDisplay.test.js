// src/components/StockDisplay.test.js
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import StockDisplay from './StockDisplay';

describe('StockDisplay Component', () => {
    beforeEach(() => {
        global.fetch = jest.fn();
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    test('fetches and displays stock price', async () => {
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({
                symbol: "AAPL",
                timestamp: "2025-02-14 19:55:00",
                open: "244.7100",
                high: "244.7500",
                low: "244.5000",
                close: "244.6400",
                volume: "2096"
            }),
        });

        render(<StockDisplay />);

        const input = screen.getByPlaceholderText(/Enter symbol, e.g., AAPL/i);
        fireEvent.change(input, { target: { value: 'AAPL' } });

        const button = screen.getByText(/Fetch Stock Price/i);
        fireEvent.click(button);

        await waitFor(() => {
            expect(screen.getByText(/Symbol:/i)).toBeInTheDocument();
            expect(screen.getByText(/AAPL/i)).toBeInTheDocument();
            expect(screen.getByText(/244.7100/i)).toBeInTheDocument();
        });
    });

    test('handles fetch error', async () => {
        global.fetch.mockResolvedValueOnce({
            ok: false,
            json: async () => ({
                detail: "Bad Request"
            }),
        });

        render(<StockDisplay />);

        const input = screen.getByPlaceholderText(/Enter symbol, e.g., AAPL/i);
        fireEvent.change(input, { target: { value: 'AAPL' } });

        fireEvent.click(screen.getByText(/Fetch Stock Price/i));

        await waitFor(() => {
            expect(screen.getByText(/Failed to fetch. Is the backend running?/i)).toBeInTheDocument();
        });
    });
});
