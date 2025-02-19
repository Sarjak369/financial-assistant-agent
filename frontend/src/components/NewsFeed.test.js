// src/components/NewsFeed.test.js
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import NewsFeed from './NewsFeed';

describe('NewsFeed Component', () => {
    beforeEach(() => {
        global.fetch = jest.fn();
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    test('fetches and displays news', async () => {
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({
                symbol: "AAPL",
                news: [
                    {
                        title: "Sample News Article",
                        url: "http://example.com",
                        summary: "This is a sample news summary.",
                        source: "Example Source"
                    }
                ]
            }),
        });

        render(<NewsFeed />);

        const input = screen.getByPlaceholderText(/Enter symbol, e.g., AAPL/i);
        fireEvent.change(input, { target: { value: 'AAPL' } });

        fireEvent.click(screen.getByText(/Fetch News/i));

        await waitFor(() => {
            expect(screen.getByText(/Sample News Article/i)).toBeInTheDocument();
            expect(screen.getByText(/Example Source/i)).toBeInTheDocument();
        });
    });

    test('handles no news scenario', async () => {
        global.fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => ({
                error: "",
                news: []
            }),
        });

        render(<NewsFeed />);

        const input = screen.getByPlaceholderText(/Enter symbol, e.g., AAPL/i);
        fireEvent.change(input, { target: { value: 'AAPL' } });
        fireEvent.click(screen.getByText(/Fetch News/i));

        await waitFor(() => {
            expect(screen.getByText(/No news available for this stock./i)).toBeInTheDocument();
        });
    });
});
